# 🚀 AF IMPERIYA - Enterprise Management System

**Version**: 2.0.0 | **Status**: Production-Ready | **Stack**: Flask + PostgreSQL + Telegram

---

## ✅ SIZDA BOR NARSALAR

- ✅ Telegram Bot Token
- ✅ Telegram Admin User ID  
- ✅ DATABASE_URL (PostgreSQL)

**MUKAMMAL!** Deploy qilishga tayyorsiz!

---

## 🚀 DEPLOY (20 DAQIQA)

### 1. GITHUB (5 min)
```bash
git init
git add .
git commit -m "Production ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/af-imperiya.git
git push -u origin main
```

### 2. RENDER.COM WEB SERVICE (5 min)
1. New → Web Service
2. Connect GitHub: af-imperiya
3. Settings:
   - Name: af-imperiya
   - Region: Frankfurt
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`

### 3. ENVIRONMENT VARIABLES (3 min)
```bash
DATABASE_URL = [Sizning PostgreSQL URL]
SECRET_KEY = [random 20+ chars]
FLASK_ENV = production
TELEGRAM_BOT_TOKEN = [Sizning token]
TELEGRAM_ADMIN_ID = [Sizning ID]
```

### 4. DEPLOY! (7 min)
Manual Deploy → Deploy latest commit → Live! ✅

### 5. LOGIN
```
https://af-imperiya.onrender.com
admin / admin123
⚠️ Parolni o'zgartiring!
```

---

## 📁 STRUKTURA

```
af_imperiya/
├── app.py                 # Main app
├── modules/               # Business logic
│   ├── models.py         # Database
│   ├── routes.py         # Routes
│   └── utils.py          # Helpers
├── templates/            # HTML
├── static/               # CSS, JS, Images
└── requirements.txt      # Dependencies
```

---

## 🎯 XUSUSIYATLAR

- 14 ta to'liq modul
- Admin Dashboard
- User Management
- Real Chat
- Telegram Bot
- Excel export
- File upload
- Professional UI/UX

---

## 🔑 DEFAULT USERS

```
admin / admin123 (Administrator)
demo / demo123 (Read-only)
```

---

## 💰 XARAJATLAR

**Free**: $0 (test uchun)
**Starter**: $14/month (production)

---

## 🎉 TAYYOR!

Deploy qiling va ishlating! **Omad! 🚀**
