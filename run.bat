@echo off
echo ======================================
echo Video Sorter ^& YouTube Uploader
echo ======================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python detecte: 
python --version
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo Environnement virtuel cree avec succes!
    echo.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)
echo.

REM Vérifier si les dépendances sont installées
echo Verification des dependances...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dependances
        pause
        exit /b 1
    )
    echo Dependances installees avec succes!
    echo.
)

REM Lancer l'application
echo Lancement de l'application...
echo.
python main.py

REM Si l'application se ferme avec une erreur
if errorlevel 1 (
    echo.
    echo L'application s'est fermee avec une erreur.
    pause
)
