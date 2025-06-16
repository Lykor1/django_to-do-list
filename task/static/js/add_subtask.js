document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-subtask-button');
    const container = document.getElementById('subtask-forms-container');

    const formsetPrefix = container ? container.dataset.formsetPrefix : null;

    if (!addButton || !container || !formsetPrefix) {
        console.error("Could not find necessary elements or formset prefix for formset handling.");
        return;
    }

    const managementForm = container.querySelector(`input[name="${formsetPrefix}-TOTAL_FORMS"]`);
    const emptyFormTemplateElement = document.getElementById('empty-form-template');

     if (!managementForm || !emptyFormTemplateElement) {
        console.error("Could not find management form or empty form template.");
        return;
     }

    const emptyFormTemplate = emptyFormTemplateElement.innerHTML;


    addButton.addEventListener('click', function() {
        const currentFormCount = parseInt(managementForm.value);

        const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, currentFormCount);

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml.trim();

        const newFormElement = tempDiv.firstElementChild;

        container.appendChild(newFormElement);

        managementForm.value = currentFormCount + 1;

        newFormElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        const firstInput = newFormElement.querySelector('input, textarea, select');
        if (firstInput) {
            firstInput.focus();
        }
    });
});