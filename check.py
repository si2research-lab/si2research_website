"""Verify generated pages, local links, unique project slugs, and page metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'dist'; errors=[]
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0;self.title=False;self.description=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.description=True
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
pages={}
for path in OUT.rglob('*.html'):
 parser=Inspect();parser.feed(path.read_text());pages[path]=parser
 if parser.h1!=1:errors.append(f'{path}: expected one h1')
 if not parser.title:errors.append(f'{path}: missing title')
 if path.name!='404.html' and not parser.description:errors.append(f'{path}: missing description')
 if len(parser.ids)!=len(set(parser.ids)):errors.append(f'{path}: duplicate ids')
for path,parser in pages.items():
 for link in parser.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  target=(path.parent/unquote(url.path)).resolve() if url.path else path
  if target.is_dir():target=target/'index.html'
  if not target.is_relative_to(OUT.resolve()):errors.append(f'{path}: link escapes site: {link}')
  elif not target.exists():errors.append(f'{path}: broken link {link}')
  elif url.fragment and target in pages and url.fragment not in pages[target].ids:errors.append(f'{path}: missing anchor {link}')
projects=json.loads((ROOT/'content/projects.json').read_text());slugs=[p['slug'] for p in projects]
assert len(slugs)==len(set(slugs)), 'Duplicate project slugs'
groups=json.loads((ROOT/'content/labops_groups.json').read_text())
tools=json.loads((ROOT/'content/labops_tools.json').read_text())
papers=json.loads((ROOT/'content/publications.json').read_text())
group_ids={g['slug'] for g in groups};tool_ids={t['slug'] for t in tools};paper_ids={p['id'] for p in papers}
assert len(tool_ids)==len(tools), 'Duplicate tool slugs'
assert len(paper_ids)==len(papers), 'Duplicate publication IDs'
for t in tools:
 assert t['group'] in group_ids and (t.get('paper') is None or t['paper'] in paper_ids), 'Invalid tool relationship'
for p in papers:
 assert p['tool'] in tool_ids, 'Invalid publication tool'
 assert p['status'] in ('Published','Preprint','Submitted','Accepted'), 'Invalid publication status'
for t in tools:
 for artifact in t.get('artifacts',[]):
  asset=ROOT/artifact['path']
  assert asset.is_file() and asset.stat().st_size>0, f'Missing artifact: {asset}'
 for person in t.get('contributors',[]):
  if person.get('photo'):assert (ROOT/person['photo']).is_file(), 'Missing contributor portrait'
people=json.loads((ROOT/'content/people.json').read_text())
for person in people:
 if person.get('photo'):assert (ROOT/person['photo']).is_file(), 'Missing directory photo'
hpc=json.loads((ROOT/'content/hpc_research.json').read_text())
assert len({p['slug'] for p in hpc}) == len(hpc), 'Duplicate HPC slugs'
from artifacts import discover
project_ids=set(slugs) | tool_ids | {p['slug'] for p in hpc}
discover(ROOT, project_ids)
for folder in (ROOT/'artifacts').iterdir():
 if not folder.is_dir():continue
 for asset in folder.iterdir():
  if asset.name in ('README.md','.gitkeep'):continue
  assert (OUT/asset.relative_to(ROOT)).is_file(), f'Artifact not copied: {asset}'
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; all internal links, fragments, metadata, and project slugs verified.')
