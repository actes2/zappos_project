import os
import mysql.connector
from faker import Faker
from dotenv import load_dotenv
from encrypt_decrypt import encrypt_password


load_dotenv()

fake = Faker()


def populate():
    conn = mysql.connector.connect(
        user=os.getenv('sql_username'),
        password=os.getenv('sql_pass'),
        database=os.getenv("database"),
        host=os.getenv("host")
    )

    cursor = conn.cursor()

    for num in range(75):
        acc = generate_fluff()
        cursor.execute("INSERT INTO accounts(username, password) VALUES (%s, %s)", acc)

    conn.commit()

    cursor.close()
    conn.close()


def generate_fluff():
    return fake.email(), encrypt_password(fake.password(), b"zappos")


if __name__ == "__main__":
    print("Init")
    populate()


