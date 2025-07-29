@echo off
echo ================================================
echo    Multi-Tool AI Platform - Quick Launch
echo ================================================
echo.
echo Starting Python backend...
cd /d "%~dp0backend"
start "Python Backend" cmd /k "python main.py"
echo Backend started in separate window
echo.
echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak >nul
echo.
echo Opening application in browser...
start http://localhost:8000
echo.
echo ================================================
echo    Application is now running!
echo    - Backend: http://localhost:8000
echo    - Close the Python Backend window to stop
echo ================================================
pause
