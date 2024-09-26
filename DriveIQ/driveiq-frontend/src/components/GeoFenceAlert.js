import React, { useEffect, useState } from 'react';
import { checkGeoFence } from '../services/api';
import '../styles/GeoFenceAlert.scss';

const GeoFenceAlert = ({ locationData }) => {
  const [geoFenceAlert, setGeoFenceAlert] = useState('');

  useEffect(() => {
    const fetchGeoFenceData = async () => {
      const response = await checkGeoFence(locationData);
      if (response.inGeofence) {
        setGeoFenceAlert('You are in a geofenced area. Please drive carefully!');
      } else {
        setGeoFenceAlert('');
      }
    };

    fetchGeoFenceData();
  }, [locationData]);

  return geoFenceAlert ? (
    <div className="geofence-alert">
      <p>{geoFenceAlert}</p>
    </div>
  ) : null;
};

export default GeoFenceAlert;
