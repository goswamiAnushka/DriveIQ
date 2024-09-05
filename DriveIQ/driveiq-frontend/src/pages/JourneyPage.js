import React, { useState } from 'react';
import { startJourney } from '../services/api';

const JourneyPage = () => {
  const [journeyStarted, setJourneyStarted] = useState(false);

  const handleStartJourney = async () => {
    const gpsData = await startJourney();
    console.log(gpsData); // You can process the GPS data or send it to the backend
    setJourneyStarted(true);
  };

  return (
    <div>
      <h1>Start Your Journey</h1>
      <button onClick={handleStartJourney}>Start Journey</button>
      {journeyStarted && <p>Journey is in progress...</p>}
    </div>
  );
};

export default JourneyPage;
