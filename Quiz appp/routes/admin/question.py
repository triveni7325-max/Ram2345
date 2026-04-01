from flask import Blueprint, render_template, request, redirect
import sqlite3

question_bp = Blueprint("question", __name__)

# ✅ Add Question
@question_bp.route("/add_question/<int:quiz_id>", methods=["GET","POST"])
def add_question(quiz_id):

    if request.method == "POST":

        q = request.form["question"]
        o1 = request.form["option1"]
        o2 = request.form["option2"]
        o3 = request.form["option3"]
        o4 = request.form["option4"]
        correct = request.form["correct"]   # A/B/C/D
        marks = request.form["marks"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO questions
        (quiz_id, question, option1, option2, option3, option4, correct, marks)
        VALUES (?,?,?,?,?,?,?,?)
        """, (quiz_id, q, o1, o2, o3, o4, correct, marks))

        conn.commit()
        conn.close()

        return redirect(f"/admin/add_question/{quiz_id}")

    return render_template("admin/add_question.html")


# ✅ View Questions
@question_bp.route("/view_questions/<int:quiz_id>")
def view_questions(quiz_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT question, option1, option2, option3, option4, correct, marks
    FROM questions WHERE quiz_id=?
    """, (quiz_id,))

    questions = cur.fetchall()
    conn.close()

    return render_template("admin/view_questions.html", questions=questions)