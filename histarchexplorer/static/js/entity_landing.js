let grid = new Muuri('.grid');

// var grid = new Muuri('.grid', {dragEnabled: true});


window.onload = function () {
    setTimeout(() => {
        grid.refreshItems().layout();
    }, 300);
};

window.addEventListener('resize', () => {
    grid.refreshItems().layout();
});
