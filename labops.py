"""AI for Laboratory Operations research, tool, and publication page rendering."""
from html import escape as esc
from pathlib import Path
from artifacts import render_artifacts
from acknowledgments import render_summary, render_full

def register(page,hero,section,icon,external,read):
 groups=read('labops_groups'); tools=read('labops_tools'); papers=read('publications'); roadmap=read('labops_roadmap')
 gm={g['slug']:g for g in groups}; pm={p['id']:p for p in papers}; tm={t['slug']:t for t in tools}
 base='projects/ai4labops/'
 def tool_url(t):return base+'tools/'+t['slug']+'/'
 def subnav(l):return '<nav class="hub-nav wrap" aria-label="AI for Laboratory Operations navigation">'+''.join(f'<a href="{l(base+route)}">{label}</a>' for route,label in [('', 'Overview'),('research/','Research themes'),('tools/','Tools & benchmarks'),('publications/','Publications'),('acknowledgments/','Acknowledgments')])+'</nav>'
 def header(title,summary,l,parent=None):return hero(title,summary,l,parent or (base,'AI for Laboratory Operations'))+subnav(l)
 def badge(p):return f'<span class="status-badge {p["status"].lower()}">{esc(p["status"])}</span>'
 def paper_card(p,l):
  citation=f'{p["authors"]} ({p["year"]}). {p["title"]}. {p["venue"]}'+(f', pp. {p["pages"]}' if p['pages'] else '')+('. Submitted.' if p['status']=='Submitted' else '.')
  action=f'<a class="text-link" href="{external(p["url"])}">Read paper ↗</a>' if p['url'] else ''
  if p.get('blog_path'):action+=f'<a class="text-link" href="{l(p["blog_path"])}">Read research story →</a>'
  return f'<article class="paper-entry" id="{p["id"]}"><div class="paper-meta"><span>{esc(p['venue'])}</span>{badge(p)}</div><h3>{esc(p["title"])}</h3><p class="paper-authors">{esc(p["authors"])}</p><p class="resource-pending">{esc(p.get('submission_status', ''))}</p><div class="paper-actions">{action}<a href="{l(tool_url(tm[p["tool"]]))}">Explore {esc(tm[p["tool"]]["name"])} →</a></div><details><summary>Citation</summary><p>{esc(citation)}</p></details></article>'
 def tool_card(t,l):
  g=gm[t['group']];p=pm.get(t.get('paper'))
  return f'<article class="tool-card {g["color"]}"><div class="tool-card-top">{icon(dict(g,icon=t["icon"]))}{badge(p) if p else '<span class="status-badge neutral">Research tool</span>'}</div><span class="label">{esc(g["title"])}</span><h3><a href="{l(tool_url(t))}">{esc(t["name"])}</a></h3><p>{esc(t["summary"])}</p><a class="text-link" href="{l(tool_url(t))}">Research & resources →</a></article>'
 def group_cards(l):return '<div class="project-grid">'+''.join(f'<a class="theme-card {g["color"]}" href="{l(base+"research/"+g["slug"]+"/")}">{icon(g)}<h3>{g["title"]}</h3><p>{g["summary"]}</p><span class="text-link">Explore research →</span></a>' for g in groups)+'</div>'
 def heading(kicker,title):return f'<div class="section-heading"><div><div class="eyebrow">{kicker}</div><h2>{title}</h2></div></div>'
 def paper_list(l,selection):return '<div class="paper-list">'+''.join(paper_card(p,l) for p in selection)+'</div>'
 def research_stories(l,slugs=None):
  stories=[p for p in read('blogs') if p.get('related','').startswith(base+'tools/') and (slugs is None or p['related'].split('/')[-2] in slugs)]
  if not stories:return ''
  return section(heading('Research stories','The ideas behind the tools.')+'<div class="community-grid">'+''.join(f'<article class="community-card"><span class="label">{esc(p["tag"])}</span><h3><a href="{l("blogs/"+p["slug"]+"/")}">{esc(p["title"])}</a></h3><p>{esc(p["summary"])}</p><a class="text-link" href="{l("blogs/"+p["slug"]+"/")}">Read the story →</a></article>' for p in stories)+'</div>')
 def hub(l):
  mission='<div class="mission-panel"><div><div class="eyebrow">The mission</div><h2>Scientific operations.<br>Intelligent by design.</h2></div><p>Build AI tools for laboratory operations that support operational excellence and predictive maintenance. Our research connects diverse operational evidence with grounded reasoning, expert oversight, and useful decision support.</p></div>'
  layers='<div class="ecosystem"><div class="ecosystem-layer"><span class="layer-number">01</span><div><h3>Operational evidence</h3><p>Engineering drawings · Incident records · Laboratory documents · Policies & procedures</p></div></div><div class="ecosystem-layer"><span class="layer-number">02</span><div><h3>Intelligence foundations</h3><p>Multimodal retrieval · Retrieval-augmented generation · Agentic reasoning · Evaluation</p></div></div><div class="ecosystem-layer"><span class="layer-number">03</span><div><h3>Research & tools</h3><p>Knowledge discovery · Safety & risk intelligence · Compliance & governance</p></div></div><div class="ecosystem-layer"><span class="layer-number">04</span><div><h3>Decision support</h3><p>Discover evidence · Assess hazards · Review decisions · Share insights</p></div></div></div>'
  return header('AI for Laboratory Operations','Intelligence for the people, records, and decisions that keep scientific laboratories moving.',l,('projects/','Projects'))+section(mission)+research_stories(l)+section(render_summary(read('acknowledgments'),l))+section(heading('Three connected directions','From evidence to informed action.')+group_cards(l))+section(heading('The ecosystem','A connected research architecture.')+layers)+section(heading('Tools & benchmarks','Explore the research portfolio.')+'<div class="tool-grid">'+''.join(tool_card(t,l) for t in tools)+'</div>')+section(heading('Research outputs','Publications & submissions.')+paper_list(l,papers)+f'<p><a class="text-link" href="{l(base+"publications/")}">Browse AI for Laboratory Operations publications →</a></p>')
 page(base.rstrip('/'),'AI for Laboratory Operations','projects',hub)
 page(base+'acknowledgments','Leadership, collaborators & support','projects',lambda l:header('Leadership, collaborators & support','Recognizing the people, partnerships, and support behind AI for Laboratory Operations.',l)+section(render_full(read('acknowledgments'),l)))
 page(base+'research','AI for Laboratory Operations research','projects',lambda l:header('Research themes','Three complementary directions for intelligent laboratory operations.',l)+section(group_cards(l)))
 for g in groups:
  def theme(l,g=g):
   items=''.join(f'<li>{esc(x)}</li>' for x in g['focus'])
   selected=[t for t in tools if t['group']==g['slug']]
   return header(g['title'],g['summary'],l,(base+'research/','AI for Laboratory Operations research'))+section(f'<div class="detail-grid"><div class="prose"><div class="eyebrow">The research question</div><h2>{esc(g["question"])}</h2></div><aside class="metadata"><h3>Research focus</h3><ul>{items}</ul></aside></div>')+section(heading('Projects in this theme','Tools & research.')+'<div class="tool-grid">'+''.join(tool_card(t,l) for t in selected)+'</div>')+section(heading('Related work','Publications & submissions.')+paper_list(l,[p for p in papers if p['tool'] in {t['slug'] for t in selected}]))+research_stories(l,{t['slug'] for t in selected})
  page(base+'research/'+g['slug'],g['title'],'projects',theme)
 def tool_index(l):
  body=''
  for g in groups:body+=heading('Research theme',g['title'])+'<div class="tool-grid">'+''.join(tool_card(t,l) for t in tools if t['group']==g['slug'])+'</div>'

  return header('Tools & benchmarks','Research frameworks, retrieval tools, and evaluation resources across AI for Laboratory Operations.',l)+section(body)
 page(base+'tools','AI for Laboratory Operations tools','projects',tool_index)
 def resources(t,l):
  links=t.get('links',[])
  body='<div id="resources">'+render_artifacts(Path(__file__).resolve().parent,t['slug'],l)
  body+=''.join(f'<p><a class="text-link" href="{external(x["url"]) if x.get("url") else l(x["path"])}">{esc(x["label"])} ↗</a></p>' for x in links)
  return section(body+'</div>') if links or (Path(__file__).resolve().parent/'artifacts'/t['slug']).exists() else ''
 def contributors(t,l):
  members=t.get('contributors',[])
  body=heading('People behind the project','Contributors.')
  if not members:return ''
  body+='<div class="contributor-grid">'
  for person in members:
   name=esc(person['name']);photo=person.get('photo')
   image=f'<img src="{l(photo)}" alt="{name}" loading="lazy">' if photo else '<span class="avatar-placeholder" aria-hidden="true">'+''.join(x[0] for x in person['name'].split()[:2])+'</span>'
   email=person.get('email','');contact=f'<a href="mailto:{esc(email,quote=True)}">Contact ↗</a>' if email else ''
   body+=f'<article class="contributor-card">{image}<div><h3>{name}</h3><p>{esc(person["role"])}</p>{contact}</div></article>'
  return section(body+'</div>')
 for t in tools:
  def tool_detail(l,t=t):
   g=gm[t['group']];p=pm.get(t.get('paper'))
   note='<div class="notice">Submitted work · Venue and submission status supplied by the authors. </div>' if p and p['status']=='Submitted' else ''
   outputs=''.join(f'<li>{esc(x)}</li>' for x in t['outputs'])
   return header(t['name'],t['summary'],l,(base+'tools/','AI for Laboratory Operations tools'))+section(f'<div class="detail-grid"><div class="prose">{note}<div class="eyebrow">Research question</div><h2>{esc(t["question"])}</h2><h2>Research approach</h2><p>{esc(t["approach"])}</p><h2>Research outputs & focus</h2><ul>{outputs}</ul></div><aside class="metadata {g["color"]}">{icon(dict(g,icon=t["icon"]))}<h3 style="margin-top:20px">Research profile</h3><dl><dt>Theme</dt><dd><a class="text-link" href="{l(base+"research/"+g["slug"]+"/")}">{g["title"]} →</a></dd><dt>Publication status</dt><dd>{badge(p) if p else 'Research tool'}</dd><dt>Venue</dt><dd>{esc(p['venue']) + ' · ' + str(p['year']) if p else 'Research in progress'}</dd></dl><a class="text-link" href="#resources">Explore project artifacts ↓</a></aside></div>')+resources(t,l)+contributors(t,l)+(section(heading('Related publications','The research behind the tool.')+paper_list(l,[p for p in papers if p['tool']==t['slug']])) if any(p['tool']==t['slug'] for p in papers) else '')
  page(tool_url(t).rstrip('/'),t['name'],'projects',tool_detail)
  for alias in t.get('aliases',[]):
   page(base+'tools/'+alias,t['name'],'projects',tool_detail)
 page(base+'publications','AI for Laboratory Operations publications','publications',lambda l:header('AI for Laboratory Operations publications','Published papers, preprints, and submitted work. Submission labels reflect the status supplied by the authors.',l)+section(paper_list(l,papers)))

 return paper_list
