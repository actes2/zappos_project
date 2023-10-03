import os
import mysql.connector
from dotenv import load_dotenv
from encrypt_decrypt import encrypt_password

load_dotenv()


def createConnection():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('sql_username'),
            password=os.getenv('sql_pass'),
            database=os.getenv("database"),
            host=os.getenv("host")
        )
        return conn
    except mysql.connector.InterfaceError as ex:
        return None


def grab_all_table_names_from_db():
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return []


    cursor = conn.cursor()
    sql_syntax = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'"

    cursor.execute(sql_syntax)

    table_names = cursor.fetchall()

    table_names = [str(item) for item in table_names]

    for c in ["(", ")", "'", ","]:
        table_names = [item.replace(c, "") for item in table_names]

    cursor.close()
    conn.close()
    return table_names


def get_table_headers(table="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return []

    cursor = conn.cursor()

    # Remember immutability saves on security injection nightmares
    sql_syntax = "SELECT * FROM {}".format(table)
    cursor.execute(sql_syntax)

    headers = cursor.column_names
    cursor.fetchall()

    # print(headers)
    # print(l_items)
    cursor.close()
    conn.close()

    return headers


def get_table_headers_and_all_items(table="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return [], []

    cursor = conn.cursor()

    # Remember immutability saves on security injection nightmares
    sql_syntax = "SELECT * FROM {}".format(table)
    cursor.execute(sql_syntax)

    headers = cursor.column_names
    l_items = cursor.fetchall()

    # print(headers)
    # print(l_items)
    cursor.close()
    conn.close()

    return headers, l_items


def modify_sql_column(column, value, key, table="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return

    value_and_key = (value, key)

    cursor = conn.cursor()

    # Remember immutability saves on security injection nightmares
    sql_syntax = "UPDATE {} SET {} = %s WHERE {} = %s;".format(table, column, table + ".key")

    cursor.execute(sql_syntax, value_and_key)

    conn.commit()

    cursor.close()
    conn.close()


def change_sql_account(account, acctable="accounts"):
    # This function assumes that the tuple presented to it is a bi-product of an initial query (Key, Username, Password)

    conn = createConnection()
    if conn is None or not conn.is_connected():
        return

    cursor = conn.cursor()

    account = (account[1], account[2], account[0])

    sql_syntax = "UPDATE {} SET `username` = %s, `password` = %s WHERE {} = %s".format(acctable, acctable + ".key")
    # Remember immutability saves on security injection nightmares
    cursor.execute(sql_syntax, account)

    conn.commit()

    cursor.close()
    conn.close()


def make_new_sql_entry(headers, values, table="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return

    cursor = conn.cursor()

    sql_syntax = "INSERT INTO {}("
    columns_syntax = ""
    values_syntax = "VALUES ("

    # "{}, {}) VALUES (%s, %s)"
    for x in range(0, len(headers)):
        if x < len(headers) - 1:
            columns_syntax = columns_syntax + "{}, "
        else:
            columns_syntax = columns_syntax + "{}) "
    for x in range(0, len(values)):
        if x < len(values) - 1:
            values_syntax = values_syntax + "%s, "
        else:
            values_syntax = values_syntax + "%s)"

    sql_syntax = sql_syntax + columns_syntax + values_syntax
    # print(sql_syntax)
    sql_syntax = sql_syntax.format(table, *headers)
    # print(sql_syntax)
    cursor.execute(sql_syntax, values)

    conn.commit()

    cursor.close()
    conn.close()


def make_new_sql_account(u_email, u_passwd, acctable="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return None

    e_pass = encrypt_password(u_passwd)

    acc = u_email, e_pass

    cursor = conn.cursor()

    sql_syntax = "INSERT INTO {}(username, password) VALUES (%s, %s)".format(acctable)
    cursor.execute(sql_syntax, acc)

    conn.commit()
    cursor.close()
    conn.close()

    return True


def delete_sql_table_item(u_key, table="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return

    cursor = conn.cursor()

    sql_syntax = "DELETE FROM {} WHERE {} = %s".format(table, table + ".key")
    # Remember immutability saves on security injection nightmares
    cursor.execute(sql_syntax, (u_key,))

    _ = cursor.fetchall()

    conn.commit()

    cursor.close()
    conn.close()


def get_account_if_exists(u_email, acctable="accounts"):
    conn = createConnection()
    if conn is None or not conn.is_connected():
        return None

    cursor = conn.cursor()

    sql_syntax = "SELECT `key`, `username`, `password` FROM {} WHERE username = %s".format(acctable)
    # Remember immutability saves on security injection nightmares
    cursor.execute(sql_syntax, (u_email,))

    raw_result = cursor.fetchall()

    conn.close()
    cursor.close()
    if len(raw_result) == 0:
        return 0
    else:
        return raw_result[0]


