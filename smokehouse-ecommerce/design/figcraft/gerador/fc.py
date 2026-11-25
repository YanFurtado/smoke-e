"""Gerador de arquivos .figcraft (zip com document.json).

Base mínima: Doc com páginas, frames, textos, elipses e linhas. Coordenadas
sempre relativas ao pai, como no FigCraft. As telas usam ui.py, que monta os
componentes da direção visual em cima desta base.
"""
import json, zipfile, io, struct, zlib

def rgb(hexstr, a=1.0):
    h = hexstr.lstrip("#")
    if len(h) == 8:
        a = int(h[6:8], 16) / 255
    return {"r": int(h[0:2], 16) / 255, "g": int(h[2:4], 16) / 255, "b": int(h[4:6], 16) / 255, "a": a}

def paint(hexstr, opacity=1.0):
    return {"type": "solid", "color": rgb(hexstr), "opacity": opacity, "visible": True, "blend": "normal"}

WEIGHT = {400: "Regular", 500: "Medium", 600: "Semi Bold", 700: "Bold"}

# Largura por caractere medida no próprio FigCraft (calibrar.py -> metricas.json).
import os as _os
_MET = json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "metricas.json")))
for _k, _v in _MET.items():
    if _v.get(" ", 0) < 0.05:  # o app corta espaço no fim do texto; medida antiga sai ~0
        _v[" "] = 0.603 if _k.startswith("Menlo") else 0.28
def text_width(s, size, weight=400, mono=False, family="Inter"):
    """Largura do texto pela tabela medida no app (metricas.json). Família sem medida usa a Inter."""
    if mono:
        key = "Menlo|400"
    else:
        w = 700 if weight >= 700 else (600 if weight >= 600 else (500 if weight >= 500 else 400))
        key = next((k for k in (f"{family}|{w}", f"{family}|400") if k in _MET), f"Inter|{min(w, 600)}")
    tab = _MET[key]
    longest = max(s.split("\n"), key=len) if s else ""
    return sum(tab.get(ch, 0.62 if not mono else 0.603) for ch in longest) * size

