@echo off
REM ============================================================
REM  LOCUTOR - doble clic y listo.
REM  - Sin argumentos: locuta el guion.txt de esta carpeta.
REM  - O arrastra tu .txt encima de este .bat.
REM  La primera vez instala solo el motor de voz (gratis).
REM ============================================================
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Falta Python. Instalalo desde https://www.python.org/downloads/
  echo (boton amarillo, y MARCA la casilla "Add python.exe to PATH")
  pause
  exit /b 1
)

python -c "import edge_tts" >nul 2>nul
if errorlevel 1 (
  echo Instalando el motor de voz (solo esta primera vez)...
  python -m pip install edge-tts
)

if "%~1"=="" (
  python locutar.py guion.txt
) else (
  python locutar.py "%~1"
)
pause
