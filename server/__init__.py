from flask import Flask
from flask_cors import CORS
from server.models import db
from server.views import task_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    app.register_blueprint(task_blueprint, url_prefix='/tasks')
    CORS(app)

    with app.app_context():
        db.create_all()

    return app
