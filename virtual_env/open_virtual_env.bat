@echo off
REM Ce script active l'environnement virtuel sous Windows.
if exist "virtual_env\venv\Scripts\activate.bat" (
    echo Verrification de l'etat de l'environement virtuel.
    if "%VIRTUAL_ENV%"=="" (
        echo Activation de l'environement virtuel.
        call virtual_env\venv\Scripts\activate.bat
    ) else (
        echo L'environement virtuel est deja active.
    )
) else (
    call virtual_env\create_virtual_env.bat
)