import json
import os
from urllib.parse import urlparse

def generate_html():
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benno Berneis</title>
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

        html_content += '        <article class="post">\n'

        # Link
        if link:
            html_content += f'            <div class="link-preview">\n'
            html_content += f'                <a href="{link["url"]}" target="_blank">{link["title"]}</a>\n'
            html_content += '            </div>\n'



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
                # Check if file exists locally (optional validity check)
                html_content += f'                <img src="images/{filename}" alt="Benno Berneis Art" loading="lazy">\n'
            html_content += '            </div>\n'

        html_content += '        </article>\n'

    html_content += """    </main>
</body>
</html>"""

    with open('index.html', 'w') as f:
        f.write(html_content)

    print("index.html generated successfully.")

if __name__ == "__main__":
    generate_html()
