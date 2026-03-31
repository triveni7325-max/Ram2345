from flask import Blueprint, render_template
import sqlite3

users_bp = Blueprint("users", __name__)

@users_bp.route("/users")
def users_list():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # users table से data लाओ
    cur.execute("SELECT id, name, email, mobile FROM users ORDER BY id DESC")
    users = cur.fetchall()

    conn.close()

    return render_template("admin/users.html", users=users)