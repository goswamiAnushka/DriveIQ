const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// Function to send GPS data to backend
export const sendGPSDataToBackend = async (gpsData) => {
    const response = await fetch(`${API_BASE_URL}/api/record-telematics`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ gps_data: gpsData })
    });
    return response.json();
};

// Function to get user's driving history
export const getUserHistory = async () => {
    const response = await fetch(`${API_BASE_URL}/api/history/1`);
    return response.json();
};
