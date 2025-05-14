document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const body = document.body;
    let themeLink = document.getElementById('theme-link'); // Изменил const на let
    const currentTheme = getCookie('theme') || 'light';

    function setCookie(name, value, options = {}) {
        options = {
            path: '/',
            ...options
        };
        if (options.expires instanceof Date) {
            options.expires = options.expires.toUTCString();
        }
        let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
        for (let optionKey in options) {
            updatedCookie += "; " + optionKey;
            let optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }
        document.cookie = updatedCookie;
    }

    function getCookie(name) {
        let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    function applyTheme(theme) {
        const darkStyleCssPath = "/static/css/dark_style.css"; // Прямой путь к стилям

        if (theme === 'dark') {
            body.classList.add('dark-theme');
            if (themeLink) {
                themeLink.href = darkStyleCssPath;
            } else {
                themeLink = document.createElement('link'); // Создаем элемент link, если его нет
                themeLink.rel = 'stylesheet';
                themeLink.href = darkStyleCssPath;
                themeLink.id = 'theme-link';
                document.head.appendChild(themeLink);
            }
        } else {
            body.classList.remove('dark-theme');
            if (themeLink) {
                themeLink.remove(); // Удаляем элемент link
                themeLink = null; // Сбрасываем ссылку
            }
        }
    }

    applyTheme(currentTheme);

    themeToggleButton.addEventListener('click', () => {
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
        setCookie('theme', newTheme, {
            'max-age': 3600 * 24 * 365
        });
        currentTheme = newTheme;
    });
});