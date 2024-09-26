import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import { getTripData } from '../services/api';
import '../styles/TripReplay.scss';

const TripReplay = ({ tripId }) => {
  const [tripData, setTripData] = useState([]);

  useEffect(() => {
    const fetchTripData = async () => {
      const response = await getTripData(tripId);
      setTripData(response.gps_data || []);
    };

    fetchTripData();
  }, [tripId]);

  return (
    <div className="trip-replay-container">
      <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '400px', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {tripData.map((point, index) => (
          <Marker
            key={index}
            position={[point.latitude, point.longitude]}
          />
        ))}
      </MapContainer>
    </div>
  );
};

export default TripReplay;
