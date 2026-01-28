import json
import os
import shutil
from urllib.parse import urlparse

OUTPUT_DIR = 'public'

def generate_html():
    # Create output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, 'images'))

    # Load posts
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benno Berneis</title>
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Benno Berneis</h1>
        <p>This blog is maintained by Michael Berneis. It is collecting information about my grandfather, the artist Benno Berneis, 1 Apr 1883 - 8 Aug 1916</p>
    </header>
    <main>
"""

    for post in posts:
        # Skip the first post if it's just the title/intro which we hardcoded,
        # but looking at the JSON, the first post is an "Article".
        # The intro text ("This blog is maintained...") was in the gathered text but not necessarily in the first "post" object
        # because of how we scraped.
        # Actually, looking at the JSON, the first item is "Article from...". The "This blog..." text was in the generic text scrape but
        # our post scraper might have missed the bio if it wasn't in a post container.
        # It's fine, we put it in the header.

        text = post.get('text', '').strip()
        images = post.get('images', [])
        link = post.get('link')

        if not text and not images and not link:
            continue

        # Link
        if link:
            html_content += f'        <div class="link-preview">\n'
            html_content += f'            <a href="{link["url"]}" target="_blank">{link["title"]}</a>\n'
            html_content += '        </div>\n'

        html_content += '        <article class="post">\n'

        # Text
        if text:
            html_content += '            <div class="post-text">\n'
            for line in text.split('\n'):
                if line.strip():
                    html_content += f'                <p>{line.strip()}</p>\n'
            html_content += '            </div>\n'

        # Images
        if images:
            html_content += '            <div class="post-images">\n'
            for img_url in images:
                # Extract filename
                filename = os.path.basename(urlparse(img_url).path)
                # Copy image to public/images
                src_path = os.path.join('images', filename)
                dst_path = os.path.join(OUTPUT_DIR, 'images', filename)
                if os.path.exists(src_path):
                    shutil.copy2(src_path, dst_path)
                    html_content += f'                <img src="images/{filename}" alt="Benno Berneis Art" loading="lazy">\n'
            html_content += '            </div>\n'

        html_content += '        </article>\n'

    html_content += """    </main>
</body>
</html>"""

    # Write index.html
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(html_content)

    # Copy static assets
    shutil.copy2('styles.css', os.path.join(OUTPUT_DIR, 'styles.css'))
    if os.path.exists('favicon.ico'):
        shutil.copy2('favicon.ico', os.path.join(OUTPUT_DIR, 'favicon.ico'))

    print(f"Site generated successfully in '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    generate_html()
