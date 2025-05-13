document.addEventListener('DOMContentLoaded', function () {
    const deleteCategoryModal = document.getElementById('deleteCategoryModal');
    const deleteForm = document.getElementById('delete-category-form');

    if (deleteCategoryModal) {
        deleteCategoryModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const categorySlug = button.getAttribute('data-category-slug');
            const categoryName = button.getAttribute('data-category-name');
            const modalBodyTextSpan = deleteCategoryModal.querySelector('.modal-body span#category-name');
            if (modalBodyTextSpan) {
                modalBodyTextSpan.textContent = categoryName;
            }
            deleteForm.action = `/category/${categorySlug}/delete/`;
        });
    }
});