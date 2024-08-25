// Set map center to Montreal, Quebec
if (document.getElementById('mapid')) {
    var map = L.map('mapid').setView([45.5017, -73.5673], 11); // Montreal's coordinates

    let customIcon1 = {
    iconUrl:"media/geolocateMapimgs/pin.png",
    iconSize:[40,40]
    }
    let user_pin = L.icon(customIcon1);
    let user_pin_options = {
        title: "You are here!",
        icon: user_pin
    }

    let customIcon2 = {
    iconUrl:"media/geolocateMapimgs/green_pin.png",
    iconSize:[25,41]
    }
    let closest_branch_pin = L.icon(customIcon2);
    let closest_branch_pin_options = {
        title: "closest branch",
        icon: closest_branch_pin
    }


    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    //Hochelaga Map Maker. randomly generated address. 
    var hochelagaMarker = L.marker([45.5447, -73.5449]).addTo(map)
        .bindPopup('<b style="font-size:15px; text-align:center;">Reeves Holy Rentals \'Chlag</b><br>123 Rue Ontario E, Montreal, QC H2X 1H4<br><img src="/media/geolocateMapimgs/Hochelaga.png" style="width:50%; display:block; margin-left:auto; margin-right:auto;">')
        .on('click', function() {
            localStorage.setItem('selectedLocation', 'Hochelaga');
            window.location.href = '/browse';
        });
    hochelagaMarker.on('mouseover', function() {
        this.openPopup();
    });
    hochelagaMarker.on('mouseout', function() {
        this.closePopup();
    });
  
    //Downtown map marker
    var downtownMarker = L.marker([45.4987, -73.5627]).addTo(map)
        .bindPopup('<b style="font-size:15px; text-align:center;">Reeves Holy Rentals Downtown</b><br>789 Rue Sainte-Catherine O, Montreal, QC H3B 0H2<br><img src="/media/geolocateMapimgs/Downtown.png" style="width:50%; display:block; margin-left:auto; margin-right:auto;">')
        .on('click', function() {
            localStorage.setItem('selectedLocation', 'Downtown');
            window.location.href = '/browse/';
        });
    downtownMarker.on('mouseover', function() {
        this.openPopup();
    });
    downtownMarker.on('mouseout', function() {
        this.closePopup();
    });

    //Verdun map marker
    var verdunMarker = L.marker([45.4574, -73.5697]).addTo(map)
        .bindPopup('<b style="font-size:15px; text-align:center;">Reeves Holy Rentals Verdun</b><br>4568 Rue Wellington, Verdun, QC H4G 1X1<br><img src="/media/geolocateMapimgs/Verdun.png" style="width:50%; display:block; margin-left:auto; margin-right:auto;">')
        .on('click', function() {
            localStorage.setItem('selectedLocation', 'Verdun');
            window.location.href = '/browse';
        });
    verdunMarker.on('mouseover', function() {
        this.openPopup();
    });
    verdunMarker.on('mouseout', function() {
        this.closePopup();
    });   

    //Outremont map marker
    var outremontMarker = L.marker([45.5202, -73.6092]).addTo(map)
        .bindPopup('<b style="font-size:15px; text-align:center;">Reeves Holy Rentals Outremont</b><br>302 Avenue Laurier O, Outremont, QC H2V 2K1<br><img src="/media/geolocateMapimgs/outremont.png" style="width:50%; display:block; margin-left:auto; margin-right:auto;">')
        .on('click', function() {
            localStorage.setItem('selectedLocation', 'Outremont');
            window.location.href = '/browse';
        });
    outremontMarker.on('mouseover', function() {
        this.openPopup();
    });
    outremontMarker.on('mouseout', function() {
        this.closePopup();
    });

    // Define markerGroup to store markers
    var markerGroup = L.layerGroup();

    var branches = [
        { name: 'Reeves Holy Rentals Hochelaga', latlng: [45.5447, -73.5449], address: '123 Rue Ontario E, Montreal, QC H2X 1H4', image: '<img src="/media/geolocateMapimgs/Hochelaga.png" style = "width:50%; display:block; margin-left:auto; margin-right:auto;">' },
        { name: 'Reeves Holy Rentals Downtown', latlng: [45.4987, -73.5627], address: '789 Rue Sainte-Catherine O, Montreal, QC H3B 0H2',image: '<img src="/media/geolocateMapimgs/Downtown.png" style = "width:50%; display:block; margin-left:auto; margin-right:auto;">' },
        { name: 'Reeves Holy Rentals Verdun', latlng: [45.4574, -73.5697], address: '4568 Rue Wellington, Verdun, QC H4G 1X1',image: '<img src="/media/geolocateMapimgs/Verdun.png" style = "width:50%; display:block; margin-left:auto; margin-right:auto;">' },
        { name: 'Reeves Holy Rentals Outremont', latlng: [45.5202, -73.6092], address: '302 Avenue Laurier O, Outremont, QC H2V 2K1',image: '<img src="/media/geolocateMapimgs/Outremont.png" style = "width:50%; display:block; margin-left:auto; margin-right:auto;">' }
    ];

    //Popping up nearest branch to postal code input on search submit
    document.getElementById('postal-code-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var postalCode = document.getElementById('postalCode').value;

        // Use OpenCage Geocoding API to geocode the postal code
        fetch('https://api.opencagedata.com/geocode/v1/json?q=' + postalCode + '&key=245c7324ddf948189841a703509d93cd')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data && data.results && data.results.length > 0) {
                // Get the coordinates of the first result
                var latlng = [parseFloat(data.results[0].geometry.lat), parseFloat(data.results[0].geometry.lng)];

                // Find the nearest branch
                var nearestBranch = branches.reduce(function(prev, curr) {
                    var prevDistance = map.distance(latlng, prev.latlng);
                    var currDistance = map.distance(latlng, curr.latlng);
                    return prevDistance < currDistance ? prev : curr;
                });

                // Zoom to the nearest branch
                map.setView(nearestBranch.latlng, 14);
            } else {
                alert('Postal code not found.');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            alert('An error occurred while processing the postal code.');
        });

    });
    // Add the user's marker to the map
    var located = false;
    document.getElementById('geolocate').addEventListener('click', function(event) {
        event.preventDefault();
        function success(pos){

            const user_lat_lang =[pos.coords.latitude,pos.coords.longitude]

            var nearestBranch_user = branches.reduce(function(prev, curr) {
                    var prevDistance = map.distance(user_lat_lang, prev.latlng);
                    var currDistance = map.distance(user_lat_lang, curr.latlng);
                    return prevDistance < currDistance ? prev : curr;
                });

            if (!located){
                L.marker(user_lat_lang, user_pin_options).addTo(map);
                located = true;

                map.setView(user_lat_lang, 14);

                setTimeout(() => {
                map.setView(user_lat_lang, 12); // Changes the zoom level to 12 after 1000 milliseconds (1 second)
                }, 1000);

                setTimeout(() => {
                map.setView(nearestBranch_user.latlng, 14); // Changes the view to the nearest branch with a zoom level of 14 after another 1000 milliseconds
                }, 2000); // Note the time is now 2000 milliseconds to ensure this runs after the first timeout
            }else{
                map.setView(user_lat_lang, 12);
            }


        }
        function error(err){
            if (err.code === 1){
                alert('Location access denied. Please allow location access to use this feature.');
            } else {
                alert('posotion unavailable');
            }
        }

        const options = {};

        window.navigator.geolocation.getCurrentPosition(success, error, options);



    });
    // Search by airport
    var airportDropdown = document.getElementById('airport-dropdown');

    // Define the airports 
    var airports = [
        { name: 'Montreal-Pierre Elliott Trudeau International Airport', latlng: [45.4577, -73.7497] },
        { name: 'Montreal-Mirabel International Airport', latlng: [45.6755, -74.0384] },
        { name: 'Montreal Metropolitan Airport', latlng: [45.5230, -73.4044] },
        { name: 'Aeroport Saint-Mathieu de laprairie', latlng: [45.3238, -73.5582] },
        // Add more airports as needed
    ];
    // Populate the dropdown menu with airports
    var airportDropdown = document.getElementById('airport-dropdown');
    airports.forEach(function(airport) {
        var option = document.createElement('option');
        option.value = airport.name;
        option.text = airport.name;
        airportDropdown.appendChild(option);
    });

    // Add an event listener to the dropdown menu
    airportDropdown.addEventListener('change', function() {
        var selectedAirport = airportDropdown.value;

        // Find the selected airport
        var airport = airports.find(function(airport) {
            return airport.name === selectedAirport;
        });

        if (airport) {
            // Find the nearest branch to the selected airport
            var nearestBranch = branches.reduce(function(prev, curr) {
                var prevDistance = map.distance(airport.latlng, prev.latlng);
                var currDistance = map.distance(airport.latlng, curr.latlng);
                return prevDistance < currDistance ? prev : curr;
            });

            // Clear previous markers
            markerGroup.clearLayers();

            // Add marker for the nearest branch
            L.marker(nearestBranch.latlng).addTo(markerGroup)
                .bindPopup('<b>' + nearestBranch.name + '</b><br>' + nearestBranch.address + '</br><br>' + nearestBranch.image)
                .openPopup();

            // Zoom to the nearest branch
            map.setView(nearestBranch.latlng, 14);
        } else {
            alert('Please select an airport.');
        }
    });

}


