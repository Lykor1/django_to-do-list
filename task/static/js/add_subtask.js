document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-subtask-button');
    const container = document.getElementById('subtask-forms-container');

    // Получаем префикс формсета из data-атрибута контейнера
    const formsetPrefix = container ? container.dataset.formsetPrefix : null;

    // Проверяем, найдены ли необходимые элементы
    if (!addButton || !container || !formsetPrefix) {
        console.error("Could not find necessary elements or formset prefix for formset handling.");
        return; // Прекращаем выполнение, если что-то не найдено
    }

    // Находим скрытое поле TOTAL_FORMS для нашего формсета, используя полученный префикс
    const managementForm = container.querySelector(`input[name="${formsetPrefix}-TOTAL_FORMS"]`);
    const emptyFormTemplateElement = document.getElementById('empty-form-template');

     if (!managementForm || !emptyFormTemplateElement) {
        console.error("Could not find management form or empty form template.");
        return;
     }

    const emptyFormTemplate = emptyFormTemplateElement.innerHTML;


    addButton.addEventListener('click', function() {
        // Получаем текущее количество форм
        const currentFormCount = parseInt(managementForm.value);

        // Заменяем плейсхолдер __prefix__ на следующий доступный индекс
        const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, currentFormCount);

        // Создаем временный элемент div для парсинга HTML строки
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml.trim(); // trim() удаляет возможные пробелы по краям

        // Получаем элемент самой формы подзадачи из временного div
        const newFormElement = tempDiv.firstElementChild; // Берем первый дочерний элемент

        // Добавляем новую форму в конец контейнера форм
        container.appendChild(newFormElement);

        // Увеличиваем значение TOTAL_FORMS на 1
        managementForm.value = currentFormCount + 1;

        // Опционально: Прокручиваем страницу к добавленной форме для удобства
        newFormElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Опционально: Устанавливаем фокус на первое поле ввода в новой форме
        const firstInput = newFormElement.querySelector('input, textarea, select');
        if (firstInput) {
            firstInput.focus();
        }
    });
});