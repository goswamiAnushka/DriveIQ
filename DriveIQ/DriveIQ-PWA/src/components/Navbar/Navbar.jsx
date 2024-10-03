import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.scss';

const Navbar = () => {
  return (
    <header className="navbar">
      <div className="logo">
        <Link to="/">
          <img src="/assets/logo.png" alt="Telematics App Logo" />
        </Link>
      </div>
      <nav className="nav-links">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/about">About Us</Link></li>
          <li><Link to="/features">Features</Link></li>
          <li><Link to="/pricing">Pricing</Link></li>
          <li><Link to="/contact">Contact Us</Link></li>
          <li><Link to="/login" className="login-button">Driver Login</Link></li>
          <li><Link to="/admin" className="admin-button">Admin Login</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
