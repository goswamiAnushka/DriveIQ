import React, { useState, useEffect } from 'react';
import { sendGPSDataToBackend } from '../../services/journeyService';
import './Journey.scss';

function Journey() {
    const [tracking, setTracking] = useState(false);
    const [gpsData, setGpsData] = useState([]);

    useEffect(() => {
        let trackingInterval;

        if (tracking) {
            trackingInterval = setInterval(() => {
                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            const newData = {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                timeStep: Date.now() // Timestamp
                            };
                            setGpsData((prevData) => [...prevData, newData]);

                            // Send the data to the backend periodically
                            sendGPSDataToBackend([newData])
                                .then((res) => {
                                    console.log("Backend response:", res);
                                })
                                .catch((err) => {
                                    console.error("Error sending GPS data:", err);
                                });
                        },
                        (error) => console.error("Error tracking position:", error),
                        { enableHighAccuracy: true }
                    );
                }
            }, 5000); // Every 5 seconds
        }

        return () => clearInterval(trackingInterval); // Cleanup interval
    }, [tracking]);

    return (
        <div className="journey-tracker">
            <h2>Journey Tracker</h2>
            <button
                className="start-btn"
                onClick={() => setTracking(true)}
                disabled={tracking}
            >
                Start Journey
            </button>
            <button
                className="stop-btn"
                onClick={() => setTracking(false)}
                disabled={!tracking}
            >
                Stop Journey
            </button>

            <div className="gps-data-list">
                {gpsData.map((data, index) => (
                    <p key={index}>
                        Lat: {data.latitude}, Long: {data.longitude}, Time: {new Date(data.timeStep).toLocaleTimeString()}
                    </p>
                ))}
            </div>
        </div>
    );
}

export default Journey;
