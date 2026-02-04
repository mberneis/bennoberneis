import json
import os
import hashlib

def generate_html():
    # Generate cache-buster from CSS file content
    with open('styles.css', 'rb') as f:
        css_hash = hashlib.md5(f.read()).hexdigest()[:8]
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
    <meta content="avatar.pnj" property="og:image">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="styles.css?v={css_hash}">
    <script>
        // Dark mode detection and initialization (runs before page renders to prevent flash)
        (function() {{
            const theme = localStorage.getItem('theme');
            if (theme === 'dark') {{
                document.documentElement.classList.add('dark');
            }} else if (theme === 'light') {{
                document.documentElement.classList.add('light');
            }}
            // If no theme set, CSS media query handles system preference
        }})();
    </script>
</head>
<body>
    <nav id="main-nav">
        <a href="#" class="nav-logo">Benno Berneis</a>
        <div class="nav-controls">
            <div class="lang-toggle">
                <button class="lang-btn" id="lang-en">EN</button>
                <button class="lang-btn" id="lang-de">DE</button>
            </div>
            <button id="dark-mode-toggle" aria-label="Toggle dark mode">
                <svg id="theme-icon" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                </svg>
            </button>
        </div>
    </nav>

    <header>
        <h1 id="header-title">Benno Berneis</h1>
        <p id="header-desc">
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
            const headerTitle = document.getElementById('header-title');
            const headerDesc = document.getElementById('header-desc');

            const headerTranslations = {{
                en: {{
                    title: "Benno Berneis",
                    desc: 'An archive of the artist Benno Berneis (1 Apr 1883 – 8 Aug 1916).<br>Maintained by his grandson <a target="_blank" href="https://michael.berneis.com">Michael Berneis</a>.'
                }},
                de: {{
                    title: "Benno Berneis",
                    desc: 'Ein Archiv des Künstlers Benno Berneis (1. Apr. 1883 – 8. Aug. 1916).<br>Gepflegt von seinem Enkel <a target="_blank" href="https://michael.berneis.com">Michael Berneis</a>.'
                }}
            }};

            // State management
            let currentLang = (navigator.language || navigator.userLanguage).startsWith('de') ? 'de' : 'en';

            const updateLanguageUI = () => {{
                langEn.classList.toggle('active', currentLang === 'en');
                langDe.classList.toggle('active', currentLang === 'de');

                // Update Header
                const trans = headerTranslations[currentLang];
                headerTitle.textContent = trans.title;
                headerDesc.innerHTML = trans.desc;

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

            // Dark Mode Toggle
            const darkModeToggle = document.getElementById('dark-mode-toggle');
            const themeIcon = document.getElementById('theme-icon');

            function getMode() {{
                const theme = localStorage.getItem('theme');
                if (theme === 'dark') return 'dark';
                if (theme === 'light') return 'light';
                return 'system';
            }}

            function applyMode(mode) {{
                document.documentElement.classList.remove('dark', 'light');
                if (mode === 'dark') {{
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                }} else if (mode === 'light') {{
                    document.documentElement.classList.add('light');
                    localStorage.setItem('theme', 'light');
                }} else {{
                    localStorage.removeItem('theme');
                    // System preference is handled by CSS media query
                }}
                updateIcon(mode);
            }}

            function updateIcon(mode) {{
                let path;
                if (mode === 'light') {{
                    // Sun icon
                    path = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
                }} else if (mode === 'dark') {{
                    // Moon icon
                    path = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>';
                }} else {{
                    // Computer/system icon
                    path = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>';
                }}
                themeIcon.innerHTML = path;
            }}

            function cycleMode() {{
                const current = getMode();
                let next;
                if (current === 'light') next = 'dark';
                else if (current === 'dark') next = 'system';
                else next = 'light';
                applyMode(next);
            }}

            darkModeToggle.addEventListener('click', cycleMode);

            // Initialize icon based on current mode
            updateIcon(getMode());

            // Listen for system preference changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {{
                if (getMode() === 'system') {{
                    // CSS handles it, but we can trigger any needed updates here
                }}
            }});
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
