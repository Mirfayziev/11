#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════"
echo "   🚀 AF IMPERIYA - RENDER.COM DEPLOY"
echo "═══════════════════════════════════════════════════════════════════"

# Check if git repo
if [ ! -d ".git" ]; then
    echo "❌ Git repository yo'q!"
    echo "Avval git init qiling"
    exit 1
fi

echo "[1/3] Git status tekshirilmoqda..."
git status

echo ""
echo "[2/3] Commit va push..."
git add .
git commit -m "Deploy to Render.com - $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main

echo ""
echo "[3/3] Render.com'da deploy boshlandi!"
echo ""
echo "✅ Git push muvaffaqiyatli!"
echo ""
echo "Render.com Dashboard'ga kiring:"
echo "https://dashboard.render.com"
echo ""
echo "Logs'ni kuzating:"
echo "Service → Logs → View full logs"
echo ""
echo "Deploy tugagach URL'ni oching:"
echo "https://af-imperiya.onrender.com"
echo ""
