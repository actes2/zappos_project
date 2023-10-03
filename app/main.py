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
    if "user" in session:
        usrname = session["user"]

        try:
            table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
        except Exception as ex:
            print("Error encountered: " + ex.__str__())
            usrname = "none"
            return render_template("index.html", username=usrname, curpage="hom-btn",
                                   t_icnt=0,
                                   t_items=(0,),
                                   t_hcnt=0,
                                   t_headers=(0,))

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
                           t_items=(0,),
                           t_hcnt=0,
                           t_headers=(0,))


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
        try:
            acc = sql_queries.check_for_sql_account(email, "any")
        except Exception as ex:
            print("Error loading database: " + ex.__str__())
            flash("Error loading database: " + ex.__str__())
            return render_template("login.html", username=usrname, curpage="log-btn")

        if acc:
            print(f"{email} exists!")

            try:
                pwd_check = check_password(pwd, acc[2])
            except Exception as ex:
                print("Looks like we encountered an error checking the password? " + ex.__str__())
                flash("Looks like we encountered an error checking the password? " + ex.__str__())

                return render_template("login.html", username=usrname, curpage="log-btn")

            if pwd_check:
                print("Successful password validation!")
                print(f"{email} is verified to log-in; saving session!")
                session["user"] = email
                session["table"] = "accounts"
                session["key"] = acc[0]
                print(session["key"])

                try:
                    table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
                except Exception as ex:
                    print("Error loading database: " + ex.__str__())
                    flash("Error loading database: " + ex.__str__())
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

        else:
            print(f"{email} does not exist!")
            flash("Username or Password is incorrect!")
            flash("If you've forgotten your password, reach out to a Database Admin for assistance.")

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
        # print(f"email is: {email}\npassword is: {pwd}")
        try:
            check_for_acc = sql_queries.check_for_sql_account(email)
        except Exception as ex:
            print("Error contacting Database: " + ex.__str__())
            flash("Error contacting Database: " + ex.__str__())
            return render_template("register.html", username=usrname, curpage="reg-btn")

        if check_for_acc:
            print("Account already exists")
            flash("Account already exists!")
            return render_template("register.html", username=usrname, curpage="reg-btn")
        else:
            print("Creating an account!")
            try:
                sql_queries.make_new_sql_account(email, pwd)
            except Exception as e:
                print("Account Creation Error: " + e.__str__())
                flash("Account Creation Error: " + e.__str__())
                return render_template("register.html", username=usrname, curpage="reg-btn")

            return render_template("login.html", username=usrname, curpage="log-btn")

    return render_template("register.html", username=usrname, curpage="reg-btn")


@app.route("/admin")
def admin():
    if "user" in session:
        try:
            table_info = sql_queries.get_table_headers_and_all_items(table=session["table"])
        except Exception as ex:
            print("Exception encountered: " + ex.__str__())
            return render_template("index.html", username=session["user"], curpage="hom-btn",
                                   t_icnt=0,
                                   t_items=(0,),
                                   t_hcnt=0,
                                   t_headers=(0,))

        table_headers = table_info[0]
        table_list = table_info[1]

        try:
            dbtable_names = sql_queries.grab_all_table_names_from_db()
        except Exception as ex:
            print("Exception encountered: " + ex.__str__())
            return render_template("index.html", username=session["user"], curpage="hom-btn",
                                   t_icnt=0,
                                   t_items=(0,),
                                   t_hcnt=0,
                                   t_headers=(0,))

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
                    x = 1
                    while x < len(unpack_req):
                        r_values.append(unpack_req[x])
                        x += 1
                    try:
                        r_headers = list(sql_queries.get_table_headers(session["table"]))

                        if "key" in r_headers:
                            r_headers.remove("key")

                        sql_queries.make_new_sql_entry(tuple(r_headers), tuple(r_values), session["table"])
                        return "modSuccess"

                    except Exception as ex:
                        print("Error encountered: " + ex.__str__())
                        return "Error encountered: " + ex.__str__()

                if unpack_req[0] == "deleteRecord" and len(unpack_req) == 2:

                    if unpack_req[1] == str(session["key"]):
                        print("That's a bit morbid, no, you may not delete yourself.")
                        return "That's a bit morbid, no, you may not delete yourself."

                    try:
                        sql_queries.delete_sql_table_item(unpack_req[1], session["table"])
                    except Exception as ex:
                        print("Error while trying to delete record: " + ex.__str__())
                        return "Error while trying to delete record: " + ex.__str__()

                    return "modSuccess"

                if unpack_req[0] == "swapTables" and len(unpack_req) == 2:

                    try:
                        sql_queries.get_table_headers_and_all_items(table=unpack_req[1])
                    except Exception as ex:
                        return ex.__str__()
                    session["table"] = unpack_req[1]
                    return "reload"

                if unpack_req[0] == "updateRecord" and len(unpack_req) == 4:

                    try:
                        sql_queries.modify_sql_column(unpack_req[1], unpack_req[2], unpack_req[3], table=session["table"])
                    except Exception as ex:
                        return ex.__str__()
                    return "modSuccess"


        if data == "acquire-duck":
            # Acquire an image of a duck.
            print("here")
            return json.loads(req.request("GET", "https://random-d.uk/api/v2/random").text)["url"]

        if data == "logout":
            session["user"] = "none"
            return "relog"

        return ""


if __name__ == "__main__":
    print("Init!")


    load_dotenv()

    key = encrypt_password(os.getenv("session_key"), "A dash of Salt and Pepper is all you need!")

    app.config['SECRET_KEY'] = str(key)
    app.run("0.0.0.0", port=80, debug=True)



