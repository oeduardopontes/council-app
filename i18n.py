"""
Simple i18n module for loading and accessing translations
"""
import json
import os
from typing import Dict, Any

# Cache for loaded translations
_translations: Dict[str, Dict[str, Any]] = {}
_current_locale = 'en'

def load_translations(locale: str) -> Dict[str, Any]:
    """Load translations for a given locale"""
    if locale in _translations:
        return _translations[locale]

    translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
    file_path = os.path.join(translations_dir, f'{locale}.json')

    if not os.path.exists(file_path):
        # Fallback to English if locale not found
        locale = 'en'
        file_path = os.path.join(translations_dir, f'{locale}.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        _translations[locale] = json.load(f)

    return _translations[locale]

def set_locale(locale: str):
    """Set the current locale"""
    global _current_locale
    _current_locale = locale
    # Preload translations
    load_translations(locale)

def get_locale() -> str:
    """Get the current locale"""
    return _current_locale

def get_nested_value(data: Dict[str, Any], key: str) -> Any:
    """Get nested dictionary value using dot notation"""
    keys = key.split('.')
    value = data
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return None
        else:
            return None
    return value

def t(key: str, **kwargs) -> str:
    """
    Translate a key to the current locale

    Args:
        key: Translation key in dot notation (e.g., 'home.title')
        **kwargs: Variables to interpolate in the translation

    Returns:
        Translated string
    """
    translations = load_translations(_current_locale)
    value = get_nested_value(translations, key)

    if value is None:
        # Fallback to English if translation not found
        if _current_locale != 'en':
            en_translations = load_translations('en')
            value = get_nested_value(en_translations, key)

        # If still not found, return the key itself
        if value is None:
            return key

    # Interpolate variables
    if kwargs:
        try:
            return str(value).format(**kwargs)
        except (KeyError, ValueError):
            return str(value)

    return str(value)

def get_all_translations(locale: str = None) -> Dict[str, Any]:
    """Get all translations for a locale (for passing to JavaScript)"""
    if locale is None:
        locale = _current_locale
    return load_translations(locale)
