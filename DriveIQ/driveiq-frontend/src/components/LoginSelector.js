import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LoginSelector.scss';

const LoginSelector = () => {
  return (
    <div className="login-selector">
      <h2>Select Login Type</h2>
      <div className="login-options">
        <Link to="/login?type=admin" className="btn">Admin Login</Link>
        <Link to="/login?type=user" className="btn btn-secondary">User Login</Link>
      </div>
    </div>
  );
};

export default LoginSelector;
