# Main server script
# TODO: Remember when publishing to swap from local network in the .env to public domain
import os

from flask import Flask, render_template, request, flash, session
import requests as req
import json
import sql_queries
from encrypt_decrypt import encrypt_password, check_password
from dotenv import load_dotenv


default_table = "accounts"

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():

    usrname = session["user"] if "user" in session else "none"

    if "table" in session:
        table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
    else:
        table_info = [], []

    table_headers = table_info[0]
    table_list = table_info[1]

    return render_template("index.html", username=usrname, curpage="hom-btn",
                           t_icnt=len(table_list),
                           t_items=table_list,
                           t_hcnt=len(table_headers),
                           t_headers=table_headers)


@app.route("/login", methods=["POST", "GET"])
def login():
    usrname = session["user"] if "user" in session else "none"

    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]

        if email.strip() == "" or pwd.strip() == "":
            flash("Email or Password cannot be empty!")
            return render_template("login.html", username=usrname, curpage="log-btn")

        print(f"Login attempt by:{email}")

        acc = sql_queries.get_account_if_exists(email)
        if acc is None:
            print(f"{email} does not exist!")
            flash("Username or Password is incorrect!")
            flash("If you've forgotten your password, reach out to a Database Admin for assistance.")

            return render_template("login.html", username=usrname, curpage="log-btn")

        else:
            print(f"{email} exists!")

            if check_password(pwd, acc[2]):
                print("Successful password validation!")
                print(f"{email} is verified to log-in; saving session!")

                session["user"] = email
                session["table"] = "accounts"
                session["key"] = acc[0]

                if "table" in session:
                    table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
                else:
                    table_info = [], []

                if len(table_info[0]) == 0 or len(table_info[1]) == 0:
                    return render_template("login.html", username=usrname, curpage="log-btn")

                table_headers = table_info[0]
                table_list = table_info[1]

                return render_template("/index.html", username=email, curpage="hom-btn",
                                       t_icnt=len(table_list),
                                       t_items=table_list,
                                       t_hcnt=len(table_headers),
                                       t_headers=table_headers)
            else:
                print("Invalid password!")
                flash("Username or Password is incorrect!")
                flash("If you've forgotten your password, reach out to a Database Admin for assistance.")

    return render_template("login.html", username=usrname, curpage="log-btn")


@app.route("/register", methods=["POST", "GET"])
def register():
    usrname = session["user"] if "user" in session else "none"

    if request.method == "POST":
        usr_details = request.form

        email = usr_details["email"]
        pwd = usr_details["password"]

        if email.strip() == "" or pwd.strip() == "":
            flash("Email or Password cannot be empty!")
            return render_template("register.html", username=usrname, curpage="reg-btn")

        # print(f"email is: {email}\npassword is: {pwd}")
        check_for_acc = sql_queries.get_account_if_exists(email)
        if check_for_acc is None:
            print("Error contacting Database")
            flash("Error contacting Database")
            return render_template("register.html", username=usrname, curpage="reg-btn")

        if check_for_acc != 0:
            print("Account already exists")
            flash("Account already exists!")
            return render_template("register.html", username=usrname, curpage="reg-btn")
        else:
            print("Creating an account!")

            if sql_queries.make_new_sql_account(email, pwd):
                return render_template("login.html", username=usrname, curpage="log-btn")

    return render_template("register.html", username=usrname, curpage="reg-btn")


@app.route("/admin")
def admin():
    if "user" in session:
        if "table" in session:
            table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
        else:
            table_info = [], []

        table_headers = table_info[0]
        table_list = table_info[1]
        dbtable_names = sql_queries.grab_all_table_names_from_db()
        if len(dbtable_names) == 0 or len(table_headers) == 0 or table_list == 0:
            return render_template("index.html", username=session["user"], curpage="hom-btn",
                                   t_icnt=len(table_list),
                                   t_items=table_list,
                                   t_hcnt=len(table_headers),
                                   t_headers=table_headers)

        return render_template("admin.html", username=session["user"], curpage="adm-btn",
                               t_icnt=len(table_list),
                               t_items=table_list,
                               t_hcnt=len(table_headers),
                               t_headers=table_headers,
                               a_table=session["table"],
                               db_table_names_cnt=len(dbtable_names),
                               db_table_names=dbtable_names)

    return render_template("404.html")


@app.route('/query_self', methods=["POST", "GET"])
def query_self():
    if request.method == "POST":

        data = request.data.decode()
        print(f"Internal request! Here's our data:\n{data}")

        # ToDo: change this from count to just literal

        # If we have an active session validated then we're fine to execute API queries here.
        if "user" in session:
            # There's no significance to the character, just a solid unicode const for delimitation
            if data.count("¬") and data != "¬":
                unpack_req = data.split('¬')

                if unpack_req[0] == "createRecord":
                    r_values = []

                    for x in range(1, len(unpack_req)):
                        r_values.append(unpack_req[x])

                    r_headers = list(sql_queries.get_table_headers(session["table"]))
                    if len(r_headers) == 0:
                        return "A connection error to the DB has occurred."

                    if "password" in r_headers:
                        password_index = None
                        for index, value in enumerate(r_headers):
                            if value == password_index:
                                password_index = index
                        if password_index is not None:
                            r_values[password_index] = encrypt_password(r_values[password_index])

                    if "key" in r_headers:
                        r_headers.remove("key")

                    sql_queries.make_new_sql_entry(r_headers, r_values, session["table"])
                    return "modSuccess"

                if unpack_req[0] == "deleteRecord" and len(unpack_req) == 2:

                    if unpack_req[1] == str(session["key"]):
                        print("That's a bit morbid, no, you may not delete yourself.")
                        return "That's a bit morbid, no, you may not delete yourself."

                    sql_queries.delete_sql_table_item(unpack_req[1], session["table"])

                    return "modSuccess"

                if unpack_req[0] == "swapTables" and len(unpack_req) == 2:

                    result = sql_queries.get_table_headers_and_all_items(table=unpack_req[1])
                    if len(result[0]) == 0 or len(result[1]) == 0:
                        return "Failure to swap"

                    session["table"] = unpack_req[1]
                    return "reload"

                if unpack_req[0] == "updateRecord" and len(unpack_req) == 4:

                    if unpack_req[1] == "password":
                        unpack_req[2] = encrypt_password(unpack_req[2])

                    sql_queries.modify_sql_column(unpack_req[1], unpack_req[2], unpack_req[3], table=session["table"])

                    return "modSuccess"

        if data == "acquire-duck":
            # Acquire an image of a duck.
            print("here")
            return json.loads(req.request("GET", "https://random-d.uk/api/v2/random").text)["url"]

        if data == "logout":

            session.pop("user", None)
            session.pop("table", None)
            session.pop("key", None)

            return "relog"

        return ""


if __name__ == "__main__":
    print("Init!")


    load_dotenv()

    key = encrypt_password(os.getenv("session_key"), "A dash of Salt and Pepper is all you need!")

    app.config['SECRET_KEY'] = str(key)
    app.run("0.0.0.0", port=80, debug=True)



