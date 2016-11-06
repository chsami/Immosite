/**
 * Created by Sami on 4/05/2016.
 */
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}

function showMaps() {
    if ($('#map').is(':hidden')) {
        $('#fotos').css('display', 'none');
        $('#streetview').css('display', 'none');
        $('#map').css('display', 'block');
        $('.left-container > h2').replaceWith("<h2>Map</h2>");
        initMap();
    }
}

function showPictures() {
    if ($('#fotos').is(':hidden')) {
        $('#streetview').css('display', 'none');
        $('#map').css('display', 'none');
        $('#fotos').css('display', 'block');
        $('.left-container > h2').replaceWith("<h2>Foto's</h2>");
    }
}

function showStreetView() {
    if ($('#streetview').is(':hidden')) {
        $('#fotos').css('display', 'none');
        $('#map').css('display', 'none');
        $('#streetview').css('display', 'block');
        $('.left-container > h2').replaceWith("<h2>Streetview</h2>");
    }
}