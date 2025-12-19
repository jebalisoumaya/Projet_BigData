# Script complet pour lancer le dashboard avec données e-commerce
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   LANCEMENT DASHBOARD + E-COMMERCE" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# 1. Lancer Streamlit en arrière-plan
Write-Host "1. Demarrage Streamlit..." -ForegroundColor Yellow
$streamlitJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\soumayaj\Downloads\TP\projet-groupe"
    & "C:/Users/soumayaj/Downloads/TP/projet-groupe/.venv/Scripts/streamlit.exe" run dashboard/app.py --server.headless true
}
Start-Sleep -Seconds 5
Write-Host "   OK Streamlit en cours: http://localhost:8501`n" -ForegroundColor Green

# 2. Lancer l'analyseur e-commerce
Write-Host "2. Demarrage analyseur e-commerce..." -ForegroundColor Yellow
$analyzerJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\soumayaj\Downloads\TP\projet-groupe"
    & "C:/Users/soumayaj/Downloads/TP/projet-groupe/.venv/Scripts/python.exe" hybride/ecommerce_analyzer.py
}
Start-Sleep -Seconds 5
Write-Host "   OK Analyseur en attente de donnees`n" -ForegroundColor Green

# 3. Envoyer les transactions HDFS -> Kafka
Write-Host "3. Envoi des transactions HDFS vers Kafka...`n" -ForegroundColor Yellow
& "C:/Users/soumayaj/Downloads/TP/projet-groupe/.venv/Scripts/python.exe" hybride/hdfs_to_kafka.py

# 4. Attendre le traitement
Write-Host "`n4. Traitement en cours (20 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# 5. Arrêter l'analyseur (il sauvegarde automatiquement)
Write-Host "`n5. Arret de l'analyseur (sauvegarde dans HDFS)..." -ForegroundColor Yellow
Stop-Job -Id $analyzerJob.Id
Remove-Job -Id $analyzerJob.Id
Start-Sleep -Seconds 2

# 6. Résumé
Write-Host "`n============================================" -ForegroundColor Green
Write-Host "   TOUT EST PRET !" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Green

Write-Host "Dashboard Streamlit: " -NoNewline -ForegroundColor Cyan
Write-Host "http://localhost:8501" -ForegroundColor White -BackgroundColor DarkGreen

Write-Host "`nDans le dashboard:" -ForegroundColor Yellow
Write-Host "  1. Allez sur 'E-Commerce Analytics'" -ForegroundColor White
Write-Host "  2. Cliquez sur 'Actualiser les donnees'" -ForegroundColor White
Write-Host "  3. Vous verrez les graphiques et statistiques`n" -ForegroundColor White

Write-Host "Pour arreter le dashboard:" -ForegroundColor Yellow
Write-Host "  Stop-Job -Id $($streamlitJob.Id)" -ForegroundColor White
Write-Host "  Remove-Job -Id $($streamlitJob.Id)`n" -ForegroundColor White

Write-Host "Ou appuyez sur Ctrl+C puis executez:" -ForegroundColor Yellow
Write-Host "  Get-Job | Stop-Job; Get-Job | Remove-Job`n" -ForegroundColor White

Write-Host "============================================`n" -ForegroundColor Green
