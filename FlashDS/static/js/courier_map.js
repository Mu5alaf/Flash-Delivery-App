// Function to initialize the map
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 9,
        center: { lat: 30.0444, lng: 31.2357 },
    });

    //gating the available tasks from api
    fetch(availableTaskApiUrl)
        .then(response => response.json())
        .then(json => {
            
            var viewPoint = new google.maps.LatLngBounds();

            for (let i = 0; i < json.tasks.length; i++) {
                const task = json.tasks[i];
                const position = { lat: task.pickup_lat, lng: task.pickup_lng };
                const marker = new google.maps.Marker({
                    position: position,
                    map: map
                });

                viewPoint.extend(position);

                new google.maps.InfoWindow({
                    content: "<small><b>" + task.name + "</b></small><br/><small>" + task.distance + "km</small>"
                }).open(map, marker);


                function showDiv() {
                    document.getElementById('task-details').style.display = "block";
                }

                marker.addListener("click", () => {
                    showTaskdetails(task);
                });

                map.fitBounds(viewPoint);
            }
        })
}

function showTaskdetails(task) {
    $("#task-details").css("display", "block");
    $("#task-name").html(task.name);
    $("#task-picture").attr('src', "/FlashMedia/" + task.picture);
    $("#duration").html(task.duration);
    $("#distance").html(task.distance);
    $("#pickup_address").html(task.pickup_address);
    $("#delivery_address").html(task.delivery_address);
    $("#price").html(task.price);
    $("#task-details").on("click", function(){
        window.location.href="/courier/task/available/" + task.id +"/";
    })
}