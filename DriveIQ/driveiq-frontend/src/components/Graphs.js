import React from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';

const Graphs = ({ drivingData }) => {
  const lineData = {
    labels: drivingData.map(d => d.date),
    datasets: [{
      label: 'Driving Scores Over Time',
      data: drivingData.map(d => d.score),
      borderColor: 'rgba(75, 192, 192, 1)',
      fill: false,
    }]
  };

  const pieData = {
    labels: ['Safe', 'Moderate', 'Aggressive'],
    datasets: [{
      data: [
        drivingData.filter(d => d.category === 'Safe').length,
        drivingData.filter(d => d.category === 'Moderate').length,
        drivingData.filter(d => d.category === 'Aggressive').length
      ],
      backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384']
    }]
  };

  const barData = {
    labels: drivingData.map(d => d.date),
    datasets: [
      {
        label: 'Average Speed (m/s)',
        data: drivingData.map(d => d.speed),
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
      },
      {
        label: 'Average Acceleration (m/s^2)',
        data: drivingData.map(d => d.acceleration),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      }
    ]
  };

  return (
    <div className="graphs-container">
      <div className="graph">
        <h3>Driving Scores Over Time</h3>
        <Line data={lineData} />
      </div>
      <div className="graph">
        <h3>Driving Behavior Distribution</h3>
        <Pie data={pieData} />
      </div>
      <div className="graph">
        <h3>Average Speed & Acceleration Over Time</h3>
        <Bar data={barData} />
      </div>
    </div>
  );
};

export default Graphs;
