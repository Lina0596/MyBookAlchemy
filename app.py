from flask import Flask
from data_models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
db.init_app(app)


with app.app_context():
  db.create_all()

if __name__ == "__main__":
    app.run()