const API_URL = 'http://localhost:5000'; // Backend API URL

// Get driving history from backend
export const getDrivingHistory = async () => {
  const response = await fetch(`${API_URL}/history`);
  return await response.json();
};

// Send GPS data to backend
export const sendGpsData = async (gpsData) => {
  const response = await fetch(`${API_URL}/record-telematics`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ gps_data: gpsData }),
  });
  return await response.json();
};

// Start a new journey (optional)
export const startJourney = async () => {
  return await fetch(`${API_URL}/start-journey`, { method: 'POST' });
};

export default { getDrivingHistory, sendGpsData, startJourney };
