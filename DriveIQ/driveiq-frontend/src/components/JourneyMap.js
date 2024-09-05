import React from 'react';
import { Map, TileLayer, Marker } from 'react-leaflet';

const JourneyMap = ({ gpsData }) => {
    const position = [gpsData[0].Latitude, gpsData[0].Longitude]; // Start position
    
    return (
        <Map center={position} zoom={13} style={{ height: "400px", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {gpsData.map((point, index) => (
                <Marker key={index} position={[point.Latitude, point.Longitude]} />
            ))}
        </Map>
    );
};

export default JourneyMap;
