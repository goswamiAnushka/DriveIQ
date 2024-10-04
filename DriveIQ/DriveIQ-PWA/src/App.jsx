import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Dashboard from './components/Dashboard/Dashboard'; // Ensure this is correctly imported
import DailyScorePopup from './components/DailyScorePopup/DailyScorePopup'; // Optional

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} /> {/* Ensure login route is here */}
          <Route path="/dashboard" element={<Dashboard />} /> {/* Add Dashboard route */}
          <Route path="/daily-summary" element={<DailyScorePopup driverId="some-driver-id" />} /> {/* Optional */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
