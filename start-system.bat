@echo off
chcp 65001 >nul
echo ===================================================
echo    Secret Management System - Auto Starter
echo ===================================================
echo.

:: Проверяем Docker
echo [1/5] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop and ensure it's running.
    pause
    exit /b 1
)

:: Создаем виртуальное окружение если нужно
echo [2/5] Setting up Python environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Устанавливаем зависимости через прямое обращение к Python
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r backend\requirements.txt

:: Запускаем Docker сервисы
echo [4/5] Starting Docker services...
cd docker-compose
docker-compose up -d postgres keycloak openbao

:: Ждем запуска
echo Waiting for services to start (15 seconds)...
timeout /t 15 /nobreak >nul

:: Запускаем бэкенд
echo [5/5] Starting FastAPI backend...
cd ..\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause