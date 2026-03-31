from flask import Blueprint, render_template, request, redirect
import sqlite3

quiz_bp = Blueprint("quiz", __name__)

# ✅ Quiz list
@quiz_bp.route("/quiz/<int:category_id>")
def quiz(category_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT q.id, q.quiz_name,
    COUNT(ques.id) as total_questions,
    CASE WHEN p.quiz_id IS NOT NULL THEN 1 ELSE 0 END as status
    FROM quizzes q
    LEFT JOIN questions ques ON q.id = ques.quiz_id
    LEFT JOIN published_quizzes p ON q.id = p.quiz_id
    WHERE q.category_id=?
    GROUP BY q.id
    """, (category_id,))

    quizzes = cur.fetchall()
    conn.close()

    return render_template(
        "admin/quiz.html",
        quizzes=quizzes,
        category_id=category_id
    )


# ✅ Add quiz (WITH TIMER)
@quiz_bp.route("/add_quiz/<int:category_id>", methods=["GET","POST"])
def add_quiz(category_id):

    if request.method == "POST":

        quiz_name = request.form["quiz_name"]
        time = request.form["time"]   # ✅ NEW

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO quizzes (category_id, quiz_name, time) VALUES (?,?,?)",
            (category_id, quiz_name, time)
        )

        conn.commit()
        conn.close()

        return redirect(f"/admin/quiz/{category_id}")

    return render_template("admin/add_quiz.html", category_id=category_id)
    
    
# ✅ Edit Quiz
@quiz_bp.route("/edit_quiz/<int:id>", methods=["GET","POST"])
def edit_quiz(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["quiz_name"]
        time = request.form["time"]

        cur.execute(
            "UPDATE quizzes SET quiz_name=?, time=? WHERE id=?",
            (name, time, id)
        )

        conn.commit()
        conn.close()

        return redirect("/admin/category")

    # GET
    cur.execute("SELECT quiz_name, time FROM quizzes WHERE id=?", (id,))
    quiz = cur.fetchone()

    conn.close()

    return render_template("admin/edit_quiz.html", quiz=quiz, id=id)
    
    
    
# ✅ Delete Quiz
@quiz_bp.route("/delete_quiz/<int:id>")
def delete_quiz(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM quizzes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


# ✅ Toggle quiz publish
@quiz_bp.route("/toggle_quiz/<int:id>")
def toggle_quiz(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM published_quizzes WHERE quiz_id=?", (id,))
    data = cur.fetchone()

    if data:
        cur.execute("DELETE FROM published_quizzes WHERE quiz_id=?", (id,))
    else:
        cur.execute("INSERT INTO published_quizzes (quiz_id) VALUES (?)", (id,))

    conn.commit()
    conn.close()

    return redirect(request.referrer)