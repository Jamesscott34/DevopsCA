#!/bin/bash

# =============================================================================
# Setup Script for SBA24070 Book Catalogue App
# =============================================================================
# This script sets up the application, creates a virtual environment, installs 
# requirements, runs migrations, sets up the admin user, and starts the Django 
# server. It handles both fresh installations and existing project setups.
# =============================================================================

# Exit on any error to prevent partial setups
set -e

# Display welcome message and script information
echo "=========================================="
echo "SBA24070 Book Catalogue Setup Script"
echo "=========================================="

# =============================================================================
# Virtual Environment Setup
# =============================================================================

# Prompt user for virtual environment name with default fallback
read -p "Enter a name for your virtual environment [devops]: " VENV_NAME
VENV_NAME=${VENV_NAME:-devops}

# =============================================================================
# Prerequisites Check
# =============================================================================

# Verify Python 3 is installed and accessible
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3 first."
    echo "Visit https://www.python.org/downloads/ for installation instructions."
    exit 1
fi

# =============================================================================
# Virtual Environment Creation
# =============================================================================

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment '$VENV_NAME'..."
    python3 -m venv "$VENV_NAME"
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment '$VENV_NAME' already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment: $VENV_NAME"
source "$VENV_NAME/bin/activate"
echo "Virtual environment activated successfully!"

# =============================================================================
# Dependencies Installation
# =============================================================================

# Install Django and requirements
echo "Installing Django and requirements..."

# Upgrade pip to latest version for better compatibility
pip install --upgrade pip

# Check if requirements.txt exists, if not install Django directly
if [ -f requirements.txt ]; then
    echo "Found requirements.txt - installing all dependencies..."
    pip install -r requirements.txt
    echo "All requirements installed successfully!"
else
    echo "No requirements.txt found, installing Django directly..."
    pip install django
    echo "Django installed successfully!"
fi

# =============================================================================
# Django Project Setup
# =============================================================================

# Check if Django project exists (look for manage.py)
if [ ! -f "manage.py" ]; then
    echo "Django project not found. Creating new Django project..."
    django-admin startproject book_catalog .
    echo "Django project 'book_catalog' created successfully!"
else
    echo "Django project already exists."
fi

# Check if books app exists
if [ ! -d "books" ]; then
    echo "Books app not found. Creating new Django app..."
    python manage.py startapp books
    echo "Books app created successfully!"
else
    echo "Books app already exists."
fi

# =============================================================================
# Database Setup
# =============================================================================

# Run Django migrations to set up the database
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Database setup completed successfully!"

# =============================================================================
# Admin User Setup
# =============================================================================

# Set up admin user using the admin management script
echo "Setting up admin user..."
python admin_manager.py
echo "Admin user setup completed!"

# =============================================================================
# Application Launch
# =============================================================================

# Start Django development server with user instructions
echo "Starting Django development server..."
echo "=========================================="
echo ""
echo "🎉 Setup Complete! Your application is ready."
echo ""
echo "📋 Quick Reference:"
echo "   • Stop server: Press CTRL+C"
echo "   • Home page: http://127.0.0.1:8000"
echo "   • Admin login: http://127.0.0.1:8000/login/"
echo ""
echo "🔑 Admin Credentials:"
echo "   • Username: admin"
echo "   • Password: admin"
echo ""
echo "👤 User Options:"
echo "   • Login as admin (recommended for first time)"
echo "   • Register new user: http://127.0.0.1:8000/register/"
echo ""
echo "📚 Features Available:"
echo "   • Book catalog management"
echo "   • User profile editing"
echo "   • Password changes"
echo "   • Admin dashboard"
echo "   • Open Library integration"
echo ""
echo "=========================================="
echo "🚀 Starting server..."
echo "=========================================="
echo ""

# Start the Django development server
python manage.py runserver 