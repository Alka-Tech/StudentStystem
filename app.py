# from crypt import methods
import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import json
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'surprise'

def get_db_connection():
    conn = sqlite3.connect('StudentSystem.db')
    conn.row_factory = sqlite3.Row
    return conn

# function returns student ID
def get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE ID = ?',
                        (id,)).fetchone()
    conn.close()
    if student is None:
        abort(404)
    return student  

# function returns student first name
def get_student_name(FirstName):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE FirstName = ?',
                        (FirstName,)).fetchone()
    conn.close()
    # if student is None:
    #     abort(404)
    return student

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     students = conn.execute('SELECT * FROM students ORDER BY ID').fetchall()
#     conn.close()
#     return render_template('index1.html', students=students)

# Login and show data 
@app.route("/",methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Get form fields
        FirstName = request.form["FirstName"]
        password = request.form["Password"]

        # student = get_student_name(FirstName)
        # if student is None:
        if FirstName not in('Admin','SuperAdmin'):
            flash('User is not valid user!')
            return render_template("login.html")
        if password == "pass123":
            return redirect(url_for('showall'))
        else:
            flash('Password mismatch!')
            return render_template("login.html")

    return render_template("login.html")


#  verify whether table exists and then process
@app.route("/showall")
def showall():
    conn = get_db_connection()
    c = conn.cursor()
                
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='students' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : 
        TableExists = True  #print('Table exists.')
    else:
        TableExists = False
                
    if TableExists == False:
        with open('schema.sql') as f:
            conn.executescript(f.read())

        cur = conn.cursor()    

        with open("json/customer_info.json") as f:
            data = json.load(f)
        
        columns = ['ID','LastName','FirstName','City','State','Gender','StudentStatus','Major','Country','Age','SAT','Grade ','Height']
        for row in data['Full']:
            keys= tuple(row[c] for c in columns)
            cur.execute('insert into students values(?,?,?,?,?,?,?,?,?,?,?,?,?)',keys)
            print(f'{row["FirstName"]} data inserted Succefully')
        
        # Closing file
        f.close()

        conn.commit()
        
    students = conn.execute('SELECT * FROM students ORDER BY ID').fetchall() 
    conn.close()   
    return render_template('showall.html', students=students)

# Add new student
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        ID = request.form['ID']
        LastName = request.form['LastName']
        FirstName = request.form['FirstName']
        City = request.form['City']
        State = request.form['State']
        Gender = request.form['Gender']
        StudentStatus = request.form['StudentStatus']
        Major = request.form['Major']
        Country = request.form['Country']
        Age = request.form['Age']
        SAT = request.form['SAT']
        Grade = request.form['Grade']
        Height = request.form['Height']
        
        if not ID:
            flash('ID is required!')
        elif not LastName:
            flash('LastName is required!')
        elif not FirstName:
            flash('FirstName is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO students (ID,LastName,FirstName,City,State,Gender,StudentStatus,Major,Country,Age,SAT,Grade,Height) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         (ID,LastName,FirstName,City,State,Gender,StudentStatus,Major,Country,Age,SAT,Grade,Height))
            conn.commit()
            conn.close()
            return redirect(url_for('showall'))

    return render_template('create.html')

# Edit Student
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    student = get_student(id)

    if request.method == 'POST':
        ID = request.form['ID']
        LastName = request.form['LastName']
        FirstName = request.form['FirstName']
        City = request.form['City']
        State = request.form['State']
        Gender = request.form['Gender']
        StudentStatus = request.form['StudentStatus']
        Major = request.form['Major']
        Country = request.form['Country']
        Age = request.form['Age']
        SAT = request.form['SAT']
        Grade = request.form['Grade']
        Height = request.form['Height']

        if not ID:
            flash('ID is required!')
        elif not LastName:
            flash('LastName is required!')
        elif not FirstName:
            flash('FirstName is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE students SET LastName = ?, FirstName = ?, City = ?, State = ?, Gender = ?, StudentStatus = ?, Major = ?, Country = ?, Age = ?, SAT = ?, Grade = ?, Height = ?'
                         ' WHERE ID = ?',
                         (LastName, FirstName, City, State, Gender, StudentStatus, Major, Country, Age, SAT, Grade, Height, id))
            conn.commit()
            conn.close()
            return redirect(url_for('showall'))

    return render_template('edit.html', student=student)

# Delete student
@app.route("/<int:id>/delete/")
def delete(id):
    student =  get_student(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    flash('student - "{}" was successfully deleted!'.format(student['FirstName']))
    return redirect(url_for('showall'))

@app.route('/logout/')
def logout():
    flash("Logout successfully.", "success")
    return redirect(url_for('login'))

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Get form fields
        FirstName = request.form["FirstName"]
        password = request.form["Password"]

        # student = get_student_name(FirstName)
        # if student is None:
        if FirstName not in('Admin','SuperAdmin'):
            flash('User is not a valid user!')
            return render_template("login.html")
        if password == "pass123":
            # flash('student - "{}" is a valid user!'.format(student['FirstName']))
            # return redirect(url_for('index'))
            return redirect(url_for('showall'))
        else:
            flash('Password mismatch!')
            return render_template("login.html")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)