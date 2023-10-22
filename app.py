from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key' # TODO

def create_database():
    conn = sqlite3.connect('database/exam.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            q1 TEXT,
            q2 TEXT,
            q3 TEXT,
            q4 TEXT,
            q5 TEXT,
            q6 TEXT,
            q7 TEXT,
            q8 TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        conn = sqlite3.connect('database/exam.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, surname) VALUES (?, ?)', (name, surname))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        session['user_id'] = user_id
        return redirect(url_for('questions'))

    return render_template('register.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        answers = {
            'q1': request.form['q1'],
            'q2': request.form['q2'],
            'q3': request.form['q3'],
            'q4': request.form['q4'],
            'q5': request.form['q5'],
            'q6': request.form['q6'],
            'q7': request.form['q7'],
            'q8': request.form['q8'],
        }

        # Her sorunun cevabını kontrol et
        for i in range(1, 9):
            question = f'q{i}'
            if question not in answers or answers[question] == '':
                return "Tüm soruları cevaplandırmalısınız!"

        conn = sqlite3.connect('database/exam.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO answers (user_id, q1, q2, q3, q4, q5, q6, q7, q8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (session['user_id'], answers['q1'], answers['q2'], answers['q3'], answers['q4'], answers['q5'], answers['q6'], answers['q7'], answers['q8']))
        conn.commit()
        conn.close()

        return redirect(url_for('results'))

    return render_template('questions.html')

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    conn = sqlite3.connect('database/exam.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, surname, q1, q2, q3, q4, q5, q6, q7, q8 FROM users INNER JOIN answers ON users.id = answers.user_id')
    results = cursor.fetchall()
    conn.close()

    correct_answers = {
        'q1': 'a',
        'q2': 'b',
        'q3': 'b',
        'q4': 'c',
        'q5': 'c',
        'q6': 'a',
        'q7': 'b',
        'q8': 'a',
    }

    if not results:
        return render_template('no_users_found.html')

    scores = []
    for result in results:
        score = 0
        for i in range(1, 9):
            correct_answer = correct_answers[f'q{i}']
            student_answer = result[i + 1]
            if student_answer == correct_answer:
                score += 1
        scores.append((result[0], result[1], score))

    scores = sorted(scores, key=lambda x: x[2], reverse=True)
    return render_template('results.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
