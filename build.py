#!/usr/bin/env python3
import os, re, glob, json

ROOT = "/workspace/rhett-portfolio"
SRC = os.path.join(ROOT, "source-html")

def video_ids(slug):
    path = os.path.join(SRC, f"{slug}.html")
    if not os.path.exists(path):
        return []
    html = open(path, encoding="utf-8").read()
    ids = []
    for i in re.findall(r"https://www-ccv.adobe.io/v1/player/ccv/([^/]+)/embed", html):
        if i not in ids:
            ids.append(i)
    return ids

def ext_cover(slug):
    d = os.path.join(ROOT, "img", slug)
    for fn in os.listdir(d):
        if fn.startswith("cover."):
            return fn
    return None

def stills(slug):
    d = os.path.join(ROOT, "img", slug)
    files = sorted(fn for fn in os.listdir(d) if re.match(r"\d{2}\.", fn))
    return files

PROJECTS = [
    {
        "slug": "found-money-friend",
        "title": "Found Money Friend",
        "year": "2026",
        "role": "AI product",
        "lede": "An AI demo that finds missed revenue in a service business and puts a team on it. Built for a real-company pitch. One tap. No login.",
        "live": "https://rhettboyakin-code.github.io/found-money-friend/",
        "new": True,
    },
    {
        "slug": "morgan-jewelers",
        "title": "Morgan Jewelers",
        "year": "2020",
        "lede": "A lot of “engaging” content. Little reason to not like it.",
    },
    {
        "slug": "zions-bank",
        "title": "Zions Bank",
        "year": "2020",
        "lede": "Big, local bank. Worked on a wide range of mediums. Everything from TV to social. Made sure that behind every number is a story.",
    },
    {
        "slug": "arches-health-plan",
        "title": "Arches Health Plan",
        "year": "2020",
        "lede": "Life’s better under the arch. See for yourself.",
    },
    {
        "slug": "vsp-individual-vision-plans",
        "title": "VSP Individual Vision Plans",
        "year": "2020",
        "lede": "Eyeglasses are simple to operate. Just put them on. These ads are easy to like. Just watch them.",
    },
    {
        "slug": "our-kids-now",
        "title": "Our Schools Now",
        "year": "2020",
        "lede": "This was a proposed bill to get more funding for classrooms. So we used the best spokespeople we could find.",
    },
    {
        "slug": "radio-spots",
        "title": "Radio Spots",
        "year": "2020",
        "lede": "I love the challenge of radio. Hopefully you’ll love these.",
        "list": [
            "Utah Department of Transportation — “Rollercoaster”",
            "Utah Department of Transportation — “Tour Guide”",
            "PacificSource Health Plans — “Cuban Forkball”",
            "PacificSource Health Plans — “Call the Shots”",
            "PacificSource Health Plans — “Swashbuckler”",
            "Morgan Jewelers — “Dream Wedding”",
            "PacificSource Health Plans — “Puberty”",
        ],
    },
    {
        "slug": "csu-global",
        "title": "CSU-Global",
        "year": "2020",
        "lede": "",
    },
    {
        "slug": "miscellaneous-stuff",
        "title": "Miscellaneous Stuff",
        "year": "2020",
        "lede": "",
    },
]

NAV = '''<header class="nav">
  <a class="wordmark" href="{home}">Rhett Boyakin</a>
  <nav>
    <a href="{home}#work">Work</a>
    <a href="{contact}">Contact</a>
  </nav>
</header>'''

FOOT = '''<footer class="foot">
  <p>Rhett Boyakin · Creative Director. Copywriter. Maker of Awesome Thingys®.</p>
  <p><a href="mailto:rhettboyakin@gmail.com">rhettboyakin@gmail.com</a></p>
</footer>'''

CSS = r'''
:root {
  --bg: #0c0c0c;
  --paper: #f3eee4;
  --mute: #9b9488;
  --line: #2a2723;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--paper);
  font-family: "Figtree", system-ui, sans-serif;
  font-weight: 400;
  line-height: 1.45;
}
a { color: inherit; text-decoration: none; }
img { max-width: 100%; display: block; height: auto; }
.nav {
  display: flex; justify-content: space-between; align-items: baseline;
  padding: 1.4rem 6vw 0;
}
.wordmark { letter-spacing: 0.12em; text-transform: uppercase; font-size: 0.78rem; font-weight: 600; }
.nav nav { display: flex; gap: 1.4rem; font-size: 0.9rem; color: var(--mute); }
.nav nav a:hover { color: var(--paper); }
.hero { padding: 12vh 6vw 8vh; max-width: 58rem; }
.hero h1 {
  font-family: "Newsreader", Georgia, serif;
  font-weight: 500;
  font-size: clamp(2.2rem, 5.4vw, 4.4rem);
  line-height: 1.08;
  letter-spacing: -0.02em;
}
.hero .sub {
  margin-top: 1.4rem;
  color: var(--mute);
  max-width: 36rem;
  font-size: 1.05rem;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem 1.2rem;
  padding: 0 6vw 8vh;
}
@media (max-width: 760px) { .grid { grid-template-columns: 1fr; } }
.card { display: block; }
.card .thumb {
  background: #1a1816;
  aspect-ratio: 4/3;
  overflow: hidden;
}
.card img { width: 100%; height: 100%; object-fit: cover; transition: transform .4s ease; }
.card:hover img { transform: scale(1.03); }
.card .meta { padding: 0.7rem 0 1.2rem; display: flex; justify-content: space-between; gap: 1rem; align-items: baseline; }
.card .meta strong { font-weight: 600; font-size: 0.95rem; }
.card .meta span { color: var(--mute); font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; }
.badge { color: var(--paper); }
.page { padding: 4vh 6vw 8vh; max-width: 52rem; margin: 0 auto; }
.page h1 {
  font-family: "Newsreader", Georgia, serif;
  font-size: clamp(2rem, 4vw, 3.4rem);
  font-weight: 500;
  line-height: 1.1;
  margin: 1.2rem 0 0.6rem;
}
.kicker { color: var(--mute); letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.72rem; }
.lede { font-size: 1.15rem; color: #d9d2c6; margin: 1rem 0 2rem; max-width: 38rem; }
.stills { display: grid; gap: 1.2rem; margin: 2rem 0; }
.stills img { width: 100%; }
.player {
  position: relative; padding-top: 56.25%; background: #111; margin: 1.2rem 0;
}
.player iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.list { margin: 0 0 2rem 1.1rem; color: #d9d2c6; }
.list li { margin: 0.25rem 0; }
.cta {
  display: inline-block; margin-top: 0.4rem; margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--paper); padding-bottom: 2px;
}
.foot {
  padding: 3rem 6vw 4rem;
  border-top: 1px solid var(--line);
  color: var(--mute);
  font-size: 0.88rem;
  display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
}
.foot a { color: var(--paper); }
.contact-block { padding: 18vh 6vw 20vh; max-width: 40rem; }
.contact-block h1 {
  font-family: "Newsreader", Georgia, serif;
  font-size: clamp(2.4rem, 5vw, 4rem);
  font-weight: 500;
}
.contact-block a.big { display: block; margin-top: 1.2rem; font-size: 1.3rem; }
'''

