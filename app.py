from flask import Flask, flash, redirect, render_template, request, session
from helpers import apology, login_required
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta


app = Flask(__name__)
app.secret_key = "your_secret_key"
db = SQL("sqlite:///habits.db")

@app.route("/progress")
@login_required
def progress():
    habits = db.execute("""
        SELECT 
            habits.id,
            habits.name,
            habits.target_days,

            COUNT(CASE
                WHEN strftime('%Y-%W', habit_logs.completed_date) = strftime('%Y-%W', 'now')
                THEN 1
            END) AS completed_this_week

        FROM habits
        LEFT JOIN habit_logs
            ON habits.id = habit_logs.habit_id
        WHERE habits.user_id = ?
        GROUP BY habits.id
        ORDER BY habits.created_at DESC
    """, session["user_id"])

    for habit in habits:
        habit["days_left"] = max(habit["target_days"] - habit["completed_this_week"], 0)
        if habit["target_days"] > 0:
            habit["percent"] = min(int((habit["completed_this_week"] / habit["target_days"]) * 100), 100)
        else:
            habit["percent"] = 0

    return render_template("progress.html", habits=habits)

@app.route("/edit/<int:habit_id>", methods=["GET", "POST"])
@login_required
def edit(habit_id):
    habit = db.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        habit_id,
        session["user_id"]
    )

    if len(habit) != 1:
        return apology("Habit not found", 404)

    habit = habit[0]

    if request.method == "POST":
        name = request.form.get("name")
        target_days = request.form.get("target_days")

        if not name:
            return apology("Habit name is required", 400)

        if not target_days:
            return apology("Target days is required", 400)

        try:
            target_days = int(target_days)
        except ValueError:
            return apology("Target days must be a number", 400)

        if target_days < 1 or target_days > 7:
            return apology("Target days must be between 1 and 7", 400)

        db.execute(
            "UPDATE habits SET name = ?, target_days = ? WHERE id = ?",
            name,
            target_days,
            habit_id
        )

        return redirect("/")

    return render_template("edit.html", habit=habit)

@app.route("/delete/<int:habit_id>", methods=["POST"])
@login_required
def delete(habit_id):
    habit = db.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        habit_id,
        session["user_id"]
    )

    if len(habit) != 1:
        return apology("Habit not found", 404)

    db.execute("DELETE FROM habit_logs WHERE habit_id = ?", habit_id)
    db.execute("DELETE FROM habits WHERE id = ?", habit_id)

    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
  if request.method == "POST":
    name = request.form.get("name")
    target_days = request.form.get("target_days")

    if not name:
      return apology("Habit name is required", 400)
    if not target_days:
      return apology("Target days is required", 400)
    try:
      target_days = int(target_days)
    except ValueError:
      return apology("Target days must be a number", 400)
    if target_days < 1 or target_days > 7:
      return apology("Target days must be between 1 and 7", 400)
    
    db.execute(
      "INSERT INTO habits (user_id, name, target_days) VALUES (?, ?, ?)",
      session["user_id"],
      name,
      target_days
    )

    return redirect("/")
  return render_template("add.html")

@app.route("/complete/<int:habit_id>", methods=["POST"])
@login_required
def complete(habit_id):
    today = date.today().isoformat()
    habit = db.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        habit_id, session["user_id"]
    )

    if len(habit) != 1:
        return apology("Habit not found", 404)

    existing = db.execute(
        "SELECT * FROM habit_logs WHERE habit_id = ? AND completed_date = ?",
        habit_id, today
    )

    if not existing:
        db.execute(
            "INSERT INTO habit_logs(habit_id, completed_date) VALUES (?, ?)",
            habit_id, today
        )
        flash(f"🎉 Great job! You completed '{habit[0]['name']}' today.")
    else:
        flash(f"'{habit[0]['name']}' is already completed for today.")

    return redirect("/")


def init():
  db.execute("""
             CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL UNIQUE,
             hash TEXT NOT NULL
             )
             """)
  db.execute("""
        CREATE TABLE IF NOT EXISTS habits(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER NOT NULL,
             name TEXT NOT NULL,
             target_days INTEGER NOT NULL,
             created_at DATE DEFAULT CURRENT_DATE,
             FOREIGN KEY(user_id) REFERENCES users(id)
             )
             """)
  db.execute("""
      CREATE TABLE IF NOT EXISTS habit_logs(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
             habit_id INTEGER NOT NULL,
             completed_date DATE NOT NULL,
             FOREIGN KEY(habit_id) REFERENCES habits(id)
             )
             """)
  return "Database initialized!"
@app.route("/")
@login_required
def index():
    habits = db.execute("""
        SELECT 
            habits.id,
            habits.name,
            habits.target_days,

            COUNT(CASE
                WHEN strftime('%Y-%W', habit_logs.completed_date) = strftime('%Y-%W','now')
                THEN 1
            END) AS completed_this_week,

            COALESCE(MAX(CASE
                WHEN habit_logs.completed_date = date('now')
                THEN 1
            END), 0) AS completed_today

        FROM habits

        LEFT JOIN habit_logs
            ON habits.id = habit_logs.habit_id

        WHERE habits.user_id = ?

        GROUP BY habits.id

        ORDER BY habits.created_at DESC

    """, session["user_id"])

    for habit in habits:

        logs = db.execute("""
            SELECT completed_date
            FROM habit_logs
            WHERE habit_id = ?
            ORDER BY completed_date DESC
        """, habit["id"])

        completed_dates = {row["completed_date"] for row in logs}

        streak = 0
        current_day = date.today()

        while current_day.isoformat() in completed_dates:
            streak += 1
            current_day -= timedelta(days=1)

        habit["streak"] = streak
    


    return render_template("index.html", habits=habits)
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
  return redirect("/login")

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
    flash("🎉 Registration successful! Please log in.")

    return redirect("/login")
  return render_template("register.html")

if __name__ == "__main__":
  app.run(debug=True)

#I wrote the code originally for all definitions and then cleared out the bugs using ChatGpt