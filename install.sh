#!/bin/bash

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "   🚀 AF IMPERIYA - AVTOMATIK O'RNATISH"
echo "   Linux/Mac uchun"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Check Python
echo "[1/6] Python tekshirilmoqda..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python topilmadi!"
    echo "Python 3.9+ ni o'rnating"
    exit 1
fi
echo "✅ Python topildi: $(python3 --version)"
echo ""

# Create virtual environment
echo "[2/6] Virtual environment yaratilmoqda..."
if [ -d "venv" ]; then
    echo "⚠️  venv mavjud, o'chirish..."
    rm -rf venv
fi
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Virtual environment yaratilmadi!"
    exit 1
fi
echo "✅ Virtual environment yaratildi"
echo ""

# Activate virtual environment
echo "[3/6] Virtual environment faollashtirilmoqda..."
source venv/bin/activate
echo "✅ Virtual environment faol"
echo ""

# Upgrade pip
echo "[4/6] pip yangilanmoqda..."
pip install --upgrade pip --quiet
echo "✅ pip yangilandi"
echo ""

# Install requirements
echo "[5/6] Kutubxonalar o'rnatilmoqda..."
echo "Bu 1-2 daqiqa davom etishi mumkin..."
echo "⚠️  psycopg2-binary o'rnatilmaydi (faqat Render.com uchun kerak)"
pip install -r requirements-local.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Kutubxonalar o'rnatilmadi!"
    echo ""
    echo "Qo'lda urinib ko'ring:"
    echo "pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug openpyxl requests python-dotenv python-telegram-bot"
    exit 1
fi
echo "✅ Barcha kutubxonalar o'rnatildi (local uchun)"
echo ""

# Create database
echo "[6/6] Database yaratilmoqda..."
python reset_database.py
if [ $? -ne 0 ]; then
    echo "❌ Database yaratilmadi!"
    exit 1
fi
echo "✅ Database yaratildi"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "   ✅ O'RNATISH MUVAFFAQIYATLI!"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Server'ni ishga tushirish uchun:"
echo "   ./start.sh"
echo ""
