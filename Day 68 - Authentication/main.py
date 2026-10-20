from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "development-key-change-before-deployment")
DB_FILE = os.path.join(os.path.dirname(__file__), "users.db")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, user_id, email):
        self.id = str(user_id)
        self.email = email


def get_db():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


@login_manager.user_loader
def load_user(user_id):
    with get_db() as db:
        row = db.execute(
            "SELECT id, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    if row is None:
        return None

    return User(row["id"], row["email"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter your email and password.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            with get_db() as db:
                db.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, password_hash)
                )
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as db:
            row = db.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            user = User(row["id"], row["email"])
            login_user(user)
            flash("You are now logged in.", "success")
            return redirect(url_for("dashboard"))

        flash("Incorrect email or password.", "error")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
