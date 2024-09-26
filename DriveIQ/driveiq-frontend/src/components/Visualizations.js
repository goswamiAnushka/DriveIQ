import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { getPreviousTrips } from '../services/api';
import '../styles/Visualizations.scss';

const Visualizations = () => {
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    const fetchTrips = async () => {
      const trips = await getPreviousTrips();
      const labels = trips.map(trip => trip.trip_id);
      const scores = trips.map(trip => trip.score);

      setChartData({
        labels,
        datasets: [
          {
            label: 'Driving Score',
            data: scores,
            fill: false,
            borderColor: '#1976d2',
          },
        ],
      });
    };

    fetchTrips();
  }, []);

  return (
    <div className="visualizations">
      <h3>Trip Performance</h3>
      <Line data={chartData} />
    </div>
  );
};

export default Visualizations;
