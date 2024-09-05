import React, { useEffect, useState } from 'react';
import { getDrivingHistory } from '../services/api';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const data = await getDrivingHistory();
      setHistory(data);
    };

    fetchHistory();
  }, []);

  return (
    <div>
      <h1>Journey History</h1>
      <ul>
        {history.map((journey, index) => (
          <li key={index}>
            <p>Journey Date: {journey.date}</p>
            <p>Score: {journey.score}</p>
            <p>Category: {journey.category}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPage;
