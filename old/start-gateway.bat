@echo off
chcp 65001 > nul
title nanobot Gateway (AI + Canales)
echo.
echo  nanobot Gateway
echo ================
echo.
echo Iniciando el gateway de nanobot...
echo Asegúrate de que el bridge de WhatsApp ya esté corriendo.
echo.

set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

python -m nanobot gateway

pause
