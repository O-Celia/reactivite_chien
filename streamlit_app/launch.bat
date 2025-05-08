@echo off
:: Définit le chemin vers le dossier contenant WinPython
set WINPYTHONPATH="D:\Document\Reactivite_Chien\WPy64-31241\python-3.12.4.amd64\python.exe"

:: Affiche le chemin de python pour vérification
echo %WINPYTHONPATH%

:: Aller dans le dossier contenant ton code et base de données
cd /d "D:\Document\Appli Loki\reactivite_chien\streamlit_app"

:: Exécuter l'app Streamlit avec Python de WinPython
%WINPYTHONPATH% -m streamlit run main_app.py

:: Pause pour éviter que la fenêtre de commande se ferme immédiatement
pause
