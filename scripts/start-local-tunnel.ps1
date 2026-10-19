$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendRoot = Join-Path $repoRoot 'backend'
$mobileRoot = Join-Path $repoRoot 'mobile'
$backendUrl = 'http://127.0.0.1:8000'
$quickTunnelConfigPaths = @(
    (Join-Path $env:USERPROFILE '.cloudflared\config.yml'),
    (Join-Path $env:USERPROFILE '.cloudflared\config.yaml')
)
$cloudflaredCommand = Get-Command cloudflared -ErrorAction SilentlyContinue
$pythonPath = Join-Path $repoRoot '.venv313\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    $pythonPath = Join-Path $backendRoot '.venv\Scripts\python.exe'
}
$tempRoot = Join-Path $env:TEMP ("mosaic-tunnel-" + [guid]::NewGuid().ToString('N'))
$backendProcess = $null
$tunnelProcess = $null
$preserveLogs = $false

function Get-LogText([string] $path) {
    if (Test-Path -LiteralPath $path) {
        return Get-Content -LiteralPath $path -Raw -ErrorAction SilentlyContinue
    }
    return ''
}

function Stop-ChildProcess($processInfo) {
    if ($null -ne $processInfo) {
        $processInfo.Refresh()
        if (-not $processInfo.HasExited) {
            Stop-Process -Id $processInfo.Id -Force -ErrorAction SilentlyContinue
            Wait-Process -Id $processInfo.Id -Timeout 5 -ErrorAction SilentlyContinue
        }
    }
}

function Get-HttpErrorSummary($errorRecord) {
    $response = $errorRecord.Exception.Response
    if ($null -eq $response) {
        return $errorRecord.Exception.Message
    }

    $statusCode = [int]$response.StatusCode
    $statusDescription = $response.StatusDescription
    $body = ''
    try {
        $reader = [System.IO.StreamReader]::new($response.GetResponseStream())
        $body = $reader.ReadToEnd()
        $reader.Dispose()
    }
    catch {
        # The status and server logs remain useful when the response has no body.
    }
    if ($body.Length -gt 600) {
        $body = $body.Substring(0, 600) + '...'
    }
    return "HTTP $statusCode $statusDescription $body"
}

