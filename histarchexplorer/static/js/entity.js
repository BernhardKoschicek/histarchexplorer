let loadedTabs = []

document.getElementById('toggleSidebar').addEventListener('click', function () {
    const nav_sidebar = document.getElementById('nav-sidebar');
    const root = document.documentElement;
    nav_sidebar.classList.toggle('expanded');
    nav_sidebar.classList.toggle('d-none');

    if (nav_sidebar.classList.contains('expanded')) {
        root.style.setProperty('--sidebar-width', '150px');
    } else {
        root.style.setProperty('--sidebar-width', '70px');
    }
});

let loadedCount = 0; // Track completed tab loads

async function loadHTML(id, tab, index, totalTabs) {
    const response = await fetch(`/getentity/${id}/${tab}`);

    if (response.status === 404) {
        console.error(`Error 404: Content for tab "${tab}" not found.`);

        document.querySelectorAll(`.to-remove-${tab}`).forEach(element => {
            element.remove();
            console.log(`Removed element with class "to-remove-${tab}".`);
        });

        loadedCount++; // Increase count even for missing tabs
        checkAndRemoveSpinner(totalTabs);
        return;
    }

    if (response.status !== 200) {
        console.error(`Unexpected response status: ${response.status}`);
        return;
    }

    document.querySelectorAll(`.to-remove-${tab}`).forEach(element => {
        element.classList.toggle('d-none');
        console.log(`Removed element with class "to-remove-${tab}".`);
    });

    const htmlText = await response.text();
    const targetElement = document.getElementById(`pane-content-${tab}`);

    if (!targetElement) {
        console.error("Target element not found!");
        return;
    }

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlText;

    const cssPromises = Array.from(tempDiv.querySelectorAll('link[rel="stylesheet"]')).map(link => {
        return new Promise(resolve => {
            if (!document.querySelector(`link[href="${link.href}"]`)) {
                const newLink = document.createElement('link');
                newLink.rel = 'stylesheet';
                newLink.href = link.href;
                newLink.onload = resolve;
                document.head.appendChild(newLink);
            } else {
                resolve(); // Already loaded
            }
        });
    });

    await Promise.all(cssPromises);

    targetElement.innerHTML = tempDiv.innerHTML;

    const scripts = Array.from(tempDiv.querySelectorAll('script'));
    for (const script of scripts) {
        await loadScript(script);
    }

    loadedTabs.push(tab);
    console.log(`HTML, CSS, and scripts for "${tab}" loaded in correct order!`);
    console.log(loadedTabs);

    loadedCount++; // Increase count when a tab is fully loaded
    checkAndRemoveSpinner(totalTabs);
}

// Function to check if all tabs are loaded and remove the spinner
function checkAndRemoveSpinner(totalTabs) {
    if (loadedCount >= totalTabs) {
        document.querySelectorAll(".to-remove-spinner").forEach(element => {
            element.remove();
            console.log("Spinner removed.");
        });
    }
}


// Load a script dynamically and wait for it to finish loading
function loadScript(script) {
    return new Promise(resolve => {
        const newScript = document.createElement('script');

        if (script.src) {
            newScript.src = script.src;
            newScript.onload = resolve;
        } else {
            newScript.textContent = script.textContent;
            resolve();
        }

        document.body.appendChild(newScript);
    });
}


tabsToLoad.forEach((tab, index) => {
    if (!loadedTabs.includes(tab)) {
        loadHTML(entityId, tab, index, tabsToLoad.length);
    }
});

document.addEventListener('DOMContentLoaded', function () {
  // Activate a tab by name, optionally skipping pushState (for popstate navigation)
  function activateTab(tabName, skipPushState = false) {
    const tabElement = document.querySelector(`#tab-${tabName}`);
    if (tabElement) {
      // Activate using Bootstrap's Tab API
      new bootstrap.Tab(tabElement).show();
      // Only update history if needed
      if (!skipPushState) {
        const newUrl = `/entity/${entityId}/${tabName}`;
        if (window.location.pathname !== newUrl) {
          history.pushState({ tab: tabName }, '', newUrl);
        }
      }
    }
  }

  // Extract the tab name from the current URL path.
  function getTabNameFromUrl() {
    const parts = window.location.pathname.split('/');
    return parts.length >= 4 ? parts[3] : 'overview';
  }

  // On page load: set initial state and activate the initial tab.
  const initialTab = getTabNameFromUrl();
  history.replaceState({ tab: initialTab }, '', window.location.pathname);
  activateTab(initialTab, true);

  // Listen for tab changes on any element with data-bs-toggle="tab"
  const tabElements = document.querySelectorAll('[data-bs-toggle="tab"]');
  tabElements.forEach(function (el) {
    el.addEventListener('shown.bs.tab', function (event) {
      const tabName = event.target.id.replace('tab-', '');
      // Only push state if we're really switching tabs.
      if (!history.state || history.state.tab !== tabName) {
        const newUrl = `/entity/${entityId}/${tabName}`;
        history.pushState({ tab: tabName }, '', newUrl);
      }
    });
  });

  // Listen for popstate (back/forward navigation)
  window.addEventListener('popstate', function (event) {
    if (event.state && event.state.tab) {
      activateTab(event.state.tab, true);
    } else {
      // Fallback: if no state, parse the URL.
      const tabName = getTabNameFromUrl();
      activateTab(tabName, true);
    }
  });
});
