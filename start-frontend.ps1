$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot 'frontend')
npm install
if ($LASTEXITCODE -ne 0) { throw 'Không cài được thư viện frontend.' }
npm run dev
