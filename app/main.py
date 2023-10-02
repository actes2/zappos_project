# Main server script
# TODO: Remember when publishing to swap from local network in the .env to public domain
import os

from flask import Flask, render_template, request, flash, session
import requests as req
import json
import sql_queries
from encrypt_decrypt import encrypt_password, check_password
from dotenv import load_dotenv



app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    if "user" in session:
        usrname = session["user"]

        table_info = sql_queries.get_table_headers_and_all_items()

        table_headers = table_info[0]
        table_list = table_info[1]

        return render_template("index.html", username=usrname, curpage="hom-btn",
                               t_icnt=len(table_list),
                               t_items=table_list,
                               t_hcnt=len(table_headers),
                               t_headers=table_headers)


    else:
        usrname = "none"

    return render_template("index.html", username=usrname, curpage="hom-btn",
                           t_icnt=0,
                           t_items=(0,0,0),
                           t_hcnt=0,
                           t_headers=(0,0,0))


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        usrname = session["user"]
    else:
        usrname = "none"

    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]

        print(f"Login attempt by:{email}")

        acc = sql_queries.check_for_sql_account(email, "any")

        if acc:
            print(f"{email} exists!")

            if check_password(pwd, acc[2]):
                print("Successful password validation!")
                print(f"{email} is verified to log-in; saving session!")
                session["user"] = email

                table_info = sql_queries.get_table_headers_and_all_items()

                table_headers = table_info[0]
                table_list = table_info[1]

                return render_template("index.html", username=usrname, curpage="hom-btn",
                                       t_icnt=len(table_list),
                                       t_items=table_list,
                                       t_hcnt=len(table_headers),
                                       t_headers=table_headers)


            else:
                print("Invalid password!")
                flash("Username or Password were incorrect!")
                flash("If you've forgotten your password, reach out to an Database admin for further assistance.")

        else:
            print(f"{email} does not exist!")
            flash("Username or Password were incorrect!")
            flash("If you've forgotten your password, reach out to an Database admin for further assistance.")

    return render_template("login.html", username=usrname, curpage="log-btn")


@app.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        usrname = session["user"]
    else:
        usrname = "none"

    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]
        print(f"email is: {email}\npassword is: {pwd}")

        if sql_queries.check_for_sql_account(email):
            print("Account already exists")
            flash("Account already exists!")
            return render_template("register.html", username=usrname, curpage="reg-btn")
        else:
            print("Creating an account!")
            sql_queries.make_new_sql_account(email, pwd)
            return  render_template("login.html", username=usrname, curpage="log-btn")

    # ToDo: Make a value pass through that denotes that we succeeded / failed to create an account.
    return render_template("register.html", username=usrname, curpage="reg-btn")


@app.route("/admin")
def admin():
    if "user" in session:
        return render_template("admin.html", username=session["user"], curpage="adm-btn")
    return render_template("404.html")


@app.route('/query_self', methods=["POST", "GET"])
def query_self():
    if request.method == "POST":
        print(f"Internal request! Here's our data: {request.data} \t here's our url: {request.base_url}")

        data = request.data.decode()
        print(data)
        # ToDo: change this from count to just literal
        if data.count("acquire-duck"):
            # Acquire an image of a duck.
            print("here")
            return json.loads(req.request("GET", "https://random-d.uk/api/v2/random").text)["url"]
        if data.count("logout"):
            session["user"] = "none"
            return "relog"

        return ""


if __name__ == "__main__":
    print("Init!")

    load_dotenv()

    key = encrypt_password(os.getenv("session_key"), "A dash of Salt and Pepper is all you need!")

    app.config['SECRET_KEY'] = str(key)
    app.run("0.0.0.0", port=80, debug=True)

