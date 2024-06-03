from flask import Blueprint, request, jsonify
from server import db
from server.models import Task

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done
    } for task in tasks])

@api_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data.get('title'),
        description=data.get('description')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'done': new_task.done
    }), 201
