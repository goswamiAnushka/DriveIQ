import React, { useState } from 'react';
import { registerUser } from '../services/api';
import '../styles/Register.scss';

const Register = () => {
  const [name, setName] = useState('');
  const [acceptedTerms, setAcceptedTerms] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    const data = { name, accepted_terms: acceptedTerms };
    const response = await registerUser(data);
    if (response.driver_id) {
      alert('Registration successful. You can now log in.');
      window.location.href = '/login-selector';
    } else {
      alert(response.error || 'Registration failed.');
    }
  };

  return (
    <div className="register">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <div>
          <input
            type="checkbox"
            checked={acceptedTerms}
            onChange={() => setAcceptedTerms(!acceptedTerms)}
          />
          <label>I accept the terms and conditions</label>
        </div>
        <button type="submit" className="btn">Register</button>
      </form>
    </div>
  );
};

export default Register;
