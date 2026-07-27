@echo off
chcp 65001 >nul
title Trading Live Studio
echo ==========================================
echo   ARRANCANDO TRADING LIVE STUDIO
echo ==========================================
echo.

if not exist node_modules (
    echo [ERROR] Primero haz doble clic en  instalar.bat
    pause
    exit /b 1
)

echo Arrancando el servidor...
start "Trading Live Studio - Servidor (NO CERRAR)" cmd /k npm start

timeout /t 4 /nobreak >nul

where python >nul 2>nul
if not errorlevel 1 (
    echo Arrancando el puente de MetaTrader 5...
    echo   (si MT5 no esta abierto, dara error - abrelo y ejecuta esto de nuevo)
    start "Puente MT5 (NO CERRAR)" cmd /k python mt5/bridge.py
)

echo Abriendo tu panel de control en el navegador...
start http://localhost:3000/panel.html

echo.
echo ==========================================
echo   TODO EN MARCHA
echo ==========================================
echo.
echo Se han abierto 2 ventanas negras: dejalas abiertas mientras
echo hagas el directo (son el servidor y el puente MT5).
echo.
echo URLs para OBS (Fuente de navegador):
echo   http://localhost:3000/overlay/positions   (posiciones)
echo   http://localhost:3000/overlay/daily       (beneficio del dia)
echo   http://localhost:3000/overlay/disclaimer  (aviso legal)
echo   http://localhost:3000/overlay/chat        (chat unificado)
echo.
echo Esta ventana ya se puede cerrar.
pause
