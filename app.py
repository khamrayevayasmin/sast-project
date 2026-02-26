from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "Login page"

@app.route("/login")
def loSgin():
    username = request.args.get("username")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
#SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return "Checked"

if __name__ == "__main__":
    app.run(debug=True)