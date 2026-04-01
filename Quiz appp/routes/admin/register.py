from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (username,email,password)
        )

        conn.commit()
        conn.close()

        flash("Register Success!")

        return redirect(url_for("login.login"))

    return render_template("admin/register.html")