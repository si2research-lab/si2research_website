"""Build the SI² website with Python's standard library."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlparse
import json, os, shutil
from artifacts import discover, render_artifacts
from acknowledgments import render_summary
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
def read(name): return json.loads((ROOT/'content'/f'{name}.json').read_text())
site=read('site'); projects=read('projects'); areas=[a for a in read('areas') if any(p['area']==a['slug'] for p in projects)]; initiatives=[]; amap={a['slug']:a for a in areas}
tool_slugs={t['slug'] for t in read('labops_tools')}
hpc_slugs={p['slug'] for p in read('hpc_research')}
discover(ROOT, {p['slug'] for p in projects} | tool_slugs | hpc_slugs)
paths={'layers':'<path d="m3 7 9-5 9 5-9 5zM3 12l9 5 9-5M3 17l9 5 9-5"/>','chip':'<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9zM9 2v3m6-3v3M9 19v3m6-3v3M2 9h3m-3 6h3m14-6h3m-3 6h3"/>','flask':'<path d="M9 3h6m-5 0v7L4 19q-1 2 2 2h12q3 0 2-2l-6-9V3M7 15h10"/><circle cx="11" cy="17" r=".7"/>','atom':'<ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1"/>','cube':'<path d="m12 2 9 5v10l-9 5-9-5V7zM3 7l9 5 9-5M12 12v10M7 4.8l10 5.5v4"/>'}
paths.update({
 'search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 10h6m-3-3v6"/>',
 'shield':'<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6zM8 12l3 3 5-6"/>',
 'check':'<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 2h6v4H9zM8 13l3 3 5-6"/>',
 'drawing':'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 17V7h10M7 13h6v4h4V7M3 9h2m-2 6h2M9 3v2m6-2v2"/>',
 'dataset':'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
 'dialogue':'<path d="M3 3h14v11H9l-5 4v-4H3zM17 8h4v13l-5-3h-5v-4"/>'
})
def icon(a): return f'<span class="icon {a["color"]}" aria-hidden="true"><svg viewBox="0 0 24 24">{paths[a["icon"]]}</svg></span>'
def external(url):
 if urlparse(url).scheme not in ('https','http'): raise ValueError('Links must use http or https')
 return esc(url,quote=True)
def card(p,link):
 a=amap[p['area']]
 return f'''<article class="project-card {a['color']}" data-project data-area="{a['slug']}"><a href="{link('projects/'+p['slug']+'/')}" aria-label="Explore {esc(p['title'])}"><div class="project-art">{icon(a)}</div></a><div class="project-content"><a class="label" href="{link('research/'+a['slug']+'/')}">{esc(a['title'])}</a><h3><a href="{link('projects/'+p['slug']+'/')}">{esc(p['title'])}</a></h3><p>{esc(p['summary'])}</p><div class="project-bottom"><span>Project overview</span><a class="text-link" href="{link('projects/'+p['slug']+'/')}">Explore <span aria-hidden="true">↗</span></a></div></div></article>'''
def area_cards(link): return '<div class="areas">'+''.join(f'''<a class="area-card {a['color']}" href="{link('research/'+a['slug']+'/')}">{icon(a)}<h3>{a['title']}</h3><p>{a['summary']}</p><span class="arrow" aria-hidden="true">↗</span></a>''' for a in areas)+'</div>'
def page(route,title,active,render):
 dest=OUT/route/'index.html'; dest.parent.mkdir(parents=True,exist_ok=True)
 def link(target=''): return os.path.relpath(OUT/target,dest.parent).replace(os.sep,'/')+('/' if not Path(target).suffix else '')
 nav=''.join(f'<a href="{link(r)}"'+(' aria-current="page"' if key==active else '')+(' class="nav-contact"' if key=='contact' else '')+f'>{label}</a>' for r,label,key in [('', 'Home','home'),('research/','Research','research'),('projects/','Projects','projects'),('people/','People','people'),('publications/','Publications','publications'),('blogs/','Stories','blogs'),('contribute/','Contribute','contribute')])
 description=site['description']+' Explore SI² research areas, projects, and initiatives.'
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} | SI² — SuperIntelligence for Science</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#101f35"><link rel="icon" href="{link('assets/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{link('assets/style.css')}"><script src="{link('assets/site.js')}" defer></script></head><body class="{'home-page' if not route else 'people-page inner-page' if route=='people' else 'inner-page'}"><a href="#main" class="skip">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{link()}"><span class="brand-mark" aria-hidden="true">SI<sup>2</sup></span><span class="brand-wordmark">SuperIntelligence<span class="brand-second-line">for Science</span></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false">Menu</button><nav class="navigation" id="navigation" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{render(link)}</main><footer class="site-footer"><div class="wrap footer-inner"><div><a class="brand footer-brand" href="{link()}" aria-label="SuperIntelligence for Science">SI<sup>2</sup></a><p>{esc(site['tagline'])}</p></div><div class="footer-links"><a href="{link('projects/')}">Explore projects</a><a href="{link('contribute/')}">Contribute</a><a href="{link('contact/')}">Contact</a></div><p>© SI² — SuperIntelligence for Science<br>Research, people & open resources</p></div></footer></body></html>'''
 dest.write_text(html)
def hero(title,summary,link,parent=None):
 crumbs=f'<a href="{link()}">Home</a><span>/</span>'
 if parent: crumbs+=f'<a href="{link(parent[0])}">{parent[1]}</a><span>/</span>'
 return f'<div class="page-hero"><div class="wrap"><div class="breadcrumbs">{crumbs}{esc(title)}</div><div class="eyebrow">SI² — SuperIntelligence for Science</div><h1>{esc(title)}</h1><p>{esc(summary)}</p></div></div>'
def section(body):return f'<section class="section"><div class="wrap">{body}</div></section>'
def init_cards(link):return '<div class="initiative-grid">'+''.join(f'<article class="initiative-card"><span class="label">Cross-cutting initiative</span><h3>{i["title"]}</h3><p>{i["summary"]}</p><a href="{link("initiatives/"+i["slug"]+"/")}">Explore initiative ↗</a></article>' for i in initiatives)+'</div>'
def home_spotlight(link):
 items=[('artifacts/blueprint/diagram.png','Engineering intelligence','BLUEPRINT','Multimodal retrieval for complex engineering drawings.','projects/ai4labops/tools/blueprint/','WACV 2027 · Accepted'),('artifacts/safelens/diagram.png','Knowledge discovery','SafeLens','Explore organizational safety records for actionable insights.','projects/ai4labops/tools/safelens/','JCDL · Published'),('assets/hpc-landscape.svg','Trustworthy computing','Recall Is Not Honesty','Benchmarking multi-agent architectures for HPC operational analytics.','projects/ai-for-hpc/recall-is-not-honesty/','SC ’26 · Accepted')]
 cards=''
 for image,theme,title,summary,url,status in items:
  cards+=f'<article class="featured-research"><a class="featured-image" href="{link(url)}"><img src="{link(image)}" alt="{title} research overview" loading="lazy"><span>{status}</span></a><div class="featured-copy"><span class="label">{theme}</span><h3><a href="{link(url)}">{title}</a></h3><p>{summary}</p><a class="text-link" href="{link(url)}">Explore the research ↗</a></div></article>'
 return '<section class="section home-featured"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">Research in focus</div><h2>From scientific questions<br>to real-world systems.</h2></div><a class="text-link" href="'+link('publications/')+'">Publications & research →</a></div><div class="featured-grid">'+cards+'</div></div></section>'
def network_art(link):
 art=(ROOT/'assets/research-network.svg').read_text()
 for slug in ('hpc','quantum','autonomous','manufacturing','labops'):
  art=art.replace('href="../research/'+slug+'/"','href="'+link('research/'+slug+'/')+'"')
 return art
def home(link):
 return '<section class="hero"><div class="wrap"><div class="eyebrow">SI² Research</div><h1>SuperIntelligence<br><em>for Science.</em></h1><p>Research in trustworthy AI for scientific computing and laboratory operations.</p><div class="actions"><a class="button" href="'+link('projects/')+'">Explore research →</a><a class="button secondary" href="'+link('publications/')+'">Publications</a></div></div></section>'+home_spotlight(link)+section('<div class="section-heading"><h2>Research areas</h2></div>'+area_cards(link))
def catalogue(link):
 filters='<div class="filters" role="group" aria-label="Filter projects by research area"><button data-filter="all" aria-pressed="true">All projects</button>'+''.join(f'<button data-filter="{a["slug"]}" aria-pressed="false">{a["title"]}</button>' for a in areas)+'</div>'
 return hero('Our projects','Explore the ideas, tools, and research taking shape across SI².',link)+section('<div class="search-row"><label for="project-search" class="eyebrow">Find a project</label><input id="project-search" type="search" placeholder="Search by name or topic…"><span id="result-count" role="status"></span></div>'+filters+'<div class="project-grid">'+''.join(card(p,link) for p in projects)+'</div><p id="empty-results" role="status" hidden>No projects match. Try another search or research area.</p>')
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir();shutil.copytree(ROOT/'assets',OUT/'assets',ignore=shutil.ignore_patterns('*.mov'));(OUT/'.nojekyll').touch()
shutil.copytree(ROOT/'artifacts',OUT/'artifacts')
page('','Home','home',home)
page('research','Research','research',lambda l:hero('Research without silos','Trustworthy AI for scientific computing and laboratory operations.',l)+section(area_cards(l)))
page('projects','Projects','projects',catalogue)
for a in areas:
 page('research/'+a['slug'],a['title'],'research',lambda l,a=a:hero(a['title'],a['summary'],l,('research/','Research'))+section(f'<div class="section-heading"><div>{icon(a)}<h2>Projects in this area</h2></div></div><div class="project-grid">'+''.join(card(p,l) for p in projects if p['area']==a['slug'])+'</div>'))
for p in projects:
 if p['slug'] in ('ai4labops','ai-for-hpc'): continue
 def detail(l,p=p):
  a=amap[p['area']]; resources=''.join(f'<p><a class="text-link" href="{external(x["url"])}">{esc(x["label"])} ↗</a></p>' for x in p['links']) or ''
  people=', '.join(esc(x) for x in p['contributors']) or ''
  extra=''
  return hero(p['title'],p['summary'],l,('projects/','Projects'))+section(f'<div class="detail-grid"><div class="prose"><h2>About the project</h2><p>{esc(p["body"])}</p>{extra}{resources}{render_artifacts(ROOT,p['slug'],l)}<p>{people}</p></div><aside class="metadata"><h3>Project information</h3><dl><dt>Research area</dt><dd><a class="text-link" href="{l("research/"+a["slug"]+"/")}">{a["title"]} →</a></dd><dt>Profile status</dt><dd>{esc(p["status"])}</dd></dl></aside></div>')
 page('projects/'+p['slug'],p['title'],'projects',detail)
def contact(l):
 links=''
 if site['email']:links+=f'<p><a class="text-link" href="mailto:{esc(site["email"],quote=True)}">{esc(site["email"])}</a></p>'
 if site['github']:links+=f'<p><a class="text-link" href="{external(site["github"])}">SI² on GitHub ↗</a></p>'
 return hero('Let’s connect','Connect around scientific questions, research projects, and shared opportunities.',l)+section('<div class="empty-state"><h2>Start a conversation.</h2><p>'+ (esc(site['affiliation']) if site['affiliation'] else '')+'</p>'+links+f'<a class="text-link" href="{l("projects/")}">Explore the portfolio →</a></div>')
page('contact','Contact','contact',contact)
page('contribute','Contribute','contribute',lambda l:hero('Contribute','Add research and resources through GitHub.',l)+section('<div class="prose"><h2>Upload project artifacts</h2><p>Open artifacts/&lt;project-slug&gt;/ in GitHub, choose Add file → Upload files, and open a pull request. PDFs, images, videos, and downloads appear automatically after merge.</p><h2>Update research content</h2><p>Edit the matching JSON entry in content/. The README documents project fields, supported files, and local checks.</p><a class="button" href="'+external(site['github']+'/blob/main/README.md')+'">Read the contribution guide ↗</a></div>'))
from labops import register
labops_papers=register(page,hero,section,icon,external,read)
from portfolio import register as register_portfolio
register_portfolio(page,hero,section,read,labops_papers)
from community import register as register_community
register_community(page,hero,section,read)
page('404','Page not found','',lambda l:hero('A little off the map.','This page could not be found. Continue exploring the SI² portfolio.',l)+section(f'<a class="button" href="{l()}">Return home →</a>'))
# A relative-path-safe 404 for GitHub Pages repositories, where the request depth is unknown.
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | SI²</title><body style="font:18px system-ui;background:#f7f9fc;color:#172337;padding:10vw"><h1>Page not found.</h1><p>Check the address or use your browser’s Back button to return to SI².</p></body></html>')
print(f'Built {len(list(OUT.rglob("*.html")))} HTML pages in {OUT}')
