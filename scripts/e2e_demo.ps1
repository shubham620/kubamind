#!/usr/bin/env pwsh
<#
E2E demo script (PowerShell):
- Start docker-compose
- Wait for services
- Ingest sample logs into Qdrant
- Run failure simulator
- Query backend endpoints and save outputs
#>

$ErrorActionPreference = 'Stop'

Write-Host "Starting KubeMind AI E2E demo..."

Push-Location -Path (Resolve-Path "$(Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)/..")

Write-Host "Bringing up docker-compose stack (detached)..."
docker-compose up -d

Write-Host "Waiting 20s for services to become healthy..."
Start-Sleep -Seconds 20

Write-Host "Ingesting logs into Qdrant (if any)..."
python -m backend.app.ingest.qdrant_ingest --source simulations --collection logs

Write-Host "Running failure simulator (background)..."
Start-Process -FilePath python -ArgumentList 'simulations/failure_simulator.py' -NoNewWindow | Out-Null

Write-Host "Waiting 10s for agents to process simulated failures..."
Start-Sleep -Seconds 10

$outDir = "demo-output"
if (-Not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

try {
    Write-Host "Querying anomalies endpoint..."
    $anoms = Invoke-RestMethod -Method Get -Uri http://localhost:8000/api/insights/anomalies -TimeoutSec 30
    $anoms | ConvertTo-Json -Depth 5 | Out-File -FilePath "$outDir/anomalies.json" -Encoding utf8

    Write-Host "Asking chat assistant: Why is payment-service slow?"
    $body = @{ message = "Why is payment-service slow?" } | ConvertTo-Json
    $chat = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/chat/message -Body $body -ContentType 'application/json' -TimeoutSec 30
    $chat | ConvertTo-Json -Depth 5 | Out-File -FilePath "$outDir/chat_response.json" -Encoding utf8

    Write-Host "E2E demo complete. Outputs saved to $outDir"
}
catch {
    Write-Host "E2E demo encountered an error: $_"
}

Pop-Location
