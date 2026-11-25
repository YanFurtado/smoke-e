"""Converte out/png/*.png em ../previas/*.jpg (leves, para o repositório). Uso: python3 previas.py
Precisa do Pillow (pip3 install pillow; ou PYLIB=<pasta> se instalado com --target)."""
import os, sys, glob
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(os.path.dirname(here), "previas"); os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(dst, "*.jpg")): os.remove(f)
n = 0
for f in sorted(glob.glob(os.path.join(here, "out", "png", "*.png"))):
    im = Image.open(f).convert("RGB")
    im.save(os.path.join(dst, os.path.basename(f)[:-4] + ".jpg"), quality=82, optimize=True)
    n += 1
print(n, "prévias em", dst)
