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
        if (confirm("Are you sure you want to delete the database entry? This deletes the entry PERMANENTLY from the database.")) {
            deleteEntry(entryId);
        }
    }


function deleteEntry(id, name, tab) {
    console.log('delete?')
    deleteName = document.getElementById('deleteName')
    deleteName.innerHTML = name
    confirmedDelete = document.getElementById('confirmedDelete')
        const deleteUrl = "delete_entry/" + id + "/" + tab
    confirmedDelete.setAttribute("href", deleteUrl)
}