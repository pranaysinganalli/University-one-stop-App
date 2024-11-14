from flask import Flask, request, render_template, redirect, url_for, flash
import cx_Oracle
from datetime import datetime


app = Flask(__name__)
#set secret_key
app.secret_key = 'your_secret_key_here'

def connect():
    connection = cx_Oracle.connect("system", "852456", "127.0.0.1:1521/xe")
    return connection


# ---------- CRUD & Display for Student ----------

# List Students
@app.route('/students', methods=['GET'])
def list_students():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('students.html', students=students)

# Create Student
@app.route('/students/new', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        email = request.form.get('email')

        connection = connect()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Student (student_id, first_name, last_name, date_of_birth, email)
                VALUES (:student_id, :first_name, :last_name, TO_DATE(:date_of_birth, 'YYYY-MM-DD'), :email)
            """, [student_id, first_name, last_name, date_of_birth, email])
            connection.commit()
            flash("Student created successfully!", "success")
        except cx_Oracle.DatabaseError as e:
            flash(f"Error creating student: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('list_students'))

    return render_template('create_student.html')

# Update Student
@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        email = request.form.get('email')

        connection = connect()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE Student
                SET first_name = :first_name, last_name = :last_name, 
                    date_of_birth = TO_DATE(:date_of_birth, 'YYYY-MM-DD'), email = :email
                WHERE student_id = :student_id
            """, [first_name, last_name, date_of_birth, email, student_id])
            connection.commit()
            flash("Student updated successfully!", "success")
        except cx_Oracle.DatabaseError as e:
            flash(f"Error updating student: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('list_students'))

    # Fetch student details to populate form for GET request
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student WHERE student_id = :student_id", [student_id])
    student = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_student.html', student=student)

# Delete Student
@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Student WHERE student_id = :student_id", [student_id])
        connection.commit()
        flash("Student deleted successfully!", "success")
    except cx_Oracle.DatabaseError as e:
        flash(f"Error deleting student: {e}", "danger")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('list_students'))

# ---------- CRUD Operations for Professor ----------
@app.route('/professors', methods=['GET'])
def list_professors():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Professor")
    professors = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('professors.html', professors=professors)

