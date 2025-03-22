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


@app.route('/', methods=['GET'])
def home():
    """
    Gets all the books and renders the content
    to the home.html template. Sets the sort function for title
    as a default. Gets the sort parameter and the search parameter
    from query.
    """
    sort_by = request.args.get("sort_by", "title")  # Default sorting by title
    if sort_by == "author":
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()

    search = request.args.get("search")
    if search:
        books = Book.query.filter(Book.title.like(f"%{search}%")).all()

    return render_template("home.html", books=books, sort_by=sort_by, search=search)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Renders the add_author.html template.
    Gets the name, birthdate and the date of
    death from post request.
    """
    if request.method == 'POST':
        if not request.form["name"] or not request.form["birthdate"]:
            error = "Empty data. Please enter all data."
            return render_template("add_author.html", error=error)
        author = Author(
            name=request.form["name"].strip(),
            birth_date=datetime.strptime(request.form["birthdate"], "%Y-%m-%d").date(),
            date_of_death=datetime.strptime(request.form["date of death"], "%Y-%m-%d").date() if request.form["date of death"] else None,
        )

        db.session.add(author)
        db.session.commit()

        flash(f"Author '{request.form['name']}' added successfully to the database", "success")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Renders the add_book.html template.
    Gets the isbn, title, publication year and
    author from post request.
    """
    if request.method == 'POST':
        if not request.form["isbn"] or not request.form["title"] or not request.form["publication year"] or not request.form["author"]:
            error = "Empty data. Please enter all data."
            return render_template("add_book.html", error=error)
        isbn_exists = Book.query.filter_by(isbn=request.form["isbn"]).first()
        if isbn_exists:
            error = "Book with this isbn already exists."
            return render_template("add_book.html", error=error)
        book_cover = get_book_cover(request.form["isbn"])
        book = Book(
            isbn=request.form["isbn"].strip(),
            title=request.form["title"].strip(),
            publication_year=int(datetime.strptime(request.form["publication year"].strip(), "%Y").year),
            cover=book_cover,
            author_id=request.form["author"]
        )

        db.session.add(book)
        db.session.commit()

        flash(f"Book '{request.form['title']}' added successfully to the database", "success")
        return redirect(url_for("add_book"))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['GET'])
def delete_book(book_id):
    """
    Deletes the book with the given book id.
    If there are no more books from an author
    in the library, deletes the author too.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)

    other_books = Book.query.filter_by(author_id=author.id).count()
    if other_books == 0:
        db.session.delete(author)

    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
