// Create and return a Google Map instance
var map = null;
var markerClusterer = null;

function initialize(langtitudes, longtitudes){
    var mapProp = {
                center: new google.maps.LatLng(51.508742,-0.120850),
                zoom: 5,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
    map = new google.maps.Map(document.getElementById("map-container"), mapProp);


    var markers = [];
    for (var i = 0; i < langtitudes.length; i++){
        var latLng = new google.maps.LatLng(langtitudes[i], longtitudes[i])
        var marker = new google.maps.Marker({
            position : latLng,
            draggable : true,
        });
        markers.push(marker)
    }
    // Create a marker clusterer
    markerClusterer = new MarkerClusterer(map, markers);
}

// Just for testing
function init_map(){
    google.maps.event.addDomListener(window, 'load', initialize);
}
