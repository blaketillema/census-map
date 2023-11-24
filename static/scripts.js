var map;
var geoJsonLayer;

window.onload = function() {
    initMap();
    document.getElementById('filter').addEventListener('submit', getData);
}

function initMap() {
    map = L.map('map').setView([-28.153, 133.275], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    geoJsonLayer = L.geoJSON().addTo(map);
}

function getData(event) {
    event.preventDefault();
    e = event;
    let formEntries = [...new FormData(document.getElementById('filter')).entries()];
    let urlParams = formEntries.map(e => e[0] + '=' + e[1]).join('&');
    fetch(window.location.href + '/data?' + urlParams)
    .then(response => response.json())
    .then(data => {
        map.removeLayer(geoJsonLayer);
        geoJsonLayer = L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.name);
            }
        }).addTo(map);
    });
}