# 运行前请在仓库根目录执行: python -m venv .venv
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")

Set-Location $Root
Write-Host "工作目录: $Root"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".venv\Scripts\Activate.ps1"
pip install -r requirements.txt
Write-Host "环境就绪。激活: .venv\Scripts\Activate.ps1"
