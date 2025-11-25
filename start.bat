@echo off
chcp 65001 > nul
echo.
echo ═══════════════════════════════════════════════════════════════════
echo    🚀 AF IMPERIYA - SERVER
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check if venv exists
if not exist venv (
    echo ❌ Virtual environment topilmadi!
    echo.
    echo install.bat ni avval ishga tushiring:
    echo    install.bat
    echo.
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if database exists
if not exist instance\af_imperiya.db (
    echo ⚠️  Database topilmadi, yaratilmoqda...
    python reset_database.py
)

REM Start server
echo ✅ Server ishga tushirilmoqda...
echo.
echo 📊 http://localhost:5000
echo.
echo ⚠️  To'xtatish: Ctrl+C
echo.
python app.py
