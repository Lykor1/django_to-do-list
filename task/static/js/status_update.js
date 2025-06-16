$(document).ready(function () {
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
            if (isNaN(date.getTime())) {
                console.error("Не удалось распарсить дату:", isoString);
                return '';
            }

            const options = {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Europe/Moscow'
            };
            let formattedString = new Intl.DateTimeFormat('ru-Ru', options).format(date);
            formattedString = formattedString.replace(', ', ' ');

            return formattedString;
        } catch (e) {
            console.error("Ошибка форматирования даты:", e);
            return '';
        }
    }

    const csrftoken = getCookie('csrftoken');

    $('.task-status-indicator').click(function () {
        var $indicator = $(this);
        var url = $indicator.data('url');
        $.ajax({
            url: url,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                if (data.status === 'success') {
                    $indicator.removeClass('status-not_active status-active status-completed')
                        .addClass('status-' + data.new_status);
                    $indicator.closest('.task-card')
                        .removeClass('task-status-not_active task-status-active task-status-completed')
                        .addClass('task-status-' + data.new_status);
                    if (data.new_status === 'completed') {
                        $indicator.html('<span class="checkmark">✔</span>');
                    } else {
                        $indicator.html('');
                    }

                    if (data.subtask_updates && data.subtask_updates.length > 0) {
                        data.subtask_updates.forEach(function (update) {
                            var $subtaskIndicator = $('.subtask-status-indicator[data-subtask-id="' + update.id + '"]');
                            if ($subtaskIndicator.length) {
                                $subtaskIndicator.removeClass('subtask-status-completed subtask-status-not_completed')
                                    .addClass('subtask-status-' + (update.is_completed ? 'completed' : 'not_completed'));
                                if (update.is_completed) {
                                    $subtaskIndicator.html('<span class="checkmark">✔</span>');
                                    const formattedTime = formatMoscowTime(data.completed_date);
                                    $subtaskIndicator.closest('.subtask-item')
                                        .find('.subtask-description')
                                        .find('p.small.text-muted')
                                        .remove()
                                        .end()
                                        .append('<p class="small text-muted mb-0">' + formattedTime + '</p>');
                                } else {
                                    $subtaskIndicator.html('');
                                    $subtaskIndicator.closest('.subtask-item')
                                        .find('.subtask-description p.small.text-muted')
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

    $('.subtask-status-indicator').click(function () {
        var $indicator = $(this);
        var url = $indicator.data('url');
        $.ajax({
            url: url,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                if (data.status === 'success') {
                    $indicator.removeClass('subtask-status-completed subtask-status-not_completed')
                        .addClass('subtask-status-' + (data.is_completed ? 'completed' : 'not_completed'));
                    if (data.is_completed) {
                        $indicator.html('<span class="checkmark">✔</span>');
                        const formattedTime = formatMoscowTime(data.completed_date);
                        $indicator.closest('.subtask-item')
                            .find('.subtask-description')
                            .find('p.small.text-muted')
                            .remove()
                            .end()
                            .append('<p class="small text-muted mb-0">' + formattedTime + '</p>');
                    } else {
                        $indicator.html('');
                        $indicator.closest('.subtask-item')
                            .find('.subtask-description p.small.text-muted')
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