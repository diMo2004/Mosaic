from django.conf import settings
from .placeholder import PlaceholderOCRProvider

def get_ocr_provider():
    provider = getattr(settings, "OCR_PROVIDER", "placeholder")
    if provider == "placeholder":
        return PlaceholderOCRProvider()

    raise ValueError(f"Unsupported OCR provider: {provider}")