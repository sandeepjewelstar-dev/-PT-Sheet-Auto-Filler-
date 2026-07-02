@echo off
REM PT Sheet Auto-Filler - Quick Start Script for Windows
REM This script will help you run the application

echo ============================================
echo PT Sheet Auto-Filler - Startup Helper
echo ============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo SOLUTION:
    echo 1. Download Python from https://www.python.org/downloads/
    echo 2. Run the installer
    echo 3. CHECK "Add Python to PATH" during installation
    echo 4. Restart Command Prompt and try again
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if required files exist
echo Checking required files...
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo.
    echo Make sure you're in the correct folder:
    echo C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main
    echo.
    pause
    exit /b 1
)

echo ✓ main.py found
echo.

REM Check if dependencies are installed
echo Checking Python dependencies...
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Dependencies may not be installed
    echo.
    echo Installing dependencies now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✓ All dependencies available
echo.

REM Create required folders
echo Creating required folders...
if not exist "templates" mkdir templates
if not exist "images" mkdir images
if not exist "output" mkdir output

echo ✓ Folders created/verified
echo.

REM Check for Tesseract
echo Checking for Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Tesseract OCR not found in system PATH
    echo.
    echo SOLUTION:
    echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Install to: C:\Program Files\Tesseract-OCR
    echo 3. Restart this script
    echo.
    echo The application may still work without Tesseract, but OCR features won't function.
    echo Continue anyway? (Y/N)
    set /p choice="Enter choice: "
    if /i not "%choice%"=="Y" (
        pause
        exit /b 1
    )
)

echo ✓ Tesseract check complete
echo.

REM Start the application
echo ============================================
echo Starting PT Sheet Auto-Filler...
echo ============================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application crashed
    echo Check the error messages above
    pause
)
