@echo off
echo Starting Crop Prediction Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and start the application
echo Activating virtual environment...
call venv\Scripts\activate

echo Starting Flask application...
python app.py

pause