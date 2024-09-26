import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Start Journey
export const startJourney = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/api/start-journey`, data);
    return response.data;
  } catch (error) {
    console.error('Start Journey Error:', error);
    return error.response ? error.response.data : { error: 'Failed to start the journey.' };
  }
};

// Record Telematics Data
export const recordTelematics = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/api/record-telematics`, data);
    return response.data;
  } catch (error) {
    console.error('Record Telematics Error:', error);
    return error.response ? error.response.data : { error: 'Failed to record telematics data.' };
  }
};

// Check if the driver is within a geofence area
export const checkGeoFence = async (locationData) => {
  try {
    const response = await axios.post(`${API_URL}/api/check-geofence`, locationData);
    return response.data;
  } catch (error) {
    console.error('GeoFence Error:', error);
    return error.response ? error.response.data : { error: 'Failed to check geofence.' };
  }
};

// Fetch leaderboard data for drivers
export const getLeaderboard = async () => {
  try {
    const response = await axios.get(`${API_URL}/admin/leaderboard`);
    return response.data;
  } catch (error) {
    console.error('Leaderboard Error:', error);
    return error.response ? error.response.data : { error: 'Failed to fetch leaderboard.' };
  }
};

// Login user
export const loginUser = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/api/login`, data);
    return response.data;
  } catch (error) {
    console.error('Login Error:', error);

    // Handle case where error response or data is not available
    return {
      success: false,
      error: error.response ? error.response.data.error : 'Login failed. Please try again.',
    };
  }
};

// Register user
export const registerUser = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/api/register`, data);
    return response.data;
  } catch (error) {
    console.error('Registration Error:', error);

    // Handle case where error response or data is not available
    return {
      success: false,
      error: error.response ? error.response.data.error : 'Registration failed. Please try again.',
    };
  }
};

// Fetch trip data for a specific trip
export const getTripData = async (tripId) => {
  try {
    const response = await axios.get(`${API_URL}/api/trip/${tripId}`);
    return response.data;
  } catch (error) {
    console.error('Trip Data Error:', error);
    return error.response ? error.response.data : { error: 'Failed to fetch trip data.' };
  }
};

// Get All Drivers
export const getAllDrivers = async () => {
  try {
    const response = await axios.get(`${API_URL}/admin/drivers`);
    return response.data;
  } catch (error) {
    console.error('All Drivers Error:', error);
    return error.response ? error.response.data : { error: 'Failed to fetch all drivers.' };
  }
};

// Get Aggregated Data for a Driver
export const getDriverAggregatedData = async (driverId) => {
  try {
    const response = await axios.get(`${API_URL}/admin/driver/${driverId}`);
    return response.data;
  } catch (error) {
    console.error('Aggregated Data Error:', error);
    return error.response ? error.response.data : { error: 'Failed to fetch aggregated data for the driver.' };
  }
};

// Generate Reports (Admin)
export const generateReport = async (driverId, format) => {
  try {
    const endpoint = format === 'pdf' ? 'pdf' : 'excel';
    const response = await axios.get(`${API_URL}/admin/report/${endpoint}/${driverId}`, { responseType: 'blob' });
    const file = new Blob([response.data], { type: format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const fileURL = URL.createObjectURL(file);
    window.open(fileURL);
  } catch (error) {
    console.error('Report generation error:', error);
  }
};
