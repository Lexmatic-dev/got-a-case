# Design exports

Raw HTML exports from the design tool live here. Keep them untouched so we can
always diff against the original design.

| Folder     | Contents                                  |
|------------|-------------------------------------------|
| `mobile/`  | Mobile breakpoint exports (one file per page/screen) |
| `desktop/` | Desktop breakpoint exports (one file per page/screen) |

## Naming

Name each file after the page it represents, lowercase with hyphens:

```
design/mobile/home.html
design/mobile/about.html
design/mobile/contact.html
design/desktop/home.html
...
```

If the export includes images, CSS or fonts, put them in an `assets/` folder
next to the HTML files (for example `design/mobile/assets/`).
