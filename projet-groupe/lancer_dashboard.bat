@echo off
REM Script de lancement du dashboard Streamlit

echo ============================================
echo   LANCEMENT DU DASHBOARD BIG DATA
echo ============================================
echo.

cd dashboard
..\.venv\Scripts\streamlit.exe run app.py --server.headless true

pause
