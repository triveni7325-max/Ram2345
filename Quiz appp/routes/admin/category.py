from flask import Blueprint, render_template, request, redirect
import sqlite3

category_bp = Blueprint("category", __name__)

# ✅ Category list + quiz count + publish status
@category_bp.route("/category")
def category():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT c.id, c.name,
    COUNT(q.id) as total_quiz,
    CASE WHEN p.category_id IS NOT NULL THEN 1 ELSE 0 END as status
    FROM categories c
    LEFT JOIN quizzes q ON c.id = q.category_id
    LEFT JOIN published_categories p ON c.id = p.category_id
    GROUP BY c.id
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("admin/category.html", data=data)


# ✅ Add Category
@category_bp.route("/add_category", methods=["GET","POST"])
def add_category():

    if request.method == "POST":

        name = request.form["name"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )

        conn.commit()
        conn.close()

        return redirect("/admin/category")

    return render_template("admin/add_category.html")
    
# ✅ Edit Category
@category_bp.route("/edit_category/<int:id>", methods=["GET","POST"])
def edit_category(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]

        cur.execute(
            "UPDATE categories SET name=? WHERE id=?",
            (name, id)
        )

        conn.commit()
        conn.close()

        return redirect("/admin/category")

    # GET
    cur.execute("SELECT name FROM categories WHERE id=?", (id,))
    category = cur.fetchone()

    conn.close()

    return render_template("admin/edit_category.html", category=category, id=id)
    
    
# ✅ Delete Category
@category_bp.route("/delete_category/<int:id>")
def delete_category(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM categories WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin/category")


# ✅ Toggle Publish (ON/OFF)
@category_bp.route("/toggle/<int:id>")
def toggle(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # check already published?
    cur.execute(
        "SELECT * FROM published_categories WHERE category_id=?",
        (id,)
    )
    data = cur.fetchone()

    if data:
        # ❌ OFF → delete
        cur.execute(
            "DELETE FROM published_categories WHERE category_id=?",
            (id,)
        )
    else:
        # ✅ ON → insert
        cur.execute(
            "INSERT INTO published_categories (category_id) VALUES (?)",
            (id,)
        )

    conn.commit()
    conn.close()

    return redirect("/admin/category")