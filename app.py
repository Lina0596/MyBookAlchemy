import os
from flask import Flask
from data_models import db


app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'library.sqlite')}"
db.init_app(app)


with app.app_context():
  db.create_all()


if __name__ == "__main__":
    app.run()