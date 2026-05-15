from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Travis05$",
        database="student_records_db"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students")
def students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("students.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        major = request.form["major"]
        gpa = request.form["gpa"]

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO students (first_name, last_name, email, major, gpa)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, email, major, gpa)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/students")

    return render_template("add_student.html")

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        major = request.form["major"]
        gpa = request.form["gpa"]

        sql = """
        UPDATE students
        SET first_name=%s, last_name=%s, email=%s, major=%s, gpa=%s
        WHERE student_id=%s
        """
        values = (first_name, last_name, email, major, gpa, student_id)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/students")

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/students")

@app.route("/search", methods=["GET", "POST"])
def search():
    students = []

    if request.method == "POST":
        keyword = request.form["keyword"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT * FROM students
        WHERE first_name LIKE %s
        OR last_name LIKE %s
        OR major LIKE %s
        """
        search_value = f"%{keyword}%"

        cursor.execute(sql, (search_value, search_value, search_value))
        students = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template("search.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)