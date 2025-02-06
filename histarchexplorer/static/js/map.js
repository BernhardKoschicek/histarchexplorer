 maptilersdk.config.apiKey = 'E7Jrgaazm79UlTuEI5f5';

const map = new maptilersdk.Map({
    container: 'mymap', // container id
    style: "dataviz",
    center: [8.94738, 45.97812], // starting position [lng, lat]
    zoom: 14, // starting zoom
    terrain: true,
    terrainControl: true,
    pitch: 70,
    bearing: -100.86,
    maxPitch: 85,
    maxZoom: 25
  });

map.on('load', () => {
    map.addSource('hillshade', {
        type: 'raster',
        tiles: [
            'https://api.maptiler.com/tiles/hillshades/{z}/{x}/{y}.png?key=E7Jrgaazm79UlTuEI5f5'
        ],
        tileSize: 256,
        maxzoom: 15
    });

    map.addLayer({
        id: 'hillshade-layer',
        type: 'raster',
        source: 'hillshade',
        layout: {},
        paint: {
            'raster-opacity': 0.5 // Adjust transparency (0 = invisible, 1 = full)
        }
    });
});

