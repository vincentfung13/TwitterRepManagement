var map = null;
var markerClusterer = null;

function initialize(langtitudes, longitudes){
    var mapProp = {
        center: new google.maps.LatLng(0, 0),
        zoom: 2,
        minZoom: 2,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    };
    map = new google.maps.Map(document.getElementById("map-container"), mapProp);


    var markers = [];
    for (var i = 0; i < langtitudes.length; i++){
        var latLng = new google.maps.LatLng(langtitudes[i], longitudes[i])
        var marker = new google.maps.Marker({
            position : latLng,
        });
        markers.push(marker)
    }
    // Create a marker clusterer
    markerClusterer = new MarkerClusterer(map, markers);
}

function init_map(lats, longs){
    google.maps.event.addDomListener(window, 'load', initialize(lats, longs));
}