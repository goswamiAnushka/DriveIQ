import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './MapView.scss';

// Custom red icon for the markers
const redIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x-red.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  shadowSize: [41, 41],
  shadowAnchor: [12, 41]
});

// Custom blue icon for route markers
const blueIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  shadowSize: [41, 41],
  shadowAnchor: [12, 41]
});

const MapView = ({ gpsData }) => {
  // Default coordinates to use when gpsData is empty
  const defaultCoords = [26.6338, 92.8006];  // Coordinates for Tezpur, India
  
  // Map GPS data into an array of [latitude, longitude]
  const route = gpsData.length ? gpsData.map(point => [point.Latitude, point.Longitude]) : [defaultCoords];

  // Set starting point and ending point for markers
  const startPoint = route[0];
  const endPoint = route[route.length - 1];

  return (
    <div className="map-view" style={{ height: '500px', width: '100%' }}>
      <MapContainer center={startPoint} zoom={14} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Draw the route as a polyline */}
        {route.length > 1 && (
          <Polyline
            positions={route}
            color="blue"
            weight={4}
            opacity={0.7}
            smoothFactor={1.5}
          />
        )}

        {/* Add a marker at the start point */}
        {startPoint && <Marker position={startPoint} icon={redIcon} />}

        {/* Add a marker at the end point */}
        {endPoint && startPoint !== endPoint && <Marker position={endPoint} icon={redIcon} />}

        {/* Optional: Add markers at key points along the route (only every 5th point for readability) */}
        {route.map((point, index) => (
          index % 5 === 0 && <Marker key={index} position={point} icon={blueIcon} />
        ))}
      </MapContainer>
    </div>
  );
};

export default MapView;
