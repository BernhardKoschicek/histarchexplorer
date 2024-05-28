 function enableEdit(entryId) {
        var form = document.getElementById('form' + entryId);
        var fields = form.querySelectorAll('input, textarea');

        // Store current values to restore them if editing is canceled
        fields.forEach(function(field) {
            field.dataset.originalValue = field.value;
            field.removeAttribute('disabled');
        });

        // Show Save and Cancel buttons, hide Edit and Delete buttons
        document.getElementById('edit' + entryId).classList.add('d-none');
        document.getElementById('delete' + entryId).classList.add('d-none');
        document.getElementById('save' + entryId).classList.remove('d-none');
        document.getElementById('cancel' + entryId).classList.remove('d-none');
    }

    function cancelEdit(entryId) {
        var form = document.getElementById('form' + entryId);
        var fields = form.querySelectorAll('input, textarea');

        // Restore original values and disable the fields again
        fields.forEach(function(field) {
            field.value = field.dataset.originalValue;
            field.setAttribute('disabled', 'disabled');
        });

        // Show Edit and Delete buttons, hide Save and Cancel buttons
        document.getElementById('edit' + entryId).classList.remove('d-none');
        document.getElementById('delete' + entryId).classList.remove('d-none');
        document.getElementById('save' + entryId).classList.add('d-none');
        document.getElementById('cancel' + entryId).classList.add('d-none');
    }

     function confirmDelete(entryId) {
        if (confirm("Are you sure you want to delete the database entry?")) {
            deleteEntry(entryId);
        }
    }

    function deleteEntry(entryId) {
        // Request to the backend to delete the entry
        fetch('/admin/delete_entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ entry_id: entryId }) // Pass the entry ID in the request body
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            location.reload(); // Reload the page after successful deletion
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
            alert('Failed to delete entry. Please try again later.');
        });
    }