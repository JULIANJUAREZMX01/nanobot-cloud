@echo off
chcp 65001 > nul
title nanobot - Lanzador

echo.
echo  nanobot Personal AI Assistant
echo ================================
echo  Proyectos: C:\Users\QUINTANA\sistemas\
echo  WhatsApp: 9813344909
echo ================================
echo.
echo Abriendo bridge y gateway en ventanas separadas...
echo.

REM Ventana 1: Bridge de WhatsApp (Node.js)
start "nanobot Bridge" cmd /k "chcp 65001 && cd /d %USERPROFILE%\.nanobot\bridge && set BRIDGE_PORT=3001 && set AUTH_DIR=%USERPROFILE%\.nanobot\whatsapp-auth && node dist/index.js"

REM Esperar 3 segundos para que el bridge inicie
timeout /t 3 /nobreak > nul

REM Ventana 2: Gateway de nanobot (Python)
start "nanobot Gateway" cmd /k "chcp 65001 && set PYTHONIOENCODING=utf-8 && set PYTHONUTF8=1 && python -m nanobot gateway"

echo.
echo Bridge y Gateway iniciados en ventanas separadas.
echo.
echo INSTRUCCIONES:
echo  1. En la ventana del Bridge: escanea el QR code con WhatsApp
echo     (Configuracion - Dispositivos vinculados - Vincular dispositivo)
echo  2. Una vez vinculado, escribe desde tu movil al numero 9813344909
echo  3. Espera la respuesta del AI assistant
echo.
echo Para chatear desde la terminal: python -m nanobot agent
echo.
pause
