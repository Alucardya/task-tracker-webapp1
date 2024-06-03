# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from server.views import register_routes  # Updated import path

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)  # Register routes after creating the app

    return app

def register_routes(app):
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        tasks_list = [task.to_dict() for task in tasks]
        return jsonify(tasks_list)

    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        new_task = Task(title=data['title'], description=data['description'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict())

    @app.route('/tasks/<int:task_id>/', methods=['PUT'])
    def update_task(task_id):
        data = request.get_json()
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        return jsonify(task.to_dict())

    @app.route('/tasks/<int:task_id>/', methods=['DELETE'])
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
