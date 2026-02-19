@echo off
chcp 65001 > nul
title nanobot WhatsApp Bridge
echo.
echo  nanobot WhatsApp Bridge
echo ========================
echo.
echo Iniciando bridge de WhatsApp...
echo Cuando aparezca el QR code, escanéalo desde tu WhatsApp:
echo   Configuración - Dispositivos vinculados - Vincular un dispositivo
echo.

cd /d "%USERPROFILE%\.nanobot\bridge"
set AUTH_DIR=%USERPROFILE%\.nanobot\whatsapp-auth
set BRIDGE_PORT=3001

node dist/index.js

pause
