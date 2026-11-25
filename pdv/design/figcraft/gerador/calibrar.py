import sys, os, json, string
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fc, fcctl
chars = string.ascii_letters + string.digits + " .,:;!?'\"()[]/\\-+*=%$#@&_<>|~·•×—–çãõáéíóúâêôàÇÃÕÁÉÍÓÚÂÊÔ"
d = fc.Doc("cal"); p = d.page("cal"); f = d.frame(p, "q", 0, 0, 4000, 4000, fill="#ffffff")
ids = {}
for fam, wt in [("Inter", 400), ("Inter", 500), ("Inter", 600), ("Menlo", 400)]:
    for ch in chars:
        nid = d.text(f, ch * 10, 0, 0, size=100, weight=wt, family=fam, name=f"{fam}|{wt}|{ch}")
        ids[nid] = (fam, wt, ch)
d.save("out/cal.figcraft")
c = fcctl.Conn()
r = c.ex("file.open", {"path": os.path.abspath("out/cal.figcraft"), "reload": True}); print(r.get("ok"), r.get("error"))
allids = list(ids)
r = c.ex("node.set", {"ids": allids, "textAutoResize": "widthAndHeight"}); print("set", r.get("ok"), r.get("error"))
res = {}
for nid, (fam, wt, ch) in ids.items():
    g = c.ex("node.get", {"id": nid})["result"]
    res.setdefault(f"{fam}|{wt}", {})[ch] = round(g["width"] / 1000, 4)
json.dump(res, open("metricas.json", "w"), ensure_ascii=False, indent=0)
print({k: (v["a"], v["M"], v["1"], v[" "]) for k, v in res.items()})
