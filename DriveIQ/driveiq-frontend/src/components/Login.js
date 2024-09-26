import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { loginUser } from '../services/api';
import '../styles/Login.scss';

const Login = () => {
  const [name, setName] = useState('');
  const [loginType, setLoginType] = useState('user');
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const type = params.get('type');
    if (type === 'admin') {
      setLoginType('admin');
    }
  }, [location]);

  const handleLogin = async (e) => {
    e.preventDefault();
    const data = { name, loginType };
    const response = await loginUser(data);
    if (response.driver_id) {
      if (loginType === 'admin') {
        window.location.href = '/admin';
      } else {
        window.location.href = '/user-journey';
      }
    } else {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="login">
      <h2>{loginType === 'admin' ? 'Admin Login' : 'User Login'}</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit" className="btn">Login</button>
      </form>
    </div>
  );
};

export default Login;
