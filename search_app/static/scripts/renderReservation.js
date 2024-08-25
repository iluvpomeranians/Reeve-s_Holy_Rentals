function renderReservation(make, model, year, color, rental_price) {
    const url = document.getElementById('render-reservation-url').value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Get CSRF token
        },
        body: JSON.stringify({
            make: make,
            model: model,
            year: year,
            color: color,
            rental_price: rental_price
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data if needed
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
