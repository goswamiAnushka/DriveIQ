import React from 'react';
import ReactDOM from 'react-dom/client'; // Use ReactDOM from 'react-dom/client' for React 18+
import './index.scss';
import App from './App';

// Get the root element from the DOM (ensure there's an element with id 'root' in your index.html)
const rootElement = document.getElementById('root');

// Check if the element exists
if (rootElement) {
  // Use createRoot for React 18+
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Root element not found!");
}
