import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App'; // Importa tu componente principal App

import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App /> {/* Usa tu componente principal App */}
  </React.StrictMode>,
  document.getElementById('root')
);

// Si deseas medir el rendimiento de tu aplicación, puedes utilizar reportWebVitals
reportWebVitals();
