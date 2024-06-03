from flask import Flask
from server.models import db  # Ensure this is the correct import path

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
