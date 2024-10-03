import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.scss';
import Navbar from '../Navbar/Navbar'; // Import Navbar
import PerformanceGraph from '../PerformanceGraph/PerformanceGraph'; // Import Performance Graph

const HomePage = () => {
  return (
    <div className="homepage">
      <Navbar />

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to DriveIQ</h1>
          <p>Drive smarter, drive safer. Track your driving performance and get rewarded with discounts on your insurance.</p>
          <Link to="/register" className="cta-button">Get Started</Link>
        </div>
        <div className="hero-image">
          <img src="/assets/hero-image.png" alt="Telematics Driving" />
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>Why Choose DriveIQ?</h2>
        <div className="features-container">
          <div className="feature">
            <i className="fas fa-chart-line"></i>
            <h3>Real-Time Driving Insights</h3>
            <p>Monitor your driving performance and get real-time insights on how you can improve your driving score.</p>
          </div>
          <div className="feature">
            <i className="fas fa-car"></i>
            <h3>Accurate GPS Tracking</h3>
            <p>Track your trips with precise GPS data and get feedback on your routes and driving habits.</p>
          </div>
          <div className="feature">
            <i className="fas fa-shield-alt"></i>
            <h3>Insurance Discounts</h3>
            <p>Good drivers deserve rewards. The better your score, the more you save on your insurance premiums.</p>
          </div>
        </div>
      </section>

      {/* Performance Graph */}
      <section className="performance-overview">
        <h2>Track Your Performance</h2>
        <PerformanceGraph />
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 DriveIQ. All rights reserved.</p>
          <nav className="footer-nav">
            <Link to="/terms">Terms of Service</Link>
            <Link to="/privacy">Privacy Policy</Link>
          </nav>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
