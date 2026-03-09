@echo off
echo ======================================================
echo   GERADOR DE EXECUTAVEL - ROBO SEGURADORA
echo ======================================================
echo.
echo 1. Instalando dependencias necessarias...
pip install -r requirements.txt
echo.
echo 2. Gerando arquivo EXE (isso pode levar alguns minutos)...
echo O executavel sera criado na pasta 'dist'
echo.
pyinstaller --noconfirm --onefile --windowed --name "RoboSeguradora" --add-data "modules;modules" --add-data "config.py;." gui_app.py

echo.
echo ======================================================
echo   CONCLUIDO! O arquivo esta na pasta 'dist'
echo ======================================================
pause
