# AF IMPERIYA - Tezkor Boshlash

## 🚀 5 Daqiqada Ishga Tushiring

### 1-Qadam: Arxivni Ochish
```bash
tar -xzf AF_IMPERIYA_*.tar.gz
cd af_imperiya
```

### 2-Qadam: Kutubxonalarni O'rnatish
```bash
pip install -r requirements.txt
```

### 3-Qadam: Serverni Ishga Tushiring
```bash
python app.py
```

### 4-Qadam: Brauzerda Oching
```
http://localhost:5000
```

### 5-Qadam: Login Qiling
```
Admin: admin / admin123
Rahbar: rahbar / rahbar123
```

---

## 📋 Asosiy Xususiyatlar

### ✅ Tayyor Funksiyalar:
- Role-based access control (Admin, Rahbar, Xodim, User)
- Database modellari (SQLAlchemy)
- Telegram bot integratsiyasi
- Login/Logout tizimi
- Dashboard
- O'zbek milliy dizayni
- Real-time xabarnomalar (Telegram)
- Deployment tayyor (Render, Railway, Docker)

### 📦 Barcha 13 ta Modul:
1. **Topshiriqlar** - Task management
2. **Avto Transport** - Vehicle management
3. **Ijro** - Execution tracking + Real-time chat
4. **Binolar** - Building management
5. **Yashil Makonlar** - Green spaces
6. **Quyosh Panellari** - Solar panels
7. **Xodimlar** - Employee management
8. **Autsorsing** - Outsourcing services
9. **Tashkilotlar** - Organizations
10. **Mehmonlar** - Guest management
11. **Tabriknomalar** - Congratulations
12. **Shartnomalar** - Contracts
13. **Ombor** - Warehouse requests

---

## 🔧 Qo'shimcha Sozlash

### Telegram Bot:
```bash
# .env faylni yarating
cp .env.example .env

# Tokenni kiriting
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

### PostgreSQL (Production):
```bash
# .env da o'zgartiring
DATABASE_URL=postgresql://user:pass@host:5432/db
```

---

## 🌐 Internet'ga Chiqarish

### Render.com (Eng Oson):
1. GitHub'ga push qiling
2. Render.com'da yangi Web Service yarating
3. Repository ni ulang
4. Deploy tugmasini bosing

Batafsil: `DEPLOYMENT.md` faylini ko'ring

---

## 🆘 Yordam

### Xatolik yuzaga kelsa:

**Database xatoligi:**
```python
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

**Port band bo'lsa:**
```bash
# Boshqa portda ishga tushiring
PORT=8000 python app.py
```

**Kutubxona xatoligi:**
```bash
pip install --upgrade -r requirements.txt
```

---

## 📚 To'liq Qo'llanmalar

- `README.md` - Umumiy ma'lumot
- `DEPLOYMENT.md` - Internet'ga chiqarish
- `QOLLANMA.txt` - O'zbekcha qo'llanma

---

**Savollaringiz bormi?** 
- Email: support@afimperiya.uz
- GitHub: Issues bo'limida yozing

---

🎉 **Muvaffaqiyatli ishlatishingizni tilaymiz!**
