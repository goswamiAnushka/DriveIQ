import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.scss';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h2>DriveIQ Insurance</h2>
      </div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/login-selector">Login</Link>
        <Link to="/register">Register</Link>
      </div>
    </nav>
  );
};

export default Navbar;
