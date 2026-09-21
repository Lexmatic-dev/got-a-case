# Got a Case

Marketing / landing site for **Got a Case**.

This repository holds two things:

1. **`design/`** – the raw HTML exports from the design tool, split by breakpoint
   (`mobile/` and `desktop/`). These are the source of truth for how each page
   should look. Drop the exported files here as-is; do not hand-edit them.
2. **`site/`** – the actual website that gets deployed. It is a plain static
   site (HTML + CSS + JS, no build step) assembled from the designs in `design/`.

```
got-a-case/
├── design/
│   ├── mobile/      # mobile HTML exports (upload here first)
│   └── desktop/     # desktop HTML exports (upload here second)
├── site/            # the deployable website
│   ├── index.html
│   └── assets/
│       ├── css/
│       ├── js/
│       ├── images/
│       └── fonts/
└── docs/            # setup notes and workflow guides
```

## Quick start

No install is required. To preview the site locally:

```bash
cd site
python3 -m http.server 8080
# open http://localhost:8080
```

## Workflow

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the step-by-step process of
adding design files and turning them into site pages.
