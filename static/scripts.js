var map;
var geoJsonLayer;

window.onload = function() {
    initMap();
    onClicks();
    initialLoad();
}

function initMap() {
    map = L.map('map').setView([-28.153, 133.275], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    geoJsonLayer = L.geoJSON().addTo(map);
}

function onClicks() {
    document.getElementById('filter').addEventListener('submit', getData);
    for(let elem of document.getElementsByClassName('level-selector')){
        if(elem.id == 'levelAUS'){
            elem.addEventListener('click', disableStateSelectors);
        } else {
            elem.addEventListener('click', enableStateSelectors);
        }
    }
    document.getElementById('reset').addEventListener('click', () => map.setView([-28.153, 133.275], 5));
}

function initialLoad() {
    document.getElementById('filter').dispatchEvent(new Event('submit'));
}

function getData(event) {
    event.preventDefault();

    let submitButton = document.getElementById('submitButton');
    submitButton.value = 'Loading...';
    submitButton.setAttribute('disabled', true);

    let formEntries = [...new FormData(document.getElementById('filter')).entries()];
    let urlParams = formEntries.map(e => e[0] + '=' + e[1]).join('&');

    fetch(window.location.protocol + '//' + window.location.host + '/data?' + urlParams)
        .then(response => response.json())
        .then(data => {
            map.removeLayer(geoJsonLayer);
            geoJsonLayer = L.geoJSON(data, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.name);
                }
            }).addTo(map);
            document.getElementById('submitButton').value = 'Update';
        })
        .catch((err) => {
            document.getElementById('submitButton').value = 'Error';
            console.error(err);
        })
        .finally(() => {
            submitButton.removeAttribute('disabled');
        });
}

function enableStateSelectors(event) {
    for(let elem of document.getElementsByClassName('state-selector')) {
        elem.removeAttribute('disabled');
    }
}

function enableLevelSelectors(event) {
    for(let elem of document.getElementsByClassName('level-selector')) {
        elem.removeAttribute('disabled');
    }
}

function disableStateSelectors(event) {
    for(let elem of document.getElementsByClassName('state-selector')) {
        elem.setAttribute('disabled', true);
        elem.checked = false;
    }
}

function disableLevelSelectors(event) {
    for(let elem of document.getElementsByClassName('level-selector')) {
        elem.setAttribute('disabled', true);
    }
}