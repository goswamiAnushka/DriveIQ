import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { startJourney, recordTelematics } from '../services/api';

const socket = io('http://localhost:5000');

const UserJourney = ({ driverId }) => {
  const [tripId, setTripId] = useState(null);
  const [gpsData, setGpsData] = useState([]);

  useEffect(() => {
    const startUserJourney = async () => {
      const response = await startJourney({ driver_id: driverId });
      if (response.trip_id) {
        setTripId(response.trip_id);
      }
    };

    startUserJourney();

    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        const data = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          timestamp: position.timestamp,
        };

        // Record GPS data
        recordTelematics({
          gps_data: [data],
          driver_id: driverId,
          trip_id: tripId,
        });

        // Emit GPS data via socket
        socket.emit('gps_update', data);

        setGpsData((prevData) => [...prevData, data]);
      },
      (error) => console.error(error),
      { enableHighAccuracy: true, maximumAge: 30000, timeout: 27000 }
    );

    return () => navigator.geolocation.clearWatch(watchId);
  }, [driverId, tripId]);

  return (
    <div>
      <h2>Real-time GPS Tracking</h2>
      <div>
        {gpsData.map((data, index) => (
          <p key={index}>
            Lat: {data.latitude}, Long: {data.longitude}, Time: {new Date(data.timestamp).toLocaleTimeString()}
          </p>
        ))}
      </div>
    </div>
  );
};

export default UserJourney;
