# Main server script
# TODO: Remember when publishing to swap from local network in the .env to public domain
from flask import Flask, render_template, request
import requests as req
import json
import sql_queries

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
        print(f"email is: {email}\npassword is: {pwd}")

        acc = sql_queries.check_for_sql_account(email, "any")

        if acc:
            print(f"{email} exists!")
            # ToDo: Login and create a proper session

        else:
            print(f"{email} does not exist!")

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
        else:
            print("Creating an account!")
            sql_queries.make_new_sql_account(email, pwd)

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
    app.run("0.0.0.0", port=80, debug=True)

