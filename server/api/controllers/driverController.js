const Driver = require('../models/Driver');

// @desc Create new driver data
// @route POST /api/drivers
exports.createDriverData = async (req, res) => {
  const { tripId, timeStamp, speed, acceleration, headingChange, latitude, longitude } = req.body;
  // Perform model prediction and classification logic here
  
  // Dummy logic for classification
  let drivingBehavior = 'Safe';
  let behaviorLabel = 0;
  
  // Your actual model prediction code should replace the dummy logic above

  const driverData = new Driver({
    tripId,
    timeStamp,
    speed,
    acceleration,
    headingChange,
    latitude,
    longitude,
    drivingBehavior,
    behaviorLabel
  });

  try {
    await driverData.save();
    res.status(201).json(driverData);
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error });
  }
};

// @desc Get all driver data
// @route GET /api/drivers
exports.getDriverData = async (req, res) => {
  try {
    const drivers = await Driver.find();
    res.status(200).json(drivers);
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error });
  }
};
