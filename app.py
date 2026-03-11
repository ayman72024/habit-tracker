from flask import Flask, render_template

app = Flask(_name_)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, password)
    return "Login submitted!"
return render_template("login.html")

if __name__ == __main__:
  app.run(debug=True)
