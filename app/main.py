# Main server script
# TODO: Remember when publishing to swap from local network in the .env to public domain
import os

from flask import Flask, render_template, request, flash
import requests as req
import json
import sql_queries
from encrypt_decrypt import encrypt_password, check_password
from dotenv import load_dotenv



app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]

        print(f"Login attempt by:{email}")

        acc = sql_queries.check_for_sql_account(email, "any")

        if acc:
            print(f"{email} exists!")

            if check_password(pwd):
                print("Successful password validation!")
                print(f"{email} is good to login!")
                # ToDo: Stuff here now that we successfully logged in with our encrypted password stored on the database

            else:
                print("Invalid password!")
                flash("Username or Password were incorrect!")
                flash("If you've forgotten your password, reach out to an Database admin for further assistance.")

        else:
            print(f"{email} does not exist!")
            flash("Username or Password were incorrect!")
            flash("If you've forgotten your password, reach out to an Database admin for further assistance.")

    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]
        print(f"email is: {email}\npassword is: {pwd}")

        if sql_queries.check_for_sql_account(email):
            print("Account already exists")
            flash("Account already exists!")
            return render_template("register.html")
        else:
            print("Creating an account!")
            sql_queries.make_new_sql_account(email, pwd)
            return  render_template("login.html")

    # ToDo: Make a value pass through that denotes that we succeeded / failed to create an account.
    return render_template("register.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route('/query_test', methods=["POST", "GET"])
def query_test():
    if request.method == "POST":
        print(f"Internal request! Here's our data: {request.data} \t here's our url: {request.base_url}")

        data = str(request.data)
        if data.count("acquire-duck"):
            # Acquire an image of a duck.
            return json.loads(req.request("GET", "https://random-d.uk/api/v2/random").text)["url"]
        return ""


if __name__ == "__main__":
    print("Init!")

    load_dotenv()

    key = encrypt_password(os.getenv("session_key"), b"A dash of Salt and Pepper is all you need!")

    app.config['SECRET_KEY'] = str(key)
    app.run("0.0.0.0", port=80, debug=True)

