@echo off
echo ========================================
echo   Building Omar's Tools EXE
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Step 1: Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Step 2: Building EXE with PyInstaller...
echo This may take a few minutes...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --console ^
    --name "OmarsTools" ^
    --add-data "frontend;frontend" ^
    --add-data "backend;backend" ^
    --hidden-import uvicorn.logging ^
    --hidden-import uvicorn.loops ^
    --hidden-import uvicorn.loops.auto ^
    --hidden-import uvicorn.protocols ^
    --hidden-import uvicorn.protocols.http ^
    --hidden-import uvicorn.protocols.http.auto ^
    --hidden-import uvicorn.protocols.websockets ^
    --hidden-import uvicorn.protocols.websockets.auto ^
    --hidden-import uvicorn.lifespan ^
    --hidden-import uvicorn.lifespan.on ^
    launcher.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ Build Complete!
echo ========================================
echo.
echo Your EXE is ready at: dist\OmarsTools.exe
echo.
echo To test: cd dist ^&^& OmarsTools.exe
echo.
echo 📦 To share with friends:
echo    - Send them dist\OmarsTools.exe
echo    - They need FFmpeg installed
echo    - No Python required!
echo.
pause