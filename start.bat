@echo off
echo ========================================
echo    Starting Omar's Tools
echo ========================================
echo.

REM Get the script directory
set "SCRIPT_DIR=%~dp0"

REM Start backend in a new window
echo [1/2] Starting Backend Server...
start "Omar's Tools - Backend" cmd /k "cd /d "%SCRIPT_DIR%backend" && python main.py"

REM Wait 3 seconds for backend to start
echo [2/2] Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

REM Open frontend in default browser
echo Opening frontend in browser...
start "" "%SCRIPT_DIR%frontend\index.html"

echo.
echo ========================================
echo    Omar's Tools is now running!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: Opened in your browser
echo.
echo Press any key to close this window...
echo (Backend will keep running in separate window)
pause >nul