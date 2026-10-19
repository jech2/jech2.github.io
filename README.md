# Eunjin Choi — academic homepage

Static GitHub Pages website using the original styles from [al-folio v0.14.0](https://github.com/alshedivat/al-folio/tree/v0.14.0), adapted for the existing HTML repository. This is a static adaptation, not the full Jekyll distribution. The upstream Sass files and MIT license are kept in `assets/al-folio/`; Bootstrap is distributed under its MIT license. Existing icon fonts and project content come from the previous Untreefolio site, with its attribution preserved on project pages.

## Edit and build

- Biography and education: `templates/about.html` (education transcribed from the repository's May 12, 2026 CV).
- Publications, categories (`mir` / `audio-game`), research keyword tags, full venue names, stable publication IDs (`C`, `J`, `P`), author order, thumbnails and links: `data/publications.json`.
- Shared navigation, metadata and footer: `templates/page.html`.
- Project descriptions: `templates/cuttingkim.html` and `templates/harmonionz.html`.
- Local style refinements: `css/academic.css`.

```sh
npm ci
npm run build
npm run preview
```

Open http://127.0.0.1:8000. To regenerate HTML after content changes without rebuilding CSS, run `python3 scripts/build.py`.

The generated HTML and CSS are committed alongside their sources. GitHub Pages can continue serving this repository directly; no Jekyll or custom deployment workflow is required. Publish by pushing the generated files to the configured Pages branch. `.nojekyll` prevents Jekyll from processing the static sources.

The homepage contains the selected Research and Other Projects papers, with category filtering and concise research keyword tags. No personal details, dates or publication statuses were inferred from the reference person's website.

Publication IDs are stored explicitly to stay unchanged when filtering or adding papers. Each type is numbered from earliest to latest within the selected list; late-breaking demos count as conference publications. Publication type labels and numbering are not displayed. Mel2Word and the chorale generation paper are excluded from the current list.

The homepage opens on Research, showing the latest five MIR papers. The top-right Other Projects link opens `other-projects.html`, with game cards and all three related publications. The Google Scholar link provides the complete publication list; no separate full-list page is generated. Publication IDs stay unchanged across tabs.
