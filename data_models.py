from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Date, Column, ForeignKey


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name}, birth date = {self.birth_date}, date of death = {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(Integer)
    title = Column(String)
    publication_year = Column(Date)
    author_id = Column(ForeignKey("authors.id"))

    def __repr__(self):
        return f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title}, publication year = {self.publication_year}, author id = {self.author_id})"
