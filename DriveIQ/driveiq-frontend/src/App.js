import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import LoginSelector from './components/LoginSelector';
import Login from './components/Login';
import Register from './components/Register';
import UserJourney from './components/UserJourney';
import AdminDashboard from './components/AdminDashboard';
import TripReplay from './components/TripReplay';
import Leaderboard from './components/Leaderboard';
import GeoFenceAlert from './components/GeoFenceAlert';
import Badges from './components/Badges';
import './styles/global.scss';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login-selector" element={<LoginSelector />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/user-journey" element={<UserJourney />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/trip-replay" element={<TripReplay />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/geo-fence" element={<GeoFenceAlert />} />
        <Route path="/badges" element={<Badges />} />
      </Routes>
    </div>
  );
}

export default App;
