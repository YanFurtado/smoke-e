"""Junta as 3 versões de cada tela numa prancha. Uso: python3 prancha.py COD [COD...]"""
import sys, os, glob
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])  # Pillow instalado fora do padrão
from PIL import Image
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "png")
os.makedirs(os.path.join(base, "..", "pranchas"), exist_ok=True)
for cod in sys.argv[1:]:
    ims = []
    for dev in ("Computador", "Tablet", "Celular"):
        f = glob.glob(os.path.join(base, f"{cod}_*{dev}*.png"))
        if f: ims.append(Image.open(f[0]).convert("RGB"))
    if not ims: print("sem", cod); continue
    H = 900
    sc = [H / max(900, im.height) if im.height > 900 else H / 900 for im in ims]
    ims = [im.resize((int(im.width * s), int(im.height * s))) for im, s in zip(ims, sc)]
    W = sum(im.width for im in ims) + 40 * (len(ims) - 1)
    out = Image.new("RGB", (W, max(im.height for im in ims)), (210, 208, 202))
    x = 0
    for im in ims: out.paste(im, (x, 0)); x += im.width + 40
    out.save(os.path.join(base, "..", "pranchas", f"{cod}.png"))
print("ok")
