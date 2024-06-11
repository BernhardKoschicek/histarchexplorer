document.addEventListener('DOMContentLoaded', function() {
        const configPropertySelect = document.getElementById('configPropertySelect');
        const dynamicSelectsDiv = document.getElementById('dynamicSelects');

        const institutionsData = {{ institutions_data | tojson | safe }};
        const personsData = {{ persons_data | tojson | safe }};
        const rolesData = {{ roles_data | tojson | safe }};

        configPropertySelect.addEventListener('change', function() {
            // Clear existing dynamic selects
            dynamicSelectsDiv.innerHTML = '';

            if (this.value === 'has_member' || this.value === 'has_affiliation' || this.value === 'has_translation') {
                // Create select elements for startName, endName, and role/attribute

                const startNameSelect = createSelectElement('start_name', 'form-select linked-select me-2', institutionsData);
                const endNameSelect = createSelectElement('end_name', 'form-select linked-select me-2', personsData);
                const roleSelect = createSelectElement('role', 'form-select linked-select me-2', rolesData);

                dynamicSelectsDiv.appendChild(startNameSelect);
                dynamicSelectsDiv.appendChild(endNameSelect);
                dynamicSelectsDiv.appendChild(roleSelect);
            }
        });

        function createSelectElement(name, className, optionsData) {
            const select = document.createElement('select');
            select.name = name;
            select.className = className;

            optionsData.forEach(function(option) {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = option.name;
                select.appendChild(optionElement);
            });

            return select;
        }
    });