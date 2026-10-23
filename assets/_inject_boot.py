#!/usr/bin/env python3
"""Inject the boot preloader markup + html.is-loading lock into every page in site/."""
import re
import pathlib

BOOT = """<div class="boot" id="boot" aria-hidden="true">
    <div class="boot-stage">
      <div class="boot-mark">
        <span class="ring r1"></span>
        <span class="ring r2"></span>
        <span class="ring r3"></span>
        <span class="core"></span>
      </div>
      <div class="boot-progress">
        <div class="boot-progress-bar" id="boot-bar"></div>
      </div>
      <div class="boot-percent" id="boot-pct">0%</div>
      <div class="boot-status" id="boot-status">Menyiapkan pengalaman…</div>
    </div>
    <div class="boot-brand">SMKN 8 JEMBER &middot; <b>ESKALABER</b></div>
  </div>
"""

root = pathlib.Path(__file__).resolve().parent.parent
changed = []
for f in sorted(root.glob("*.html")):
    src = f.read_text(encoding="utf-8")
    orig = src

    # 1. body lock class on <html>
    src = re.sub(r"<html(\s[^>]*?)?>", lambda m: "<html" + (m.group(1) or "") + " class=\"is-loading\">", src, count=1)
    # avoid double class if re-run
    src = src.replace('class="is-loading" class="is-loading"', 'class="is-loading"')

    # 2. preloader as first child of <body>
    if 'id="boot"' not in src:
        src = re.sub(r"(<body[^>]*>)", r"\1\n" + BOOT.replace("\\", "\\\\"), src, count=1)

    if src != orig:
        f.write_text(src, encoding="utf-8")
        changed.append(f.name)

print("updated:", ", ".join(changed) if changed else "none")
