"""Render the static al-folio adaptation using only Python's standard library."""
from pathlib import Path
from string import Template
from html import escape
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
papers = json.loads((ROOT / 'data/publications.json').read_text())
shell = Template((ROOT / 'templates/page.html').read_text())
style_version = hashlib.sha256((ROOT / 'css/academic.css').read_bytes()).hexdigest()[:12]

def publications(limit=None, category="mir"):
    displayed_papers = [paper for paper in papers if paper.get("homepage_selected", True)] if limit is not None else papers
    research_count = 0
    displayed_papers = [paper for paper in displayed_papers if paper["category"] == category]
    rows = []
    for index, paper in enumerate(displayed_papers):
        title = escape(paper['title'])
        authors = escape(paper['authors']).replace('Eunjin Choi', '<strong>Eunjin Choi</strong>')
        rendered_links = []
        for link in paper['links']:
            markup = f'<a class="btn btn-sm" href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>'
            if link.get('disabled'):
                markup = f'<!-- {escape(link.get("disabled_reason", "Link disabled"))}: {markup} -->'
            rendered_links.append(markup)
        links = ' '.join(rendered_links)
        preview = ''
        if paper.get('show_preview', True):
            preview = f'<img src="{escape(paper["image"])}" class="preview rounded" alt="{title} — preview" loading="lazy" width="140" height="100">'
        tags = '<ul class="research-tags" aria-label="Research keywords">' + ''.join(f'<li>{escape(tag)}</li>' for tag in paper['tags']) + '</ul>'
        is_research = paper['category'] == 'mir'
        hidden = " hidden" if limit is not None and index >= limit else ""
        if is_research:
            research_count += 1
        rows.append(f'''<li{hidden} data-category="{escape(paper['category'])}"><div class="row">
<div class="col-sm-2 abbr"><span class="badge rounded w-100">{escape(paper['venue'])}</span>{preview}</div>
<div class="col-sm-10"><div class="title">{title}</div><div class="author">{authors}</div><div class="periodical"><em>{escape(paper['venue_full'])}</em>, {paper['year']}</div>{tags}<div class="links">{links}</div></div></div></li>''')
    mir = sum(p['category'] == 'mir' for p in displayed_papers)
    audio_game = len(displayed_papers) - mir
    summary = f'Showing {min(limit or mir, mir)} of {mir} research papers' if category == 'mir' else f'2 games &amp; interactive works · {audio_game} related publications'
    projects = (ROOT / 'templates/games.html').read_text() if category == 'audio-game' else ''
    section_title = 'Selected Publications' if category == 'mir' else 'Other Projects'
    projects_section = f'<div id="other-projects">{projects}<h3 class="related-publications-heading">Related Publications</h3></div>' if projects else ''
    introduction = '<p class="projects-intro">Here are some projects I enjoyed working on as a developer.</p>' if category == 'audio-game' else ''
    contribution_note = '<p class="muted publication-note">* Equal contribution.</p>' if category == 'audio-game' else ''
    page_class = "other-projects-page" if category == "audio-game" else "research-page"
    return f'''<section class="{page_class}" id="publications" data-limit="{limit or 0}"><div class="publications-header"><h2>{section_title}</h2>
</div>
{introduction}
{projects_section}
<div class="publications"><ol class="bibliography">{''.join(rows)}</ol></div>
<p class="scholar-link">More publications on <a href="https://scholar.google.com/citations?user=3VWIf88AAAAJ">Google Scholar</a>.</p>
{contribution_note}</section>'''

def render(filename, title, content):
    is_other = filename in ('other-projects.html', 'cuttingkim.html', 'harmonionz.html')
    (ROOT / filename).write_text(shell.substitute(title=escape(title), content=content, style_version=style_version, research_current='' if is_other else ' aria-current="page"', other_current=' aria-current="page"' if is_other else ''))

about = Template((ROOT / 'templates/about.html').read_text()).substitute(publications=publications(limit=5))
render('index.html', 'Eunjin Choi', about)
render('other-experiences.html', 'Other Experiences | Eunjin Choi', (ROOT / 'templates/other-experiences.html').read_text())
render('other-projects.html', 'Other Projects | Eunjin Choi', publications(category='audio-game'))
for filename, title in [('cuttingkim.html', 'Cutting Kim'), ('harmonionz.html', 'Harmonionz, Rescue the Planet')]:
    render(filename, title + ' | Eunjin Choi', (ROOT / 'templates' / filename).read_text())
render('blogs.html', 'Blog | Eunjin Choi', '<header class="post-header"><h1>Blog</h1></header><p>Currently, this page is under construction.</p><p>See you soon!</p>')
print(f'Built 6 pages with {len(papers)} publications.')
