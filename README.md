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

## Deployment

This site is designed to be deployed to **Cloudflare Pages**.

### Cloudflare Pages Settings

1.  Connect your GitHub repository.
2.  **Build settings**:
    - **Framework preset**: `None`
    - **Build command**: `python3 generate_site.py`
    - **Build output directory**: `public`
    - **Root directory**: (Leave empty / default `/`)
2.  **Deploy settings**:
    - **Deploy command**: `true` (If required by the UI; this is a "do-nothing" command)
3.  **Environment variables** (Optional): None needed.

> **Note:** Do not put `public` in the "Root directory" path settings. Cloudflare needs to run the build command in the main repository folder first to create the `public` folder.

The build script will:
1.  Read `posts.json`.
2.  Generate `index.html` inside the `public/` folder.
3.  Copy `styles.css` and `favicon.ico` to `public/`.
4.  Copy all images from `images/` to `public/images/`.

This ensures a clean deployment package.
