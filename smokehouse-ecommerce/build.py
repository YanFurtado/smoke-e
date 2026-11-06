#!/usr/bin/env python3
"""Gera o index.html final (arquivo único) a partir de src/ e assets/web/.

Uso:  python3 build.py
Lê src/template.html (HTML + CSS), injeta src/app.js no lugar de /*{{APP_JS}}*/
e troca {{img:nome}} / {{font:brush}} pelos arquivos de assets/web em base64.
"""
import base64, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
app = (ROOT / "src/app.js").read_text(encoding="utf-8")
html = tpl.replace("/*{{APP_JS}}*/", app)
cache = {}
def embed(m):
    kind, name = m.group(1), m.group(2)
    key = m.group(0)
    if key not in cache:
        if kind == "font":
            data, mime = (ROOT / "assets/web/brush.woff2").read_bytes(), "font/woff2"
        else:
            data, mime = (ROOT / f"assets/web/{name}.webp").read_bytes(), "image/webp"
        cache[key] = f"data:{mime};base64," + base64.b64encode(data).decode()
    return cache[key]
html = re.sub(r"\{\{(img|font):([\w-]+)\}\}", embed, html)
# tudo até o primeiro </style> vai para o <head>; o resto é o <body>
cut = html.index("</style>") + len("</style>")
head, body = html[:cut], html[cut:]
RESET = "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"
page = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<meta name=\"robots\" content=\"noindex\">\n" + RESET + "\n" + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"index.html gerado ({len(page)/1e6:.2f} MB)")
