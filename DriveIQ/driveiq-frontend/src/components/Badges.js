import React from 'react';
import '../styles/Badges.scss';

const Badges = ({ badges }) => {
  return (
    <div className="badges-container">
      <h2>Your Badges</h2>
      <div className="badge-list">
        {badges.length > 0 ? (
          badges.map((badge, index) => (
            <div key={index} className="badge-item">
              <img src={badge.icon} alt={badge.name} />
              <p>{badge.name}</p>
            </div>
          ))
        ) : (
          <p>No badges earned yet!</p>
        )}
      </div>
    </div>
  );
};

export default Badges;
