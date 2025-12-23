@echo off
REM Chennai Local Guide - Windows Startup Script
REM This batch file provides an easy way to start the server on Windows

echo 🎬 Chennai Local Guide - Demo Server
echo =====================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "start_server.py" (
    echo ❌ start_server.py not found
    echo Please run this script from the Chennai Local Guide project directory
    pause
    exit /b 1
)

REM Start the server with default settings
echo 🚀 Starting Chennai Local Guide server...
python start_server.py --dev

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ❌ Server failed to start
    pause
)