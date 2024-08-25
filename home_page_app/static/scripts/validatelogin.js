function validateLoginForm() {

    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    // Check if both fields are not empty
    if (email.trim() === '' || password.trim() === '') {
        alert('Please enter both email and password.');
        return false; // Prevent form submission
    }

    
    document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.target.id === 'response-message') {
        // assuming the server returns JSON response inside the 'response-message' div
        var response = event.target.textContent;
        try {
            var responseData = JSON.parse(response);
            if (responseData.exists) {
                if (responseData.correctPassword) {

                    let failMessage = document.getElementById('fail-message');
                    failMessage.style.display = 'none';
                    let successMessage = document.getElementById('success-message'); 
                        successMessage.textContent = 'Login successful!';
                        successMessage.style.color = 'green';
                        successMessage.style.display = 'block';
                        document.getElementById('account-li').style.display = ''; 
                        document.getElementById('login-li').style.display = 'none'; 
                        document.getElementById('register-li').style.display = 'none'; 
                    
                        setTimeout(function() {   
                            document.getElementById('modal').style.display = 'none';
                            successMessage.style.display = 'none'; 
                        }, 2000);

                    console.log('Password is correct');
                    
                    if(responseData.csrfToken)
                    {
                        console.log('CSRF token found in response data');
                        updateCSRFToken(responseData.csrfToken);
                    }
                    else
                    {
                        console.log('No CSRF token found in response data');
                    }

                } else {
                    let successMessage = document.getElementById('success-message');
                    successMessage.style.display = 'none';
                    let failMessage = document.getElementById('fail-message');
                        failMessage.style.display = '';
                        failMessage.textContent = 'Incorrect login credentials!';
                        failMessage.style.color = 'red';
                        failMessage.style.display = 'block';
                        console.log('Incorrect password');
                }
            } else {
                let successMessage = document.getElementById('success-message');
                successMessage.style.display = 'none';
                let dneMessage = document.getElementById('fail-message');
                    dneMessage.style.display = ''; 
                    dneMessage.textContent = 'User does not exist!';
                    dneMessage.style.color = 'red';
                    dneMessage.style.display = 'block';
                    console.log('User does not exist');
            }
        } catch (error) {
            console.error('Error parsing response data: ', error);
        }
        }
    });

      

    return true;
}

function updateCSRFToken(newToken) {

    // Update CSRF token in hidden input fields within forms
    document.querySelectorAll('input[name="csrfmiddlewaretoken"]').forEach(input => {
        input.value = newToken;
    });

    // If using a meta tag to store the CSRF token for AJAX requests, update it too
    const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
    if (csrfMetaTag) {
        csrfMetaTag.setAttribute('content', newToken);
    }

    // Update the global headers for HTMX requests with the new CSRF token
    // This assumes you have a global way to set headers for HTMX and that HTMX is used in your project
    document.body.setAttribute('hx-headers', JSON.stringify({'X-CSRFToken': newToken}));

    console.log('CSRF token updated.');

}

