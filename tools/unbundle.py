#!/usr/bin/env python3
"""Unpack a "bundled page" HTML export into plain HTML plus an assets folder.

The design tool exports each page as a single self-contained HTML file. The
real page markup lives in a <script type="__bundler/template"> tag as a JSON
string, and every image / font / script it references is stored base64
encoded (optionally gzipped) in a <script type="__bundler/manifest"> tag,
keyed by UUID. At load time a small script decodes everything into blob URLs.

This script does the same decoding offline so we get editable files:

    python3 tools/unbundle.py design/mobile/contact.html design/mobile/unpacked/contact

produces

    design/mobile/unpacked/contact/index.html
    design/mobile/unpacked/contact/assets/<uuid>.<ext>
"""
import base64
import gzip
import hashlib
import json
import mimetypes
import os
import re
import sys

MIME_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/svg+xml": ".svg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "font/woff2": ".woff2",
    "font/woff": ".woff",
    "font/ttf": ".ttf",
    "application/javascript": ".js",
    "text/javascript": ".js",
    "application/x-javascript": ".js",
    "text/css": ".css",
    "application/json": ".json",
}


def read_tag(html, tag_type):
    m = re.search(
        r'<script type="%s">\s*(.*?)\s*</script>' % re.escape(tag_type),
        html,
        re.S,
    )
    return m.group(1) if m else None


def main(src, out_dir):
    with open(src, encoding="utf-8") as fh:
        html = fh.read()

    manifest_raw = read_tag(html, "__bundler/manifest")
    template_raw = read_tag(html, "__bundler/template")
    if manifest_raw is None or template_raw is None:
        sys.exit("%s: not a bundled page (missing manifest/template)" % src)

    manifest = json.loads(manifest_raw)
    template = json.loads(template_raw)
    ext_raw = read_tag(html, "__bundler/ext_resources")
    ext_resources = json.loads(ext_raw) if ext_raw else []

    assets_dir = os.path.join(out_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Assets that the page refers to by a friendly name (e.g. assets/crash.png)
    # are listed in ext_resources; name the extracted file after that id so
    # the reference resolves without the runtime's window.__resources lookup.
    names = {e["uuid"]: e["id"] for e in ext_resources if e.get("uuid") and e.get("id")}

    paths = {}
    report = []
    for uuid, entry in manifest.items():
        data = base64.b64decode(entry["data"])
        if entry.get("compressed"):
            data = gzip.decompress(data)
        mime = entry.get("mime", "application/octet-stream")
        ext = MIME_EXT.get(mime) or mimetypes.guess_extension(mime) or ".bin"
        fname = names.get(uuid, uuid) + ext
        with open(os.path.join(assets_dir, fname), "wb") as fh:
            fh.write(data)
        paths[uuid] = "assets/" + fname
        report.append((fname, mime, len(data), hashlib.sha1(data).hexdigest()[:10]))

    # Only raw UUID references are rewritten. Named references already point
    # at assets/<id>.<ext>, which is where we just wrote the file.
    for uuid, path in paths.items():
        template = template.replace(uuid, path)

    template = re.sub(r'\s+integrity="[^"]*"', "", template, flags=re.I)
    template = re.sub(r'\s+crossorigin="[^"]*"', "", template, flags=re.I)

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(template)

    print("%s -> %s" % (src, out_dir))
    print("  template: %d chars, %d assets" % (len(template), len(paths)))
    for fname, mime, size, digest in sorted(report, key=lambda r: -r[2]):
        print("  %-48s %-24s %9d  %s" % (fname, mime, size, digest))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: unbundle.py <bundled.html> <out_dir>")
    main(sys.argv[1], sys.argv[2])
