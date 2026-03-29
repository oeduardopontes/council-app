// Internationalization helper for client-side
let currentLocale = getCookie('locale') || 'en';
let translations = {};

// Get cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Set cookie
function setCookie(name, value, days = 365) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/`;
}

// Switch locale
async function switchLocale(locale) {
    try {
        const response = await fetch('/api/set-locale', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locale })
        });

        if (response.ok) {
            // Reload page to apply new locale
            window.location.reload();
        }
    } catch (error) {
        console.error('Error switching locale:', error);
    }
}

// Translate error messages (for client-side use)
function t(key, variables = {}) {
    let value = translations;
    const keys = key.split('.');

    for (const k of keys) {
        if (value && typeof value === 'object') {
            value = value[k];
        } else {
            return key; // Return key if not found
        }
    }

    if (typeof value === 'string') {
        // Replace variables
        return value.replace(/\{(\w+)\}/g, (match, varName) => {
            return variables[varName] !== undefined ? variables[varName] : match;
        });
    }

    return key;
}

// Initialize locale switcher
document.addEventListener('DOMContentLoaded', () => {
    // Get translations from page if available
    const translationsEl = document.getElementById('translations-data');
    if (translationsEl) {
        try {
            translations = JSON.parse(translationsEl.textContent);
        } catch (e) {
            console.error('Failed to parse translations:', e);
        }
    }
});
