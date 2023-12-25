
// Function to handle touchstart event
function handleTouchStart(event) {
    // Your touchstart event handling logic goes here
    console.log('Touchstart event detected!');
    console.log('Event details:', event);
}

// Function to initialize the map
function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: { lat: 41.85, lng: -87.65 },
    });

    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}

// Function to calculate and display the route
function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    directionsService.route(
        {
            origin: new google.maps.LatLng(pickup_lat, pickup_lng),
            destination: new google.maps.LatLng(delivery_lat, delivery_lng),
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status === "OK") {
                directionsRenderer.setDirections(response);
            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );
}

document.addEventListener('touchstart', handleTouchStart, { passive: true });

// Call initMap when the page is loaded
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});
