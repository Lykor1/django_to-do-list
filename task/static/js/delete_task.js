document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('[data-bs-target="#deleteTaskModal"]');
    const taskTitleSpan = document.getElementById('task-title');
    const deleteForm = document.getElementById('delete-task-form');
    const modal = new bootstrap.Modal(document.getElementById('deleteTaskModal'));

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            const taskTitle = this.dataset.taskTitle;

            // Устанавливаем название задачи
            taskTitleSpan.textContent = taskTitle;

            // Устанавливаем action формы
            deleteForm.action = `/task/${taskId}/delete/`;

            // Показываем модальное окно
            modal.show();
        });
    });
});