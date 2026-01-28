import json

def patch_posts():
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    updates = [
        {
            "keyword": "German Wikipedia entry",
            "link": {
                "url": "http://de.wikipedia.org/wiki/Benno_Berneis",
                "title": "Wikipedia"
            }
        },
        {
            "keyword": "about Gertrud Eysoldt",
            "link": {
                "url": "http://de.wikipedia.org/wiki/Gertrud_Eysoldt",
                "title": "Wikipedia - Gertrud Eysoldt"
            }
        },
        {
            "keyword": "Späte Rückkehr",
            "link": {
                "url": "http://www.berlinischegalerie.de/sammlung/neuzugaenge/spaete-rueckkehr-benno-berneis/",
                "title": "Späte Rückkehr: Benno Berneis | Berlinische Galerie | Ihr Museum für moderne und zeitgenössische Kunst in Berlin"
            }
        }
    ]

    count = 0
    for post in posts:
        text = post.get('text', '')
        for update in updates:
            if update['keyword'] in text and 'link' not in post:
                post['link'] = update['link']
                print(f"Patched post: {update['keyword']}")
                count += 1
                break

    if count > 0:
        with open('posts.json', 'w') as f:
            json.dump(posts, f, indent=2)
        print(f"Successfully patched {count} posts.")
    else:
        print("No posts needed patching (or keywords not found).")

if __name__ == "__main__":
    patch_posts()
