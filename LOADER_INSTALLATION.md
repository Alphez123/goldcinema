# How to Add the Modern Page Loader to Your Website

I've created a beautiful, cinema-themed page loader for Gold Cinema. Here's how to add it:

## Files Created:
1. **`static/css/loader.css`** - The loader styles
2. **`users/templates/includes/loader.html`** - The loader HTML structure

## Installation Steps:

### Step 1: Add CSS Link to Your Templates
In the `<head>` section of your HTML files, add this line after the Font Awesome link:

```html
<link rel="stylesheet" href="{% static 'css/loader.css' %}">
```

### Step 2: Add Loader HTML
Right after the opening `<body>` tag, add:

```html
{% include 'includes/loader.html' %}
```

## Example for landing-page.html:

**In the `<head>` section (around line 12):**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
<link rel="stylesheet" href="{% static 'css/loader.css' %}">  <!-- ADD THIS LINE -->
```

**After `<body>` tag (around line 434):**
```html
<body>

    {% include 'includes/loader.html' %}  <!-- ADD THIS LINE -->

    <div class="background"></div>
```

## Features of the Loader:

✨ **Spinning Film Reel** - Animated cinema reel with golden glow
🌟 **Wave Text Animation** - "Gold Cinema" text with wave effect
📊 **Progress Bar** - Smooth loading progress indicator
✨ **Floating Particles** - Golden particles floating around
🎨 **Auto-Hide** - Automatically fades out when page loads (0.5 second delay)
📱 **Responsive** - Works perfectly on mobile and desktop

## Customization:

To change the loader duration, edit the delay in `includes/loader.html`:
```javascript
setTimeout(() => {
    loader.classList.add('hidden');
}, 500); // Change 500 to your preferred milliseconds
```

## Apply to Other Pages:

You can add the same loader to:
- `homepage.html`
- `login.html`
- `register.html`
- `movie_details.html`

Just follow the same two steps above!

---

**Note:** The loader will automatically disappear once the page finishes loading, creating a smooth, professional user experience.
