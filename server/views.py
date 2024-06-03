from flask import Blueprint, request, jsonify
from server.models import db, Task

task_blueprint = Blueprint('tasks', __name__)

@task_blueprint.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]
    return jsonify(tasks_list)

@task_blueprint.route('/', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'completed': new_task.completed})
