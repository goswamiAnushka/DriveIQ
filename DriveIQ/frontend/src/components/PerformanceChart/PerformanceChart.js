import React from 'react';
import { Line } from 'react-chartjs-2';
import './PerformanceChart.scss';

// Helper function to convert timestamp into month
function getMonthFromTimeStep(timeStep) {
    const date = new Date(timeStep);
    return date.toLocaleString('default', { month: 'long', year: 'numeric' });
}

function PerformanceChart({ history }) {
    const months = [...new Set(history.map((trip) => getMonthFromTimeStep(trip.timeStep)))];
    const scores = history.map((trip) => trip.driving_score);

    const data = {
        labels: months,
        datasets: [
            {
                label: 'Driving Score Over Time',
                data: scores,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
        ]
    };

    return (
        <div className="performance-chart">
            <h3>Performance Over Time</h3>
            <Line data={data} />
        </div>
    );
}

export default PerformanceChart;
