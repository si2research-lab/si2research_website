"""Discover public project uploads; no artifact manifest is required."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SUPPORTED = {'.pdf', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.webm', '.zip', '.csv', '.txt', '.bib', '.ipynb'}
IGNORE = {'README.md', '.gitkeep'}

def discover(root, project_slugs):
    """Fail early on unknown projects, unsupported files, or unsafe paths."""
    directory = root / 'artifacts'
    directory.mkdir(exist_ok=True)
    for folder in directory.iterdir():
        if folder.name in IGNORE:
            continue
        if folder.is_symlink() or not folder.is_dir() or folder.name not in project_slugs:
            raise ValueError(f'Unknown artifact project: {folder.name}; add its content entry first')
        for file in folder.iterdir():
            if file.name in IGNORE:
                continue
            if file.is_symlink() or not file.is_file() or not re.fullmatch(r'[a-z0-9][a-z0-9._-]*', file.name):
                raise ValueError(f'Use a flat folder and lowercase filenames without spaces: {file}')
            if file.suffix.lower() not in SUPPORTED:
                raise ValueError(f'Unsupported artifact type: {file}')
            if not 0 < file.stat().st_size < 100 * 1024 * 1024:
                raise ValueError(f'Artifact must be nonempty and under 100 MiB: {file}')

def render_artifacts(root, slug, link):
    folder = root / 'artifacts' / slug
    if not folder.exists():
        return ''
    cards = []
    for file in sorted(folder.iterdir()):
        if file.name in IGNORE:
            continue
        path = 'artifacts/' + slug + '/' + file.name
        url = escape(link(path), quote=True)
        title = escape(file.stem.replace('-', ' ').replace('_', ' ').title())
        extension = file.suffix.lower()
        media = ''
        if extension in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
            media = f'<a href="{url}"><img src="{url}" alt="{title}" loading="lazy"></a>'
        elif extension in {'.mp4', '.webm'}:
            media = f'<video controls preload="none" playsinline aria-label="{title}" src="{url}"></video>'
        size = file.stat().st_size / (1024 * 1024)
        cards.append(f'<article class="artifact-item"><h3><a href="{url}">{title} ↗</a></h3><p>{escape(extension[1:].upper())} · {size:.1f} MB</p>{media}</article>')
    return '<h2>Artifacts</h2><div class="artifact-list">' + ''.join(cards) + '</div>' if cards else ''
