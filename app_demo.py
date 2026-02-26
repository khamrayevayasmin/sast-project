from flask import Flask, request
import sqlite3

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
        except:
            pass

    conn.commit()
    conn.close()
    print(" База данных инициализирована")


@app.route("/")
def home():
    return '''
    <h1>Login page</h1>
    <p>Try: <a href="/login?username=admin">/login?username=admin</a></p>
    <p>Try SQL Injection: <a href="/login?username=' OR '1'='1">/login?username=' OR '1'='1</a></p>
    '''


@app.route("/login")
def login():
    username = request.args.get("username", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    #  SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Executing query: {query}")  # Для отладки

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return f" User found: {result[1]}"
    else:
        return f" User '{username}' not found"


if __name__ == "__main__":
    init_db()  # Инициализируем БД при запуске
    app.run(debug=True)