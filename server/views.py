from flask import Blueprint, request, jsonify
from models import Task, db

bp = Blueprint('tasks', __name__)

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]
    return jsonify(tasks_list)

@bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict())

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if 'completed' in data:
        task.completed = data['completed']
    
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})
