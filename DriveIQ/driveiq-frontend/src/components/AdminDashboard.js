import React, { useState, useEffect } from 'react';
import { getAllDrivers, generateReport, getDriverAggregatedData } from '../services/api';
import Leaderboard from './Leaderboard';
import io from 'socket.io-client'; // Import Socket.IO client
import '../styles/AdminDashboard.scss';

const socket = io('http://localhost:5000/admin'); // Connect to admin namespace on the backend

const AdminDashboard = () => {
  const [drivers, setDrivers] = useState([]);
  const [selectedDriver, setSelectedDriver] = useState(null);
  const [aggregatedData, setAggregatedData] = useState(null);

  useEffect(() => {
    const fetchDrivers = async () => {
      const driverList = await getAllDrivers();
      setDrivers(driverList);
    };
    fetchDrivers();
  }, []);

  // Listen for real-time updates for the selected driver
  useEffect(() => {
    if (selectedDriver) {
      socket.emit('monitor_driver', { driverId: selectedDriver });

      socket.on('driver_data_update', (data) => {
        console.log('Real-time Driver Data:', data);
      });

      return () => {
        socket.off('driver_data_update');
      };
    }
  }, [selectedDriver]);

  const handleSelectDriver = async (driverId) => {
    setSelectedDriver(driverId);
    const data = await getDriverAggregatedData(driverId);
    setAggregatedData(data);
  };

  const handleGenerateReport = async (driverId, format) => {
    await generateReport(driverId, format);
    alert(`Report generated in ${format} format!`);
  };

  return (
    <div className="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <div className="driver-list">
        <h3>Select a Driver to Monitor</h3>
        <ul>
          {drivers.length > 0 ? (
            drivers.map((driver) => (
              <li key={driver.id}>
                <button onClick={() => handleSelectDriver(driver.id)}>
                  {driver.name}
                </button>
              </li>
            ))
          ) : (
            <p>No drivers available.</p>
          )}
        </ul>
      </div>

      {selectedDriver && aggregatedData && (
        <div className="aggregated-data">
          <h3>Aggregated Data for Driver {selectedDriver}</h3>
          <p><strong>Total Trips:</strong> {aggregatedData.total_trips}</p>
          <p><strong>Average Score:</strong> {aggregatedData.average_score}</p>
          <p><strong>Risk Level:</strong> {aggregatedData.risk_level}</p>

          <div className="report-buttons">
            <button onClick={() => handleGenerateReport(selectedDriver, 'pdf')}>Generate PDF Report</button>
            <button onClick={() => handleGenerateReport(selectedDriver, 'excel')}>Generate Excel Report</button>
          </div>
        </div>
      )}

      <Leaderboard />
    </div>
  );
};

export default AdminDashboard;
