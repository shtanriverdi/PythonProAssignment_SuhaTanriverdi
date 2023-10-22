# seed.py
import sqlite3
import random

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

def seed_data():
    create_database()
    conn = sqlite3.connect('database/exam.db')
    cursor = conn.cursor()

    # Rastgele kullanıcılar oluştur
    names = ['Ahmet', 'Ayşe', 'Mehmet', 'Elif', 'Mustafa', 'Zeynep', 'Emir', 'Leyla']
    surnames = ['Yılmaz', 'Demir', 'Kaya', 'Arslan', 'Aydın', 'Güneş', 'Kurt', 'Koç']

    for _ in range(30):
        name = random.choice(names)
        surname = random.choice(surnames)
        cursor.execute('INSERT INTO users (name, surname) VALUES (?, ?)', (name, surname))

    # Rasgele puanlar ekle (1 ila 8 arası)
    for user_id in range(1, 31):
        answers = [random.choice(['a', 'b', 'c', 'd']) for _ in range(8)]
        cursor.execute('INSERT INTO answers (user_id, q1, q2, q3, q4, q5, q6, q7, q8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, *answers))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_data()
