window.mediaGrid = null;

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.grid-media');
    if (!container) return;

     window.mediaGrid.refreshItems().layout();

    setTimeout(() => {
        window.mediaGrid.refreshItems().layout();
    }, 700);
});

window.mediaGrid = new Muuri('.grid-media', {
    layout: {
        fillGaps: true,
    }
});


