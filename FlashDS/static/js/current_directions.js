// Declare userLocImageUrl before using it
const userLocImageUrl = "/static/images/user-loc.png";

// Function to initialize the map
function initMap() {
    const mapElement = document.getElementById("map");
    if (!mapElement) {
        return;
    }

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();

    const map = new google.maps.Map(mapElement, {
        zoom: 7,
        center: { lat: 30.0444, lng: 31.2357 },
    });

    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer, map, userLocImageUrl);
}

// Function to calculate and display the route
function calculateAndDisplayRoute(directionsService, directionsRenderer, map, userLocImageUrl) {
    directionsService.route(
        {
            origin: new google.maps.LatLng(pickup_lat, pickup_lng),
            destination: new google.maps.LatLng(delivery_lat, delivery_lng),
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status === "OK") {
                directionsRenderer.setDirections(response);
                // Add marker for the delivery place
                const deliveryMarker = new google.maps.Marker({
                    position: new google.maps.LatLng(delivery_lat, delivery_lng),
                    map: map,
                    icon: {
                        url: userLocImageUrl,
                        scaledSize: new google.maps.Size(70, 70),
                    },
                });
                courierPosition(map);
            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );
}

// Function to add or update courier marker
function addCourierMarker(map, position) {
    // Check if courier is within 1km of delivery or pickup location
    const courierLocation = new google.maps.LatLng(position.lat, position.lng);
    const deliveryLocation = new google.maps.LatLng(delivery_lat, delivery_lng);
    const pickupLocation = new google.maps.LatLng(pickup_lat, pickup_lng);
    if (google.maps.geometry.spherical.computeDistanceBetween(courierLocation, deliveryLocation) < 1000 ||
        google.maps.geometry.spherical.computeDistanceBetween(courierLocation, pickupLocation) < 1000) {
        map.panTo(position);
    }
}

// Function to update courier position
function courierPosition(map) {
    navigator.permissions.query({ name: 'geolocation' })
        .then(permissionStatus => {
            if (permissionStatus.state === 'granted') {
                // Geolocation permission already granted
                startWatchingPosition(map);
            } else if (permissionStatus.state === 'prompt') {
                // Geolocation permission not granted yet, ask the user
                navigator.geolocation.getCurrentPosition(
                    pos => {
                        const courierCurrentPos = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
                        addCourierMarker(map, courierCurrentPos);
                    },
                    err => {
                        console.error('Error getting location:', err);
                    },
                    { enableHighAccuracy: true }
                );
            } else {
                // Geolocation permission denied
                console.error('Geolocation permission denied');
            }
        })
        .catch(err => {
            console.error('Error querying geolocation permission:', err);
        });
}

function startWatchingPosition(map) {
    navigator.geolocation.watchPosition(
        pos => {
            const courierCurrentPos = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
            addCourierMarker(map, courierCurrentPos);
        },
        err => {
            console.error('Error getting location:', err);
        },
        { enableHighAccuracy: true }
    );
}

// Call courierPosition and initMap when the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    const mapElement = document.getElementById("map");
    if (mapElement) {
        initMap();
    }
});
