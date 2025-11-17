
@echo off
echo ========================================
echo    Stopping Omar's Tools
echo ========================================
echo.

REM Kill all Python processes running main.py
echo Stopping backend server...
taskkill /FI "WINDOWTITLE eq Omar's Tools - Backend*" /T /F 2>nul

if %ERRORLEVEL% EQU 0 (
    echo Backend stopped successfully!
) else (
    echo No backend process found.
)

echo.
echo ========================================
echo    Omar's Tools stopped!
echo ========================================
echo.
pause