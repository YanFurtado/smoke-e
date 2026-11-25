"""Monta o arquivo .figcraft do projeto a partir dos módulos em telas/.

Uso: python3 build.py [--so mod1,mod2] [--saida arquivo.figcraft] [--sem-espelho]
- Lê projeto.json ({"nome": "...", "ordem": ["capa", "app", ...]}) na pasta do gerador.
- Sem --saida, grava em ../<nome>.figcraft, guarda a versão anterior em backups/ e copia para
  ~/Documents/figcraft/ (onde o FigCraft lista os arquivos).
Cada módulo de telas/ expõe PAGE (nome da página), APP (chave de ui.APPS) e
SCREENS = [(codigo, titulo, funcao)], com funcao(d, f, device, app) desenhando no quadro f.
A função pode devolver uma altura maior (tela que rola). Um módulo pode ter build_page(d, page)
para desenhar uma página livre (capa, direção visual).
"""
import importlib, json, os, shutil, sys, time, traceback
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fc, ui

DEV_LABEL = {"desktop": "Computador 1440", "tablet": "Tablet 1180", "mobile": "Celular 390"}

def projeto():
    p = os.path.join(HERE, "projeto.json")
    cfg = json.load(open(p)) if os.path.exists(p) else {}
    cfg.setdefault("nome", "Telas")
    if "ordem" not in cfg:
        cfg["ordem"] = sorted(m[:-3] for m in os.listdir(os.path.join(HERE, "telas")) if m.endswith(".py") and not m.startswith("_"))
    cfg.setdefault("aparelhos", ["desktop", "tablet", "mobile"])
    return cfg

def build(out, only=None):
    cfg = projeto()
    d = fc.Doc(cfg["nome"])
    errors = []
    for name in cfg["ordem"]:
        if only and name not in only: continue
        if not os.path.exists(os.path.join(HERE, "telas", name + ".py")):
            print("  aviso: telas/%s.py não existe, página pulada" % name); continue
        mod = importlib.import_module("telas." + name)
        page = d.page(mod.PAGE, bg="#e2e0da")
        if hasattr(mod, "build_page"):
            mod.build_page(d, page); continue
        y = 0
        for code, title, fn in mod.SCREENS:
            ui.T(d, page, f"{code} · {title}", 0, y, size=28, weight=500, lh=36, name=f"Título {code}")
            x, row_h = 0, 0
            for dev in getattr(mod, "DEVICES", cfg["aparelhos"]):
                W, H = ui.DEVICES[dev]
                ui.T(d, page, DEV_LABEL[dev], x, y + 52, size=14, color=ui.C["text2"], lh=20, name=f"Rótulo {code} {dev}")
                f, _, _ = ui.screen(d, page, f"{code} · {title} · {DEV_LABEL[dev]}", dev, x, y + 84, app=mod.APP)
                try:
                    hh = fn(d, f, dev, mod.APP)
                    if hh and hh > H: d.nodes[f]["height"] = float(hh)
                except Exception:
                    errors.append(f"{code} {dev}: " + traceback.format_exc().splitlines()[-1]); traceback.print_exc()
                row_h = max(row_h, d.nodes[f]["height"]); x += W + 120
            y += 84 + row_h + 200
    pngs = os.path.join(HERE, "out", "png")
    capa = os.path.join(pngs, "00_Capa.png")
    if not os.path.exists(capa) and os.path.isdir(pngs):  # sem capa: a primeira tela renderizada vira a miniatura
        cand = sorted(f for f in os.listdir(pngs) if f.endswith(".png"))
        capa = os.path.join(pngs, cand[0]) if cand else capa
    d.save(out, open(capa, "rb").read() if os.path.exists(capa) else None)
    print(f"{out}: {len(d.nodes)} camadas" + (f", {len(errors)} ERROS" if errors else ""))
    for e in errors: print("  ERRO", e)
    return not errors

if __name__ == "__main__":
    a = sys.argv[1:]
    only = a[a.index("--so") + 1].split(",") if "--so" in a else None
    if "--saida" in a:
        ok = build(a[a.index("--saida") + 1], only)
    else:
        final = os.path.join(os.path.dirname(HERE), projeto()["nome"] + ".figcraft")
        os.makedirs(os.path.join(HERE, "backups"), exist_ok=True)
        if os.path.exists(final):
            shutil.copy(final, os.path.join(HERE, "backups", time.strftime(projeto()["nome"] + " %Y%m%d-%H%M%S.figcraft")))
        ok = build(final, only)
        if "--sem-espelho" not in a:
            esp = os.path.expanduser(os.path.join("~/Documents/figcraft", os.path.basename(final)))
            if os.path.abspath(esp) != os.path.abspath(final):
                os.makedirs(os.path.dirname(esp), exist_ok=True); shutil.copy(final, esp); print("cópia:", esp)
    sys.exit(0 if ok else 1)
