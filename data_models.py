from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    """
    Defined an Author model that includes the properties
    id, name, birth_date, and date_of_death.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        """
        Represents the Author model in a readable way.
        """
        return f"Author(id = {self.id}, name = {self.name}, birth date = {self.birth_date}, date of death = {self.date_of_death})"


class Book(db.Model):
    """
    Defines a Book model that includes the properties
    id, isbn, title, publication_year and author_id as columns
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.ForeignKey("authors.id"))

    def __repr__(self):
        """
        Represents the Book model in a readable way.
        """
        return f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title}, publication year = {self.publication_year}, author id = {self.author_id}, book cover = {self.book_cover})"
