const map = new maplibregl.Map({
    container: 'mymap',
    center: [8.94738, 45.97812], // starting position [lng, lat]
    style: 'https://api.maptiler.com/maps/topo-v2/style.json?key=E7Jrgaazm79UlTuEI5f5',
    zoom: 14, // starting zoom
    pitch: 70,
    hash: false,
    bearing: -100.86,
    maxPitch: 85,
    maxZoom: 25,
});

map.on('load', () => {
    // Add terrain source


    map.addSource('terrainSource', {
        type: 'raster-dem',
        url: 'https://api.maptiler.com/tiles/terrain-rgb-v2/tiles.json?key=E7Jrgaazm79UlTuEI5f5',
        tileSize: 256
    });

    // Add hillshade source
    map.addSource('hillshadeSource', {
        type: 'raster-dem',
        url: 'https://api.maptiler.com/tiles/terrain-rgb-v2/tiles.json?key=E7Jrgaazm79UlTuEI5f5',
        tileSize: 256
    });

    // Add hillshade layer
    map.addLayer({
        id: 'hills',
        type: 'hillshade',
        source: 'hillshadeSource',
        layout: {visibility: 'visible'},
        paint: {'hillshade-shadow-color': 'rgba(71,59,36,0.56)'}
    });

    // Set terrain
    map.setTerrain({
        source: 'terrainSource',
        exaggeration: 1
    });


    // Add navigation control
    map.addControl(
        new maplibregl.NavigationControl({
            visualizePitch: true,
            showZoom: true,
            showCompass: true
        })
    );

    // Add terrain control
    map.addControl(
        new maplibregl.TerrainControl({
            source: 'terrainSource',
            exaggeration: 1
        })
    );

    map.setSky({
        "sky-color": "#b2ddfa",
        "horizon-color": "#FFFFFF",
        "fog-color": "#FFFFFF",
        "fog-ground-blend": 0.8,
        "horizon-fog-blend": 0.1,
        "sky-horizon-blend": 0.6,
        "atmosphere-blend": 0.5,
    })

    map.addSource('geojson-data', {
        type: 'geojson',
        data: mapData
    });

    // Add polygon layer
    map.addLayer({
        id: 'polygon-layer',
        type: 'fill',
        source: 'geojson-data',
        paint: {
            'fill-color': '#088',
            'fill-opacity': 0.5
        },
        filter: ['==', ['get', 'shapeType'], 'shape']
    });

    // Add point layer
    map.addLayer({
        id: 'point-layer',
        type: 'circle',
        source: 'geojson-data',
        paint: {
            'circle-radius': 6,
            'circle-color': '#f00'
        },
        filter: ['==', ['get', 'shapeType'], 'centerpoint']
    });

    // Add popups on click
    map.on('click', 'point-layer', (e) => {
        new maplibregl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(`<strong>${e.features[0].properties.title}</strong>`)
            .addTo(map);
    });
})
;
