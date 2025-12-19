# Script simple pour lancer le dashboard
# Utilisez ce script si vous avez des problèmes

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   LANCEMENT DASHBOARD STREAMLIT" -ForegroundColor Cyan  
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Demarrage du dashboard..." -ForegroundColor Yellow
Write-Host "Le dashboard s'ouvrira automatiquement dans votre navigateur`n" -ForegroundColor White

# Lancer Streamlit
& "C:/Users/soumayaj/Downloads/TP/projet-groupe/.venv/Scripts/streamlit.exe" run dashboard/app.py

Write-Host "`nDashboard arrete." -ForegroundColor Yellow
