import json
import os

def generate_html():
    # Load posts
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    # Prepare JS-embedded JSON
    posts_json_str = json.dumps(posts, indent=2)

    html_content = f"""<!DOCTYPE html>
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
    <main id="posts-container">
        <!-- Posts will be injected here by JavaScript -->
    </main>

    <script id="posts-data" type="application/json">
        {posts_json_str}
    </script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const postsContainer = document.getElementById('posts-container');
            const postsData = JSON.parse(document.getElementById('posts-data').textContent);

            postsData.forEach(post => {{
                if (!post.text && (!post.images || post.images.length === 0) && !post.link) {{
                    return;
                }}

                // Link Preview (if exists)
                if (post.link) {{
                    const linkDiv = document.createElement('div');
                    linkDiv.className = 'link-preview';
                    const a = document.createElement('a');
                    a.href = post.link.url;
                    a.target = '_blank';
                    a.textContent = post.link.title;
                    linkDiv.appendChild(a);
                    postsContainer.appendChild(linkDiv);
                }}

                const article = document.createElement('article');
                article.className = 'post';

                // Text (if exists)
                if (post.text) {{
                    const textDiv = document.createElement('div');
                    textDiv.className = 'post-text';
                    post.text.split('\\n').forEach(line => {{
                        if (line.trim()) {{
                            const p = document.createElement('p');
                            p.textContent = line.trim();
                            textDiv.appendChild(p);
                        }}
                    }});
                    article.appendChild(textDiv);
                }}

                // Images (if exist)
                if (post.images && post.images.length > 0) {{
                    const imagesDiv = document.createElement('div');
                    imagesDiv.className = 'post-images';
                    post.images.forEach(imgUrl => {{
                        const img = document.createElement('img');
                        // Extract filename from URL
                        const filename = imgUrl.split('/').pop().split('?')[0];
                        img.src = `images/${{filename}}`;
                        img.alt = 'Benno Berneis Art';
                        img.loading = 'lazy';

                        // Special handling for the first post if it has a PDF link (based on old index.html)
                        // This pattern match is a bit specific but keeps the original behavior for the first post
                        if (post.text && post.text.includes('Der Welt Spiegel') && filename === 'tumblr_olsmth70ux1qk1nkmo1_1280.png') {{
                            const a = document.createElement('a');
                            a.href = './pdfs/der-welt-spiegel-1917.pdf';
                            a.target = '_blank';
                            a.appendChild(img);
                            imagesDiv.appendChild(a);
                        }} else {{
                            imagesDiv.appendChild(img);
                        }}
                    }});
                    article.appendChild(imagesDiv);
                }}

                postsContainer.appendChild(article);
            }});
        }});
    </script>
</body>
</html>"""

    # Write index.html
    with open('index.html', 'w') as f:
        f.write(html_content)

    print("index.html generated successfully with dynamic rendering.")

if __name__ == "__main__":
    generate_html()
