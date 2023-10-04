import os
import mysql.connector
from faker import Faker
from dotenv import load_dotenv
from sql_queries import make_new_sql_account, make_new_extra, make_new_details
from random import randint


load_dotenv()

fake = Faker()


def populate():
    for num in range(75):
        acc = generate_fluff()
        make_new_sql_account(acc[0], acc[1])
        make_new_extra(generate_extra())
        make_new_details(generate_details())


def generate_extra():
    return randint(1000, 10000), randint(1, 30), randint(3, 11), randint(1, 3), randint(1, 102), fake.city(), randint(1, 140)


def generate_details():
    return fake.address(), fake.company(), randint(0, 10)


def generate_fluff():
    return fake.email(), fake.password()


if __name__ == "__main__":
    print("Init")
    populate()


