import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from './Navbar';
import '../styles/Home.scss';

const Home = () => {
  return (
    <div className="home">
      <Navbar />
      <div className="home-content">
        <h1>Welcome to DriveIQ Insurance</h1>
        <p>Your trusted partner for telematics-based insurance.</p>
        <div className="home-buttons">
          <Link to="/login-selector" className="btn">Login</Link>
          <Link to="/register" className="btn btn-secondary">Register</Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
