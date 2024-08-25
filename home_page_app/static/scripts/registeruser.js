function validateRegisterForm() {
    
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var firstName = document.getElementById('firstname').value; // Make sure you have this field
    var lastName = document.getElementById('lastname').value; // Make sure you have this field
    var driversLiscene = document.getElementById('license').value; // Make sure you have this field
    
    // Check if all fields are not empty
    if (email.trim() === '' || password.trim() === '' || firstName.trim() === '' || lastName.trim() === '' || driversLiscene.trim() === '') {
        alert('Please enter all required fields.');
        return false; // Prevent form submission
    }

    document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.detail.target.id === 'form-response-message') {
            // This code runs after the HTMX swap has occurred
            var responseData = JSON.parse(event.detail.target.innerText);
    
            // Check if registration was successful based on server response
            if (responseData.success) {
                // Display success message and make necessary DOM adjustments
                document.getElementById('fail-form-message').style.display = 'none';
                let successMessage = document.getElementById('success-form-message');
                successMessage.textContent = 'Registration successful!';
                successMessage.style.color = 'green';
                successMessage.style.display = 'block';
                document.getElementById('account-li').style.display = 'block';
                document.getElementById('login-li').style.display = 'none';
                document.getElementById('register-li').style.display = 'none';
    
                setTimeout(function() {
                    document.getElementById('modal').style.display = 'none';
                    successMessage.style.display = 'none';
                }, 2000);
            } else {
                let successMessage = document.getElementById('success-form-message');
                successMessage.style.display = 'none';
                let failMessage = document.getElementById('fail-form-message');
                failMessage.textContent = responseData.error || 'Registration failed!';
                failMessage.style.display = 'block';
            }
        }
    });

    return false; // Prevent the form from submitting traditionally
}
