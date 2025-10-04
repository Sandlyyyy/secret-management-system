@echo off
chcp 65001 >nul
echo ===================================================
echo    Secret Management System - Python 3.13
echo ===================================================
echo.

echo Python Version: 3.13.7 64-bit
echo.

:: Проверяем Docker
echo [1/6] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop and ensure it's running.
    pause
    exit /b 1
)

:: Очищаем старое окружение
echo [2/6] Cleaning old environment...
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

:: Создаем новое виртуальное окружение
echo [3/6] Creating new virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Устанавливаем зависимости с совместимыми версиями
echo [4/6] Installing Python 3.13 compatible packages...
pip install --upgrade pip

:: Устанавливаем пакеты по одному для лучшего контроля
pip install "fastapi>=0.104.0"
pip install "uvicorn[standard]>=0.24.0"
pip install "sqlalchemy>=2.0.0"
pip install "psycopg>=3.1.0"
pip install "python-jose[cryptography]>=3.3.0"
pip install "passlib[bcrypt]>=1.7.4"
pip install "cryptography>=41.0.0"
pip install "httpx>=0.25.0"
pip install "python-multipart>=0.0.6"
pip install "pydantic>=2.5.0"
pip install "alembic>=1.12.0"
pip install "python-keycloak>=2.14.0"
pip install "hvac>=1.1.0"

:: Запускаем сервисы
echo [5/6] Starting Docker services...
cd docker-compose
docker-compose up -d postgres keycloak openbao

:: Ждем запуска
echo Waiting for services to start (25 seconds)...
timeout /t 25 /nobreak >nul

:: Запускаем бэкенд
echo [6/6] Starting FastAPI backend...
cd ..\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause