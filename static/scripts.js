var map;
var geoJsonLayer;
var colours = {}

window.onload = function() {
    initMap();
    onClicks();
    // initialLoad();
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
    document.getElementById('reset').addEventListener('click', (event) => {
        event.preventDefault();
        map.setView([-28.153, 133.275], 5);
    });
}

function initialLoad() {
    document.getElementById('filter').dispatchEvent(new Event('submit'));
}

function getStyle(feature) {
    let colour = colours.hasOwnProperty(feature.properties.code) ?
        `rgb(${colours[feature.properties.code].colour.map((channel) => channel * 255.0).slice(0, 3).join(',')})` :
        '#3388ff'
    let opacity = colours.hasOwnProperty(feature.properties.code) ? colours[feature.properties.code].norm : 0.2
    return {
        color: colour,
        fillColor: colour,
        weight: 0.8,
        opacity: 1,
        fillOpacity: opacity * 0.8 + 0.2
    }
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
            console.log(data)
            colours = data.colours;
            map.removeLayer(geoJsonLayer);
            geoJsonLayer = L.geoJSON(JSON.parse(data.data), {
                onEachFeature: function (feature, layer) {
                    if(feature.properties.targetStatistic !== undefined){
                        layer.bindPopup(`${feature.properties.name} - ${feature.properties.targetStatistic}`)
                    } else {
                        layer.bindPopup(feature.properties.name);
                    }
                },
                style: getStyle,
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