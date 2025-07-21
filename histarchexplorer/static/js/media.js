const mediaGrid = new Muuri('.grid-media', {
    layout: {
        fillGaps: true,
    },
});

mediaGrid.layout();

let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        mediaGrid.refreshItems().layout();
    }, 300);
});