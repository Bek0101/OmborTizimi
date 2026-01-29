@echo off
REM Inventory Management System - Quick Start Script for Windows

echo.
echo ========================================
echo   Inventory Management System Launcher
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Checking database...
python manage.py migrate --noinput

echo.
echo Creating admin user...
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>nul
if errorlevel 1 (
    echo Admin user already exists or creation failed
) else (
    echo Setting admin password...
    python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Starting Django development server...
echo.
echo Access the application at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin/
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
