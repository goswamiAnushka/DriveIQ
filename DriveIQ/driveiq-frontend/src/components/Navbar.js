import React from 'react';
import { Link } from 'react-router-dom';
import '../assets/styles.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/journey">Start Journey</Link>
      <Link to="/history">History</Link>
    </nav>
  );
};

export default Navbar;
