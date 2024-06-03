import React from 'react';

const TaskItem = ({ task, onComplete, onDelete }) => {
  return (
    <li className={`task-item ${task.completed ? 'completed' : ''}`} id={`task-${task.id}`}>
      <input 
        type="checkbox" 
        checked={task.completed} 
        onChange={() => onComplete(task.id)} 
      />
      <span className="task-text">{task.description}</span>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </li>
  );
};

export default TaskItem;
