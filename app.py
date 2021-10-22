from flask import Flask, jsonify, request
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


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
    import random
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


@app.route("/books/<int:bid>")
def book(bid):
    books = read_books("books.json")

    cur_book = {}

    for book in books:

        if book["id"] == bid:
            cur_book = book
            break

    if cur_book:
        return jsonify(cur_book), 200
    return jsonify("Book hasn't found"), 404


@app.route("/add_book", methods=["POST"])
def add_book():
    books = read_books("books.json")
    new_book = request.get_json()[0]
    new_book["id"] = generate_id("books.json")
    new_book["isbn"] = generate_ISBN("books.json")

    books.append(new_book)

    with open("books.json", "w") as file:
        file.write(json.dumps(books))

    return jsonify(books)


if __name__ == "__main__":
    app.run(port=8000, debug=True)