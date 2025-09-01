@echo off
echo =================================================
echo   Samsung Pass Converter Build Script
echo =================================================
echo.

REM Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3 from python.org and try again.
    pause
    exit /b 1
)

echo Found Python installation.
echo.

REM Set up virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install cryptography sv-ttk darkdetect pyinstaller
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo =================================================
echo   Running PyInstaller...
echo =================================================
echo This may take a few moments.
echo.

if exist "icon.ico" (
    echo Found icon.ico, including it in the build.
    pyinstaller --onefile --windowed --name "SamsungPassConverter" --icon="icon.ico" gui.py
) else (
    echo icon.ico not found, building without a custom icon.
    pyinstaller --onefile --windowed --name "SamsungPassConverter" gui.py
)


echo.
echo =================================================
if exist "dist\SamsungPassConverter.exe" (
    echo Build successful!
    echo The executable can be found in the 'dist' folder:
    echo %cd%\dist\SamsungPassConverter.exe
) else (
    echo Build failed. Please check the output above for errors.
)
echo =================================================
echo.

pause
