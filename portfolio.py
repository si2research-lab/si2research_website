"""People directory and AI for HPC research pages."""
from html import escape as esc
from pathlib import Path
from artifacts import render_artifacts

def register(page,hero,section,read,labops_papers):
 people=read('people');research=read('hpc_research');base='projects/ai-for-hpc/'
 def heading(kicker,title):return f'<div class="section-heading"><div><div class="eyebrow">{kicker}</div><h2>{title}</h2></div></div>'
 def person_card(p,l):
  name=esc(p.get('display_name',p['name']));photo=p.get('photo')
  image=f'<img src="{l(photo)}" alt="{name}" loading="lazy">' if photo else '<span class="directory-initials" aria-hidden="true">'+''.join(x[0] for x in p['name'].split()[:2])+'</span>'
  contact=f'<a class="text-link" href="mailto:{esc(p["email"],quote=True)}">Contact ↗</a>' if p['email'] else ''
  return f'<article class="person-card"><div class="person-photo">{image}</div><div class="person-info"><span class="label">{esc(p["role"])}</span><h3>{name}</h3><p>{esc(p["affiliation"])}</p>'+ (f'<p class="person-division">{esc(p["division"])}</p>' if p['division'] else '')+contact+'</div></article>'
 def directory(l):
  result=hero('People','Researchers, scientific collaborators, and domain experts working together across the SI² portfolio.',l)
  categories=[('pi','Research leadership','Principal Investigator'),('researchers','Core research team','Researchers'),('internal','Scientific partnerships','Internal collaborators & subject-matter experts'),('external','Across institutions','External collaborators & subject-matter experts'),('technical','Research enablement','Technical collaborators'),('alumni','Our wider community','Former researchers')]
  for key,kicker,title in categories:
   members=[p for p in people if p['category']==key]
   if members:result+=section(heading(kicker,title)+f'<div class="people-grid {"pi-grid" if key=="pi" else ""}">'+''.join(person_card(p,l) for p in members)+'</div>')

  return result
 page('people','People','people',directory)
 def badge(p):return f'<span class="status-badge {p["status"].lower()}">{esc(p["status"])}</span>'
 def research_card(p,l):
  return f'<article class="hpc-card"><div class="paper-meta">{badge(p)}<span>{esc(p["venue"]) if p["venue"] else "Research in progress"}</span></div><h3><a href="{l(base+p["slug"]+"/")}">{esc(p["short_title"])}</a></h3><p>{esc(p["summary"])}</p><a class="text-link" href="{l(base+p["slug"]+"/")}">Explore research →</a></article>'
 def hpc_nav(l):return f'<nav class="hub-nav wrap" aria-label="AI for HPC research"><a href="{l(base)}">Overview</a>'+''.join(f'<a href="{l(base+p["slug"]+"/")}">{esc(p["short_title"])}</a>' for p in research)+'</nav>'
 def author_list(p):
  equal=p['equal_contribution'];orgs=list(dict.fromkeys(a['affiliation'] for a in p['authors']))
  names=', '.join(esc(a['name'])+ ('<sup>*</sup>' if a['name'] in equal else '')+f'<sup>{orgs.index(a["affiliation"])+1}</sup>' for a in p['authors'])
  return f'<div class="author-block"><p>{names}</p><ol>'+''.join(f'<li>{esc(org)}</li>' for org in orgs)+'</ol><p class="resource-pending">* Equal contribution, as indicated in the supplied author list.</p></div>'
 def hpc(l):
  return hero('AI for HPC','Trustworthy operational analytics and defensible decisions for high-performance computing.',l,('projects/','Projects'))+hpc_nav(l)+section('<div class="mission-panel"><div><div class="eyebrow">Research focus</div><h2>Operational evidence.<br>Trustworthy intelligence.</h2></div><p>Our research explores how multi-agent systems can analyze HPC operations and telemetry, with an emphasis on trustworthy analysis and defensible decisions.</p></div>')+section(heading('Current research','Analytics that earn trust.')+'<div class="hpc-grid">'+''.join(research_card(p,l) for p in research)+'</div>')+section(heading('Research collaborations','Across institutions.')+'<div class="institution-list">'+''.join(f'<span>{esc(org)}</span>' for org in dict.fromkeys(a['affiliation'] for p in research for a in p['authors']))+'</div>')
 page(base.rstrip('/'),'AI for HPC','projects',hpc)
 for p in research:
  def detail(l,p=p):
   status=f'{p["venue"]} · {p["year"]}' if p['status']=='Accepted' else 'Ongoing research'
   return hero(p['short_title'],p['title'],l,(base,'AI for HPC'))+hpc_nav(l)+section(f'<div class="detail-grid"><div class="prose"><div class="paper-meta">{badge(p)}<span>{esc(status)}</span></div><h2 style="margin-top:25px">Research question</h2><p>{esc(p["question"])}</p><h2>Overview</h2><p>{esc(p["body"])}</p></div><aside class="metadata"><h3>Research information</h3><dl><dt>Status</dt><dd>{badge(p)}</dd><dt>Venue</dt><dd>{esc(p["venue"]) if p["venue"] else "Not announced"}</dd><dt>Research area</dt><dd>AI for HPC</dd></dl></aside></div>')+section(render_artifacts(Path(__file__).resolve().parent,p['slug'],l))+section(heading('Research team','Authors & affiliations.')+author_list(p))
  page(base+p['slug'],p['short_title'],'projects',detail)
 def hpc_publications(l):
  result='<div class="paper-list">'
  for p in research:
   result+=f'<article class="paper-entry"><div class="paper-meta">{badge(p)}<span>{esc(p["venue"]) if p["venue"] else "Ongoing research"}</span></div><h3>{esc(p["title"])}</h3><p class="paper-authors">{esc(", ".join(a["name"] for a in p["authors"]))}</p><a class="text-link" href="{l(base+p["slug"]+"/")}">Research details & affiliations →</a></article>'
  return result+'</div>'
 page('publications','Publications','publications',lambda l:hero('Publications & research','Published work, accepted papers, preprints, and ongoing research across SI².',l)+section(heading('AI for HPC','Accepted work & ongoing research.')+hpc_publications(l))+section(heading('AI for Laboratory Operations','Publications, preprints & submissions.')+labops_papers(l,read('publications'))))
