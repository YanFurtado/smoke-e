"""Mede no FigCraft a largura de cada caractere e grava em metricas.json (junta ao que já existe).
Uso (com a instância de controle aberta, FC_PORT definido):
  python3 calibrar.py "Poppins:400,500,600,700" "BrushUpTooW01-Regular:400"
Sem argumentos mede Inter 400/500/600 e Menlo 400. Confira antes com file.fontReport se a família existe no app."""
import sys, os, json, string
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fc, fcctl
chars = string.ascii_letters + string.digits + " .,:;!?'\"()[]/\\-+*=%$#@&_<>|~·•×—–çãõáéíóúâêôàÇÃÕÁÉÍÓÚÂÊÔ"
alvos = []
for a in (sys.argv[1:] or ["Inter:400,500,600", "Menlo:400"]):
    fam, ws = a.rsplit(":", 1); alvos += [(fam, int(w)) for w in ws.split(",")]
d = fc.Doc("cal"); p = d.page("cal"); f = d.frame(p, "q", 0, 0, 4000, 4000, fill="#ffffff")
ids = {}
for fam, wt in alvos:
    for ch in chars:
        ids[d.text(f, "x" + ch * 10 + "x", 0, 0, size=100, weight=wt, family=fam)] = (fam, wt, ch)
    ids[d.text(f, "xx", 0, 0, size=100, weight=wt, family=fam)] = (fam, wt, "__xx")
os.makedirs(os.path.join(os.path.dirname(HERE), "gerador", "out") if False else os.path.join(HERE, "out"), exist_ok=True)
path = os.path.join(HERE, "out", "cal.figcraft"); d.save(path)
c = fcctl.Conn(); r = c.ex("file.open", {"path": path, "reload": True})
if not r.get("ok"): sys.exit(r)
c.ex("node.set", {"ids": list(ids), "textAutoResize": "widthAndHeight"})
med = {}
for nid, (fam, wt, ch) in ids.items():
    med.setdefault(f"{fam}|{wt}", {})[ch] = c.ex("node.get", {"id": nid})["result"]["width"]
mp = os.path.join(HERE, "metricas.json"); res = json.load(open(mp)) if os.path.exists(mp) else {}
for k, v in med.items():
    base = v.pop("__xx")
    res[k] = {ch: round((w - base) / 1000, 4) for ch, w in v.items()}
json.dump(res, open(mp, "w"), ensure_ascii=False, indent=0)
print("medidas:", ", ".join(med))
