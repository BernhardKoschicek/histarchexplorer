function toggleFields(form, enabled) {
    // Select all input, textarea, and select elements within the form that are not hidden or part of button actions
    const fields = form.querySelectorAll('input:not([type="hidden"]), textarea');

    fields.forEach(field => {
        if (enabled) {
            // Store the original value before enabling for potential cancellation
            field.dataset.originalValue = field.value;
            field.removeAttribute('disabled');
            // Re-add required attribute if it was originally present (based on your HTML/config)
            if (field.hasAttribute('data-required-field')) { // Assuming you add this data attribute in Jinja for required fields
                field.setAttribute('required', 'required');
            }
        } else {
            // Restore original value and disable the field
            field.value = field.dataset.originalValue;
            field.setAttribute('disabled', 'disabled');
            // Remove required attribute when disabled to prevent client-side validation issues on disabled fields
            field.removeAttribute('required');
            // Remove validation classes when disabled to clear visual feedback
            field.classList.remove('is-invalid');
            field.classList.remove('is-valid');
        }
    });
}

function toggleButtons(entryId, isEditing) {
    ['edit', 'delete', 'save', 'cancel'].forEach(action => {
        const button = document.getElementById(`${action}${entryId}`);
        if (button) { // Ensure the button exists before trying to toggle
            button.classList.toggle(
                'd-none',
                action === 'edit' || action === 'delete' ? isEditing : !isEditing
            );
        }
    });
}

function toggleMapButtons(mapId, isEditing) {
    ['editMap', 'deleteMap', 'saveMap', 'cancelMap'].forEach(action => {
        const button = document.getElementById(`${action}${mapId}`);
        if (button) { // Ensure the button exists
            button.classList.toggle(
                'd-none',
                action === 'editMap' || action === 'deleteMap' ? isEditing : !isEditing
            );
        }
    });
}

function changeEdit(entryId, enabled) {
    const form = document.getElementById(`form${entryId}`);
    if (form) { // Check if form exists
        toggleFields(form, enabled);
        toggleButtons(entryId, enabled);
        // If enabling, remove was-validated class to reset validation state
        if (enabled) {
            form.classList.remove('was-validated');
        }
    }
}

function editMap(mapId, enabled) {
    const form = document.getElementById(`mapForm${mapId}`);
    if (form) { // Check if form exists
        toggleFields(form, enabled);
        toggleMapButtons(mapId, enabled);
        if (enabled) {
            form.classList.remove('was-validated');
        }
    }
}

function addMap() {
    const modalElement = document.getElementById('addMapModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

function addEntry(category) {
    const hiddenField = document.getElementById('currentTab');
    if (hiddenField) {
        hiddenField.value = category.replace('nav-', '');
        console.log(hiddenField.value);

        // Hide all modal inputs first
        document.querySelectorAll('.modal-input').forEach(el => el.classList.add('d-none'));
        // Show only the inputs relevant to the selected category
        document.querySelectorAll(`.${hiddenField.value}-show`).forEach(el => el.classList.remove('d-none'));

        const modalElement = document.getElementById('addEntryModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }
}

(() => {
    'use strict';

    const forms = document.querySelectorAll('.needs-validation');

    // Loop over each form and add submit event listener to prevent submission if invalid
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            // Only validate if the 'Save' button is visible, meaning the form is in edit mode
            const saveButton = form.querySelector('button[type="submit"]');
            if (saveButton && !saveButton.classList.contains('d-none')) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            } else {
                // If not in edit mode, prevent submission (e.g., if someone tries to force it)
                event.preventDefault();
                event.stopPropagation();
            }
        });
    });
})();

document.getElementById('resetButton')?.addEventListener('click', function () {
    if (confirm('Are you sure you want to reset the settings?')) {
        window.location.href = '/reset';
    }
});


function deleteEntry(id, name, tab) {
    const deleteName = document.getElementById('deleteName');
    if (deleteName) {
        deleteName.textContent = name;
    }

    const confirmedDelete = document.getElementById('confirmedDelete');
    if (confirmedDelete) {
        confirmedDelete.href = `/admin/delete_entry/${id}/${tab}`;
    }
    const myModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    myModal.show();
}

function deleteMap(id, name) {
    const deleteName = document.getElementById('deleteName');
    if (deleteName) {
        deleteName.textContent = name;
    }

    const confirmedDelete = document.getElementById('confirmedDelete');
    if (confirmedDelete) {
        confirmedDelete.href = `/admin/delete_map/${id}`;
    }
    const myModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    myModal.show(); // Ensure modal is shown
}


function deleteLink(linkId, startName, configProperty, endName, tab, entry) {
    const deleteName = document.getElementById('deleteName');
    if (deleteName) {
        deleteName.textContent = `${startName} - ${configProperty} - ${endName} ?`;
    }

    const confirmedDelete = document.getElementById('confirmedDelete');
    if (confirmedDelete) {
        confirmedDelete.href = `/admin/delete_link/${linkId}/${tab}/${entry}`;
    }

    const myModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    myModal.show();
}


const connectionSelects = document.querySelectorAll('.connection-select');

