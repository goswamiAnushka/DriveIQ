// src/components/BatchProcessing/BatchProcessing.jsx
import React, { useEffect, useState } from 'react';
import api from '../../utils/api';

const BatchProcessing = ({ gpsData }) => {
  const [processedData, setProcessedData] = useState(null);

  useEffect(() => {
    if (gpsData.length > 0) {
      processBatch(gpsData);
    }
  }, [gpsData]);

  const processBatch = async (batch) => {
    try {
      const driver_id = localStorage.getItem('driver_id');
      const response = await api.post('/record-telematics', { driver_id, gps_data: batch });
      setProcessedData(response.data);
    } catch (error) {
      console.error('Error processing batch:', error);
    }
  };

  return (
    <div className="batch-processing-container">
      <h3>Batch Processing</h3>
      {processedData ? (
        <div>
          <p>Processed batch data successfully!</p>
          <pre>{JSON.stringify(processedData, null, 2)}</pre>
        </div>
      ) : (
        <p>No batch processed yet.</p>
      )}
    </div>
  );
};

export default BatchProcessing;
