function addVehicle() {
    const vehicleNumber = document.getElementById('vehicleNumber').value;
    const closingKM = document.getElementById('closingKM').value;

    fetch('/api/add_vehicle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vehicle_number: vehicleNumber,
            closing_km: closingKM,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('addResult').innerText = data.message || data.error || 'Unknown error occurred.';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('addResult').innerText = 'Failed to add vehicle.';
    });
}

function deleteVehicle() {
    const vehicleNumber = document.getElementById('deleteVehicleNumber').value;

    fetch(`/api/delete_vehicle/${vehicleNumber}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('deleteResult').innerText = data.message || data.error || 'Unknown error occurred.';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('deleteResult').innerText = 'Failed to delete vehicle.';
    });
}
