const mongoose = require('mongoose');

const DriverSchema = new mongoose.Schema({
  tripId: { type: String, required: true },
  timeStamp: { type: Date, required: true },
  speed: { type: Number, required: true },
  acceleration: { type: Number, required: true },
  headingChange: { type: Number, required: true },
  latitude: { type: Number, required: true },
  longitude: { type: Number, required: true },
  drivingBehavior: { type: String, required: true }, // Aggressive, Average, Cautious, Moderate
  behaviorLabel: { type: Number, required: true }   // Corresponding numeric label
});

module.exports = mongoose.model('Driver', DriverSchema);