connectionSelects.forEach(selectConnection => {
    selectConnection.addEventListener('change', () => {
        const isEnabled = selectConnection.selectedIndex !== 0;

        // Enable/Disable next sibling elements based on selection
        // We only expect to enable the 'link-target' select after 'link-type'
        // and 'link-role' after 'link-target'.
        // The previous sibling logic was incorrect for enabling.
        if (selectConnection.nextElementSibling) {
            selectConnection.nextElementSibling.disabled = !isEnabled;
            // If the next select is disabled, also disable the one after it (role) and the save button
            if (selectConnection.nextElementSibling.classList.contains('link-target')) {
                 selectConnection.nextElementSibling.selectedIndex = 0; // Reset target selection
                 const roleSelect = selectConnection.nextElementSibling.nextElementSibling;
                 if (roleSelect) {
                    roleSelect.disabled = true;
                    roleSelect.selectedIndex = 0; // Reset role selection
                 }
                 const saveButton = selectConnection.parentNode.querySelector('button:last-child');
                 if (saveButton) {
                    saveButton.disabled = true; // Disable save button
                 }
            }
            if (selectConnection.nextElementSibling.classList.contains('link-role')) {
                selectConnection.nextElementSibling.selectedIndex = 0; // Reset role selection
                const saveButton = selectConnection.parentNode.querySelector('button:last-child');
                if (saveButton) {
                   saveButton.disabled = !isEnabled; // Enable/disable save button based on role selection
                }
            }
        } else {
            // This is for the last select (link-role), when it changes, it affects the save button
            const saveButton = selectConnection.parentNode.querySelector('button:last-child');
            if (saveButton) {
               saveButton.disabled = !isEnabled;
            }
        }


        // Locate the save button and selected option data
        const saveButton = selectConnection.parentNode.querySelector('button:last-child');
        const optionData = selectConnection.options[selectConnection.selectedIndex];

        // Call setSaveValues with relevant parameters
        setSaveValues(selectConnection.classList, saveButton, optionData, selectConnection);
    });
});

function setSaveValues(classList, saveButton, info, thisElement) {
    const {value} = info;

    if (classList.contains('link-type')) {
        saveButton.dataset.domain = info.getAttribute('data-entry');
        saveButton.dataset.direction = info.getAttribute('data-direction');
        saveButton.dataset.property = value;

        const selectNode = thisElement.nextElementSibling; // link-target select dropdown
        const configClassToShow = `config-class-${info.getAttribute('data-range')}`;

        // Filter target nodes based on the selected link-type's range
        Array.from(selectNode.options).forEach((option, i) => {
            // Keep the default "select node" option (index 0) visible
            // And show options that match the configClassToShow
            option.classList.toggle('d-none', !(option.classList.contains(configClassToShow) || i === 0));
        });
    }

    if (classList.contains('link-target')) {
        saveButton.dataset.range = value;
    }

    if (classList.contains('link-role')) {
        saveButton.dataset.role = value;
    }
}


function saveLinkValues(button) {
    let domain = button.dataset.domain;
    let range = button.dataset.range;

    // Check if domain, range, property, and role are all set before proceeding
    if (!domain || !range || !button.dataset.property || !button.dataset.role) {
        alert('Please select a connection type, target node, and role.'); // Or use a more sophisticated UI feedback
        return;
    }

    if (button.dataset.direction !== 'direct') {
        [domain, range] = [range, domain];
    }

    const { property, role, tab, entry } = button.dataset;

    const params = new URLSearchParams({
        domain,
        range,
        property,
        role,
        tab,
        entry
    });

    // Construct URL with query parameters
    window.location.href = `/admin/add_link/?${params.toString()}`;
}


// --- Sortable JS for Maps ---
const accordionContainer = document.getElementById('mapsAccordion');
if (accordionContainer) { // Ensure the element exists before initializing Sortable
    new Sortable(accordionContainer, {
        animation: 150,
        handle: '.accordion-button', // Specify the handle for sorting
        onEnd: function (evt) {
            // This function runs when sorting is done
            const items = Array.from(accordionContainer.getElementsByClassName('accordion-item'));
            items.forEach((item, index) => {
                item.setAttribute("data-order", index + 1);
            });

            // Map items to array of objects with order and id
            const sortedItems = items.map(item => ({
                order: item.getAttribute("data-order"),
                id: item.getAttribute("data-id")
            }));
            saveSortOrder(sortedItems, 'maps');
        }
    });
}


// --- Sortable JS for Links ---
const sortableDivs = Array.from(document.getElementsByClassName('link-divs'));

sortableDivs.forEach((item) => {
    makeSortables(item);
});

function makeSortables(containerDiv) {
    new Sortable(containerDiv, {
        animation: 150,
        handle: '.d-flex', // Specify the handle for sorting
        onEnd: function (evt) {
            const items = Array.from(containerDiv.getElementsByClassName('d-flex'));
            // Update order attribute based on visual sorting
            items.forEach((item, index) => {
                item.setAttribute("data-order", index + 1);
            });

            // Map items to array of objects with order and id
            const sortedItems = items.map(item => ({
                order: item.getAttribute("data-order"),
                id: item.getAttribute("data-id")
            }));
            saveSortOrder(sortedItems, 'links');
        }
    });
}

function saveSortOrder(items, table) {
    fetch('/sortlinks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({criteria: items, table: table}),
    })
    .then(response => {
        if (!response.ok) {
            console.error('Failed to save sort order:', response.statusText);
            // Optionally, show a flash message or revert UI changes
        }
    })
    .catch(error => {
        console.error('Error saving sort order:', error);
        // Handle network errors
    });
}
