import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Dashboard from './components/Dashboard/Dashboard';
import HomePage from './pages/HomePage/HomePage';  // Corrected import path for HomePage
import DailyScorePopup from './components/DailyScorePopup/DailyScorePopup'; // Optional

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<HomePage />} />  {/* Home page as the default landing page */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/daily-summary" element={<DailyScorePopup driverId="some-driver-id" />} /> {/* Optional */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
