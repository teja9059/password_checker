from flask import Flask, render_template, request, redirect, session
import sqlite3
import re
import bcrypt
import math
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ---------------- PASSWORD STRENGTH ----------------
def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[!@#$%^&*]", password): score += 1
    return score

# ---------------- ENTROPY ----------------
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[!@#$%^&*]", password): charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 2)
# ---------------- AI SUGGESTION ----------------
def suggest_password():
    import random, string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        data = c.fetchone()
        conn.close()

        if data and bcrypt.checkpw(pwd.encode(), data[1].encode()):
            session["user"] = user
            return redirect("/")
        return render_template("login.html", error="Invalid login")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)", (user, hashed.decode()))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/check", methods=["POST"])
def check():
    password = request.form["password"]

    score = check_strength(password)
    entropy = calculate_entropy(password)
    suggestion = suggest_password()

    return {
        "score": score,
        "entropy": entropy,
        "suggestion": suggestion
    }

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)