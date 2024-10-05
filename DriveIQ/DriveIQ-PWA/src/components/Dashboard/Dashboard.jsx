import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2'; // Import Bar for distribution chart
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import api from '../../utils/api';
import { smartGpsTracking, generateSimulatedRoute } from '../../utils/geolocation';
import BatchProcessing from '../BatchProcessing/BatchProcessing';
import './Dashboard.scss';

import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

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

  // Render the distribution graph for daily features
  const renderDistributionGraph = () => {
    if (!dailyData || !dailyData.aggregated_data) return null;

    const labels = ['Speed(m/s)', 'Acceleration(m/s^2)', 'Jerk(m/s^3)', 'Braking Intensity'];
    const data = [
      cleanValue(dailyData.aggregated_data['Speed(m/s)']),
      cleanValue(dailyData.aggregated_data['Acceleration(m/s^2)']),
      cleanValue(dailyData.aggregated_data['Jerk(m/s^3)']),
      cleanValue(dailyData.aggregated_data['Braking_Intensity'])
    ];

    const chartData = {
      labels,
      datasets: [
        {
          label: 'Daily Feature Distribution',
          backgroundColor: ['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(75, 192, 192, 0.8)', 'rgba(153, 102, 255, 0.8)'],
          borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
          borderWidth: 2,
          hoverBackgroundColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
          hoverBorderColor: '#fff',
          hoverBorderWidth: 3,
          data: data,
          barThickness: 50,  // Adjust bar thickness
        }
      ]
    };

    return (
      <div className="distribution-chart-container">
        <Bar
          data={chartData}
          options={{
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)',
                },
                ticks: {
                  color: '#34495e',
                },
              },
              x: {
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)',
                },
                ticks: {
                  color: '#34495e',
                },
              },
            },
            plugins: {
              legend: {
                labels: {
                  color: '#34495e',
                  font: {
                    size: 14,
                    family: 'Poppins',
                  },
                },
              },
              tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                  family: 'Poppins',
                  size: 14,
                },
                bodyFont: {
                  family: 'Poppins',
                  size: 12,
                },
                displayColors: false,
              },
            },
          }}
        />
      </div>
    );
  };

  const renderChart = (label, data, borderColor, gradientColor) => {
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
              backgroundColor: gradientColor,  // Gradient background
              pointBackgroundColor: '#fff',  // White point dots for contrast
              pointRadius: 5,  // Larger point size for visibility
              borderWidth: 3,  // Thicker lines for more visibility
              fill: true,  // Enable fill under the line
              tension: 0.4,  // Smooth line curves
            },
          ],
        }}
        options={{
          responsive: true,
          animation: {
            duration: 2000,  // Smooth 2-second load animation
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(255, 255, 255, 0.1)',  // Lighter grid lines
              },
              ticks: {
                color: '#34495e',  // Darker text for labels
              },
            },
            y: {
              grid: {
                color: 'rgba(255, 255, 255, 0.1)',  // Lighter grid lines
              },
              ticks: {
                color: '#34495e',  // Darker text for labels
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                color: '#34495e',  // Darker legend labels
                font: {
                  size: 14,
                  family: 'Poppins',
                },
              },
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',  // Dark tooltip background
              titleFont: {
                family: 'Poppins',
                size: 14,
              },
              bodyFont: {
                family: 'Poppins',
                size: 12,
              },
              displayColors: false,  // Hide color boxes in tooltip
            },
          },
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
          {renderChart('Speed (m/s)', speedData, 'rgba(75, 192, 192, 1)', 'rgba(0, 255, 255, 0.2)')}
          {renderChart('Acceleration (m/s²)', accelerationData, 'rgba(255, 165, 0, 1)', 'rgba(255, 165, 0, 0.2)')}
          {renderChart('Jerk (m/s³)', jerkData, 'rgba(75, 192, 192, 1)', 'rgba(75, 192, 192, 0.2)')}
          {renderChart('Braking Intensity', brakingData, 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)')}
        </div>
      </div>

      {/* Distribution Graph for daily data */}
      {renderDistributionGraph()}

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
