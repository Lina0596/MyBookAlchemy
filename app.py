import os
from flask import Flask, request, url_for, render_template, flash, redirect
from datetime import datetime
from data_models import db, Author, Book
import requests


app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dd0c02f28da0b1aee669432457e20529'
db.init_app(app)


def get_book_cover(isbn):
    """
    Fetches book cover from Open Library API using ISBN.
    Returns None if thee is no cover to the given ISBN.
    """
    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    response = requests.get(cover_url)
    if response.status_code == 200:
        return cover_url
    return None


@app.route('/')
def home():
    books = Book.query.all()
    for book in books:
        book.cover_url = get_book_cover(book.isbn)
    return render_template("home.html", books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        author = Author(
            name=request.form["name"],
            birth_date=datetime.strptime(request.form["birthdate"], "%Y-%m-%d").date(),
            date_of_death=datetime.strptime(request.form["date of death"], "%Y-%m-%d").date() if request.form["date of death"] else None,
        )
        db.session.add(author)
        db.session.commit()
        flash(f"Author '{request.form["name"]}' added successfully to the database", "success")
        return redirect(url_for("add_author"))
    return render_template("add_author.html")


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = Book(
            isbn=request.form["isbn"],
            title=request.form["title"],
            publication_year=int(datetime.strptime(request.form["publication year"], "%Y").year),
            author_id=request.form["author"]
        )
        db.session.add(book)
        db.session.commit()
        flash(f"Book '{request.form["title"]}' added successfully to the database", "success")
        return redirect(url_for("add_book"))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


if __name__ == "__main__":
    app.run()


"""
with app.app_context():
  db.create_all()
"""