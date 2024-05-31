// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Це ваш загальний файл CSS, де ви можете розмістити глобальні стилі
import App from './App'; // Імпорт компонента App
import reportWebVitals from './reportWebVitals'; // Опціонально, для збору метрик

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Рендеринг App компонента у <div id="root"></div>
);

reportWebVitals();
