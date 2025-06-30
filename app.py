from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'patients.db'


def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL,
                height REAL,
                age INTEGER,
                medications TEXT
            )
        ''')
        conn.commit()
        conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name, weight, height, age, medications FROM patients')
    patients = c.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)


@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        height = request.form['height']
        age = request.form['age']
        medications = request.form['medications']
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            'INSERT INTO patients (name, weight, height, age, medications) '
            'VALUES (?, ?, ?, ?, ?)',
            (name, weight, height, age, medications))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_patient.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=False)
