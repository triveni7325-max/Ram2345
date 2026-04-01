from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return redirect(url_for("category.category"))
        else:
            return "Invalid Login"

    return render_template("admin/login.html")