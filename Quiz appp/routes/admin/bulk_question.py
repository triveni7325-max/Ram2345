from flask import Blueprint, render_template, request, redirect
import sqlite3

bulk_bp = Blueprint("bulk", __name__)

@bulk_bp.route("/bulk_add/<int:quiz_id>", methods=["GET","POST"])
def bulk_add(quiz_id):

    if request.method == "POST":

        data = request.form.get("data")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        lines = data.strip().split("\n")

        for line in lines:
            parts = line.split("|")

            if len(parts) == 7:
                q, o1, o2, o3, o4, correct, marks = parts

                cur.execute("""
                INSERT INTO questions
                (quiz_id, question, option1, option2, option3, option4, correct, marks)
                VALUES (?,?,?,?,?,?,?,?)
                """, (quiz_id, q, o1, o2, o3, o4, correct, marks))

        conn.commit()
        conn.close()

        return redirect(f"/admin/quiz/{quiz_id}")

    return render_template("admin/bulk_add.html", quiz_id=quiz_id)