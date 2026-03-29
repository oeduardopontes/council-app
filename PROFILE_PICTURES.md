# Custom Profile Pictures Guide

## Overview
Each agent can have a custom profile picture that displays in the agent selection grid. Currently, placeholder SVG images are being used with different colors for each agent.

## File Locations
All agent profile pictures are stored in:
```
/Users/dwardo/Claude/deejay.com.br/static/images/agents/
```

## Agent IDs and Files
Each agent has a unique ID that corresponds to its image file:

- `ar.svg` - Artistic Mentor (A&R)
- `coach.svg` - DJ Coach
- `produtor.svg` - Music Producer Mentor
- `curador.svg` - Curator / Music Critic
- `estratega.svg` - Digital Strategist
- `booker.svg` - Booker / Show Agent
- `manager.svg` - Manager / Career Consultant
- `advogado.svg` - Entertainment Lawyer
- `placeholder.svg` - Fallback image if agent-specific image fails to load

## Image Specifications

### Recommended Format
- **Format**: PNG or SVG
- **Size**: 48x48 pixels
- **Shape**: Square (will be displayed as circle via CSS)
- **File naming**: Use the agent ID as the filename (e.g., `ar.png`, `coach.png`)

### Supported Formats
The application supports both PNG and SVG formats. Choose based on your preference:
- **PNG**: Better for photos or complex images
- **SVG**: Better for icons, logos, or vector graphics (smaller file size)

## How to Add Custom Profile Pictures

### Option 1: Replace SVG files
Replace the existing SVG files with your custom images:
```bash
# Navigate to the images directory
cd /Users/dwardo/Claude/deejay.com.br/static/images/agents/

# Replace the file (keep the same name)
cp /path/to/your/custom-image.svg ar.svg
```

### Option 2: Add PNG files
If you prefer PNG format, the application will automatically use `.png` files if you update the code:

1. Create 48x48 pixel PNG images for each agent
2. Save them in `/Users/dwardo/Claude/deejay.com.br/static/images/agents/`
3. Update the file extension in `app.js` from `.svg` to `.png`:
   ```javascript
   // In static/js/app.js, line ~80
   <img src="/static/images/agents/${agent.id}.png" ...>
   ```

### Option 3: Mix and match formats
You can use different formats for different agents. Just make sure to use consistent naming with the agent ID.

## Design Recommendations

1. **Consistent Style**: Use a consistent visual style across all agent pictures for a cohesive look
2. **Clear Imagery**: Images should be clear and recognizable even at 48x48 pixels
3. **Color Palette**: Consider using colors that complement the purple gradient theme:
   - Primary: #667eea
   - Secondary: #764ba2
   - Accent colors: #8b5cf6, #a855f7, #c084fc

4. **Background**: Consider using:
   - Transparent background for PNG files
   - Solid color backgrounds that match the app's color scheme
   - Circular framing (CSS will add the circular mask)

## Deployment

After adding or updating profile pictures:

1. Test locally first:
   ```bash
   cd /Users/dwardo/Claude/deejay.com.br
   python app.py
   ```

2. Deploy to production server:
   ```bash
   # Sync files to edumini.local
   rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' --exclude '.env' \
     /Users/dwardo/Claude/deejay.com.br/ dwardo@edumini.local:~/deejay-app/

   # Restart the service (changes to static files don't require restart, but good practice)
   ssh dwardo@edumini.local 'launchctl stop com.deejay.app && launchctl start com.deejay.app'
   ```

## CSS Styling

The profile pictures are styled with the following CSS (in `static/css/style.css`):
```css
.agent-profile-pic {
    width: 48px;
    height: 48px;
    border-radius: 50%;        /* Makes it circular */
    object-fit: cover;         /* Ensures proper scaling */
    flex-shrink: 0;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s;
}

.agent-option:hover .agent-profile-pic {
    border-color: #667eea;     /* Purple border on hover */
}

.agent-option input:checked ~ .agent-profile-pic {
    border-color: #667eea;     /* Purple border when selected */
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}
```

## Troubleshooting

### Image not showing
1. Check that the file exists in `/Users/dwardo/Claude/deejay.com.br/static/images/agents/`
2. Verify the filename matches the agent ID exactly
3. Clear browser cache (Cmd+Shift+R on Mac)

### Image appears distorted
1. Ensure the image is square (same width and height)
2. Use `object-fit: cover` in CSS (already set)

### Changes not appearing on live site
1. Clear browser cache
2. Verify files were deployed: `ssh dwardo@edumini.local 'ls -la ~/deejay-app/static/images/agents/'`
3. Check browser console for any loading errors

## Current Color Scheme

The current placeholder images use these colors:
- AR: #667eea (blue-purple)
- Coach: #764ba2 (purple)
- Produtor: #8b5cf6 (violet)
- Curador: #a855f7 (bright purple)
- Estratega: #c084fc (light purple)
- Booker: #d8b4fe (very light purple)
- Manager: #7c3aed (deep purple)
- Advogado: #6366f1 (indigo)
- Placeholder: #9ca3af (gray)
