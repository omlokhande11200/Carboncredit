document.getElementById('inputForm').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send the form data to the Flask backend
    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams(data)
    })
    .then(response => response.json())  // Parse JSON response from the backend
    .then(data => {
        // If the backend returns a prediction, display it
        if (data.error) {
            document.getElementById('result').innerHTML = 'Error: ' + data.error;
        } else {
            document.getElementById('result').innerHTML = 'Predicted Carbon Credits: ' + data.prediction + ' credits';
        }
    })
    .catch(error => {
        // Catch and display errors if the fetch request fails
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred while submitting the form. Please try again.';
    });
});
