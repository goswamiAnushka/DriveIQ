import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './TelematicsMap.scss';

function TelematicsMap({ gpsData }) {
    const [position, setPosition] = useState([51.505, -0.09]); // Default position (London)

    useEffect(() => {
        if (gpsData.length > 0) {
            const latestPosition = [
                gpsData[gpsData.length - 1].latitude,
                gpsData[gpsData.length - 1].longitude
            ];
            setPosition(latestPosition);
        }
    }, [gpsData]);

    return (
        <div className="telematics-map">
            <h3>Journey Map</h3>
            <MapContainer center={position} zoom={13} scrollWheelZoom={false} style={{ height: '400px', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {gpsData.length > 0 && (
                    <>
                        <Marker position={position}></Marker>
                        <Polyline positions={gpsData.map((data) => [data.latitude, data.longitude])} />
                    </>
                )}
            </MapContainer>
        </div>
    );
}

export default TelematicsMap;
