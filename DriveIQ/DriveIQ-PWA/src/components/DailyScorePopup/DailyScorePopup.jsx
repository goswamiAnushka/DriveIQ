// src/components/DailyScorePopup/DailyScorePopup.jsx
import React from 'react';
import './DailyScorePopup.scss';

const DailyScorePopup = ({ data, onClose }) => {
  const { total_distance_covered_km, driving_score, driving_category } = data;

  return (
    <div className="daily-score-popup">
      <div className="popup-content">
        <h2>Daily Driving Summary</h2>
        <p><strong>Total Distance:</strong> {total_distance_covered_km} km</p>
        <p><strong>Driving Score:</strong> {driving_score}</p>
        <p><strong>Driving Category:</strong> {driving_category}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default DailyScorePopup;
