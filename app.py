from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'       # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'            # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''            # Replace with your MySQL password
app.config['MYSQL_DB'] = 'crud'              # Replace with your database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return results as dictionaries

# Initialize MySQL
mysql = MySQL(app)

# Routes

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    results = cur.fetchall()
    cur.close()
    return render_template('index.html', students=results)

@app.route('/add')
def add_student_page():
    return render_template('add.html')

@app.route('/students', methods=['POST'])
def create_student():
    data = request.form
    student_id = int(data['student_id'])
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO students (student_id, first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s, %s)',
                (student_id, first_name, last_name, dob, amount_due))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    result = cur.fetchone()
    cur.close()
    return render_template('edit.html', student=result)

@app.route('/students/<int:student_id>', methods=['POST'])
def update_student(student_id):
    data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    cur = mysql.connection.cursor()
    cur.execute('UPDATE students SET first_name = %s, last_name = %s, dob = %s, amount_due = %s WHERE student_id = %s',
                (first_name, last_name, dob, amount_due, student_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



