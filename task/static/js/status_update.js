$(document).ready(function () {
    // Получаем CSRF-токен из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function formatMoscowTime(isoString) {
        if (!isoString) {
            return '';
        }
        try {
            const date = new Date(isoString);
            // Проверяем, удалось ли распарсить дату
            if (isNaN(date.getTime())) {
                console.error("Не удалось распарсить дату:", isoString);
                return ''; // Возвращаем пустую строку или сообщение об ошибке
            }

            const options = {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Europe/Moscow' // Указываем нужный часовой пояс
            };
            let formattedString = new Intl.DateTimeFormat('ru-Ru', options).format(date);
            formattedString = formattedString.replace(', ', ' ');

            return formattedString;
        } catch (e) {
            console.error("Ошибка форматирования даты:", e);
            return ''; // Обработка ошибок при форматировании
        }
    }

    const csrftoken = getCookie('csrftoken');

    // Обработка клика по статусу задачи
    $('.task-status-indicator').click(function () {
        var $indicator = $(this);
        var url = $indicator.data('url');
        $.ajax({
            url: url,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                if (data.status === 'success') {
                    // Обновляем классы и содержимое для задачи
                    $indicator.removeClass('status-not_active status-active status-completed')
                        .addClass('status-' + data.new_status);
                    $indicator.closest('.task-card')
                        .removeClass('task-status-not_active task-status-active task-status-completed')
                        .addClass('task-status-' + data.new_status);
                    // Обновляем галочку для задачи
                    if (data.new_status === 'completed') {
                        $indicator.html('<span class="checkmark">✔</span>');
                    } else {
                        $indicator.html('');
                    }

                    // Обновляем подзадачи, если есть subtask_updates
                    if (data.subtask_updates && data.subtask_updates.length > 0) {
                        data.subtask_updates.forEach(function (update) {
                            var $subtaskIndicator = $('.subtask-status-indicator[data-subtask-id="' + update.id + '"]');
                            if ($subtaskIndicator.length) {
                                $subtaskIndicator.removeClass('subtask-status-completed subtask-status-not_completed')
                                    .addClass('subtask-status-' + (update.is_completed ? 'completed' : 'not_completed'));
                                // Обновляем галочку
                                if (update.is_completed) {
                                    $subtaskIndicator.html('<span class="checkmark">✔</span>');
                                    // Обновляем дату выполнения
                                    const formattedTime = formatMoscowTime(data.completed_date);
                                    $subtaskIndicator.closest('.subtask-item')
                                        .find('.subtask-description')
                                        .find('.small.text-muted')
                                        .remove()
                                        .end()
                                        .append('<span class="small text-muted">' + formattedTime + '</span>');
                                } else {
                                    $subtaskIndicator.html('');
                                    $subtaskIndicator.closest('.subtask-item')
                                        .find('.subtask-description .small.text-muted')
                                        .remove();
                                }
                            }
                        });
                    }
                }
            },
            error: function () {
                alert('Ошибка при изменении статуса задачи.');
            }
        });
    });

    // Обработка клика по статусу подзадачи
    $('.subtask-status-indicator').click(function () {
        var $indicator = $(this);
        var url = $indicator.data('url');
        $.ajax({
            url: url,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                if (data.status === 'success') {
                    // Обновляем классы и содержимое
                    $indicator.removeClass('subtask-status-completed subtask-status-not_completed')
                        .addClass('subtask-status-' + (data.is_completed ? 'completed' : 'not_completed'));
                    // Обновляем галочку
                    if (data.is_completed) {
                        $indicator.html('<span class="checkmark">✔</span>');
                        // Обновляем дату выполнения
                        const formattedTime = formatMoscowTime(data.completed_date);
                        $indicator.closest('.subtask-item')
                            .find('.subtask-description')
                            .find('.small.text-muted')
                            .remove()
                            .end()
                            .append('<span class="small text-muted">' + formattedTime + '</span>');
                    } else {
                        $indicator.html('');
                        // Удаляем дату выполнения
                        $indicator.closest('.subtask-item')
                            .find('.subtask-description .small.text-muted')
                            .remove();
                    }
                }
            },
            error: function () {
                alert('Ошибка при изменении статуса подзадачи.');
            }
        });
    });
});