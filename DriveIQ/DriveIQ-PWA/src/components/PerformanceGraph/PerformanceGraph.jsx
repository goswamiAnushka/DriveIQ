import React, { useEffect, useRef } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import 'chart.js/auto'; // Ensure auto-import for Chart.js components

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PerformanceGraph = ({ gpsData }) => {
  const chartRef = useRef(null);
  let chartInstance = null;

  const renderChart = () => {
    const ctx = chartRef.current.getContext('2d');

    if (chartInstance !== null) {
      chartInstance.destroy();  // Destroy previous chart instance
    }

    // Prepare labels and data for speed and acceleration
    const labels = gpsData.map((_, index) => `T-${index + 1}`);
    const speedData = gpsData.map(data => data.Speed || 0);  // Extract speed
    const accelerationData = gpsData.map(data => data.Acceleration || 0);  // Extract acceleration

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Speed (m/s)',
            data: speedData,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
          },
          {
            label: 'Acceleration (m/s^2)',
            data: accelerationData,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            fill: false,
          },
        ],
      },
      options: {
        scales: {
          x: {
            type: 'category',
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  };

  useEffect(() => {
    renderChart();
    return () => {
      if (chartInstance) chartInstance.destroy();  // Cleanup on component unmount
    };
  }, [gpsData]);  // Re-render the chart when gpsData changes

  return (
    <div className="performance-graph" style={{ height: '400px', width: '100%' }}> {/* Set height for visibility */}
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default PerformanceGraph;
