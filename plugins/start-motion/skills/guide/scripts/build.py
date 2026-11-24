#!/usr/bin/env python3
"""Builds a walkthrough guide page (index.html) from a content file.

  python3 build.py guide.json            writes index.html beside guide.json

The page is one self-contained HTML file plus the screenshots it points at (shots/). The same file
is published as the web page and printed to PDF (build-pdf.sh), so the two always match.
Text fields may hold simple inline HTML (<b>, <i>, <a>); everything else is escaped by hand in the
content file, so write "&amp;" for an ampersand.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = {  # 32x32, stroke only; the colour comes from the node's lane
    "convert": '<circle cx="13" cy="11" r="5"/><path d="M4 26c0-5 4-8 9-8s9 3 9 8"/><path d="M22 12h7m-3-3 3 3-3 3"/>',
    "book": '<path d="M6 6h9a3 3 0 0 1 3 3v17a3 3 0 0 0-3-3H6z"/><path d="M26 6h-5a3 3 0 0 0-3 3v17a3 3 0 0 1 3-3h5z"/>',
    "box": '<path d="M16 4 27 10v12L16 28 5 22V10z"/><path d="M5 10l11 6 11-6M16 16v12"/>',
    "calendar": '<rect x="5" y="7" width="22" height="20" rx="3"/><path d="M5 13h22M11 4v6M21 4v6M11 19h4"/>',
    "document": '<path d="M8 4h11l6 6v18H8z"/><path d="M19 4v6h6M12 16h9M12 21h9"/>',
    "download": '<path d="M8 4h11l6 6v18H8z"/><path d="M19 4v6h6"/><path d="M16 14v9m-4-4 4 4 4-4"/>',
    "person": '<circle cx="16" cy="11" r="5"/><path d="M6 27c0-6 4-9 10-9s10 3 10 9"/>',
    "check": '<circle cx="16" cy="16" r="11"/><path d="M11 16l4 4 7-8"/>',
    "list": '<path d="M11 9h15M11 16h15M11 23h15"/><circle cx="6" cy="9" r="1.2"/><circle cx="6" cy="16" r="1.2"/><circle cx="6" cy="23" r="1.2"/>',
    "gear": '<circle cx="16" cy="16" r="4"/><path d="M16 4v4M16 24v4M4 16h4M24 16h4M7.5 7.5l2.8 2.8M21.7 21.7l2.8 2.8M7.5 24.5l2.8-2.8M21.7 10.3l2.8-2.8"/>',
    "send": '<path d="M4 16 28 5l-7 23-5-10z"/><path d="M16 18 28 5"/>',
    "chart": '<path d="M5 27h22M9 27V16M16 27V8M23 27v-7"/>',
}

def read(p): return open(p, encoding="utf-8").read()

def lanes_css(lanes):
    """Column template for the lane bands and colour stops for the line behind the nodes."""
    counts = [len(l["nodes"]) for l in lanes]; total = sum(counts) or 1
    cols = " ".join(f"{c}fr" for c in counts)
    colours = ["var(--cyan)", "var(--blue)", "var(--deep)"]
    stops, done = [], 0
    for i, c in enumerate(counts):
        # the line runs between the centres of the first and last node, so stops sit between nodes
        start = 0 if i == 0 else round((done - 0.5) / (total - 1) * 100) if total > 1 else 0
        done += c
        end = 100 if i == len(counts) - 1 else round((done - 0.5) / (total - 1) * 100) if total > 1 else 100
        stops.append(f"{colours[min(i, 2)]} {start}% {end}%")
    edge = round(50 / total, 2)
    return cols, total, ", ".join(stops), edge

def build(g, base):
    b = g.get("brand", {})
    over = "".join(f"--{k}:{v};" for k, v in (b.get("colors") or {}).items())
    fonts = b.get("fonts_href", "https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap")
    logo = b.get("logo_svg") and read(os.path.join(base, b["logo_svg"])).replace("<svg", '<svg class="logo"', 1) or \
        (b.get("logo_img") and f'<img class="logo" src="{b["logo_img"]}" alt="{g["client"]}">' or f'<b style="color:#fff;font:700 22px var(--display)">{g["client"]}</b>')
    ks_white = read(os.path.join(HERE, "assets/kicksaw-wordmark-white.svg")).replace("<svg", '<svg class="ks"', 1)
    ks_navy = read(os.path.join(HERE, "assets/kicksaw-wordmark-navy.svg")).replace("<svg", '<svg class="ks"', 1)
    out = [f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{g["title"]}</title>',
           f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="{fonts}">',
           "<style>\n" + read(os.path.join(HERE, "assets/guide.css"))]
    if over: out.append(":root{" + over + "}")
    if b.get("display_font"): out.append(f':root{{--display:"{b["display_font"]}","Segoe UI",Arial,sans-serif}}')
    if b.get("body_font"): out.append(f':root{{--sans:"{b["body_font"]}","Segoe UI",Arial,sans-serif}}')

    path = g.get("path")
    if path:
        cols, total, stops, edge = lanes_css(path["lanes"])
        out.append(f".lanes{{grid-template-columns:{cols}}}.nodes{{grid-template-columns:repeat({total},minmax(0,1fr))}}"
                   f".nodes::before{{left:{edge}%;right:{edge}%;background:linear-gradient(90deg,{stops})}}")
    out.append("</style>\n</head><body>")

    # cover
    h = g["cover"]
    facts = "".join(f'<div class="fact"><b>{f["n"]}</b><span>{f["label"]}</span></div>' for f in h.get("facts", []))
    out.append(f'<header class="hero"><div class="wrap">\n<div class="topbar">{logo}<span class="by">Prepared by {ks_white}</span></div>\n'
               f'<div><p class="tag">{h.get("tag", "Salesforce user guide")}</p><h1>{h["headline"]}</h1>\n<p class="lede">{h["lede"]}</p></div>\n'
               + (f'<div class="facts">{facts}</div>' if facts else "") + "</div></header>\n<main class=\"wrap\">")

    def head(s): return (f'<div class="sec-head"><span class="eyebrow">{s["eyebrow"]}</span><h2>{s["title"]}</h2>'
                         + (f'<p>{s["intro"]}</p>' if s.get("intro") else "") + "</div>")

    # the path at a glance
    if path:
        out.append('<section id="path">' + head(path) + '<div class="flow">\n<div class="lanes">'
                   + "".join(f'<div class="lane l{min(i, 2) + 1}">{l["label"]}</div>' for i, l in enumerate(path["lanes"])) + "</div>\n<nav class=\"nodes\" aria-label=\"Steps\">")
        n = 0
        for i, l in enumerate(path["lanes"]):
            for nd in l["nodes"]:
                n += 1
                out.append(f'<a class="node n{min(i, 2) + 1}" href="#step-{nd.get("step", n)}"><span class="ic"><i>{n}</i><svg viewBox="0 0 32 32">{ICONS.get(nd.get("icon"), ICONS["check"])}</svg></span>'
                           f'<b>{nd["title"]}</b><span class="d">{nd.get("detail", "")}</span></a>')
        out.append("</nav></div>")
        if path.get("before_you_start"):
            out.append('<div class="start"><h3>Before you start</h3><ul>' + "".join(f"<li>{x}</li>" for x in path["before_you_start"]) + "</ul></div>")
        out.append("</section>")

    # reference blocks before the steps (a catalog, a set of record types, a list of fields)
    ref = g.get("reference")
    if ref:
        out.append('<section id="reference">' + head(ref))
        if ref.get("panels"):
            out.append(f'<div class="books" style="grid-template-columns:{" ".join(str(p.get("weight", 1)) + "fr" for p in ref["panels"])}">')
            for p in ref["panels"]:
                out.append(f'<div class="book"><header><h3>{p["title"]}</h3>' + (f'<p>{p["sub"]}</p>' if p.get("sub") else "") + "</header>")
                for gr in p["groups"]:
                    out.append('<div class="grp">' + (f'<h4>{gr["label"]}</h4>' if gr.get("label") else ""))
                    for r in gr.get("rows", []):
                        val = f'<b class="you">{r["pill"]}</b>' if r.get("pill") else f'<b>{r.get("value", "")}</b>'
                        out.append(f'<div class="row"><span>{r["name"]}</span>{val}</div>' + (f'<p>{r["note"]}</p>' if r.get("note") else ""))
                    if gr.get("note"): out.append(f'<p>{gr["note"]}</p>')
                    out.append("</div>")
                out.append("</div>")
            out.append("</div>")
        if ref.get("terms"):
            out.append('<div class="terms">' + "".join(f'<div class="term"><b>{t["term"]}</b><span>{t["means"]}</span></div>' for t in ref["terms"]) + "</div>")
        out.append("</section>")

    # the steps
    st = g["steps"]
    out.append('<section id="steps">' + head(st))
    for i, s in enumerate(st["items"], 1):
        out.append(f'<article class="step" id="step-{i}">')
        n = 1
        for j, sh in enumerate(s["shots"]):
            lis = "".join(f"<li><span>{x}</span></li>" for x in sh.get("instructions", []))
            block = ('<div class="shot">' + (f'<ol start="{n}">{lis}</ol>' if lis else "")
                     + (f'<p class="note">{sh["note"]}</p>' if sh.get("note") else "")
                     + (f'<figure><img src="{sh["image"]}" alt="{sh.get("alt", "")}" loading="lazy"></figure>' if sh.get("image") else "") + "</div>")
            n += len(sh.get("instructions", []))
            if j == 0:   # the step header stays on the same printed page as its first screenshot
                block = f'<div class="keep"><header><span class="num">{i}</span><div><h3>{s["title"]}</h3><p>{s.get("sub", "")}</p></div></header>{block}</div>'
            out.append(block)
        out.append("</article>")
    out.append("</section>")

    # the finished thing, explained (a document, a record, a report)
    res = g.get("result")
    if res:
        out.append('<section id="pdf">' + head(res) + f'<div class="pdf">\n<figure><img src="{res["image"]}" alt="{res.get("alt", "")}" loading="lazy"></figure>\n<ol class="legend">'
                   + "".join(f'<li><i>{k}</i><div><b>{it["name"]}</b><span>{it["from"]}</span></div></li>' for k, it in enumerate(res["items"], 1)) + "</ol>\n</div></section>")

    # good to know
    gk = g.get("good_to_know")
    if gk:
        out.append('<section id="know">' + head(gk) + '<div class="grid3">' + "".join(f'<div class="card"><h3>{c["title"]}</h3><p>{c["text"]}</p></div>' for c in gk["cards"]) + "</div></section>")

    out.append(f'</main>\n<footer><div class="wrap"><span class="by">Prepared for {g["client"]} by {ks_navy}</span><span>{g.get("footer", "")}</span></div></footer>')
    out.append("<script>document.querySelectorAll('.shot ol').forEach(function(ol){var n=parseInt(ol.getAttribute('start')||'1',10);ol.querySelectorAll('li').forEach(function(li){li.setAttribute('data-n',n++);});});</script>\n</body></html>")
    return "\n".join(out)

if __name__ == "__main__":
    src = sys.argv[1]; base = os.path.dirname(os.path.abspath(src))
    g = json.load(open(src, encoding="utf-8"))
    missing = [sh["image"] for s in g["steps"]["items"] for sh in s["shots"] if sh.get("image") and not os.path.exists(os.path.join(base, sh["image"]))]
    open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(build(g, base))
    shots = sum(len(s["shots"]) for s in g["steps"]["items"])
    print(f"index.html written: {len(g['steps']['items'])} steps, {shots} screenshots" + (f"; MISSING IMAGES: {missing}" if missing else ""))
