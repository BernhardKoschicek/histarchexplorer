var grid = new Muuri('.grid');

// To make the items draggable
// try this next...
// var grid = new Muuri('.grid', {dragEnabled: true});


window.onload = function () {
    setTimeout(() => {
        grid.refreshItems().layout();
    }, 500);
};


var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
