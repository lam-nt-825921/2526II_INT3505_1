param(
    [string]$BaseUrl = "https://week-10-observability-api.onrender.com",
    [ValidateSet("health", "items", "metrics", "trace", "rate-limit", "external", "security", "all")]
    [string]$Scenario = "all"
)

$ErrorActionPreference = "Continue"
$BaseUrl = $BaseUrl.TrimEnd("/")

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "=== $Message ===" -ForegroundColor Cyan
}

function Invoke-DemoRequest {
    param(
        [string]$Method = "GET",
        [string]$Path,
        [object]$Body = $null
    )

    $uri = "$BaseUrl$Path"
    Write-Host "$Method $uri" -ForegroundColor Yellow

    try {
        if ($null -eq $Body) {
            $response = Invoke-WebRequest -Uri $uri -Method $Method -UseBasicParsing
        }
        else {
            $json = $Body | ConvertTo-Json -Depth 10
            $response = Invoke-WebRequest -Uri $uri -Method $Method -ContentType "application/json" -Body $json -UseBasicParsing
        }

        Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
        if ($response.Content) {
            Write-Host $response.Content
        }
        return $response
    }
    catch {
        $response = $_.Exception.Response
        $status = $null
        if ($response) {
            $status = $response.StatusCode.value__
        }
        if (-not $status -and $response) {
            $status = [int]$response.StatusCode
        }

        if ($status) {
            Write-Host "Status: $status" -ForegroundColor Red
            try {
                if ($_.ErrorDetails.Message) {
                    Write-Host $_.ErrorDetails.Message
                }
                elseif ($response.Content) {
                    Write-Host $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
                }
                elseif ($response.PSObject.Methods.Name -contains "GetResponseStream") {
                    $reader = New-Object System.IO.StreamReader($response.GetResponseStream())
                    Write-Host $reader.ReadToEnd()
                }
            }
            catch {
                Write-Host $_.Exception.Message
            }
        }
        else {
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
}

function Demo-Health {
    Write-Step "Health and readiness"
    Invoke-DemoRequest -Path "/health" | Out-Null
    Invoke-DemoRequest -Path "/ready" | Out-Null
}

function Demo-Items {
    Write-Step "Create item, list items, and trigger audit log"
    $name = "demo-item-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"
    Invoke-DemoRequest -Method "POST" -Path "/api/v1/items" -Body @{
        name = $name
        description = "Created by scripts/demo-api.ps1"
    } | Out-Null
    Invoke-DemoRequest -Path "/api/v1/items" | Out-Null
}

function Demo-Metrics {
    Write-Step "Prometheus metrics"
    Invoke-DemoRequest -Path "/health" | Out-Null
    Invoke-DemoRequest -Path "/api/v1/items" | Out-Null

    $metrics = Invoke-DemoRequest -Path "/metrics"
    if ($metrics -and $metrics.Content) {
        Write-Host ""
        Write-Host "Metric lines to point at:" -ForegroundColor Cyan
        $metrics.Content -split "`n" |
            Where-Object { $_ -match "http_.*request|items_created_total" } |
            Select-Object -First 20
    }
}

function Demo-Trace {
    Write-Step "Internal request trace"
    $response = Invoke-DemoRequest -Path "/health"
    if ($response) {
        $traceId = $response.Headers["X-Trace-ID"]
        Write-Host ""
        Write-Host "Trace ID: $traceId" -ForegroundColor Cyan
        Invoke-DemoRequest -Path "/admin/traces/$traceId" | Out-Null
    }
}

function Demo-RateLimit {
    Write-Step "Rate limiting on POST /api/v1/items"
    1..12 | ForEach-Object {
        $body = @{
            name = "rate-limit-demo-$_"
            description = "Request $_ from demo script"
        }
        Invoke-DemoRequest -Method "POST" -Path "/api/v1/items" -Body $body | Out-Null
    }
}

function Demo-External {
    Write-Step "External dependency and circuit breaker"
    Write-Host "Normal mode: EXTERNAL_FAILURE_MODE=false should return 200." -ForegroundColor Gray
    Write-Host "Circuit breaker demo: set EXTERNAL_FAILURE_MODE=true in Render Environment, wait for redeploy, then run this scenario again." -ForegroundColor Gray
    1..6 | ForEach-Object {
        Invoke-DemoRequest -Path "/api/v1/external/status" | Out-Null
    }
}

function Demo-Security {
    Write-Step "Security headers"
    $response = Invoke-DemoRequest -Path "/health"
    if ($response) {
        Write-Host ""
        Write-Host "Headers to point at:" -ForegroundColor Cyan
        "X-Content-Type-Options: $($response.Headers["X-Content-Type-Options"])"
        "X-Frame-Options: $($response.Headers["X-Frame-Options"])"
    }
}

switch ($Scenario) {
    "health" { Demo-Health }
    "items" { Demo-Items }
    "metrics" { Demo-Metrics }
    "trace" { Demo-Trace }
    "rate-limit" { Demo-RateLimit }
    "external" { Demo-External }
    "security" { Demo-Security }
    "all" {
        Demo-Health
        Demo-Items
        Demo-Metrics
        Demo-Trace
        Demo-Security
        Write-Host ""
        Write-Host "Run rate-limit and external separately during the demo because they intentionally produce errors." -ForegroundColor Magenta
        Write-Host ".\scripts\demo-api.ps1 -Scenario rate-limit" -ForegroundColor Magenta
        Write-Host ".\scripts\demo-api.ps1 -Scenario external" -ForegroundColor Magenta
    }
}
