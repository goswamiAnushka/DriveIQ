import React from 'react';
import Navbar from '../components/Navbar';
import Dashboard from '../components/Dashboard';

const HomePage = ({ drivingData }) => {
  return (
    <div>
      <Navbar />
      <h1>Welcome to DriveIQ</h1>
      <Dashboard drivingData={drivingData} />
    </div>
  );
};

export default HomePage;
