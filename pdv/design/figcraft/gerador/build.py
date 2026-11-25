"""Monta o arquivo FigCraft do PDV a partir dos módulos em telas/.

Uso: python3 build.py [saida.figcraft] [--so MODULO]
Cada módulo de telas/ expõe PAGE (nome da página), APP (dav|nfce|host) e
SCREENS = [(codigo, titulo, funcao)], com funcao(d, f, device, app) desenhando
dentro do quadro f, que já tem o tamanho do aparelho (computador, tablet, celular).
Uma função pode devolver uma altura maior para o quadro (tela que rola).
"""
import importlib, os, sys, pkgutil, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fc, ui

ORDER = ["capa", "dav_a", "dav_b", "nfce", "host_a", "host_b"]
DEV_LABEL = {"desktop": "Computador 1440", "tablet": "Tablet 1180", "mobile": "Celular 390"}

def build(out, only=None):
    d = fc.Doc("Smoke House · PDV")
    mods = [m for m in ORDER if os.path.exists(os.path.join(os.path.dirname(__file__), "telas", m + ".py"))]
    if only: mods = [m for m in mods if m in only]
    errors = []
    for name in mods:
        mod = importlib.import_module("telas." + name)
        page = d.page(mod.PAGE, bg="#e2e0da")
        if hasattr(mod, "build_page"):
            mod.build_page(d, page); continue
        y = 0
        for code, title, fn in mod.SCREENS:
            ui.T(d, page, f"{code} · {title}", 0, y, size=28, weight=500, lh=36, name=f"Título {code}")
            x, row_h = 0, 0
            for dev in ("desktop", "tablet", "mobile"):
                W, H = ui.DEVICES[dev]
                ui.T(d, page, DEV_LABEL[dev], x, y + 52, size=14, color=ui.C["text2"], lh=20, name=f"Rótulo {code} {dev}")
                f, _, _ = ui.screen(d, page, f"{code} · {title} · {DEV_LABEL[dev]}", dev, x, y + 84, app=mod.APP)
                try:
                    hh = fn(d, f, dev, mod.APP)
                    if hh and hh > H:
                        d.nodes[f]["height"] = float(hh)
                except Exception:
                    errors.append(f"{code} {dev}: " + traceback.format_exc().splitlines()[-1])
                    traceback.print_exc()
                row_h = max(row_h, d.nodes[f]["height"])
                x += W + 120
            y += 84 + row_h + 200
    thumb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "png", "00_Capa.png")
    d.save(out, open(thumb, "rb").read() if os.path.exists(thumb) else None)
    print(f"{out}: {len(d.nodes)} camadas" + (f", {len(errors)} erros" if errors else ""))
    for e in errors: print("  ERRO", e)
    return d

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = None
    if "--so" in sys.argv:
        only = sys.argv[sys.argv.index("--so") + 1].split(",")
        args = [a for a in args if a not in only]
    if args:
        build(args[0], only)
    else:
        import shutil, time
        here = os.path.dirname(os.path.abspath(__file__))
        final = os.path.join(os.path.dirname(here), "Smoke House · PDV.figcraft")
        if os.path.exists(final):  # regra "Backup do layout": guarda a versão anterior
            shutil.copy(final, os.path.join(here, "backups", time.strftime("Smoke House · PDV %Y%m%d-%H%M.figcraft")))
        build(final, only)
        espelho = os.path.expanduser("~/Documents/figcraft/Smoke House · PDV.figcraft")
        os.makedirs(os.path.dirname(espelho), exist_ok=True)
        shutil.copy(final, espelho)
        print("cópia para o FigCraft:", espelho)
