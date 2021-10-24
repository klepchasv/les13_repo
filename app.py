from flask import Flask, jsonify, request
from functions import read_books, generate_ISBN, generate_id, write_file

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


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

    write_file("books.json", books)

    return jsonify(books)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
