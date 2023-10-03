import os
import mysql.connector
from faker import Faker
from dotenv import load_dotenv
from sql_queries import make_new_sql_account


load_dotenv()

fake = Faker()


def populate():
    for num in range(75):
        acc = generate_fluff()
        make_new_sql_account(acc[0], acc[1])


def generate_fluff():
    return fake.email(), fake.password()


if __name__ == "__main__":
    print("Init")
    populate()


