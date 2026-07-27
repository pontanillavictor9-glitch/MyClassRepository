@echo off
chcp 65001 >nul
title Tienda de Dropshipping
echo ==========================================
echo   ARRANCANDO LA TIENDA
echo ==========================================
echo.

if not exist node_modules (
    echo [ERROR] Primero haz doble clic en  instalar.bat
    pause
    exit /b 1
)

echo Arrancando el servidor de la tienda...
start "Tienda - Servidor (NO CERRAR)" cmd /k npm run tienda

timeout /t 3 /nobreak >nul

echo Abriendo la tienda en el navegador...
start http://localhost:4000/

echo.
echo ==========================================
echo   TIENDA EN MARCHA
echo ==========================================
echo.
echo Deja abierta la ventana negra del servidor mientras la uses.
echo.
echo Para poner TUS productos edita:   tienda\js\productos.js
echo Guia del negocio paso a paso:     tienda\README.md
echo.
echo Esta ventana ya se puede cerrar.
pause
