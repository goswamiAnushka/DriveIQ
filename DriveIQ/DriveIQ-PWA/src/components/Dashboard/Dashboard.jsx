import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'; // Import Marker and Popup
import 'leaflet/dist/leaflet.css'; // Ensure this is here
import L from 'leaflet'; // Import Leaflet to customize marker icons
import api from '../../utils/api';
import { smartGpsTracking, generateSimulatedRoute } from '../../utils/geolocation';
import BatchProcessing from '../BatchProcessing/BatchProcessing';
import './Dashboard.scss';

// Register Chart.js components
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Define custom marker icon
const customIcon = new L.Icon({
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  iconSize: [25, 41], // Size of the marker icon
  iconAnchor: [12, 41], // Position of the icon anchor relative to its size
  popupAnchor: [1, -34], // Position of the popup relative to the icon
});

const Dashboard = () => {
  const [gpsData, setGpsData] = useState([]);
  const [speedData, setSpeedData] = useState([]);
  const [accelerationData, setAccelerationData] = useState([]);
  const [jerkData, setJerkData] = useState([]);
  const [brakingData, setBrakingData] = useState([]);
  const [route, setRoute] = useState([]); // For route lines
  const [markers, setMarkers] = useState([]); // For markers/pins on the map
  const [isTracking, setIsTracking] = useState(false);
  const [error, setError] = useState(null);

  const toggleTracking = () => {
    if (isTracking) {
      setIsTracking(false);
    } else {
      setIsTracking(true);
      startTracking();
    }
  };

  const startTracking = () => {
    const simulatedBatches = generateSimulatedRoute(1, 5); // Generate 5 GPS batches
    simulatedBatches.forEach((batch, index) => {
      setTimeout(() => processBatch(batch), index * 5000); // Process each batch after 5 seconds
    });
  };

  const processBatch = async (batch) => {
    const isMoving = smartGpsTracking(batch.gps_data, gpsData);
    if (isMoving) {
      try {
        const driver_id = localStorage.getItem('driver_id');
        const response = await api.post('/record-telematics', {
          driver_id,
          gps_data: batch.gps_data, // Send GPS data for processing
        });

        console.log('Telematics Response:', response.data);

        const features = response.data.features;

        if (features) {
          const speed = features['Speed(m/s)'] ?? 0;
          const acceleration = features['Acceleration(m/s^2)'] ?? 0;
          const jerk = features['Jerk(m/s^3)'] ?? 0;
          const brakingIntensity = features['Braking_Intensity'] ?? 0;

          // Update data for each chart
          setSpeedData((prevData) => [...prevData, speed]);
          setAccelerationData((prevData) => [...prevData, acceleration]);
          setJerkData((prevData) => [...prevData, jerk]);
          setBrakingData((prevData) => [...prevData, brakingIntensity]);

          // Update GPS data and route points
          setGpsData((prevData) => [...prevData, ...batch.gps_data]);

          // Add only the last point of each batch as a marker
          const lastPoint = batch.gps_data[batch.gps_data.length - 1];
          setMarkers((prevMarkers) => [
            ...prevMarkers,
            { lat: lastPoint.Latitude, lng: lastPoint.Longitude },
          ]);

          // Update route for polyline
          setRoute((prevRoute) => [
            ...prevRoute,
            ...batch.gps_data.map((point) => [point.Latitude, point.Longitude]),
          ]);
        } else {
          console.error('Error: Features object is undefined or missing keys');
        }
      } catch (error) {
        console.error('Error recording telematics data:', error);
        setError('Error processing GPS data. Please try again.');
      }
    }
  };

  const renderChart = (label, data, borderColor) => {
    const chartLabels = data.map((_, index) => `Batch ${index + 1}`);
    return (
      <Line
        data={{
          labels: chartLabels,
          datasets: [
            {
              label: label,
              data: data,
              borderColor: borderColor,
              fill: false,
            },
          ],
        }}
      />
    );
  };

  return (
    <div className="dashboard-container">
      <h2>Driver Dashboard</h2>

      <div className="tracking-controls">
        <button onClick={toggleTracking}>
          {isTracking ? 'Stop Tracking' : 'Start Tracking'}
        </button>
      </div>

      {/* Map Section */}
      <div className="map-section">
        <h3>Route Map</h3>
        <MapContainer center={[26.6337, 92.7926]} zoom={13} scrollWheelZoom={false} className="map-container">
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          {/* Display the polyline for the route */}
          <Polyline positions={route} color="blue" />

          {/* Add only the last marker of each batch */}
          {markers.map((marker, idx) => (
            <Marker key={idx} position={[marker.lat, marker.lng]} icon={customIcon}>
              <Popup>
                Latitude: {marker.lat}, Longitude: {marker.lng}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Charts Section */}
      <div className="chart-section">
        <h3>Driving Feature Fluctuations</h3>
        <div className="chart-container">
          {/* Speed Chart */}
          {renderChart('Speed (m/s)', speedData, 'rgba(75, 192, 192, 1)')}

          {/* Acceleration Chart */}
          {renderChart('Acceleration (m/s²)', accelerationData, 'rgba(255, 99, 132, 1)')}

          {/* Jerk Chart */}
          {renderChart('Jerk (m/s³)', jerkData, 'rgba(54, 162, 235, 1)')}

          {/* Braking Intensity Chart */}
          {renderChart('Braking Intensity', brakingData, 'rgba(153, 102, 255, 1)')}
        </div>
      </div>

      {/* Batch Processing Section */}
      <BatchProcessing gpsData={gpsData} /> {/* Pass the GPS data to BatchProcessing */}

      {/* Error Message */}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default Dashboard;
