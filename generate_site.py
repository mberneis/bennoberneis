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
    <title>Benno Berneis | Artist Archive</title>
    <meta name="description" content="Archive of the artist Benno Berneis (1883-1916). Collecting his works, letters and history.">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <nav id="main-nav">
        <a href="#" class="nav-logo">Benno Berneis</a>
        <div class="lang-toggle">
            <button class="lang-btn" id="lang-en">EN</button>
            <button class="lang-btn" id="lang-de">DE</button>
        </div>
    </nav>

    <header>
        <h1>Benno Berneis</h1>
        <p>
            An archive of the artist Benno Berneis (1 Apr 1883 – 8 Aug 1916).<br>
            Maintained by his grandson <a target="_blank" href="https://michael.berneis.com">Michael Berneis</a>.
        </p>
    </header>

    <main id="posts-container">
        <!-- Posts will be injected here by JavaScript -->
    </main>

    <div id="lightbox">
        <img src="" alt="Lightbox Image">
    </div>

    <button id="back-to-top" title="Back to Top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>
    </button>

    <footer style="text-align: center; padding: 60px 20px; color: #666; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.05); background: #050505;">
        <p>&copy; {os.popen('date +%Y').read().strip()} Benno Berneis Archive. All rights reserved.</p>
    </footer>

    <script id="posts-data" type="application/json">
        {posts_json_str}
    </script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const postsContainer = document.getElementById('posts-container');
            const postsData = JSON.parse(document.getElementById('posts-data').textContent);
            const nav = document.getElementById('main-nav');
            const btBtn = document.getElementById('back-to-top');
            const lightbox = document.getElementById('lightbox');
            const lightboxImg = lightbox.querySelector('img');
            const langEn = document.getElementById('lang-en');
            const langDe = document.getElementById('lang-de');

            // State management
            let currentLang = (navigator.language || navigator.userLanguage).startsWith('de') ? 'de' : 'en';

            const updateLanguageUI = () => {{
                langEn.classList.toggle('active', currentLang === 'en');
                langDe.classList.toggle('active', currentLang === 'de');
                renderPosts();
            }};

            langEn.addEventListener('click', () => {{
                currentLang = 'en';
                updateLanguageUI();
            }});

            langDe.addEventListener('click', () => {{
                currentLang = 'de';
                updateLanguageUI();
            }});

            // Scroll animations & Effects
            window.addEventListener('scroll', () => {{
                const scrolled = window.scrollY > 100;
                nav.classList.toggle('scrolled', scrolled);
                btBtn.classList.toggle('visible', window.scrollY > 500);
            }});

            btBtn.addEventListener('click', () => {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});

            // Lightbox
            const openLightbox = (src) => {{
                lightboxImg.src = src;
                lightbox.classList.add('active');
                document.body.style.overflow = 'hidden';
            }};

            const closeLightbox = () => {{
                lightbox.classList.remove('active');
                document.body.style.overflow = '';
            }};

            lightbox.addEventListener('click', closeLightbox);
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') closeLightbox();
            }});

            // Intersection Observer
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px"
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('visible');
                    }}
                }});
            }}, observerOptions);

            const renderPosts = () => {{
                postsContainer.innerHTML = '';
                const isGerman = currentLang === 'de';

                postsData.forEach((post, index) => {{
                    const textContent = isGerman ? (post.text_de || post.text_en) : post.text_en;

                    if (!textContent && (!post.images || post.images.length === 0) && !post.link) {{
                        return;
                    }}

                    // Link Preview
                    if (post.link) {{
                        const linkDiv = document.createElement('div');
                        linkDiv.className = 'link-preview post';
                        const a = document.createElement('a');
                        a.href = post.link.url;
                        a.target = '_blank';
                        a.textContent = post.link.title;
                        linkDiv.appendChild(a);
                        postsContainer.appendChild(linkDiv);
                        observer.observe(linkDiv);
                        return;
                    }}

                    const article = document.createElement('article');
                    article.className = 'post';

                    // Text
                    if (textContent) {{
                        const textDiv = document.createElement('div');
                        textDiv.className = 'post-text';
                        textContent.split('\\n').forEach(line => {{
                            if (line.trim()) {{
                                const p = document.createElement('p');
                                p.textContent = line.trim();
                                textDiv.appendChild(p);
                            }}
                        }});
                        article.appendChild(textDiv);
                    }}

                    // Images
                    if (post.images && post.images.length > 0) {{
                        const imagesDiv = document.createElement('div');
                        imagesDiv.className = 'post-images';
                        post.images.forEach(imgUrl => {{
                            const img = document.createElement('img');
                            const filename = imgUrl.split('/').pop().split('?')[0];
                            const localPath = `images/${{filename}}`;
                            img.src = localPath;
                            img.alt = 'Benno Berneis Art';
                            img.loading = 'lazy';

                            img.addEventListener('click', (e) => {{
                                if (!img.closest('a')) {{
                                    e.preventDefault();
                                    openLightbox(localPath);
                                }}
                            }});

                            const picLink = post.piclink || post.picLink;
                            if (textContent && textContent.includes('Der Welt Spiegel') && filename === 'tumblr_olsmth70ux1qk1nkmo1_1280.png') {{
                                const a = document.createElement('a');
                                a.href = './pdfs/der-welt-spiegel-1917.pdf';
                                a.target = '_blank';
                                a.appendChild(img);
                                imagesDiv.appendChild(a);
                            }} else if (picLink) {{
                                const a = document.createElement('a');
                                a.href = picLink;
                                a.target = '_blank';
                                a.appendChild(img);
                                imagesDiv.appendChild(a);
                            }} else {{
                                imagesDiv.appendChild(img);
                            }}
                        }});
                        article.appendChild(imagesDiv);
                    }}

                    // Footer
                    if (post.footer) {{
                        const footerDiv = document.createElement('div');
                        footerDiv.className = 'post-footer';
                        const p = document.createElement('p');
                        p.style.color = 'var(--text-secondary)';
                        p.style.fontSize = '0.9rem';
                        p.style.marginTop = '20px';
                        p.textContent = post.footer;
                        footerDiv.appendChild(p);
                        article.appendChild(footerDiv);
                    }}

                    postsContainer.appendChild(article);
                    observer.observe(article);
                }});
            }};

            updateLanguageUI();
        }});
    </script>
</body>
</html>"""

    # Write index.html
    with open('index.html', 'w') as f:
        f.write(html_content)

    print("index.html generated successfully with premium styling and enhanced interactivity.")

if __name__ == "__main__":
    generate_html()
