import React, { useEffect, useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import api from '../services/api';

const Dashboard = () => {
    const [drivingData, setDrivingData] = useState(null);

    useEffect(() => {
        const fetchDrivingData = async () => {
            const response = await api.getDrivingHistory(); // Fetch from the backend
            setDrivingData(response.data);
        };
        fetchDrivingData();
    }, []);

    if (!drivingData) {
        return <p>Loading...</p>;
    }

    // Example bar chart data (Driving behavior distribution)
    const behaviorData = {
        labels: ['Safe', 'Moderate', 'Aggressive'],
        datasets: [{
            label: 'Driving Behavior',
            data: [drivingData.safeCount, drivingData.moderateCount, drivingData.aggressiveCount],
            backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
        }],
    };

    // Example line chart data (Driving score over time)
    const scoreData = {
        labels: drivingData.journeys.map(journey => journey.date),
        datasets: [{
            label: 'Driving Score',
            data: drivingData.journeys.map(journey => journey.score),
            fill: false,
            borderColor: '#4caf50',
        }],
    };

    // Example pie chart data (Time spent in each category)
    const timeData = {
        labels: ['Safe', 'Moderate', 'Aggressive'],
        datasets: [{
            label: 'Time Spent',
            data: [drivingData.safeTime, drivingData.moderateTime, drivingData.aggressiveTime],
            backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
        }],
    };

    return (
        <div className="dashboard-container">
            <h2>Driving Dashboard</h2>

            <div className="chart">
                <h3>Driving Behavior Distribution</h3>
                <Bar data={behaviorData} />
            </div>

            <div className="chart">
                <h3>Driving Score Over Time</h3>
                <Line data={scoreData} />
            </div>

            <div className="chart">
                <h3>Time Spent in Each Driving Category</h3>
                <Pie data={timeData} />
            </div>
        </div>
    );
};

export default Dashboard;
