#!/bin/bash

# Inventory Management System - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "  Inventory Management System Launcher"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Checking database..."
python manage.py migrate --noinput

echo ""
echo "Creating admin user..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>/dev/null || true

echo "Setting admin password..."
python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save()" 2>/dev/null || true

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "Starting Django development server..."
echo ""
echo "Access the application at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin/"
echo ""
echo "Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
