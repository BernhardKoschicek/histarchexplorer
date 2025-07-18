let grid = new Muuri('.grid-muuri', {
    layout: {
        fillGaps: true,
    }
});

// var grid = new Muuri('.grid', {dragEnabled: true});


window.onload = function () {
    setTimeout(() => {
        grid.refreshItems().layout();
    }, 500);
};

let resizeTimeout;

window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    grid.refreshItems().layout();
  }, 300);
});



const observer = new MutationObserver(() => {
  const copyBtn = document.getElementById('copyCitationBtn');
  const citationText = document.getElementById('citationText');

  if (copyBtn && citationText) {
    copyBtn.addEventListener('click', () => {
      const text = citationText.innerText.trim();

      navigator.clipboard.writeText(text)
        .then(() => {
          // Change button text
          copyBtn.innerHTML = '<i class="bi bi-check-circle"></i> Citation copied!';

          // Change button class
          copyBtn.classList.remove('btn-primary');
          copyBtn.classList.add('btn-info');

          // Optional: Revert after 2 seconds
          setTimeout(() => {
            copyBtn.innerHTML = '<i class="bi bi-copy"></i> Copy Citation';
            copyBtn.classList.remove('btn-info');
            copyBtn.classList.add('btn-primary');
          }, 2000);
        })
        .catch(err => {
          console.error('Clipboard copy failed:', err);
        });
    });

    observer.disconnect(); // Stop observing once hooked
  }
});

observer.observe(document.body, { childList: true, subtree: true });
