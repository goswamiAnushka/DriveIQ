const express = require('express');
const router = express.Router();
const { createDriverData, getDriverData } = require('../controllers/driverController');

router.post('/', createDriverData);
router.get('/', getDriverData);

module.exports = router;
