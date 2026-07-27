@echo off
chcp 65001 >nul
title Instalacion - Trading Live Studio
echo ==========================================
echo   INSTALACION DE TRADING LIVE STUDIO
echo ==========================================
echo.

where node >nul 2>nul
if errorlevel 1 (
    echo [ERROR] No tienes Node.js instalado.
    echo.
    echo   1. Ve a https://nodejs.org y descarga la version LTS
    echo   2. Instalala con siguiente-siguiente
    echo   3. Vuelve a hacer doble clic en este archivo
    echo.
    start https://nodejs.org
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias del servidor (puede tardar un par de minutos)...
call npm install
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion. Cierra y vuelve a intentarlo.
    pause
    exit /b 1
)

echo [2/3] Creando tu archivo de configuracion...
if not exist config.json copy config.example.json config.json >nul

echo [3/3] Instalando el puente de MetaTrader 5 (opcional)...
where python >nul 2>nul
if errorlevel 1 (
    echo   [AVISO] No tienes Python: el puente MT5 no funcionara todavia.
    echo   Si quieres usar MT5: instala Python de https://python.org
    echo   marcando "Add Python to PATH", y ejecuta este archivo otra vez.
) else (
    python -m pip install --quiet MetaTrader5 requests
    echo   Puente MT5 listo.
)

echo.
echo ==========================================
echo   INSTALACION COMPLETADA
echo ==========================================
echo.
echo Ahora se abrira tu configuracion en el Bloc de notas.
echo Cambia: tus canales de Twitch/YouTube/TikTok, el nombre
echo de tu comunidad y el panelToken (inventate una clave).
echo Guarda con Ctrl+S y cierralo.
echo.
echo Despues, haz doble clic en  arrancar.bat  para empezar.
echo.
notepad config.json
pause
