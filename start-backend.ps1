$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Không tạo được môi trường Python.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r backend\requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Không cài được thư viện Python.' }
Set-Location backend
& '..\.venv\Scripts\python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
