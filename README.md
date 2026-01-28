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
    - **Build output directory**: `.` (Root)
    - **Root directory**: (Leave empty / default `/`)

The build script will:
1.  Read `posts.json`.
2.  Generate `index.html` in the root folder.

This keeps the repository simple.
