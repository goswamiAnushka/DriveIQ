import React from 'react';
import ReactDOM from 'react-dom/client'; // Use createRoot from React 18
import './styles/global.scss'; // Global styles
import App from './App';
import { BrowserRouter as Router } from 'react-router-dom';

// Create root for React 18
const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <Router>
      <App />
    </Router>
  </React.StrictMode>
);
