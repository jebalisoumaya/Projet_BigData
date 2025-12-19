# PowerShell script pour lancer le dashboard
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   LANCEMENT DU DASHBOARD BIG DATA" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Demarrage de Streamlit...`n" -ForegroundColor Yellow

Set-Location -Path "dashboard"

# Lancer Streamlit avec les bonnes options
& "$PSScriptRoot\.venv\Scripts\streamlit.exe" run app.py --server.headless true --browser.gatherUsageStats false

Write-Host "`nDashboard arrete." -ForegroundColor Yellow
