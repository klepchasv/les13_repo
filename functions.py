import json
import random


def read_books(filename):
    with open(filename, "r") as file:
        try:
            books = json.load(file)
        except Exception as e:
            print(e)
            books = []

        return books


def generate_id(filename):
    books = read_books(filename)
    ids = []
    for book in books:
        ids.append(book["id"])

    new_id = max(ids) + 1

    return new_id


def generate_ISBN(filename):
    books = read_books(filename)

    isbns = []

    for book in books:
        isbns.append(book["isbn"])

    while True:
        valid_isbn = True
        first_num = str(random.randint(1, 999)).zfill(3)
        second_num = str(random.randint(1, 7))
        third_num = str(random.randint(1, 999)).zfill(3)
        fourth_num = "0" + str(random.randint(1, 9999)).zfill(4)
        fiveth_num = str(random.randint(1, 4))

        new_isbn = "-".join([first_num, second_num, third_num, fourth_num, fiveth_num])

        if new_isbn is isbns:
            valid_isbn = False

        if valid_isbn:
            break

    return new_isbn


def write_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
