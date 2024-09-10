import React, { useState, useEffect } from 'react';
import { getUserHistory } from '../../services/journeyService';
import PerformanceChart from '../PerformanceChart/PerformanceChart';
import './Dashboard.scss';

function Dashboard() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        getUserHistory()
            .then((data) => setHistory(data))
            .catch((err) => console.error(err));
    }, []);

    return (
        <div className="dashboard">
            <h2>User Dashboard</h2>
            {history.length > 0 ? (
                <>
                    {history.map((trip, index) => (
                        <div className="trip-item" key={index}>
                            <p>Trip ID: {trip.trip_id}</p>
                            <p>Score: {trip.driving_score}</p>
                            <p>Category: {trip.category}</p>
                        </div>
                    ))}
                    {/* Add a performance chart for monthly visualization */}
                    <PerformanceChart history={history} />
                </>
            ) : (
                <p>No trip history available</p>
            )}
        </div>
    );
}

export default Dashboard;
