import React, { useEffect, useState } from 'react';
import { getLeaderboard } from '../services/api';
import '../styles/Leaderboard.scss';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const response = await getLeaderboard();
      setLeaderboard(response);
    };

    fetchLeaderboard();
  }, []);

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <ul>
        {leaderboard.map((driver, index) => (
          <li key={index}>
            {driver.name} - Average Score: {driver.average_score}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;
