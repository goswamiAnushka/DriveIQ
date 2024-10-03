// src/components/Login/Login.jsx

import React, { useState } from 'react';
import './Login.scss'; // Importing the SCSS for styling
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaCommentDots } from 'react-icons/fa'; // Chatbot icon

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login', { email, password });
      if (response.status === 200) {
        // Save the token and navigate to the dashboard
        localStorage.setItem('token', response.data.token);
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  const openChatBot = () => {
    navigate('/chatbot'); // Navigate to the ChatBot component
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Driver Login</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="btn-login">Login</button>
        </form>

        <p className="register-link">
          Don't have an account? <Link to="/register">Register here</Link>.
        </p>
      </div>

      {/* Chatbot Icon */}
      <div className="chatbot-icon" onClick={openChatBot}>
        <FaCommentDots />
      </div>
    </div>
  );
};

export default Login;