def page_shell(title, body, home="../index.html", contact="../contact.html"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600&family=Newsreader:opsz,wght@6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{'css/site.css' if home=='index.html' else '../css/site.css'}">
</head>
<body>
{NAV.format(home=home, contact=contact)}
{body}
{FOOT}
</body>
</html>
'''

# index
cards = []
for p in PROJECTS:
    cover = ext_cover(p["slug"]) if os.path.isdir(os.path.join(ROOT,"img",p["slug"])) else None
    href = f"work/{p['slug']}.html"
    img = f"img/{p['slug']}/{cover}" if cover else ""
    year = p["year"] + (" · new" if p.get("new") else "")
    cards.append(f'''<a class="card" href="{href}">
  <div class="thumb">{f'<img src="{img}" alt="{p["title"]}">' if img else ''}</div>
  <div class="meta"><strong>{p["title"]}</strong><span>{year}</span></div>
</a>''')

index_body = f'''
<section class="hero">
  <h1>Creative Director. Copywriter. Maker of Awesome Thingys®.</h1>
  <p class="sub">Utah CD for brands like Zions and VSP. Now building with AI — Found Money Friend, and more. Currently in a Leland AI cohort, with a certificate on the way.</p>
</section>
<section class="grid" id="work">
{''.join(cards)}
</section>
'''
open(os.path.join(ROOT,"index.html"),"w").write(page_shell("Rhett Boyakin", index_body, home="index.html", contact="contact.html"))

os.makedirs(os.path.join(ROOT,"css"), exist_ok=True)
open(os.path.join(ROOT,"css/site.css"),"w").write(CSS)

os.makedirs(os.path.join(ROOT,"work"), exist_ok=True)
for p in PROJECTS:
    vids = video_ids(p["slug"]) if p["slug"] != "found-money-friend" else []
    cover = ext_cover(p["slug"])
    imgs = stills(p["slug"])
    bits = [f'<p class="kicker">{p["year"]}{" · " + p["role"] if p.get("role") else ""}</p>',
            f'<h1>{p["title"]}</h1>']
    if p.get("lede"):
        bits.append(f'<p class="lede">{p["lede"]}</p>')
    if p.get("live"):
        bits.append(f'<a class="cta" href="{p["live"]}">Open the live demo</a>')
    if p.get("list"):
        bits.append("<ul class='list'>" + "".join(f"<li>{x}</li>" for x in p["list"]) + "</ul>")
    if cover:
        bits.append(f'<div class="stills"><img src="../img/{p["slug"]}/{cover}" alt="{p["title"]}"></div>')
    for v in vids:
        src = f"https://www-ccv.adobe.io/v1/player/ccv/{v}/embed?bgcolor=%230c0c0c&lazyLoading=true&api_key=BehancePro2View"
        bits.append(f'<div class="player"><iframe title="Video" src="{src}" allowfullscreen allow="fullscreen"></iframe></div>')
    if vids:
        orig = f"https://rhettboyakinportfolio.com/{p['slug']}"
        bits.append(f'<p class="lede">If a player doesn’t load here, it’s on the <a class="cta" href="{orig}">original case study</a>.</p>')
    still_html = "".join(f'<img src="../img/{p["slug"]}/{fn}" alt="">' for fn in imgs)
    if still_html:
        bits.append(f'<div class="stills">{still_html}</div>')
    body = '<article class="page">' + "".join(bits) + "</article>"
    open(os.path.join(ROOT,"work", f"{p['slug']}.html"),"w").write(
        page_shell(f"{p['title']} — Rhett Boyakin", body)
    )

contact_body = '''
<section class="contact-block">
  <h1>Say hey.</h1>
  <a class="big" href="mailto:rhettboyakin@gmail.com">rhettboyakin@gmail.com</a>
  <p class="lede" style="margin-top:2rem">Also on <a href="https://github.com/rhettboyakin-code">GitHub</a>.</p>
</section>
'''
open(os.path.join(ROOT,"contact.html"),"w").write(page_shell("Contact — Rhett Boyakin", contact_body, home="index.html", contact="contact.html"))

print("built index +", len(PROJECTS), "projects")
