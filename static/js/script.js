document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const form = document.querySelector('#prediction-form');
    
    // Get the prediction display element
    const predictionDisplay = document.querySelector('#prediction-display');
    
    // Add event listener for form submission
    form.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Create FormData object
        const formData = new FormData(form);
        
        // Show loading state
        predictionDisplay.textContent = 'Calculating...';
        
        // Send POST request to the server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                // If response is not ok, get the error message
                return response.text().then(text => {
                    throw new Error(text);
                });
            }
            return response.text();
        })
        .then(result => {
            // Display the prediction result
            predictionDisplay.textContent = `₹${result}`;
        })
        .catch(error => {
            // Display the error message
            predictionDisplay.textContent = error.message;
        });
    });
    
    // Handle company selection change
    const companySelect = document.querySelector('#company');
    const carModelSelect = document.querySelector('#car_models');
    
    companySelect.addEventListener('change', function() {
        const selectedCompany = companySelect.value;
        
        // Filter car models based on selected company
        if (selectedCompany !== 'Select Company') {
            // You may need to adjust this based on your data structure
            // This is a placeholder for the filtering logic
            updateCarModels(selectedCompany);
        }
    });
    
    // Function to update car models based on selected company
    function updateCarModels(company) {
        // This is a placeholder function
        // You would typically make an AJAX request to get models for the selected company
        // Or filter from a pre-loaded list
        
        // For demonstration purposes:
        fetch(`/get_models?company=${company}`)
            .then(response => response.json())
            .then(models => {
                // Clear current options
                carModelSelect.innerHTML = '';
                
                // Add new options
                models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    carModelSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching car models:', error);
            });
    }
});