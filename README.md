# SI² Research

Website: **https://si2research-lab.github.io/**

Compact research website for **SuperIntelligence for Science**. Python 3.12+ and the standard library build the site; no dependencies or database are needed.

## Contribute through GitHub

Small updates can be made entirely in the GitHub browser interface:

1. Open the relevant folder, choose **Add file → Upload files** (or edit an existing JSON file).
2. Choose **Create a new branch** and open a pull request with a short description.
3. The **Check website** workflow validates the build and local links. Review the change and merge into `main`.
4. The Pages workflow rebuilds and publishes the site automatically. Check its run for the deployed URL.

### Upload artifacts — no code or manifest changes

Put files in **`artifacts/<project-slug>/`**. Every supported file appears automatically in the project's **Artifacts** section, sorted by filename. Images are previewed, videos have playback controls, and PDFs and other files have direct links. Replace a file at the same path to update it; delete it to remove it from the page. Allow the Pages workflow to finish after merging.

Existing tool folders: `blueprint`, `safelens`, `chemsafe`, `orchid`, `regchange`. HPC folders: `recall-is-not-honesty`, `epic-plus-plus` (create the folder on first upload).

```text
artifacts/
  blueprint/
    diagram.png
    paper.pdf
    slides.pdf
    demo.mp4
  recall-is-not-honesty/
    paper.pdf
```

Use lowercase filenames with letters, digits, dots, hyphens, and underscores; no spaces or subfolders. Names become labels (`evaluation-results.csv` → “Evaluation Results”). Supported types: PDF; PNG/JPG/JPEG/WebP/GIF; MP4/WebM; ZIP/CSV/TXT/BibTeX/notebooks. Each file must be nonempty and under 100 MiB. Compress videos before uploading; GitHub's browser uploader has a smaller limit (25 MB), so use Git for larger files. Keep only material approved for public release. Notebooks are downloads, not executed. HTML, scripts, and SVG uploads are deliberately unsupported.

For repositories or externally hosted demos, edit the project's `links` list in `content/labops_tools.json` with `{"label": "Code", "url": "https://github.com/organization/project"}`.

### Update research, people, and stories

| File | Contents |
| --- | --- |
| `content/site.json` | Name, description, GitHub link, optional contact details |
| `content/projects.json` | Research project cards and overview pages |
| `content/labops_tools.json` | Tool questions, methods, links, contributors, publication relationships |
| `content/labops_groups.json` | Laboratory research themes |
| `content/publications.json` | Laboratory paper citations, venues, status and URLs |
| `content/hpc_research.json` | HPC research, authors, status and affiliations |
| `content/people.json` | Directory; optional portraits under `assets/tools/developers/` |
| `content/blogs.json` | Research stories, figures and references |
| `content/awards.json`, `content/events.json`, `content/acknowledgments.json` | Recognition, events and support |

Copy a nearby entry to preserve its required fields. Use valid JSON (double quotes, no trailing commas), stable unique slugs, and existing relationship IDs. Leave unavailable optional fields empty rather than adding “coming soon” text. Preserve accurate attribution and publication status.

### Add a project

For a standalone project, append an entry to `content/projects.json`:

```json
{
  "slug": "example-project",
  "title": "Example Project",
  "area": "hpc",
  "summary": "One sentence describing the research.",
  "status": "Ongoing",
  "body": "The research question, approach, and current work.",
  "contributors": ["Researcher Name"],
  "links": [{"label": "Code", "url": "https://github.com/organization/project"}]
}
```

Choose an area from `content/areas.json`. The project card, detail page, research-area listing, and `artifacts/example-project/` discovery are generated together. Add a new laboratory tool by copying a complete entry in `content/labops_tools.json` instead; it automatically gets a tool page and artifact discovery. Add associated papers to `content/publications.json` with matching tool IDs. For new HPC studies, copy an entry in `content/hpc_research.json`.

## Preview and validate

```bash
git clone https://github.com/si2research-lab/si2research-lab.github.io.git
cd si2research-lab.github.io
python3 build.py
python3 check.py
python3 -m http.server 8000 --directory dist
```

Visit http://localhost:8000. Rebuild after changes. Validation checks artifact folders/types, relationships, metadata, and all local links and anchors. `dist/` is generated and ignored; never edit or commit it. Styling lives in `assets/style.css`, interactions in `assets/site.js`, and page layouts in the Python modules.

## GitHub Pages setup (maintainer, once)

1. Open [Settings → Pages](https://github.com/si2research-lab/si2research-lab.github.io/settings/pages).
2. Under **Build and deployment → Source**, select **GitHub Actions**. Do **not** select “Deploy from a branch”: the repository contains Python source, and branch publishing renders this README instead of the generated website.
3. Open [Actions → Deploy SI² to GitHub Pages](https://github.com/si2research-lab/si2research-lab.github.io/actions/workflows/deploy.yml) and choose **Run workflow** on `main`, or push a change to `main`.
4. Wait for the deployment to succeed, then visit **https://si2research-lab.github.io/**.

The workflow builds and checks `dist/`, then publishes that generated directory. Keep `dist/` ignored. The repository name `si2research-lab.github.io` gives the organization its root website URL; no repository suffix is needed.

### If the homepage shows the README or project links return 404

Confirm **Pages → Source → GitHub Actions** first. Branch publishing and the custom deployment workflow can overwrite each other when both are active. After correcting the source, rerun **Deploy SI² to GitHub Pages** and check its final deployment result. A successful **Check website** run validates the source but does not publish it.
