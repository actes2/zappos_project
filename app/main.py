# Main server script
from flask import Flask, render_template


app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    print("Hello world!")
    app.run("0.0.0.0", port=80)

