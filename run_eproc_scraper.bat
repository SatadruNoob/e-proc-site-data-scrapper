@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM ======================================================
REM NIC eProcurement Tender Scraper - One Click Launcher
REM ======================================================

REM Get directory where this BAT file is located
set SCRIPT_DIR=%~dp0

echo ======================================
echo NIC eProcurement Tender Scraper
echo ======================================
echo.

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Virtual environment not found.
    echo [INFO] Creating virtual environment...
    python -m venv venv

    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate

    echo [INFO] Installing dependencies...
    pip install --upgrade pip
    pip install playwright pandas openpyxl

    echo [INFO] Installing Playwright Chromium...
    playwright install chromium
) else (
    echo [INFO] Activating existing virtual environment...
    call venv\Scripts\activate
)

echo.
echo [INFO] Running eProcurement scraper...
echo.

python eproc_data_scraper.py

echo.
echo ======================================
echo Scraping finished.
echo Excel file updated successfully.
echo ======================================
echo.

pause
ENDLOCAL
