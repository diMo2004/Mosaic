"""Shared HTTP access for external source adapters.

Every provider request goes through ``provider_get`` so that:

* a descriptive User-Agent with contact information is always sent
  (required by Wikimedia, recommended by the other providers);
* a per-domain minimum interval is enforced (best effort; shared across
  worker processes only when CACHES points at a shared backend such as Redis);
* provider back-off signals (HTTP 429/503 ``Retry-After``, Stack Exchange
  ``backoff``) put the domain into a cool-down instead of being retried hot;
* failures are classified as transient (retry) or permanent (record and stop).
"""
import logging
import time
import urllib.robotparser
from urllib.parse import urlsplit

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Longest we block a worker waiting for a domain slot; beyond this the job is
# rescheduled instead.
MAX_INLINE_WAIT_SECONDS = 15.0


class ProviderError(RuntimeError):
    """Base class for provider failures."""


class TransientProviderError(ProviderError):
    """Timeouts, connection errors, and 5xx responses. Safe to retry."""


class RateLimitedError(TransientProviderError):
    def __init__(self, message: str, retry_after: float = 60.0):
        super().__init__(message)
        self.retry_after = retry_after


class PermanentProviderError(ProviderError):
    """4xx responses (other than 429) and malformed payloads. Do not retry."""


class AccessDisallowedError(PermanentProviderError):
    """robots.txt or the source allowlist forbids this URL."""


def user_agent() -> str:
    return getattr(settings, "INGESTION_USER_AGENT", "") or "MosaicKnowledgeBot/1.0"


def _min_interval(domain: str) -> float:
    intervals = getattr(settings, "INGESTION_DOMAIN_MIN_INTERVAL_SECONDS", {}) or {}
    for key, value in intervals.items():
        if domain == key or domain.endswith("." + key):
            return float(value)
    return float(getattr(settings, "INGESTION_DEFAULT_MIN_INTERVAL_SECONDS", 1.0))


def _rate_key(domain: str) -> str:
    return f"ingest:rl:{domain}"


def _cooldown_key(domain: str) -> str:
    return f"ingest:cooldown:{domain}"


def set_cooldown(domain: str, seconds: float) -> None:
    seconds = max(float(seconds), 1.0)
    cache.set(_cooldown_key(domain), time.time() + seconds, timeout=int(seconds) + 5)
    logger.warning("ingestion.http.cooldown domain=%s seconds=%.0f", domain, seconds)


def wait_for_slot(domain: str) -> None:
    now = time.time()
    cooldown_until = cache.get(_cooldown_key(domain))
    if cooldown_until and cooldown_until > now:
        raise RateLimitedError(f"{domain} is cooling down.", retry_after=cooldown_until - now)

    interval = _min_interval(domain)
    last = cache.get(_rate_key(domain))
    if last:
        wait = interval - (now - last)
        if wait > MAX_INLINE_WAIT_SECONDS:
            raise RateLimitedError(f"{domain} slot unavailable.", retry_after=wait)
        if wait > 0:
            time.sleep(wait)
    cache.set(_rate_key(domain), time.time(), timeout=int(interval) + 60)


def _retry_after_seconds(response, default: float = 60.0) -> float:
    value = response.headers.get("Retry-After") if response is not None else None
    try:
        return max(float(value), 1.0)
    except (TypeError, ValueError):
        return default


def provider_get(url: str, *, params=None, headers=None, timeout: float = 15.0, expect_json: bool = False):
    """GET a provider URL with rate limiting and failure classification."""
    domain = (urlsplit(url).hostname or "").lower()
    wait_for_slot(domain)
    merged_headers = {"User-Agent": user_agent()}
    merged_headers.update(headers or {})
    try:
        response = requests.get(url, params=params, headers=merged_headers, timeout=timeout)
    except (requests.Timeout, requests.ConnectionError) as exc:
        raise TransientProviderError(f"{domain} request failed: {exc}") from exc

    status_code = response.status_code
    if status_code == 429 or (status_code == 403 and response.headers.get("x-ratelimit-remaining") == "0"):
        retry_after = _retry_after_seconds(response)
        set_cooldown(domain, retry_after)
        raise RateLimitedError(f"{domain} rate limited ({status_code}).", retry_after=retry_after)
    if status_code == 503:
        retry_after = _retry_after_seconds(response, default=30.0)
        set_cooldown(domain, retry_after)
        raise RateLimitedError(f"{domain} unavailable (503).", retry_after=retry_after)
    if status_code >= 500:
        raise TransientProviderError(f"{domain} server error {status_code}.")
    if status_code >= 400:
        payload = _json_or_none(response) if expect_json else None
        # Stack Exchange reports throttling as HTTP 400 with error_id 502.
        if isinstance(payload, dict) and (payload.get("error_id") == 502 or payload.get("error_name") == "throttle_violation"):
            set_cooldown(domain, 120)
            raise RateLimitedError(f"{domain} throttle violation.", retry_after=120)
        raise PermanentProviderError(f"{domain} returned {status_code}.")

    if expect_json:
        payload = _json_or_none(response)
        if payload is None:
            raise PermanentProviderError(f"{domain} returned invalid JSON.")
        # Stack Exchange: callers must wait `backoff` seconds before the next call.
        if isinstance(payload, dict) and payload.get("backoff"):
            set_cooldown(domain, float(payload["backoff"]))
        return payload
    return response


def _json_or_none(response):
    try:
        return response.json()
    except ValueError:
        return None


_ROBOTS_TTL_SECONDS = 24 * 3600


def robots_allows(url: str) -> bool:
    """Respect robots.txt for HTML page fetches (API endpoints are governed by their terms)."""
    parts = urlsplit(url)
    domain = (parts.hostname or "").lower()
    cache_key = f"ingest:robots:{domain}"
    lines = cache.get(cache_key)
    if lines is None:
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        try:
            response = provider_get(robots_url, timeout=10)
            lines = response.text.splitlines()
        except PermanentProviderError:
            # No robots.txt (e.g. 404) means no restrictions were published.
            lines = []
        cache.set(cache_key, lines, timeout=_ROBOTS_TTL_SECONDS)
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(lines)
    return parser.can_fetch(user_agent(), url)
