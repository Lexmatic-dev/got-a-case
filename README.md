# Got a Case

Marketing site and Case Score quiz for **GotACase™** (gotacase.com).

The site is plain HTML, CSS and JavaScript with no build step. Open
`site/index.html` in a browser, or run a local server:

```bash
cd site
python3 -m http.server 8080
# then open http://localhost:8080
```

## Layout

```
got-a-case/
├── design/                 # raw exports from the design tool (source of truth, never hand-edited)
│   ├── mobile/             # mobile breakpoint, one bundled .html per page
│   └── desktop/            # desktop breakpoint (to be uploaded)
├── site/                   # the deployable website
│   ├── index.html          # Home
│   ├── quiz.html           # Case Score quiz (multi-step)
│   ├── portal.html         # "My Case Portal" – reads the quiz result from localStorage
│   ├── alabama.html        # Alabama landing page
│   ├── contact.html        # Contact form
│   └── assets/
│       ├── css/fonts.css   # self-hosted Plus Jakarta Sans
│       ├── css/main.css    # shared tokens, hamburger menu, footer
│       ├── fonts/
│       └── images/         # optimised logos, hero photo, quiz illustrations
├── tools/
│   └── unbundle.py         # unpacks a design export into editable HTML + assets
└── docs/
    └── WORKFLOW.md         # how a design export becomes a site page
```

## Pages

| Page | Notes |
|------|-------|
| `index.html` | Static sections plus small scripts for the case-type carousel, animated gauges and score-range cards. |
| `quiz.html` | 16-screen quiz. Computes a preliminary category client-side and stores `gac_score`, `gac_category` and `gac_id` in `localStorage`. |
| `portal.html` | Shows the stored category / ID. Good and Very Good categories see the "path forward" options; others see the locked state. |
| `contact.html` | Form validation is client-side; `submitForm()` in the page is a stub to wire to a backend. |
| `alabama.html` | Static. |

## Design exports

The design tool exports each page as a single "bundled" HTML file: the real
markup and every image/font are base64-packed inside `<script>` tags and
unpacked in the browser. Those files live untouched in `design/`. To get
editable HTML out of one:

```bash
python3 tools/unbundle.py design/mobile/contact.html /tmp/unpacked/contact
```

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the full process, including
what was changed when the mobile exports were turned into `site/`.