try {
    if (-not $cloudflaredCommand) {
        throw "cloudflared is not installed. Install it once with: winget install --id Cloudflare.cloudflared --exact"
    }
    if (-not (Test-Path -LiteralPath $pythonPath)) {
        throw "Project Python environment not found at $pythonPath. Create/activate the Mosaic backend environment first."
    }
    $quickTunnelConfig = $quickTunnelConfigPaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($quickTunnelConfig) {
        throw "Quick Tunnels do not work while $quickTunnelConfig exists. Move that config outside .cloudflared, then rerun."
    }

    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
    $tunnelStdout = Join-Path $tempRoot 'cloudflared.stdout.log'
    $tunnelStderr = Join-Path $tempRoot 'cloudflared.stderr.log'
    $backendStdout = Join-Path $tempRoot 'django.stdout.log'
    $backendStderr = Join-Path $tempRoot 'django.stderr.log'

    Write-Host 'Starting a temporary HTTPS tunnel for the local Django API...'
    $tunnelProcess = Start-Process `
        -FilePath $cloudflaredCommand.Source `
        -ArgumentList @('tunnel', '--url', $backendUrl, '--http-host-header', 'localhost') `
        -WindowStyle Hidden `
        -RedirectStandardOutput $tunnelStdout `
        -RedirectStandardError $tunnelStderr `
        -PassThru

    $tunnelDeadline = [DateTime]::UtcNow.AddSeconds(90)
    $apiUrl = $null
    while ([DateTime]::UtcNow -lt $tunnelDeadline) {
        $tunnelLogs = (Get-LogText $tunnelStdout) + "`n" + (Get-LogText $tunnelStderr)
        $urlMatch = [regex]::Match(
            $tunnelLogs,
            'https://[a-zA-Z0-9-]+\.trycloudflare\.com'
        )
        if ($urlMatch.Success) {
            $apiUrl = $urlMatch.Value.TrimEnd('/') + '/'
            break
        }
        $tunnelProcess.Refresh()
        if ($tunnelProcess.HasExited) {
            throw "cloudflared exited before creating a tunnel:`n$tunnelLogs"
        }
        Start-Sleep -Seconds 1
    }
    if (-not $apiUrl) {
        $tunnelLogs = (Get-LogText $tunnelStdout) + "`n" + (Get-LogText $tunnelStderr)
        throw "Timed out waiting for Cloudflare to create a tunnel:`n$tunnelLogs"
    }

    $tunnelHost = ([uri]$apiUrl).Host
    $env:DEBUG = 'False'
    # The public URL is generated per run. Accept its forwarded Host header only
    # for this short-lived, loopback-bound development process. Cloudflared also
    # sends localhost to the Django origin through --http-host-header above.
    $env:ALLOWED_HOSTS = '*'
    $env:TUNNEL_HOST = $tunnelHost
    $env:TRUST_PROXY_SSL = 'True'

    Write-Host 'Starting Django with the existing backend/.env Neon DATABASE_URL...'
    $backendProcess = Start-Process `
        -FilePath $pythonPath `
        -ArgumentList @('manage.py', 'runserver', '127.0.0.1:8000', '--noreload') `
        -WorkingDirectory $backendRoot `
        -WindowStyle Hidden `
        -RedirectStandardOutput $backendStdout `
        -RedirectStandardError $backendStderr `
        -PassThru

    $backendDeadline = [DateTime]::UtcNow.AddSeconds(90)
    $backendReady = $false
    while ([DateTime]::UtcNow -lt $backendDeadline) {
        $backendProcess.Refresh()
        if ($backendProcess.HasExited) {
            throw "Django exited during startup:`n$(Get-LogText $backendStderr)"
        }
        try {
            $health = Invoke-RestMethod `
                -Uri "$backendUrl/api/health/" `
                -Method Get `
                -TimeoutSec 3
            if ($health.status -eq 'ok' -and $health.database -eq 'ok') {
                $backendReady = $true
                break
            }
        }
        catch {
            # Wait for Django and the Neon connection to become ready.
        }
        Start-Sleep -Seconds 2
    }
    if (-not $backendReady) {
        throw "Django did not become ready against Neon within 90 seconds. Check backend/.env DATABASE_URL and the backend log:`n$(Get-LogText $backendStderr)"
    }

    $tunnelReady = $false
    $lastTunnelError = 'No response received yet.'
    # Quick Tunnel DNS and edge routing can lag behind URL creation by a minute.
    $publicDeadline = [DateTime]::UtcNow.AddSeconds(120)
    while ([DateTime]::UtcNow -lt $publicDeadline) {
        try {
            $health = Invoke-RestMethod `
                -Uri "${apiUrl}api/health/" `
                -Method Get `
                -TimeoutSec 5
            if ($health.status -eq 'ok' -and $health.database -eq 'ok') {
                $tunnelReady = $true
                break
            }
        }
        catch {
            $lastTunnelError = Get-HttpErrorSummary $_
        }
        Start-Sleep -Seconds 2
    }
    if (-not $tunnelReady) {
        $tunnelProcess.Refresh()
        if ($tunnelProcess.HasExited) {
            throw "cloudflared exited before the public health check succeeded:`n$(Get-LogText $tunnelStderr)"
        }
        Write-Warning "This computer could not resolve the new public tunnel yet. Expo will still use $apiUrl. Last probe: $lastTunnelError"
    }

    $env:EXPO_PUBLIC_API_URL = $apiUrl
    Write-Host "API URL ready: $apiUrl"
    Write-Host 'Starting Expo. Use the QR code in Expo Go; keep this window open.'
    Push-Location $mobileRoot
    try {
        npm run start -- --lan --clear
        if ($LASTEXITCODE -ne 0) {
            throw "Expo exited with code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }
}
catch {
    $preserveLogs = $true
    Write-Host $_ -ForegroundColor Red
    if (Test-Path -LiteralPath $tempRoot) {
        Write-Host "Diagnostic logs were kept at: $tempRoot" -ForegroundColor Yellow
    }
    throw
}
finally {
    Stop-ChildProcess $backendProcess
    Stop-ChildProcess $tunnelProcess
    if (-not $preserveLogs -and (Test-Path -LiteralPath $tempRoot)) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
