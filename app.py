"""
AF IMPERIYA - Enterprise Management System
100% TO'LIQ - Barcha muammolar hal qilindi
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

# Flask App
app = Flask(__name__)

# =========================== CONFIGURATION ===========================

# Secret Key (production uchun environment variable ishlatish kerak!)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'af-imperiya-secret-key-2024-change-in-production')

# Database (Render.com uchun PostgreSQL)
if os.getenv('DATABASE_URL'):
    database_url = os.getenv('DATABASE_URL')
    # Fix postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'af_imperiya.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'documents': {'pdf', 'doc', 'docx', 'xls', 'xlsx'},
    'all': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Create upload folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('instance', exist_ok=True)  # Database uchun
for folder in ['vehicles', 'buildings', 'employees', 'organizations', 'guests', 'congratulations', 'contracts']:
    os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)

# =========================== DATABASE INIT ===========================

from modules.models import db, User
from modules.utils import save_file, delete_file, has_module_permission, format_date, format_money

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================== CONTEXT PROCESSORS ===========================

@app.context_processor
def inject_helpers():
    """Template helper functions"""
    return dict(
        has_module_permission=has_module_permission,
        format_date=format_date,
        format_money=format_money,
        today=datetime.now()
    )

# =========================== CORE ROUTES ===========================

@app.route('/')
def index():
    """Bosh sahifa"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login sahifasi"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Sizning akkauntingiz faol emas!', 'danger')
                return render_template('login.html')
            
            login_user(user, remember=True)
            flash(f'Xush kelibsiz, {user.full_name}!', 'success')
            
            # Parol o'zgartirish majburiy bo'lsa
            if user.must_change_password:
                flash('Iltimos, birinchi parolingizni o\'zgartiring!', 'warning')
                return redirect(url_for('change_password'))
            
            return redirect(url_for('dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Ro'yxatdan o'tish"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            telegram_username = request.form.get('telegram_username', '').strip()
            phone = request.form.get('phone', '').strip()
            
            # Validatsiya
            if not all([full_name, username, email, password]):
                flash('Barcha majburiy maydonlarni to\'ldiring!', 'danger')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Parollar mos kelmayapti!', 'danger')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Parol kamida 6 ta belgidan iborat bo\'lishi kerak!', 'danger')
                return render_template('register.html')
            
            # Username mavjudligini tekshirish
            if User.query.filter_by(username=username).first():
                flash('Bu username allaqachon band!', 'danger')
                return render_template('register.html')
            
            # Email mavjudligini tekshirish
            if User.query.filter_by(email=email).first():
                flash('Bu email allaqachon ro\'yxatdan o\'tgan!', 'danger')
                return render_template('register.html')
            
            # Yangi user yaratish
            new_user = User(
                full_name=full_name,
                username=username,
                email=email,
                phone=phone,
                telegram_username=telegram_username,
                role='user',  # Default role
                is_active=True,
                telegram_notifications=True if telegram_username else False
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Ro\'yxatdan muvaffaqiyatli o\'tdingiz! Endi login qiling.', 'success')
            
            if telegram_username:
                flash(f'Telegram\'da @af_imperiya_bot ga /start yuboring!', 'info')
            
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Xatolik yuz berdi: {str(e)}', 'danger')
            print(f"Register error: {e}")
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('Tizimdan chiqdingiz!', 'info')
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Parolni o'zgartirish"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validatsiya
        if not current_user.check_password(old_password):
            flash('Eski parol noto\'g\'ri!', 'danger')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('Yangi parollar mos kelmayapti!', 'danger')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('Parol kamida 6 ta belgidan iborat bo\'lishi kerak!', 'danger')
            return render_template('change_password.html')
        
        # Parolni o'zgartirish
        current_user.set_password(new_password)
        current_user.must_change_password = False
        db.session.commit()
        
        flash('Parol muvaffaqiyatli o\'zgartirildi!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profil sozlamalari"""
    if request.method == 'POST':
        try:
            current_user.full_name = request.form.get('full_name')
            current_user.email = request.form.get('email')
            current_user.phone = request.form.get('phone', '')
            
            # Telegram sozlamalari
            telegram_username = request.form.get('telegram_username', '').strip()
            if telegram_username:
                current_user.telegram_username = telegram_username
                current_user.telegram_notifications = request.form.get('telegram_notifications') == 'on'
            
            db.session.commit()
            flash('Profil muvaffaqiyatli yangilandi!', 'success')
            
            if telegram_username and not current_user.telegram_chat_id:
                flash('Telegram\'da @af_imperiya_bot ga /start yuboring!', 'info')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Xatolik: {str(e)}', 'danger')
    
    return render_template('profile.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - Professional"""
    from modules.models import Task, Vehicle, Contract, Outsourcing
    
    # Statistics
    stats = {
        'total_tasks': Task.query.filter_by(is_active=True).count(),
        'completed_tasks': Task.query.filter_by(status='completed', is_active=True).count(),
        'overdue_tasks': Task.query.filter(
            Task.deadline < datetime.now(),
            Task.status != 'completed',
            Task.is_active == True
        ).count(),
        'total_amount': db.session.query(db.func.sum(Contract.amount)).scalar() or 0
    }
    
    # Recent tasks
    if current_user.role in ['admin', 'rahbar']:
        recent_tasks = Task.query.filter_by(is_active=True).order_by(Task.created_at.desc()).limit(5).all()
    else:
        recent_tasks = Task.query.filter_by(
            assigned_to_id=current_user.id,
            is_active=True
        ).order_by(Task.created_at.desc()).limit(5).all()
    
    # Vehicles
    vehicles = Vehicle.query.filter_by(is_active=True).limit(4).all()
    
    # Contracts
    contracts = Contract.query.filter_by(is_active=True).order_by(Contract.start_date.desc()).limit(3).all()
    
    # Outsourcing
    outsourcing = Outsourcing.query.filter_by(is_active=True).limit(3).all()
    
    # Employee stats
    employee_stats = {
        'admin': User.query.filter_by(role='admin', is_active=True).count(),
        'rahbar': User.query.filter_by(role='rahbar', is_active=True).count(),
        'xodim': User.query.filter(User.role.in_(['xodim', 'user']), User.is_active == True).count()
    }
    
    return render_template('dashboard_professional.html',
                         stats=stats,
                         recent_tasks=recent_tasks,
                         vehicles=vehicles,
                         contracts=contracts,
                         outsourcing=outsourcing,
                         employee_stats=employee_stats)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Uploaded file serve"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# =========================== CHAT API ===========================

@app.route('/api/chat/messages')
@login_required
def api_chat_messages():
    """Get chat messages"""
    from modules.models import ChatMessage
    
    module = request.args.get('module', '')
    
    # Get messages
    if current_user.role == 'admin':
        # Admin barcha xabarlarni ko'radi
        messages = ChatMessage.query.filter_by(module_name=module).order_by(ChatMessage.created_at).limit(50).all()
    else:
        # User faqat o'z xabarlarini ko'radi
        messages = ChatMessage.query.filter(
            ChatMessage.module_name == module,
            db.or_(
                ChatMessage.sender_id == current_user.id,
                ChatMessage.receiver_id == current_user.id
            )
        ).order_by(ChatMessage.created_at).limit(50).all()
    
    return jsonify({
        'messages': [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]
    })

@app.route('/api/chat/send', methods=['POST'])
@login_required
def api_chat_send():
    """Send chat message"""
    from modules.models import ChatMessage, User
    
    data = request.get_json()
    message_text = data.get('message', '').strip()
    module = data.get('module', '')
    receiver_role = data.get('receiver_role', 'admin')
    
    if not message_text:
        return jsonify({'error': 'Message required'}), 400
    
    # Find receiver (admin or rahbar)
    receiver = User.query.filter_by(role=receiver_role, is_active=True).first()
    if not receiver:
        receiver = User.query.filter_by(role='admin', is_active=True).first()
    
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404
    
    # Create message
    message = ChatMessage(
        module_name=module,
        sender_id=current_user.id,
        receiver_id=receiver.id,
        message=message_text
    )
    
    db.session.add(message)
    db.session.commit()
    
    # Send Telegram notification
    from modules.utils import send_telegram_notification
    send_telegram_notification(
        receiver,
        "Yangi chat xabari",
        f"{current_user.full_name}: {message_text}"
    )
    
    return jsonify({'success': True, 'id': message.id})

@app.route('/api/chat/unread')
@login_required
def api_chat_unread():
    """Get unread message count"""
    from modules.models import ChatMessage
    
    unread = ChatMessage.query.filter_by(
        receiver_id=current_user.id,
        is_read=False
    ).count()
    
    return jsonify({'unread': unread})

# =========================== ADMIN ROUTES ===========================

@app.route('/admin/users')
@login_required
def admin_users():
    """Admin: User management"""
    if current_user.role != 'admin':
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
def admin_user_new():
    """Admin: Yangi user yaratish"""
    if current_user.role != 'admin':
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            user = User(
                full_name=request.form.get('full_name'),
                username=request.form.get('username'),
                email=request.form.get('email'),
                phone=request.form.get('phone', ''),
                telegram_username=request.form.get('telegram_username', ''),
                role=request.form.get('role', 'user'),
                is_active=request.form.get('is_active') == 'on',
                must_change_password=request.form.get('must_change_password') == 'on'
            )
            
            password = request.form.get('password', '123456')
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'User {user.username} yaratildi!', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Xatolik: {str(e)}', 'danger')
    
    return render_template('admin/user_form.html', user=None)

@app.route('/admin/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit(id):
    """Admin: User tahrirlash"""
    if current_user.role != 'admin':
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(id)
    
    # Admin o'zini tahrirlay olmaydi
    if user.username == 'admin' and current_user.id != id:
        flash('Admin foydalanuvchisini tahrirlab bo\'lmaydi!', 'danger')
        return redirect(url_for('admin_users'))
    
    if request.method == 'POST':
        try:
            user.full_name = request.form.get('full_name')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone', '')
            user.telegram_username = request.form.get('telegram_username', '')
            user.role = request.form.get('role')
            user.is_active = request.form.get('is_active') == 'on'
            
            db.session.commit()
            flash(f'User {user.username} yangilandi!', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Xatolik: {str(e)}', 'danger')
    
    return render_template('admin/user_form.html', user=user)

@app.route('/admin/users/<int:id>/delete', methods=['POST'])
@login_required
def admin_user_delete(id):
    """Admin: User o'chirish"""
    if current_user.role != 'admin':
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(id)
    
    # Admin va demo o'chirib bo'lmaydi
    if user.username in ['admin'] or user.is_demo:
        flash('Bu foydalanuvchini o\'chirib bo\'lmaydi!', 'danger')
        return redirect(url_for('admin_users'))
    
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} o\'chirildi!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:id>/reset-password', methods=['POST'])
@login_required
def admin_user_reset_password(id):
    """Admin: Parolni tiklash"""
    if current_user.role != 'admin':
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(id)
    
    try:
        user.set_password('123456')
        user.must_change_password = True
        db.session.commit()
        flash(f'{user.username} uchun parol 123456 ga o\'zgartirildi!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('admin_users'))

# =========================== DATABASE INIT ===========================

def init_db():
    """Database initialization"""
    with app.app_context():
        db.create_all()
        
        # Admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@af-imperiya.uz',
                full_name='Administrator',
                role='admin',
                is_active=True,
                must_change_password=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Demo user
            demo = User(
                username='demo',
                email='demo@af-imperiya.uz',
                full_name='Demo User',
                role='rahbar',
                is_active=True,
                is_demo=True
            )
            demo.set_password('demo123')
            db.session.add(demo)
            
            db.session.commit()
            print("✅ Default users created!")

def create_folders():
    """Create necessary folders for uploads"""
    folders = [
        'uploads',
        'uploads/vehicles',
        'uploads/buildings',
        'uploads/employees',
        'uploads/documents',
        'instance'
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ Folders created!")

# =========================== ADMIN ROUTES ===========================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin Dashboard"""
    if current_user.role != 'admin':
        flash('Ruxsat yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    from modules.models import Task
    
    # User statistics
    users = User.query.all()
    user_stats = {
        'total': len(users),
        'admin': len([u for u in users if u.role == 'admin']),
        'rahbar': len([u for u in users if u.role == 'rahbar']),
        'xodim': len([u for u in users if u.role == 'xodim']),
        'user': len([u for u in users if u.role == 'user']),
        'active': len([u for u in users if u.is_active]),
        'inactive': len([u for u in users if not u.is_active]),
    }
    
    # Task statistics
    tasks = Task.query.all()
    task_stats = {
        'total': len(tasks),
        'pending': len([t for t in tasks if t.status == 'pending']),
        'in_progress': len([t for t in tasks if t.status == 'in_progress']),
        'completed': len([t for t in tasks if t.status == 'completed']),
        'overdue': len([t for t in tasks if t.deadline and t.deadline < datetime.now() and t.status != 'completed']),
    }
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Telegram connected
    telegram_connected = len([u for u in users if u.telegram_chat_id])
    
    return render_template('admin/dashboard.html',
                         user_stats=user_stats,
                         task_stats=task_stats,
                         recent_users=recent_users,
                         telegram_connected=telegram_connected)
def chat_messages():
    """Chat xabarlarini olish"""
    from modules.models import ChatMessage
    
    # Admin barcha xabarlarni ko'radi
    if current_user.role == 'admin':
        messages = ChatMessage.query.order_by(ChatMessage.created_at.desc()).limit(50).all()
    else:
        # Xodim faqat o'z xabarlarini ko'radi
        messages = ChatMessage.query.filter(
            db.or_(
                ChatMessage.sender_id == current_user.id,
                ChatMessage.receiver_id == current_user.id
            )
        ).order_by(ChatMessage.created_at.desc()).limit(50).all()
    
    return jsonify([{
        'id': m.id,
        'sender_name': m.sender.full_name,
        'sender_role': m.sender.role,
        'message': m.message,
        'created_at': m.created_at.strftime('%d.%m.%Y %H:%M'),
        'is_read': m.is_read,
        'is_mine': m.sender_id == current_user.id
    } for m in messages])


@app.route('/api/chat/send', methods=['POST'])
@login_required
def chat_send():
    """Chat xabari yuborish"""
    from modules.models import ChatMessage
    
    data = request.get_json()
    message_text = data.get('message', '').strip()
    receiver_id = data.get('receiver_id')
    module_name = data.get('module_name')
    
    if not message_text:
        return jsonify({'error': 'Xabar bo\'sh!'}), 400
    
    try:
        # Admin bilan chat
        if current_user.role != 'admin':
            # Xodim admin'ga yozadi
            admin = User.query.filter_by(role='admin').first()
            if not admin:
                return jsonify({'error': 'Admin topilmadi!'}), 404
            receiver_id = admin.id
        else:
            # Admin xodimga javob beradi
            if not receiver_id:
                return jsonify({'error': 'Receiver ID kerak!'}), 400
        
        message = ChatMessage(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            message=message_text,
            module_name=module_name
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({'success': True, 'message_id': message.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# =========================== ROUTES INIT ===========================

from modules.routes import init_routes
init_routes(app, db)

# =========================== MAIN ===========================

if __name__ == '__main__':
    create_folders()
    init_db()
    print("🚀 AF IMPERIYA ishga tushdi!")
    print("📊 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)