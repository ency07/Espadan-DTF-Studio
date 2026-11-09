@echo off
setlocal
cd /d "%~dp0"
if not exist "dtf_env\Scripts\python.exe" (
    echo [ERROR] No se encontro dtf_env. Creando entorno...
    python -m venv dtf_env
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno. Verifica que Python 3.10+ este instalado.
        pause
        exit /b 1
    )
    dtf_env\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Fallo la instalacion de dependencias.
        pause
        exit /b 1
    )
)
echo Iniciando Espadan DTF Studio...
dtf_env\Scripts\python.exe main.py
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion termino con error.
    pause
)
endlocal
