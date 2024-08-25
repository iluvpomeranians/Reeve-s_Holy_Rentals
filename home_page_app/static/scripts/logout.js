function logout() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is included for POST requests
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.logged_out) {
            document.getElementById('login-li').style.display = 'block';
            document.getElementById('register-li').style.display = 'block';
            document.getElementById('logout-button').style.display = 'none';
            document.getElementById('account-li').style.display = 'none';
            window.location.href = "/"; // Redirect to login page or homepage
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}