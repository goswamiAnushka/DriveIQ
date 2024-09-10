import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.scss';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <h2>Telematics App</h2>
                <ul className="navbar-links">
                    <li>
                        <Link to="/dashboard">Dashboard</Link>
                    </li>
                    <li>
                        <Link to="/journey">Journey</Link>
                    </li>
                    <li>
                        <Link to="/login">Login</Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
