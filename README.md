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

This site is optimized for **Cloudflare Pages**.

### Cloudflare Pages Configuration

1.  Push this repository to GitHub/GitLab.
2.  In the Cloudflare Dashboard, go to **Workers & Pages** > **Create application** > **Pages**.
3.  Connect your repository.
4.  **Build settings**:
    - **Framework preset**: `None`
    - **Build command**: `python3 generate_site.py`
    - **Build output directory**: `.` (Root)
    - **Root directory**: `/`

### Manual Refresh

If you add new posts to `posts.json`, simply run:
```bash
python3 generate_site.py
```
And commit the updated `index.html`.

## Archive Details

This project preserves the artistic legacy of Benno Berneis, ensuring all assets (images and text) are hosted locally and rendered in a modern, premium gallery interface.

Old Tumblr site: https://www.tumblr.com/benno-berneis
