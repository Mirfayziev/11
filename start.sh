#!/bin/bash

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "   🚀 AF IMPERIYA - SERVER"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment topilmadi!"
    echo ""
    echo "install.sh ni avval ishga tushiring:"
    echo "   ./install.sh"
    echo ""
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if database exists
if [ ! -f "instance/af_imperiya.db" ]; then
    echo "⚠️  Database topilmadi, yaratilmoqda..."
    python reset_database.py
fi

# Start server
echo "✅ Server ishga tushirilmoqda..."
echo ""
echo "📊 http://localhost:5000"
echo ""
echo "⚠️  To'xtatish: Ctrl+C"
echo ""
python app.py
