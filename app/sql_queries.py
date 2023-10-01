import os
import mysql.connector
from dotenv import load_dotenv
from encrypt_decrypt import encrypt_password

load_dotenv()


def change_sql_account(account):
    # This function assumes that the tuple presented to it is a bi-product of an initial query (Key, Username, Password)

    conn = mysql.connector.connect(
        user=os.getenv('sql_username'),
        password=os.getenv('sql_pass'),
        database=os.getenv("database"),
        host=os.getenv("host")
    )

    cursor = conn.cursor()

    account = (account[1], account[2], account[0])

    # Remember immutability saves on security injection nightmares
    cursor.execute("UPDATE `accounts` SET `username` = %s, `password` = %s WHERE accounts.key = %s", account)

    conn.commit()

    cursor.close()
    conn.close()


def make_new_sql_account(u_email, u_passwd):
    e_pass = encrypt_password(u_passwd, b"zappos_reg")

    acc = u_email, e_pass

    conn = mysql.connector.connect(
        user=os.getenv('sql_username'),
        password=os.getenv('sql_pass'),
        database=os.getenv("database"),
        host=os.getenv("host")
    )

    cursor = conn.cursor()

    cursor.execute("INSERT INTO accounts(username, password) VALUES (%s, %s)", acc)

    cursor.close()
    conn.close()


def delete_sql_account(u_key):
    conn = mysql.connector.connect(
        user=os.getenv('sql_username'),
        password=os.getenv('sql_pass'),
        database=os.getenv("database"),
        host=os.getenv("host")
    )

    cursor = conn.cursor()

    # Remember immutability saves on security injection nightmares
    cursor.execute("DELETE FROM accounts WHERE accounts.key = %s", (u_key,))

    result = cursor.fetchall()

    conn.commit()

    cursor.close()
    conn.close()


def check_for_sql_account(u_email, ret_t="bool"):
    conn = mysql.connector.connect(
        user=os.getenv('sql_username'),
        password=os.getenv('sql_pass'),
        database=os.getenv("database"),
        host=os.getenv("host")
    )

    cursor = conn.cursor()

    # Remember immutability saves on security injection nightmares
    cursor.execute("SELECT `key`, `username`, `password` FROM accounts WHERE username = %s", (u_email,))

    raw_result = cursor.fetchall()

    conn.close()
    cursor.close()
    if len(raw_result) == 0:
        return False

    result = raw_result[0]

    if ret_t == "bool":
        return True
    else:
        return result


