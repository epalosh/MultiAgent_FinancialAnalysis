@echo off
echo Starting Financial Analysis Research Platform...
echo.

echo Starting Backend Server...
cd backend
start "Backend Server" cmd /k "python app.py"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo Starting Frontend Development Server...
cd ..\frontend
start "Frontend Server" cmd /k "npm start"

echo.
echo Both servers are starting...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo The frontend should automatically open in your browser.
echo Press any key to close this window...
pause > nul
