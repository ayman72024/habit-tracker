from flask import Flask, render_template, request, session, redirect
from helpers import apology
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"
db = SQL("sqlite:///habits.db")

@app.route("/init")
def init():
  db.execute("""
             CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL UNIQUE,
             hash TEXT NOT NULL
             )
             """)
  return "Database initialized!"
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username:
      return apology("Username is required!", 400)
    if not password:
      return apology("Password is required!", 400)
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if len(rows) != 1:
       return apology("Username does not exist", 403)
    if not check_password_hash(rows[0]["hash"],password):
        return apology("Incorrect password", 403)
    session["user_id"] = rows[0]["id"]
    return redirect("/")
    
  return render_template("login.html")

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username:
      return apology("Username is required!", 400)
    if not password:
      return apology("Password is required!", 400)
    if not confirmation:
      return apology("Please confirm your password!", 400)
    if password != confirmation:
      return apology("Passwords must match", 400)
    print(username, password, confirmation)
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if len(rows) != 0:
      return apology("Username already exists", 400)
    hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username,hash) VALUES (?, ?)", username, hash)

    return "Register submitted!"
  return render_template("register.html")

if __name__ == "__main__":
  app.run(debug=True)
