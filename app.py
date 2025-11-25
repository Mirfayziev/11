from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"


# ============================
#   MODELLAR
# ============================

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    telegram_username = db.Column(db.String(120))   # 🔥 YANGI QO‘SHILDI
    password_hash = db.Column(db.String(300))
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, p):
        self.password_hash = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self.password_hash, p)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="New")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


with app.app_context():
    db.create_all()


# ============================
#       AUTH (Login / Register)
# ============================

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Login yoki parol noto‘g‘ri!", "danger")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        telegram_username = request.form.get("telegram_username", "").strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm_password"].strip()

        if password != confirm:
            flash("Parollar mos emas!", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Bu username band!", "danger")
            return render_template("register.html")

        u = User(
            username=username,
            full_name=full_name,
            email=email,
            telegram_username=telegram_username,
            role="user"
        )
        u.set_password(password)

        db.session.add(u)
        db.session.commit()

        flash("Muvaffaqiyatli ro'yxatdan o'tdingiz. Endi login qiling!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ============================
#       DASHBOARD
# ============================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# ============================
#       ADMIN — USERS
# ============================

@app.route("/admin/users")
@login_required
def admin_users():
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))

    users = User.query.all()
    return render_template("admin/users.html", users=users)


# ============================
#       TASKS
# ============================

@app.route("/tasks")
@login_required
def tasks_list():
    tasks = Task.query.all()
    return render_template("tasks/list.html", tasks=tasks)


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def tasks_new():
    if request.method == "POST":
        t = Task(
            title=request.form["title"],
            description=request.form["description"],
            assigned_to=current_user.id,
        )
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("tasks_list"))

    return render_template("tasks/form.html")


if __name__ == "__main__":
    app.run(debug=True)
