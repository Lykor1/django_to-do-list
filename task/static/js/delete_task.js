// static/js/delete_task.js

document.addEventListener('DOMContentLoaded', function () {
    const deleteTaskModal = document.getElementById('deleteTaskModal');
    const deleteForm = document.getElementById('delete-task-form');

    if (deleteTaskModal) {
        deleteTaskModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const taskId = button.getAttribute('data-task-id');
            const taskTitle = button.getAttribute('data-task-title');
            const modalBodyTextSpan = deleteTaskModal.querySelector('.modal-body span#task-title');
            if (modalBodyTextSpan) {
                modalBodyTextSpan.textContent = taskTitle;
            }
            const currentQueryString = window.location.search;
            const baseUrl = `/task/${taskId}/delete/`;
            deleteForm.action = baseUrl + currentQueryString;
        });
    }
});