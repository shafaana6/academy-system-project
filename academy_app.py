from flask import Flask, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

# ---------- LOAD ENVIRONMENT VARIABLES ----------
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# ---------- COMMON STYLES ----------
style = """
<style>
    body { background-color:#F5F0E1; font-family:Arial; color:#000000; }
    .box { background-color:#D2B48C; padding:20px; border-radius:10px; }
    .table { border-collapse:collapse; width:80%; margin:auto; text-align:center; background-color:#D2B48C; color:#000000; }
    .table th { background-color:#A0522D; color:#000000; }
    button { padding:5px 10px; background-color:#D2B48C; color:#000000; border:1px solid #000000; border-radius:5px; cursor:pointer; }
    button:hover { background-color:#C19A6B; }
    a { color:#000000; text-decoration:none; }
    a:hover { color:#8B4513; }
    .delete:hover { color:#8B0000; }
</style>
"""

# ---------- HOME PAGE ----------
@app.route("/")
def home():
    return f"""
    {style}
    <h1 style='text-align:center;'>Academy System</h1>
    <div style='display:flex;gap:50px; justify-content:center; margin-top:20px;'>

        <div class="box">
            <h3>Add Learner</h3>
            <form method="POST" action="/add_learner">
                <input name="full_name" placeholder="Full Name" required><br><br>
                <input name="email" placeholder="Email" required><br><br>
                <input name="course" placeholder="Course" required><br><br>
                <input name="year" type="number" placeholder="Year" required><br><br>
                <button>Add Learner</button>
            </form>
        </div>

        <div class="box">
            <h3>Add Grade</h3>
            <form method="POST" action="/add_grade">
                <input name="learner_id" type="number" placeholder="Learner ID" required><br><br>
                <input name="subject" placeholder="Subject Name" required><br><br>
                <input name="score" type="number" placeholder="Score" required><br><br>
                <button>Add Grade</button>
            </form>
        </div>

    </div>

    <br><hr style='border-color:#000000;'><br>

    <div style='text-align:center;'>
        <a href="/view_learners" style='margin-right:20px;'>View Learners</a>
        <a href="/view_grades">View Grades</a>
    </div>
    """

# ---------- ADD LEARNER ----------
@app.route("/add_learner", methods=["POST"])
def add_learner():
    cursor.execute(
        "INSERT INTO learners (full_name, email_address, course_name, year_of_study) VALUES (%s,%s,%s,%s)",
        (
            request.form["full_name"],
            request.form["email"],
            request.form["course"],
            request.form["year"]
        )
    )
    conn.commit()
    return "<h3>Learner added successfully!</h3><a href='/'>Go Back</a>"

# ---------- VIEW LEARNERS ----------
@app.route("/view_learners")
def view_learners():
    cursor.execute("SELECT * FROM learners")
    learners = cursor.fetchall()

    html = f"""
    {style}
    <h2 style='text-align:center;'>Learners List</h2>
    <table class="table" border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Course</th>
            <th>Year</th>
            <th>Actions</th>
        </tr>
    """

    for l in learners:
        html += f"""
        <tr>
            <td>{l[0]}</td>
            <td>{l[1]}</td>
            <td>{l[2]}</td>
            <td>{l[3]}</td>
            <td>{l[4]}</td>
            <td>
                <a href="/edit/{l[0]}">Edit</a> |
                <a href="/delete/{l[0]}" class="delete" onclick="return confirm('Delete this learner?')">Delete</a>
            </td>
        </tr>
        """

    html += "</table><br><div style='text-align:center;'><a href='/'>Go Back</a></div>"
    return html

# ---------- DELETE LEARNER ----------
@app.route("/delete/<int:learner_id>")
def delete_learner(learner_id):
    cursor.execute("DELETE FROM learners WHERE learner_id=%s", (learner_id,))
    conn.commit()
    return "<h3>Learner deleted!</h3><a href='/view_learners'>Go Back</a>"

# ---------- EDIT / UPDATE LEARNER ----------
@app.route("/edit/<int:learner_id>", methods=["GET", "POST"])
def edit_learner(learner_id):
    if request.method == "POST":
        cursor.execute(
            "UPDATE learners SET full_name=%s, course_name=%s, year_of_study=%s WHERE learner_id=%s",
            (
                request.form["full_name"],
                request.form["course"],
                request.form["year"],
                learner_id
            )
        )
        conn.commit()
        return redirect("/view_learners")
    else:
        cursor.execute("SELECT * FROM learners WHERE learner_id=%s", (learner_id,))
        learner = cursor.fetchone()
        return f"""
        {style}
        <h2 style='text-align:center;'>Edit Learner</h2>
        <form method="POST" style='text-align:center;'>
            <input name="full_name" value="{learner[1]}" required><br><br>
            <input name="course" value="{learner[3]}" required><br><br>
            <input name="year" type="number" value="{learner[4]}" required><br><br>
            <button>Update</button>
        </form>
        <br><div style='text-align:center;'><a href='/view_learners'>Cancel</a></div>
        """

# ---------- ADD GRADE ----------
@app.route("/add_grade", methods=["POST"])
def add_grade():
    cursor.execute(
        "INSERT INTO grades (learner_id, subject_name, score) VALUES (%s,%s,%s)",
        (
            request.form["learner_id"],
            request.form["subject"],
            request.form["score"]
        )
    )
    conn.commit()
    return "<h3>Grade added successfully!</h3><a href='/'>Go Back</a>"

# ---------- VIEW GRADES ----------
@app.route("/view_grades")
def view_grades():
    cursor.execute("""
        SELECT g.grade_id, l.full_name, g.subject_name, g.score
        FROM grades g
        JOIN learners l ON g.learner_id = l.learner_id
    """)
    grades = cursor.fetchall()

    html = f"""
    {style}
    <h2 style='text-align:center;'>Grades List</h2>
    <table class="table" border="1" cellpadding="8">
        <tr>
            <th>Grade ID</th>
            <th>Learner Name</th>
            <th>Subject</th>
            <th>Score</th>
        </tr>
    """

    for g in grades:
        html += f"""
        <tr>
            <td>{g[0]}</td>
            <td>{g[1]}</td>
            <td>{g[2]}</td>
            <td>{g[3]}</td>
        </tr>
        """

    html += "</table><br><div style='text-align:center;'><a href='/'>Go Back</a></div>"
    return html

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
