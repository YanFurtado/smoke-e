"""Abre o arquivo na instância de controle e exporta cada tela em PNG. Uso: python3 render.py arquivo.figcraft [filtro]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fcctl
path = os.path.abspath(sys.argv[1]); filt = sys.argv[2] if len(sys.argv) > 2 else ""
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "png"); os.makedirs(outdir, exist_ok=True)
c = fcctl.Conn()
r = c.ex("file.open", {"path": path, "reload": True})
if not r.get("ok"): print(r); sys.exit(1)
print("aberto", r["result"])
import zipfile
doc = json.loads(zipfile.ZipFile(path).read("document.json"))
n = 0
for pid in doc["pages"]:
    pg = doc["nodes"][str(pid)]
    c.ex("page.select", {"id": pid})
    for cid in pg.get("children", []):
        node = doc["nodes"][str(cid)]
        if node["type"] != "frame" or filt not in node["name"]: continue
        fn = node["name"].replace(" · ", "_").replace(" ", "-").replace("/", "-") + ".png"
        rr = c.ex("file.export", {"ids": [cid], "format": "png", "scale": 1, "path": os.path.join(outdir, fn)})
        if not rr.get("ok"): print("ERRO", node["name"], rr.get("error")); continue
        n += 1
print(n, "telas exportadas em", outdir)
