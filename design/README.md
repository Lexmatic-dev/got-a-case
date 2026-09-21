# Design exports

Raw exports from the design tool. Keep them untouched so we can always diff
a new export against the previous one.

| Folder     | Contents |
|------------|----------|
| `mobile/`  | Mobile breakpoint, one bundled `.html` per page, plus the hero photo |
| `desktop/` | Desktop breakpoint (pending) |

Each export is a single self-contained "bundled page": the markup, images
and fonts are base64-packed inside `<script type="__bundler/...">` tags and
unpacked by JavaScript when opened. Use `tools/unbundle.py` to get editable
files out of one. See `docs/WORKFLOW.md`.

## Naming

Name each file after the page it represents, lowercase with hyphens:
`index`, `quiz`, `portal`, `alabama`, `contact`.
