function initMapByType(type, initLat, initLng) {
    const map = new google.maps.Map(document.getElementById(type + "-map"), {
        center: { lat: initLat || 26.8206, lng: initLng || 30.8025 },
        zoom: 15,
        mapTypeControl: false,
    });

    const card = document.getElementById("card-body");
    const input = document.getElementById("id_" + type + "_address");
    const infowindowContent = document.getElementById(type + "-infowindow-content");

    map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);

    const autocomplete = new google.maps.places.Autocomplete(input, {
        fields: ["formatted_address", "geometry", "name", "icon"],
        strictBounds: false,
    });

    autocomplete.bindTo("bounds", map);

    const infowindow = new google.maps.InfoWindow();
    infowindow.setContent(infowindowContent);

    const marker = new google.maps.Marker({
        map,
        anchorPoint: new google.maps.Point(0, -29),
    });

    autocomplete.addListener("place_changed", () => {
        infowindow.close();
        marker.setVisible(false);

        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        $("#" + type + "_lat").val(place.geometry.location.lat());
        $("#" + type + "_lng").val(place.geometry.location.lng());

        marker.setPosition(place.geometry.location);
        marker.setVisible(true);
        infowindowContent.children[type + "-place-name"].textContent = place.name;
        infowindowContent.children[type + "-place-icon"].src = place.icon;
        infowindowContent.children[type + "-place-address"].textContent = place.formatted_address;
        infowindow.open(map, marker);
    });

    if (initLat && initLng) {
        new google.maps.Marker({
            position: new google.maps.LatLng(initLat, initLng),
            map: map,
        });
    }
}

function initMap() {
    initMapByType('pickup', pickup_latitude, pickup_longitude);
    initMapByType('delivery', delivery_latitude, delivery_longitude);
}

window.initMap = initMap;
