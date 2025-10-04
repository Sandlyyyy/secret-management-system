@echo off
chcp 65001 >nul
echo Testing basic setup with Python 3.13...

:: ������� venv
python -m venv venv_test
call venv_test\Scripts\activate.bat

:: ������� ���������� ������ ����� ����������� ������
echo Installing minimal packages...
pip install --upgrade pip

:: FastAPI � �����������
pip install fastapi
pip install uvicorn
pip install pydantic
pip install typing-extensions

:: SQLAlchemy � SQLite (�� ������� �������������� ���������)
pip install sqlalchemy

:: ��������� ��� ������������
echo.
echo Installed packages:
pip list

pause