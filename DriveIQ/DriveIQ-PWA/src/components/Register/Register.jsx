import React, { useState } from 'react';
import api from '../../utils/api'; // Import the centralized Axios instance
import { useNavigate } from 'react-router-dom';
import './Register.scss';

const Register = () => {
  const navigate = useNavigate(); // React Router hook to navigate between pages
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    acceptedTerms: false,
  });

  const [identityProof, setIdentityProof] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file.size > 5000000) {
      alert('File size should be less than 5MB');
    } else if (!['image/png', 'image/jpg', 'image/jpeg', 'image/gif'].includes(file.type)) {
      alert('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.');
    } else {
      setIdentityProof(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.acceptedTerms) {
      alert('You must accept the terms and conditions.');
      return;
    }

    const formPayload = new FormData();
    formPayload.append('name', formData.name);
    formPayload.append('email', formData.email);
    formPayload.append('password', formData.password);
    formPayload.append('accepted_terms', formData.acceptedTerms);
    formPayload.append('identity_proof', identityProof);

    try {
      setIsSubmitting(true);
      const response = await api.post('/register', formPayload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.status === 201) {
        alert('Registration successful! Redirecting to login.');
        navigate('/login'); // Correctly navigate to login after registration
      }
    } catch (error) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Register for DriveIQ Telematics</h2>
      {error && <p className="error-message">{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Enter your name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
        <label htmlFor="identity_proof">Upload Identity Proof</label>
        <input
          type="file"
          name="identity_proof"
          accept=".png, .jpg, .jpeg, .gif"
          onChange={handleFileChange}
          required
        />

        <div className="terms-conditions">
          <label>
            <input
              type="checkbox"
              name="acceptedTerms"
              checked={formData.acceptedTerms}
              onChange={(e) => setFormData({ ...formData, acceptedTerms: e.target.checked })}
              required
            />
            I accept the{' '}
            <a href="/terms">terms and conditions</a> of DriveIQ, including GPS tracking for telematics insurance.
          </label>
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Registering...' : 'Register'}
        </button>
      </form>

      <div className="chatbot-icon">
        <a href="/chatbot">Need help? Chat with us!</a>
      </div>

      <div className="no-account">
        <p>Already have an account?</p>
        <a href="/login">Login here</a>
      </div>
    </div>
  );
};

export default Register;
