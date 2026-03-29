# Translation Files

This directory contains translation files for the AI Agent Council application.

## Available Languages

- **en.json** - English (US)
- **pt.json** - Portuguese (Brazilian)

## How to Edit Translations

Each translation file is a JSON file with a structured hierarchy of translation keys and their corresponding text.

### File Structure

```json
{
  "key": "Translation text",
  "nested": {
    "key": "Nested translation"
  }
}
```

### Examples

**To change the home page title:**
```json
{
  "home": {
    "title": "Your New Title Here"
  }
}
```

**To change error messages:**
```json
{
  "errors": {
    "question_required": "Your custom error message"
  }
}
```

### Variable Interpolation

Some translations support variables using `{variable_name}` syntax:

```json
{
  "errors": {
    "rate_limit": "Please wait {seconds} seconds"
  }
}
```

The `{seconds}` will be replaced with an actual number at runtime.

## Adding a New Language

To add support for a new language (e.g., Spanish):

1. Copy `en.json` to `es.json`
2. Translate all values to Spanish (keep the keys in English)
3. Update `app.py` to add 'es' to the valid locales list
4. Add an "ES" button to the locale switcher in templates

## Testing Translations

1. Edit the translation file (`en.json` or `pt.json`)
2. Save the file
3. Sync to Mac Mini:
   ```bash
   rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' /Users/dwardo/Claude/eduardopontes.com/ dwardo@edumini.local:~/council-app/
   ```
4. Restart the service:
   ```bash
   ssh dwardo@edumini.local "launchctl stop com.council.app && launchctl start com.council.app"
   ```
5. Refresh the website to see changes

## Translation Keys Reference

### Common Keys
- `app_title` - Application title
- `powered_by` - Footer text

### Home Page (`home`)
- `title` - Main heading
- `subtitle` - Subheading text

### Council Page (`council.executive`)
- `title` - Council name
- `subtitle` - Council description
- `description` - Detailed description
- `members.{role}` - Team member roles

### Form Elements (`form`)
- `question_label` - Question field label
- `question_placeholder` - Question field placeholder
- `question_hint` - Keyboard shortcut hint
- `context_label` - Context section label
- `context_add` - Add context button
- `agents_label` - Agent selection label
- `submit_button` - Submit button text
- `results_title` - Results section title
- `loading_message` - Loading indicator text

### Navigation (`navigation`)
- `back_to_councils` - Back button text

### Errors (`errors`)
- `question_required` - Empty question error
- `deliberation_error` - General error message
- `connection_error` - Connection failure message
- `rate_limit` - Rate limit message (supports `{seconds}` variable)
- `timeout` - Timeout error message
- `api_config_error` - API configuration error

### Locale Selector (`locale`)
- `language` - Language label
- `en` - English language name
- `pt` - Portuguese language name

## Tips for Translators

1. **Keep formatting** - Maintain any special characters like colons, periods, etc.
2. **Preserve variables** - Don't translate `{variable}` placeholders, only the surrounding text
3. **Test thoroughly** - Check both desktop and mobile views
4. **Context matters** - Consider where the text appears (button, heading, error, etc.)
5. **Keep it concise** - Especially for button labels and UI elements
6. **Match tone** - Maintain consistent formality/informality across translations

## Need Help?

If you're unsure about a translation or need to add new keys, refer to the existing structure or consult the development team.
