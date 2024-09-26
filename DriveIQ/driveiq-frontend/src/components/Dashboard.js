import React, { useState, useEffect } from 'react';
import { getDriverData, getNotifications, getBadges } from '../services/api';
import TripReplay from './TripReplay';
import Badges from './Badges';
import Notifications from './Notifications';
import '../styles/Dashboard.scss';

const Dashboard = ({ driverId }) => {
  const [driverData, setDriverData] = useState(null);
  const [tripHistory, setTripHistory] = useState([]);
  const [badges, setBadges] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Fetch driver data and trip history
    const fetchDriverData = async () => {
      const data = await getDriverData(driverId);
      setDriverData(data);
      setTripHistory(data.trips);
    };

    // Fetch notifications and badges
    const fetchExtras = async () => {
      const fetchedNotifications = await getNotifications(driverId);
      const fetchedBadges = await getBadges(driverId);
      setNotifications(fetchedNotifications);
      setBadges(fetchedBadges);
    };

    fetchDriverData();
    fetchExtras();
  }, [driverId]);

  return (
    <div className="dashboard-container">
      <h2>Driver Dashboard</h2>
      {driverData && (
        <div className="driver-stats">
          <p><strong>Driver Name:</strong> {driverData.name}</p>
          <p><strong>Total Trips:</strong> {driverData.total_trips}</p>
          <p><strong>Average Score:</strong> {driverData.average_score}</p>
        </div>
      )}

      <Badges badges={badges} />
      <Notifications notifications={notifications} />

      <div className="trip-history">
        <h3>Your Trip History</h3>
        {tripHistory.length > 0 ? (
          tripHistory.map((trip) => (
            <div key={trip.trip_id} className="trip-item">
              <p><strong>Trip ID:</strong> {trip.trip_id}</p>
              <p><strong>Score:</strong> {trip.score}</p>
              <p><strong>Category:</strong> {trip.category}</p>
              <TripReplay tripId={trip.trip_id} />
            </div>
          ))
        ) : (
          <p>No trips recorded yet.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
