// src/static/js/main.js
function startTracking() {
    // Gather input data
    const avg_speed = document.getElementById('avg_speed').value;
    const max_acceleration = document.getElementById('max_acceleration').value;
    const total_heading_change = document.getElementById('total_heading_change').value;

    // Create data object
    const data = {
        avg_speed: parseFloat(avg_speed),
        max_acceleration: parseFloat(max_acceleration),
        total_heading_change: parseFloat(total_heading_change)
    };

    // Make a POST request to the /predict endpoint
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            document.getElementById('result').innerHTML = 'Predicted Behavior: ' + result.predicted_behavior;
        } else {
            document.getElementById('result').innerHTML = 'Error: ' + result.message;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = 'Error: ' + error.message;
    });
}
