# Benno Berneis Website

This is a static recreation of the Benno Berneis website (originally a Tumblr blog).

## Project Structure

- `index.html`: The main website file containing all content.
- `styles.css`: The stylesheet.
- `images/`: Directory containing all downloaded images.
- `download_images.sh`: Script used to download the images from the original source.
- `generate_site.py`: Python script used to generate `index.html` from `posts.json`.
- `posts.json`: Structured data scraped from the original site.

## Local Development

To view the site locally, simply open `index.html` in your web browser.

## Deployment on Cloudflare Pages

This site is ready for Cloudflare Pages.

1.  Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2.  Go to **Pages**.
3.  Click **Create a project** > **Connect to Git** (if you push this to GitHub/GitLab) OR **Direct Upload** (drag and drop the folder).
4.  **If using Git:**
    - Select your repository.
    - **Build command:** (Leave empty, this is a plain static site).
    - **Build output directory:** (Leave empty or set to root `/` if asked, but usually for static sites without a build step, just the root is fine. If Cloudflare asks for an output directory, you may need to ensure it serves the root. Actually, for plain HTML, standard settings work fine. If you strictly need a build command, `exit 0` works).
5.  **If using Direct Upload:**
    - Drag and drop the `bennoberneis` folder.
    - Use the project name `benno-berneis` (or similar).
    - Deploy.

The site requires no build process. It is pure HTML/CSS.
