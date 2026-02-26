from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)


def init_db():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')


    test_users = [
        ('admin', 'admin123'),
        ('user1', 'password1'),
        ('test', 'test123')
    ]

    for username, password in test_users:
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
        except Exception as e:
            # ИСПРАВЛЕНО: не просто pass, а вывод ошибки
            print(f"Пользователь {username} уже существует: {e}")

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")


@app.route("/")
def home():
    return '''
    <h1>Login page</h1>
    <p>Try: <a href="/login?username=admin">/login?username=admin</a></p>
    <p>Try SQL Injection (should FAIL now): <a href="/login?username=' OR '1'='1">/login?username=' OR '1'='1</a></p>
    '''


@app.route("/login")
def login():
    username = request.args.get("username", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ИСПРАВЛЕНО: Параметризованный запрос (БЕЗОПАСНО!)
    query = "SELECT * FROM users WHERE username = ?"
    print(f"Executing safe query: {query} with param: {username}")

    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return f"✅ User found: {result[1]}"
    else:
        return f"❌ User '{username}' not found"


if __name__ == "__main__":
    init_db()
    # ИСПРАВЛЕНО: Безопасный debug режим
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Debug mode: {debug_mode}")
    app.run(debug=debug_mode)