@app.route('/professors/new', methods=['GET', 'POST'])
def create_professor():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        salary = request.form['salary']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Professor (professor_id, first_name, last_name, department_id, salary)
            VALUES (:professor_id, :first_name, :last_name, :department_id, :salary)
        """, [professor_id, first_name, last_name, department_id, salary])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Professor created successfully!", "success")
        return redirect(url_for('list_professors'))
    return render_template('create_professor.html')

@app.route('/professors/<int:professor_id>/edit', methods=['GET', 'POST'])
def update_professor(professor_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        salary = request.form['salary']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Professor SET first_name=:first_name, last_name=:last_name,
            department_id=:department_id, salary=:salary WHERE professor_id=:professor_id
        """, [first_name, last_name, department_id, salary, professor_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Professor updated successfully!", "success")
        return redirect(url_for('list_professors'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Professor WHERE professor_id=:professor_id", [professor_id])
    professor = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_professor.html', professor=professor)

@app.route('/professors/<int:professor_id>/delete', methods=['POST'])
def delete_professor(professor_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Professor WHERE professor_id=:professor_id", [professor_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Professor deleted successfully!", "success")
    return redirect(url_for('list_professors'))
# ---------- CRUD Operations for Course ----------
@app.route('/courses', methods=['GET'])
def list_courses():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('courses.html', courses=courses)

@app.route('/courses/new', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        credits = request.form['credits']
        department_id = request.form['department_id']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Course (course_id, title, credits, department_id)
            VALUES (:course_id, :title, :credits, :department_id)
        """, [course_id, title, credits, department_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Course created successfully!", "success")
        return redirect(url_for('list_courses'))
    return render_template('create_course.html')

@app.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
def update_course(course_id):
    if request.method == 'POST':
        title = request.form['title']
        credits = request.form['credits']
        department_id = request.form['department_id']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Course SET title=:title, credits=:credits, department_id=:department_id
            WHERE course_id=:course_id
        """, [title, credits, department_id, course_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Course updated successfully!", "success")
        return redirect(url_for('list_courses'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Course WHERE course_id=:course_id", [course_id])
    course = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_course.html', course=course)

@app.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Course WHERE course_id=:course_id", [course_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Course deleted successfully!", "success")
    return redirect(url_for('list_courses'))
# ---------- CRUD Operations for Department ----------
@app.route('/departments', methods=['GET'])
def list_departments():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('departments.html', departments=departments)

@app.route('/departments/new', methods=['GET', 'POST'])
def create_department():
    if request.method == 'POST':
        department_id = request.form['department_id']
        name = request.form['name']
        strength = request.form['strength']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Department (department_id, name, strength)
            VALUES (:department_id, :name, :strength)
        """, [department_id, name, strength])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Department created successfully!", "success")
        return redirect(url_for('list_departments'))
    return render_template('create_department.html')

@app.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def update_department(department_id):
    if request.method == 'POST':
        name = request.form['name']
        strength = request.form['strength']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Department SET name=:name, strength=:strength
            WHERE department_id=:department_id
        """, [name, strength, department_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Department updated successfully!", "success")
        return redirect(url_for('list_departments'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Department WHERE department_id=:department_id", [department_id])
    department = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_department.html', department=department)

@app.route('/departments/<int:department_id>/delete', methods=['POST'])
def delete_department(department_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Department WHERE department_id=:department_id", [department_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Department deleted successfully!", "success")
    return redirect(url_for('list_departments'))
# ---------- CRUD Operations for Assignment ----------
@app.route('/assignments', methods=['GET'])
def list_assignments():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Assignment")
    assignments = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('assignments.html', assignments=assignments)

@app.route('/assignments/new', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        assignment_id = request.form['assignment_id']
        title = request.form['title']
        due_date = request.form['due_date']
        total_marks = request.form['total_marks']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Assignment (assignment_id, title, due_date, total_marks)
            VALUES (:assignment_id, :title, TO_DATE(:due_date, 'YYYY-MM-DD'), :total_marks)
        """, [assignment_id, title, due_date, total_marks])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Assignment created successfully!", "success")
        return redirect(url_for('list_assignments'))
    return render_template('create_assignment.html')

@app.route('/assignments/<int:assignment_id>/edit', methods=['GET', 'POST'])
def update_assignment(assignment_id):
    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']
        total_marks = request.form['total_marks']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Assignment SET title=:title, due_date=TO_DATE(:due_date, 'YYYY-MM-DD'), 
            total_marks=:total_marks WHERE assignment_id=:assignment_id
        """, [title, due_date, total_marks, assignment_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Assignment updated successfully!", "success")
        return redirect(url_for('list_assignments'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Assignment WHERE assignment_id=:assignment_id", [assignment_id])
    assignment = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_assignment.html', assignment=assignment)

@app.route('/assignments/<int:assignment_id>/delete', methods=['POST'])
def delete_assignment(assignment_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Assignment WHERE assignment_id=:assignment_id", [assignment_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Assignment deleted successfully!", "success")
    return redirect(url_for('list_assignments'))

# ---------- CRUD Operations for Classroom ----------
@app.route('/classrooms', methods=['GET'])
def list_classrooms():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classroom")
    classrooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('classrooms.html', classrooms=classrooms)

@app.route('/classrooms/new', methods=['GET', 'POST'])
def create_classroom():
    if request.method == 'POST':
        room_number = request.form['room_number']
        building_name = request.form['building_name']
        capacity = request.form['capacity']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Classroom (room_number, building_name, capacity)
            VALUES (:room_number, :building_name, :capacity)
        """, [room_number, building_name, capacity])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Classroom created successfully!", "success")
        return redirect(url_for('list_classrooms'))
    return render_template('create_classroom.html')

@app.route('/classrooms/<room_number>/edit', methods=['GET', 'POST'])
def update_classroom(room_number):
    if request.method == 'POST':
        building_name = request.form['building_name']
        capacity = request.form['capacity']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Classroom SET building_name=:building_name, capacity=:capacity
            WHERE room_number=:room_number
        """, [building_name, capacity, room_number])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Classroom updated successfully!", "success")
        return redirect(url_for('list_classrooms'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classroom WHERE room_number=:room_number", [room_number])
    classroom = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_classroom.html', classroom=classroom)

@app.route('/classrooms/<room_number>/delete', methods=['POST'])
def delete_classroom(room_number):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Classroom WHERE room_number=:room_number", [room_number])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Classroom deleted successfully!", "success")
    return redirect(url_for('list_classrooms'))

# ---------- CRUD Operations for Teaches (Professor teaches Course) ----------
@app.route('/teaches', methods=['GET'])
def list_teaches():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Teaches")
    teaches = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('teaches.html', teaches=teaches)

@app.route('/teaches/new', methods=['GET', 'POST'])
def create_teaches():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        course_id = request.form['course_id']
        semester = request.form['semester']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Teaches (professor_id, course_id, semester)
            VALUES (:professor_id, :course_id, :semester)
        """, [professor_id, course_id, semester])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Teaches relationship created successfully!", "success")
        return redirect(url_for('list_teaches'))
    return render_template('create_teaches.html')

@app.route('/teaches/<int:professor_id>/<int:course_id>/edit', methods=['GET', 'POST'])
def update_teaches(professor_id, course_id):
    if request.method == 'POST':
        semester = request.form['semester']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Teaches SET semester=:semester
            WHERE professor_id=:professor_id AND course_id=:course_id
        """, [semester, professor_id, course_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Teaches relationship updated successfully!", "success")
        return redirect(url_for('list_teaches'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Teaches WHERE professor_id=:professor_id AND course_id=:course_id", [professor_id, course_id])
    teaches = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_teaches.html', teaches=teaches)

@app.route('/teaches/<int:professor_id>/<int:course_id>/delete', methods=['POST'])
def delete_teaches(professor_id, course_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Teaches WHERE professor_id=:professor_id AND course_id=:course_id", [professor_id, course_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Teaches relationship deleted successfully!", "success")
    return redirect(url_for('list_teaches'))
# ---------- CRUD Operations for Submits (Student submits Assignment) ----------
@app.route('/submits', methods=['GET'])
def list_submits():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Submits")
    submits = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('submits.html', submits=submits)

@app.route('/submits/new', methods=['GET', 'POST'])
def create_submits():
    if request.method == 'POST':
        student_id = request.form['student_id']
        assignment_id = request.form['assignment_id']
        submission_date = request.form['submission_date']
        marks_obtained = request.form['marks_obtained']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Submits (student_id, assignment_id, submission_date, marks_obtained)
            VALUES (:student_id, :assignment_id, TO_DATE(:submission_date, 'YYYY-MM-DD'), :marks_obtained)
        """, [student_id, assignment_id, submission_date, marks_obtained])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Submission created successfully!", "success")
        return redirect(url_for('list_submits'))
    return render_template('create_submits.html')

@app.route('/submits/<int:student_id>/<int:assignment_id>/edit', methods=['GET', 'POST'])
def update_submits(student_id, assignment_id):
    if request.method == 'POST':
        submission_date = request.form['submission_date']
        marks_obtained = request.form['marks_obtained']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Submits SET submission_date=TO_DATE(:submission_date, 'YYYY-MM-DD'), 
            marks_obtained=:marks_obtained WHERE student_id=:student_id AND assignment_id=:assignment_id
        """, [submission_date, marks_obtained, student_id, assignment_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Submission updated successfully!", "success")
        return redirect(url_for('list_submits'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Submits WHERE student_id=:student_id AND assignment_id=:assignment_id", [student_id, assignment_id])
    submit = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_submits.html', submit=submit)

@app.route('/submits/<int:student_id>/<int:assignment_id>/delete', methods=['POST'])
def delete_submits(student_id, assignment_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Submits WHERE student_id=:student_id AND assignment_id=:assignment_id", [student_id, assignment_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Submission deleted successfully!", "success")
    return redirect(url_for('list_submits'))

# ---------- CRUD Operations for Manages (Professor manages Department) ----------
@app.route('/manages', methods=['GET'])
def list_manages():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Manages")
    manages = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('manages.html', manages=manages)

@app.route('/manages/new', methods=['GET', 'POST'])
def create_manages():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        department_id = request.form['department_id']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Manages (professor_id, department_id)
            VALUES (:professor_id, :department_id)
        """, [professor_id, department_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Manages relationship created successfully!", "success")
        return redirect(url_for('list_manages'))
    return render_template('create_manages.html')

@app.route('/manages/<int:professor_id>/<int:department_id>/edit', methods=['GET', 'POST'])
def update_manages(professor_id, department_id):
    if request.method == 'POST':
        new_professor_id = request.form['professor_id']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Manages SET professor_id=:new_professor_id
            WHERE professor_id=:professor_id AND department_id=:department_id
        """, [new_professor_id, professor_id, department_id])
        connection.commit()
        cursor.close()
        connection.close()
        flash("Manages relationship updated successfully!", "success")
        return redirect(url_for('list_manages'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Manages WHERE professor_id=:professor_id AND department_id=:department_id", [professor_id, department_id])
    manages = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_manages.html', manages=manages)

@app.route('/manages/<int:professor_id>/<int:department_id>/delete', methods=['POST'])
def delete_manages(professor_id, department_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Manages WHERE professor_id=:professor_id AND department_id=:department_id", [professor_id, department_id])
    connection.commit()
    cursor.close()
    connection.close()
    flash("Manages relationship deleted successfully!", "success")
    return redirect(url_for('list_manages'))

# ---------- CRUD Operations for Scheduled_In (Course scheduled in Classroom) ----------
@app.route('/scheduled_in', methods=['GET'])
def list_scheduled_in():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Scheduled_In")
    scheduled_in = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('scheduled_in.html', scheduled_in=scheduled_in)

@app.route('/scheduled_in/new', methods=['GET', 'POST'])
def create_scheduled_in():
    if request.method == 'POST':
        course_id = request.form['course_id']
        room_number = request.form['room_number']
        schedule_time = request.form['schedule_time']
        days_of_week = request.form['days_of_week']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Scheduled_In (course_id, room_number, schedule_time, days_of_week)
            VALUES (:course_id, :room_number, :schedule_time, :days_of_week)
        """, {
            'course_id': course_id,
            'room_number': room_number,
            'schedule_time': schedule_time,
            'days_of_week': days_of_week
        })
        connection.commit()
        cursor.close()
        connection.close()
        flash("Scheduled In record created successfully!", "success")
        return redirect(url_for('list_scheduled_in'))
    return render_template('create_scheduled_in.html')

@app.route('/scheduled_in/<int:course_id>/<room_number>/edit', methods=['GET', 'POST'])
def update_scheduled_in(course_id, room_number):
    if request.method == 'POST':
        schedule_time = request.form['schedule_time']
        days_of_week = request.form['days_of_week']
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Scheduled_In SET schedule_time=:schedule_time, days_of_week=:days_of_week
            WHERE course_id=:course_id AND room_number=:room_number
        """, {
            'schedule_time': schedule_time,
            'days_of_week': days_of_week,
            'course_id': course_id,
            'room_number': room_number
        })
        connection.commit()
        cursor.close()
        connection.close()
        flash("Scheduled In record updated successfully!", "success")
        return redirect(url_for('list_scheduled_in'))

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Scheduled_In WHERE course_id=:course_id AND room_number=:room_number", {
        'course_id': course_id,
        'room_number': room_number
    })
    scheduled = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_scheduled_in.html', scheduled=scheduled)

@app.route('/scheduled_in/<int:course_id>/<room_number>/delete', methods=['POST'])
def delete_scheduled_in(course_id, room_number):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Scheduled_In WHERE course_id=:course_id AND room_number=:room_number", {
        'course_id': course_id,
        'room_number': room_number
    })
    connection.commit()
    cursor.close()
    connection.close()
    flash("Scheduled In record deleted successfully!", "success")
    return redirect(url_for('list_scheduled_in'))

#--------------------------------------------------------------------------------------------


# Main entry point
if __name__ == '__main__':
    app.run(debug=True)