class Doc:
    def __init__(self, name):
        self.name = name
        self.nodes = {}
        self.pages = []
        self._id = 0
        self.styles = []
        self.images = {}

    def image(self, parent, path, x, y, w, h, name="Imagem", radius=0, mode="fit"):
        import hashlib
        data = open(path, "rb").read()
        hsh = hashlib.sha256(data).hexdigest()
        if hsh not in self.images:
            pw, ph = _img_size(data)
            self.images[hsh] = (data, pw, ph)
        n = {"name": name, "type": "rectangle", "blend": "normal",
             "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)], "width": float(w), "height": float(h),
             "fills": [{"type": "image", "image": hsh, "scale_mode": mode, "scale": 1.0, "rotation": 0, "crop": None,
                        "filters": {"exposure": 0.0, "contrast": 0.0, "saturation": 0.0, "temperature": 0.0,
                                    "tint": 0.0, "highlights": 0.0, "shadows": 0.0},
                        "opacity": 1.0, "visible": True, "blend": "normal"}]}
        if radius:
            n["corners"] = {"radii": [float(radius)] * 4, "smoothing": 0.0}
        return self._new(n, parent)

    def _new(self, node, parent):
        self._id += 1
        node["id"] = self._id
        if parent is not None:
            node["parent"] = parent
            self.nodes[parent].setdefault("children", []).append(self._id)
        self.nodes[self._id] = node
        return self._id

    def page(self, name, bg="#e9e7e1"):
        pid = self._new({"name": name, "type": "page", "background": rgb(bg), "flows": [],
                         "prototype": {"device": "None", "background": rgb(bg), "rotation": "portrait"},
                         "children": [], "width": 0.0, "height": 0.0}, None)
        self.pages.append(pid)
        return pid

    def frame(self, parent, name, x, y, w, h, fill=None, stroke=None, radius=0, clip=False,
              stroke_w=1.0, sides=None, opacity=1.0, fill_opacity=1.0, stroke_opacity=1.0, shadow=None):
        n = {"name": name, "type": "frame", "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
             "width": float(w), "height": float(h), "fills": [paint(fill, fill_opacity)] if fill else [],
             "clip": clip, "children": []}
        if stroke:
            n["strokes"] = [paint(stroke, stroke_opacity)]
            n["stroke"] = {"weight": float(stroke_w), "align": "inside", "sides": sides, "cap_start": "none",
                           "cap_end": "none", "join": "miter", "miter_limit": 4.0, "dashes": []}
        if radius:
            r = radius if isinstance(radius, (list, tuple)) else [radius] * 4
            n["corners"] = {"radii": [float(v) for v in r], "smoothing": 0.0}
        if opacity != 1.0:
            n["opacity"] = opacity
        if shadow:
            n["effects"] = [shadow]
        return self._new(n, parent)

    def text(self, parent, s, x, y, size=14, weight=400, color="#1f1b16", w=None, lh=None,
             family="Inter", align="left", ls=0.0, name=None, mono=False, opacity=1.0, valign=None, valign_h=None):
        if mono:
            family = MONO
        lh = lh or round(size * 1.4 / 2) * 2
        est = text_width(s, size, weight, mono, family)
        if w is None and align == "left":
            box_w, auto, lines = est + 2, "widthAndHeight", 1 + s.count("\n")
        elif w is None:
            box_w, auto, lines = est * 1.25 + 16, "height", 1 + s.count("\n")
            x = x - box_w if align == "right" else x - box_w / 2
        else:
            box_w, auto = w, "height"
            lines = sum(max(1, -(-int(text_width(seg, size, weight, mono, family)) // int(max(1, w)))) for seg in s.split("\n"))
        n = {"name": name or s[:48], "type": "text", "characters": s,
             "style": {"font_family": family, "font_style": WEIGHT.get(weight, "Regular"), "font_size": float(size),
                       "line_height": {"unit": "pixels", "value": float(lh)},
                       "letter_spacing": {"unit": "percent", "value": float(ls)}, "decoration": "none",
                       "case": "original", "fills": None, "link": None, "style_id": None},
             "auto_resize": auto, "blend": "normal",
             "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)], "width": float(box_w), "height": float(lh * lines),
             "fills": [paint(color)]}
        if align != "left":
            n["align_h"] = align
        if valign:
            n["align_v"] = valign
            n["auto_resize"] = "none"
            n["height"] = float(valign_h)
        if opacity != 1.0:
            n["opacity"] = opacity
        return self._new(n, parent)

    def ellipse(self, parent, x, y, d, fill, name="Ponto", stroke=None):
        n = {"name": name, "type": "ellipse", "start": 0.0, "sweep": 6.283185307179586, "inner": 0.0,
             "blend": "normal", "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)], "width": float(d),
             "height": float(d), "fills": [paint(fill)] if fill else []}
        if stroke:
            n["strokes"] = [paint(stroke)]
            n["stroke"] = {"weight": 1.5, "align": "inside", "sides": None, "cap_start": "none", "cap_end": "none",
                           "join": "miter", "miter_limit": 4.0, "dashes": []}
        return self._new(n, parent)

    def polyline(self, parent, pts, color, weight=1.5, name="Linha", x=0, y=0, dashes=None):
        """Retas (ícones simples, serrilha do cupom). pts relativos a (x, y)."""
        minx = min(p[0] for p in pts); miny = min(p[1] for p in pts)
        maxx = max(p[0] for p in pts); maxy = max(p[1] for p in pts)
        verts = [{"x": float(p[0] - minx), "y": float(p[1] - miny), "radius": 0.0} for p in pts]
        segs = [{"a": i, "b": i + 1, "ta": [0.0, 0.0], "tb": [0.0, 0.0]} for i in range(len(pts) - 1)]
        n = {"name": name, "type": "vector", "network": {"vertices": verts, "segments": segs, "regions": []},
             "blend": "normal", "transform": [1.0, 0.0, 0.0, 1.0, float(x + minx), float(y + miny)],
             "width": float(max(maxx - minx, 0.01)), "height": float(max(maxy - miny, 0.01)),
             "strokes": [paint(color)],
             "stroke": {"weight": float(weight), "align": "center", "sides": None, "cap_start": "round",
                        "cap_end": "round", "join": "round", "miter_limit": 4.0, "dashes": dashes or []}}
        return self._new(n, parent)

    def link(self, node_id, dest):
        self.nodes[node_id]["interactions"] = [{"trigger": {"type": "onClick"},
            "actions": [{"type": "navigate", "dest": dest}], "transition": {"type": "dissolve"},
            "duration_ms": 180, "easing": "easeOut"}]

    def flow(self, page, name, start, description=""):
        self.nodes[page]["flows"].append({"name": name, "start": start, "description": description})

    def save(self, path, thumb_png=None):
        nodes = {str(k): v for k, v in self.nodes.items()}
        doc = {"format": "figcraft", "version": 1,
               "imageIndex": [{"hash": k, "width": v[1], "height": v[2]} for k, v in self.images.items()], "name": self.name, "pages": self.pages,
               "nodes": nodes, "next_id": 4294967297, "styles": self.styles,
               "variables": {"collections": [], "variables": []}, "current_page": self.pages[0],
               "document_colors": [], "comments": []}
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("document.json", json.dumps(doc, ensure_ascii=False))
            z.writestr("thumbnail.png", thumb_png or _blank_png())
            for k, v in self.images.items():
                z.writestr("images/" + k, v[0])

def _img_size(data):
    """Largura e altura de um PNG ou JPEG (o FigCraft aceita os dois como imagem)."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            if data[i] != 0xFF: i += 1; continue
            m = data[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9]); return w, h
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise ValueError("imagem precisa ser PNG ou JPEG")

def _blank_png(w=4, h=4):
    raw = b"".join(b"\x00" + b"\xff\xff\xff" * w for _ in range(h))
    def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + \
        chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")

MONO = "Menlo"
