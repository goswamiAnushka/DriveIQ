import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import api from '../../utils/api';
import { smartGpsTracking, generateSimulatedRoute } from '../../utils/geolocation';
import BatchProcessing from '../BatchProcessing/BatchProcessing';
import './Dashboard.scss';

import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Define custom marker icon
const customIcon = new L.Icon({
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const Dashboard = () => {
  const [gpsData, setGpsData] = useState([]);
  const [speedData, setSpeedData] = useState([]);
  const [accelerationData, setAccelerationData] = useState([]);
  const [jerkData, setJerkData] = useState([]);
  const [brakingData, setBrakingData] = useState([]);
  const [route, setRoute] = useState([]);
  const [markers, setMarkers] = useState([]);
  const [isTracking, setIsTracking] = useState(false);
  const [error, setError] = useState(null);
  const [dailyData, setDailyData] = useState(null); // New state for daily data

  // Function to clean NaN values for display
  const cleanValue = (value) => (isNaN(value) ? 'N/A' : value);

  // Check if the daily data is updated and log it to debug rendering
  useEffect(() => {
    if (dailyData) {
      console.log('Rendering Daily Data: ', dailyData);
    }
  }, [dailyData]);

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
      setTimeout(() => {
        processBatch(batch).then(() => {
          if (index === simulatedBatches.length - 1) {
            processDailyData();  // Call processDailyData after the last batch
          }
        });
      }, index * 5000); // Process each batch after 5 seconds
    });
  };

  const processBatch = async (batch) => {
    const isMoving = smartGpsTracking(batch.gps_data, gpsData);
    if (isMoving) {
      try {
        const driver_id = localStorage.getItem('driver_id');
        const response = await api.post('/record-telematics', {
          driver_id,
          gps_data: batch.gps_data,
        });

        const features = response.data.features;
        if (features) {
          const speed = features['Speed(m/s)'] ?? 0;
          const acceleration = features['Acceleration(m/s^2)'] ?? 0;
          const jerk = features['Jerk(m/s^3)'] ?? 0;
          const brakingIntensity = features['Braking_Intensity'] ?? 0;

          setSpeedData((prevData) => [...prevData, speed]);
          setAccelerationData((prevData) => [...prevData, acceleration]);
          setJerkData((prevData) => [...prevData, jerk]);
          setBrakingData((prevData) => [...prevData, brakingIntensity]);

          setGpsData((prevData) => [...prevData, ...batch.gps_data]);

          const lastPoint = batch.gps_data[batch.gps_data.length - 1];
          setMarkers((prevMarkers) => [
            ...prevMarkers,
            { lat: lastPoint.Latitude, lng: lastPoint.Longitude },
          ]);

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

  const processDailyData = async () => {
    try {
      const driver_id = localStorage.getItem('driver_id');
      const response = await api.post('/process-daily-data', { driver_id });

      console.log('Daily Data Response:', response.data);
      setDailyData(response.data);  // Store daily data in the state
    } catch (error) {
      console.error('Error processing daily data:', error);
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

      {/* Add a button to manually call processDailyData */}
      <div className="manual-process-controls">
        <button onClick={processDailyData}>Process Daily Data</button>
      </div>

      {/* Map Section */}
      <div className="map-section">
        <h3>Route Map</h3>
        <MapContainer center={[26.6337, 92.7926]} zoom={13} scrollWheelZoom={false} className="map-container">
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          <Polyline positions={route} color="blue" />

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
          {renderChart('Speed (m/s)', speedData, 'rgba(75, 192, 192, 1)')}
          {renderChart('Acceleration (m/s²)', accelerationData, 'rgba(255, 99, 132, 1)')}
          {renderChart('Jerk (m/s³)', jerkData, 'rgba(54, 162, 235, 1)')}
          {renderChart('Braking Intensity', brakingData, 'rgba(153, 102, 255, 1)')}
        </div>
      </div>

      {/* Display Daily Data */}
      {dailyData ? (
        dailyData.aggregated_data ? (
          <div className="daily-data-section">
            <h3>Daily Driving Performance</h3>
            <p>Driving Score: {dailyData.driving_score}</p>
            <p>Driving Category: {dailyData.driving_category}</p>
            <p>Total Trips: {dailyData.total_trips}</p>
            <p>Total Distance Covered: {dailyData.total_distance_covered_km} km</p>
            <div className="aggregated-data">
              <p>Average Speed: {cleanValue(dailyData.aggregated_data['Speed(m/s)'])} m/s</p>
              <p>Average Acceleration: {cleanValue(dailyData.aggregated_data['Acceleration(m/s^2)'])} m/s²</p>
              <p>Average Jerk: {cleanValue(dailyData.aggregated_data['Jerk(m/s^3)'])} m/s³</p>
              <p>Average Braking Intensity: {cleanValue(dailyData.aggregated_data['Braking_Intensity'])}</p>
            </div>
          </div>
        ) : (
          <p>Aggregated data is missing.</p>
        )
      ) : (
        <p>No daily data available yet.</p>
      )}

      {/* Batch Processing Section */}
      <BatchProcessing gpsData={gpsData} />

      {/* Error Message */}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default Dashboard;
