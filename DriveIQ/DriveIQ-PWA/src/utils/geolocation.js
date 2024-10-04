// src/utils/geolocation.js

export const getCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          const timestamp = Math.floor(Date.now() / 1000);
          resolve({ latitude, longitude, timestamp });
        },
        (error) => reject(error),
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    } else {
      reject(new Error('Geolocation not supported'));
    }
  });
};

// Simulates GPS data when testing on a laptop
export const simulateGpsData = () => [
  { Latitude: 26.6337, Longitude: 92.7926, Time_Step: 1 },
  { Latitude: 26.6347, Longitude: 92.7936, Time_Step: 60 },
  { Latitude: 26.6357, Longitude: 92.7946, Time_Step: 120 },
  { Latitude: 26.6367, Longitude: 92.7956, Time_Step: 180 },
];

// Smart logic for detecting vehicle movement or idle time
export const smartGpsTracking = (currentBatch, previousBatch) => {
  const SPEED_THRESHOLD = 2; // m/s (~7.2 km/h)

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3; // Earth radius in meters
    const toRad = (deg) => (deg * Math.PI) / 180;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in meters
  };

  const calculateSpeed = (distance, timeDiff) => distance / timeDiff;

  if (previousBatch.length > 0) {
    const lastPoint = previousBatch[previousBatch.length - 1];
    const firstPoint = currentBatch[0];
    const distance = calculateDistance(
      lastPoint.Latitude,
      lastPoint.Longitude,
      firstPoint.Latitude,
      firstPoint.Longitude
    );
    const timeDiff = firstPoint.Time_Step - lastPoint.Time_Step;

    if (calculateSpeed(distance, timeDiff) < SPEED_THRESHOLD) {
      console.log('Vehicle idle detected');
      return false;
    }
  }

  return true;
};

// Generate simulated routes for testing
export const generateSimulatedRoute = (driverId, batchSize) => {
  const gpsBatches = [];
  let lat = 26.6337;
  let lon = 92.7926;
  let timeStep = 0;

  for (let i = 0; i < batchSize; i++) {
    const batch = [];
    for (let j = 0; j < 10; j++) {
      lat += Math.random() * 0.001; // Simulated random movement
      lon += Math.random() * 0.001;
      timeStep += 60;
      batch.push({ Latitude: lat, Longitude: lon, Time_Step: timeStep });
    }
    gpsBatches.push({ driver_id: driverId, gps_data: batch });
  }

  return gpsBatches;
};
