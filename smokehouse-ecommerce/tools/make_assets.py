#!/usr/bin/env python3
"""Converte os artefatos PNG (fundo transparente) em assets/marca/ + assets/web/*.webp.

Uso:  py tools/make_assets.py
Recorta pelo bbox do alpha (limiar >40, porque as bordas têm ruído), reduz para
~380 px no maior lado e salva WebP lossy com alpha.
"""
import pathlib, shutil
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = {  # arquivo na raiz -> nome do asset
    "Imagem ChatGPT 10_11_2026, 08_54_47-1.png": "nuvem",
    "Imagem ChatGPT 10_11_2026, 08_54_48-3.png": "charuto",
    "Imagem ChatGPT 10_11_2026, 08_54_49-4.png": "narguile",
    "Imagem ChatGPT 10_11_2026, 08_54_49-5.png": "pinca",
    "Imagem ChatGPT 10_11_2026, 08_54_50-6.png": "cinzeiro",
    "Imagem ChatGPT 10_11_2026, 08_54_51-7.png": "folha",
    "Imagem ChatGPT 10_11_2026, 08_54_51-8.png": "bolsa",
}
MAX = 380
for fn, name in SRC.items():
    p = ROOT / fn
    if not p.exists():
        p = ROOT / "assets/marca" / f"{name}.png"
    im = Image.open(p).convert("RGBA")
    box = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop(box)
    im.thumbnail((MAX, MAX), Image.LANCZOS)
    out = ROOT / "assets/web" / f"{name}.webp"
    im.save(out, "WEBP", quality=72, alpha_quality=80, method=6)
    dst = ROOT / "assets/marca" / f"{name}.png"
    if p != dst:
        shutil.copyfile(p, dst)
    print(f"{name:9} {im.size} {out.stat().st_size/1024:.1f} KB")
