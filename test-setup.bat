@echo off
chcp 65001 >nul
echo Testing basic setup with Python 3.13...

:: Создаем venv
python -m venv venv_test
call venv_test\Scripts\activate.bat

:: Пробуем установить только самые необходимые пакеты
echo Installing minimal packages...
pip install --upgrade pip

:: FastAPI и зависимости
pip install fastapi
pip install uvicorn
pip install pydantic
pip install typing-extensions

:: SQLAlchemy с SQLite (не требует дополнительных драйверов)
pip install sqlalchemy

:: Проверяем что установилось
echo.
echo Installed packages:
pip list

pause