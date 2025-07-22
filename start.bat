@echo off
echo Starting Multi-Agent Financial Analysis System...
echo.

echo Setting up Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo IMPORTANT: Configure your OpenAI API key
echo ========================================
echo Edit backend\agents\financial_orchestrator.py
echo Replace "your-openai-api-key-here" with your actual OpenAI API key
echo.
pause

echo Starting Flask server...
start cmd /k "cd /d %CD% && call venv\Scripts\activate && python app.py"

cd ..\frontend

echo.
echo Setting up Frontend...
echo Installing Node.js dependencies...
call npm install

echo Starting React development server...
start cmd /k "cd /d %CD% && npm start"

echo.
echo ========================================
echo System is starting up!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Make sure to configure your OpenAI API key before using the system.
pause
