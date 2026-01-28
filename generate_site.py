import json
import os
from urllib.parse import urlparse

def generate_html():
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
        <p>This site is maintained by <a target="_blank" href='https://michael.berneis.com'>Michael Berneis</a>. <br>It is collecting information
            about my<br>grandfather,<br>the artist Benno Berneis,<br>1 Apr 1883 - 8 Aug 1916</p>
    </header>
    <main>
"""

    for post in posts:
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
                html_content += f'                <img src="images/{filename}" alt="Benno Berneis Art" loading="lazy">\n'
            html_content += '            </div>\n'

        html_content += '        </article>\n'

    html_content += """    </main>
</body>
</html>"""

    # Write index.html
    with open('index.html', 'w') as f:
        f.write(html_content)

    print("index.html generated successfully.")

if __name__ == "__main__":
    generate_html()
