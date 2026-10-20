"""Community pages based on supplied team content."""
from html import escape as esc

def register(page,hero,section,read):
 ack=read('acknowledgments')
 def heading(title):return f'<div class="section-heading"><h2>{title}</h2></div>'
 def cards(items,l):return '<div class="community-grid">'+''.join(f'<article class="community-card"><span class="label">{esc(tag)}</span><h3>{esc(title)}</h3><p>{esc(body)}</p><a class="text-link" href="{l(path)}">Explore →</a></article>' for tag,title,body,path in items)+'</div>'
 def sponsors(l):
  items=[('Operations collaboration','ORNL Operations',ack['operations'],'people/'),('Enterprise readiness','ITSD software team',ack['engineering'],'projects/ai4labops/acknowledgments/'),('Community development','SAILOR',ack['sailor']['body'],'projects/ai4labops/acknowledgments/')]
  return hero('Sponsors & partners','Recognizing the support and partnerships behind AI for Laboratory Operations.',l)+section(f'<div class="sponsor-feature"><span class="label">Sponsor acknowledgment</span><h2>{esc(ack["sponsors"][0])}</h2><p>{esc(ack["sponsors"][1])}</p><span>{esc(ack["doe"])}</span></div>')+section(heading('From research to operations.')+cards(items,l))
 page('sponsors','Sponsors & partners','sponsors',sponsors)
 posts=read('blogs')
 page('blogs','Blogs','blogs',lambda l:hero('Research perspectives','Short introductions to the ideas, systems, and collaborations shaping our work.',l)+section(cards([(p['tag'],p['title'],p['summary'],'blogs/'+p['slug']+'/') for p in posts],l)))
 def cite_text(text):
  return esc(text).replace('[1]','<a class="inline-citation" href="#reference-1">[1]</a>')
 for post in posts:
  def detail(l,p=post):
   body=''
   if p.get('announcement'):body+=f'<div class="blog-announcement"><span class="status-badge accepted">{esc(p["announcement"])}</span><span>{esc(p["reading_time"])}</span></div>'
   for index,item in enumerate(p['sections']):
    body+=f'<h2>{esc(item["heading"])}</h2><p>{cite_text(item["body"])}</p>'
    figures=p.get('figures',[])+([p['figure']] if p.get('figure') else [])
    for figure in figures:
     if figure['after_section']==index:
      body+=f'<figure class="blog-figure"><a href="{l(figure["path"])}"><img src="{l(figure["path"])}" alt="{esc(figure["alt"])}" loading="lazy"></a><figcaption>{cite_text(figure["caption"])} <a href="{esc(figure["source"],quote=True)}">Paper figure ↗</a></figcaption></figure>'
    if p.get('results') and index==p['results'].get('after_section',2):
     result=p['results']
     body+='<div class="blog-table"><table><caption>'+esc(result['caption'])+'</caption><thead><tr>'+''.join(f'<th scope="col">{esc(x)}</th>' for x in result['headers'])+'</tr></thead><tbody>'
     for row in result['rows']:
      body+='<tr><th scope="row">'+esc(row[0])+'</th>'+''.join('<td>'+esc(x)+'</td>' for x in row[1:])+'</tr>'
     body+='</tbody></table></div>'
   if p.get('resources'):
    body+=f'<div class="blog-resources"><h2>{esc(p.get("resources_heading","Paper & code"))}</h2><div class="actions">'+''.join(f'<a class="button secondary" href="{esc(x["url"],quote=True) if x.get("url") else l(x["path"])}">{esc(x["label"])} ↗</a>' for x in p['resources'])
    body+=(f'<a class="button" href="{esc(p["github_url"],quote=True)}">Code on GitHub ↗</a>' if p.get('github_url') else '')+'</div>'
    if False:body+=f'<p class="resource-pending">{esc(p["github_note"])}</p>'
    body+='</div>'
   if p.get('bibliography'):
    body+='<section class="blog-bibliography" aria-label="Bibliography"><h2>Bibliography</h2><ol>'+''.join(f'<li id="reference-1"><a href="{esc(x["url"],quote=True)}">{esc(x["text"])}</a></li>' for x in p['bibliography'])+'</ol></section>'
   return hero(p['title'],p['summary'],l,('blogs/','Research perspectives'))+section('<article class="prose blog-prose"><span class="label">Research perspective · SI² — SuperIntelligence for Science</span>'+body+f'<a class="text-link" href="{l(p["related"])}">Explore related research →</a></article>')
  page('blogs/'+post['slug'],post['title'],'blogs',detail)
 def award_card(a,l):
  url=a.get('url') or l(a['related_path'])
  return f'<article class="recognition-card"><div class="recognition-top"><span class="award-symbol" aria-hidden="true">🏆</span><span class="label">{esc(a["category"])}</span></div><span class="recognition-venue">{esc(a["venue"])}</span><h2>{esc(a["award"])}</h2><p class="award-recipient">{esc(a["authors"])}</p><h3>{esc(a["title"])}</h3><p>{esc(a["description"])}</p><a class="text-link" href="{esc(url,quote=True)}">{esc(a["link_label"])} ↗</a></article>'
 def awards(l):
  items=[('SC ’26 · Accepted','Recall Is Not Honesty','Benchmarking multi-agent architectures for trustworthy HPC operational analytics.','projects/ai-for-hpc/recall-is-not-honesty/'),('WACV 2027 · Accepted','BLUEPRINT','Multimodal retrieval for complex engineering drawings and documents.','projects/ai4labops/tools/blueprint/')]
  return hero('Awards & recognition','A place to celebrate team achievements and research milestones.',l)+section(heading('Awards & honors')+'<div class="awards-grid">'+''.join(award_card(a,l) for a in read('awards'))+'</div>')+section(heading('Research milestones · Conference acceptances')+cards(items,l))
 page('awards','Awards & recognition','awards',awards)
 def event_card(e,l):
  return f'<article class="event-card"><div class="event-date"><strong>{esc(e["date"])}</strong><span>{esc(e["status"])}</span></div><div><span class="label">{esc(e["location"])}</span><h3>{esc(e["title"])}</h3><p>{esc(e["body"])}</p><a class="text-link" href="{l("projects/ai4labops/acknowledgments/")}">Related initiative →</a></div></article>'
 events=read('events')
 page('events','Events','events',lambda l:hero('Events & scientific exchange','Symposia and opportunities to connect around AI for scientific operations.',l)+(section(heading('Upcoming events')+''.join(event_card(e,l) for e in events if e['status']=='Planned')) if any(e['status']=='Planned' for e in events) else '')+section(heading('Past events')+''.join(event_card(e,l) for e in events if e['status']=='Past')))
