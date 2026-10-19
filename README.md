# DS 115 Week 6: Where Can Data Science Take Me?

The opening review has been compressed from eight slides into one. There are 15 main slides and three optional reference slides.

This standalone Week 6 website package includes editable Quarto source, rendered HTML in `docs/`, a separate final reflection page, sources, speaker notes, and a survey guide for Google Forms.

## Open the materials

- Website: `docs/index.html`
- Presentation: `docs/slides/day6.html`
- Final reflection: `docs/reflection.html`
- Sources and calculations: `docs/resources.html`
- Survey setup and settings: `survey/google-forms-setup.md`
- Survey copy-and-paste text: `survey/google-forms-copy.txt`
- Class timing and facilitation: `teaching-guide.md`

The rendered slide HTML embeds its styles and Reveal.js runtime and can be opened directly without a server. Use arrow keys to navigate and S for speaker notes. Your browser must permit the speaker-view popup. For notes and website navigation, serving locally is recommended: `python3 -m http.server 8000 --directory docs`, then open `http://localhost:8000/`.

## Build with Quarto

Install the Quarto CLI, then run from this directory:

```sh
quarto render
```

The project configuration sets `project.type: website` and `output-dir: docs`. The slides use Reveal.js and the existing DS 115 theme from the Day 4 package. The render list contains only the student pages and slide deck, keeping the survey guide and teaching guide out of the public site.

### Build environment note

The initial rendered HTML in this package was generated with Pandoc and the bundled Reveal.js runtime because Quarto was not installed and this environment could not download it. A native Quarto render was not run. The source uses standard Quarto website/Reveal.js conventions. The fallback previews the static content and does not emulate every Quarto feature. Browser-based slide testing was also unavailable because a browser could not be downloaded.

To regenerate the same preview with Pandoc:

```sh
python3 scripts/render.py --fallback
```

Without `--fallback`, the script uses `quarto render` when Quarto is installed. Fallback CSS is a compiled snapshot of the prior course theme. After changing `theme.scss`, use native Quarto to compile that change.

## Add Week 6 to an existing course website

This package is an addition, not a replacement for the full course website. Keep the other weeks and their files.

1. Copy `slides/day6.qmd` and `slides/day6.css` into the course's `slides/` directory.
2. Use the existing course theme and slide metadata. This package's `slides/_metadata.yml` shows the defaults used here. Do not overwrite newer course-wide settings without comparing them.
3. Copy `reflection.qmd` and `resources.qmd` if wanted, choosing distinct filenames if those pages already exist. Update any links to match the chosen names.
4. Add `slides/day6.qmd` to the existing project's render list and navigation. Retain `output-dir: docs`.
5. Run `quarto render` from the existing project root. Commit the needed source and `docs/` output to the course repository.

For GitHub Pages serving committed HTML, choose the repository's publishing branch and `/docs` as the source folder. This package includes `docs/.nojekyll`. No deployment or repository change has been performed.

## Survey access

The instructor's completed survey is https://forms.gle/EtDPQS7N3yaDtz8f9. The survey slide includes a large QR code and clickable link, and the website links directly to the form. The QR PNG is in assets/survey-qr.png and the rendered presentation embeds it so the standalone HTML works offline. No quiz password is stored in the slides or website. The survey guides retain the original proposed wording as a reference, not a verified copy of the live form.

The final reflection remains a separate Canvas assignment. Its full supplied wording is preserved in `reflection.qmd`.

## Evidence and scope

NSF percentages use 2023 primary-work-activity counts, not a causal estimate or leadership measure. The Google posting is one dated example, not a representative hiring sample. The industry percentage concerns notable AI models, not all data science research. Sources and full interpretation notes appear on the resources page and in relevant slide notes.

## Bundled preview runtime

The fallback reuses Reveal.js 5.1.0 and its notes plugin from the previously supplied Day 4 HTML. Their original copyright and MIT license notices remain embedded. The course CSS is likewise retained as a preview snapshot. Quarto uses its own packaged runtime when rendering normally.

