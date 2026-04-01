from flask import Flask, session, redirect, request
import os

app = Flask(__name__)

# 🔐 SECRET KEY
app.secret_key = "secret123"


# =========================
# 🔐 ADMIN AUTH
# =========================
from routes.admin.register import register_bp
from routes.admin.login import login_bp

# =========================
# 🛠️ ADMIN PANEL
# =========================

from routes.admin.users import users_bp

from routes.admin.category import category_bp
from routes.admin.quiz import quiz_bp
from routes.admin.question import question_bp
from routes.admin.bulk_question import bulk_bp

# =========================
# 🌍 USER SIDE
# =========================
from routes.user.auth import auth_bp
from routes.user.home import home_bp
from routes.user.quiz import user_quiz_bp
from routes.user.play import play_bp
from routes.user.score import score_bp


# =========================
# 🔗 REGISTER BLUEPRINTS
# =========================

# ADMIN

app.register_blueprint(users_bp, url_prefix="/admin")
app.register_blueprint(register_bp, url_prefix="/admin")
app.register_blueprint(login_bp, url_prefix="/admin")

app.register_blueprint(category_bp, url_prefix="/admin")
app.register_blueprint(quiz_bp, url_prefix="/admin")
app.register_blueprint(question_bp, url_prefix="/admin")
app.register_blueprint(bulk_bp, url_prefix="/admin")

# USER
app.register_blueprint(auth_bp)              # /login /register
app.register_blueprint(home_bp)              # /
app.register_blueprint(user_quiz_bp, url_prefix="/user")
app.register_blueprint(play_bp, url_prefix="/user")
app.register_blueprint(score_bp, url_prefix="/user")


# =========================
# 🔒 LOGIN PROTECTION
# =========================
@app.before_request
def protect():

    open_routes = ["/login", "/register", "/admin/login", "/admin/register", "/static"]

    if "user_id" not in session:

        # अगर admin route है तो छोड़ दो
        if request.path.startswith("/admin"):
            return None

        if not any(request.path.startswith(route) for route in open_routes):
            return redirect("/login")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)