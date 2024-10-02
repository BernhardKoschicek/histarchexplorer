var grid = new Muuri('.grid');

// var grid = new Muuri('.grid', {dragEnabled: true});


window.onload = function () {
    setTimeout(() => {
        grid.refreshItems().layout();
    }, 500);
};


var map = L.map('muuri-map', {
    center: [51.505, -0.09],
    zoom: 13,
    zoomControl: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    touchZoom: false,
    boxZoom: false
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
