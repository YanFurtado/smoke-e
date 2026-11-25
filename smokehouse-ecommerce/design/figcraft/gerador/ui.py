"""Componentes de interface para telas no FigCraft (modelo da skill figcraft-telas).

Copiado para <projeto>/gerador/ui.py pelo novo_projeto.py. Ajuste os TOKENS (C, APPS) para a
direção visual do projeto antes de desenhar; os componentes leem tudo daqui.

Regras que valem para todas as telas (mude só se a direção do projeto mandar):
- Grade de 4 px. Raio: tecla 4, controle 8, cartão 12, janela 16.
- Neutros quase cinzas; a cor do aplicativo só no botão principal, no foco e na aba ativa.
- Inter 400/500 (600 raro). Menlo para códigos, valores de tabela e teclas.
- Seleção em lista: fundo cinza claro + borda fina escura.
- Sem emoji, sem gradiente, sem brilho, sem caixa alta espaçada, sem ponto final em rótulo/botão.
"""
import os
import fc

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- tokens ----------
C = {  # marca Smoke House (src/template.html: --bg, --fg, --green, --ink, --line, --muted, --hot)
    "page": "#f3f2ed", "deep": "#e9e7e0", "card": "#ffffff", "raised": "#efede7", "sel": "#e6e4dd",
    "ink": "#151614", "text2": "#4f524b", "muted": "#6a6d66", "line": "#151614", "paper": "#fffdf8",
    "pos": "#256d45", "neg": "#c62f32", "warn": "#9a6a00", "info": "#2f5d8a", "overlay": "#0e0f0d",
    "black": "#0e0f0d", "bar": "#1b1d1a", "green": "#34925e", "yellow": "#ffbe00",
}
LINE_A = 0.10
APPS = {
    "loja":   {"nome": "Vitrine", "sigla": "LOJA", "acc": "#2b7d50", "soft": "#e2efe7", "logo": "logo-branco.png"},
    "colab":  {"nome": "Área do colaborador", "sigla": "COLAB", "acc": "#2b7d50", "soft": "#e2efe7", "logo": "logo-branco.png"},
    "donos":  {"nome": "Painel dos donos", "sigla": "DONOS", "acc": "#2b7d50", "soft": "#e2efe7", "logo": "logo-branco.png"},
}
FONT = "Poppins"                      # texto da marca (template.html: --body)
DISPLAY = "BrushUpTooW01-Regular"     # títulos pincelados (--brush); instalada em ~/Library/Application Support/Craft Fonts
_tw = fc.text_width
def _text_width(s, size, weight=400, mono=False, family=None):
    return _tw(s, size, weight, mono, family or FONT)
fc.text_width = _text_width            # componentes medem com a fonte da marca por padrão
DEFAULT_APP = "loja"
DEVICES = {"desktop": (1440, 900), "tablet": (1180, 820), "mobile": (390, 844)}
PAD = {"desktop": 24, "tablet": 20, "mobile": 16}
R_KEY, R_CTL, R_CARD, R_WIN = 4, 8, 12, 16

def brl(v, sign=False):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    pre = "-" if v < 0 else ("+" if sign and v > 0 else "")
    return f"{pre}R$ {s}"

def acc(app): return APPS[app]["acc"]

# ---------- primitivas ----------
def shadow(a=0.08, oy=8, r=24):
    return {"type": "dropShadow", "color": fc.rgb("#000000", a), "offset": [0.0, float(oy)], "radius": float(r),
            "spread": 0.0, "blend": "normal", "show_behind": False, "visible": True}

def T(d, p, s, x, y, size=14, weight=400, color=None, **kw):
    if not kw.get("mono"): kw.setdefault("family", FONT)
    return d.text(p, s, x, y, size=size, weight=weight, color=color or C["ink"], **kw)

def hair(d, p, x, y, w, h=1, name="Linha"):
    return d.frame(p, name, x, y, w, h, fill=C["line"], fill_opacity=LINE_A)

def box(d, p, x, y, w, h, fill=None, radius=R_CARD, border=True, name="Caixa", stroke=None, sw=1, so=None):
    return d.frame(p, name, x, y, w, h, fill=fill, stroke=(stroke or C["line"]) if border else None,
                   stroke_opacity=(so if so is not None else (1.0 if stroke else LINE_A)), stroke_w=sw, radius=radius)

def keycap(d, p, x, y, label, dark=False, h=20):
    w = max(h, fc.text_width(label, 11, 500, mono=True) + 10)
    k = d.frame(p, f"Tecla {label}", x, y, w, h, fill="#2a2925" if dark else C["card"],
                stroke=C["ink"], stroke_opacity=0.18, radius=R_KEY)
    d.frame(k, "Base", 0, h - 2, w, 2, fill=C["ink"], fill_opacity=0.10)
    T(d, k, label, w / 2, (h - 14) / 2 - 1, size=11, weight=500, mono=True,
      color="#f4f3ef" if dark else C["text2"], align="center", lh=14)
    return w

# ---------- ícones (linha 1.5, cor do texto) ----------
def icon(d, p, name, x, y, s=16, color=None):
    c = color or C["muted"]; k = s / 16
    def L(pts): d.polyline(p, [(x + a * k, y + b * k) for a, b in pts], c, weight=1.5, name=f"Ícone {name}")
    def O(cx, cy, r): d.ellipse(p, x + (cx - r) * k, y + (cy - r) * k, 2 * r * k, None, name=f"Ícone {name}", stroke=c)
    if name == "busca": O(7, 7, 5); L([(11, 11), (15, 15)])
    elif name == "menu": L([(2, 4), (14, 4)]); L([(2, 8), (14, 8)]); L([(2, 12), (14, 12)])
    elif name == "cadeado": L([(3, 7), (13, 7), (13, 15), (3, 15), (3, 7)]); L([(5, 7), (5, 4), (8, 1.5), (11, 4), (11, 7)])
    elif name == "fechar": L([(3, 3), (13, 13)]); L([(13, 3), (3, 13)])
    elif name == "seta-dir": L([(6, 3), (11, 8), (6, 13)])
    elif name == "seta-baixo": L([(3, 6), (8, 11), (13, 6)])
    elif name == "seta-esq": L([(10, 3), (5, 8), (10, 13)])
    elif name == "ok": L([(2, 8.5), (6, 12.5), (14, 4)])
    elif name == "mais": L([(8, 2), (8, 14)]); L([(2, 8), (14, 8)])
    elif name == "menos": L([(2, 8), (14, 8)])
    elif name == "pessoa": O(8, 5, 3); L([(2, 15), (3.5, 11), (8, 9.5), (12.5, 11), (14, 15)])
    elif name == "dica": O(8, 7, 5); L([(6, 14), (10, 14)]); L([(8, 10), (8, 12)])
    elif name == "impressora": L([(4, 6), (4, 2), (12, 2), (12, 6)]); L([(2, 6), (14, 6), (14, 12), (2, 12), (2, 6)]); L([(4, 10), (12, 10), (12, 15), (4, 15), (4, 10)])
    elif name == "aviso": L([(8, 2), (15, 14), (1, 14), (8, 2)]); L([(8, 6), (8, 10)]); L([(8, 12), (8, 12.2)])
    elif name == "relogio": O(8, 8, 6.5); L([(8, 4), (8, 8), (11, 10)])
    elif name == "caixa": L([(2, 5), (14, 5), (14, 14), (2, 14), (2, 5)]); L([(1, 2), (15, 2), (15, 5), (1, 5)]); L([(6, 8), (10, 8)])
    elif name == "grafico": L([(2, 14), (14, 14)]); L([(4, 12), (4, 8)]); L([(8, 12), (8, 4)]); L([(12, 12), (12, 7)])
    elif name == "pessoas": O(6, 5, 2.5); L([(1, 14), (2, 10.5), (6, 9), (10, 10.5), (11, 14)]); O(11.5, 4.5, 2); L([(12, 8.5), (14.5, 9.5), (15, 12)])
    elif name == "moeda": O(8, 8, 6.5); L([(10, 5.5), (7, 5.5), (6, 6.5), (6.5, 7.8), (9.5, 8.2), (10, 9.5), (9, 10.5), (6, 10.5)]); L([(8, 4), (8, 12)])
    elif name == "doc": L([(3, 1.5), (10, 1.5), (13, 4.5), (13, 14.5), (3, 14.5), (3, 1.5)]); L([(5.5, 7), (10.5, 7)]); L([(5.5, 10), (10.5, 10)])
    elif name == "engrenagem": O(8, 8, 2.5); O(8, 8, 6)
    elif name == "chat": L([(2, 3), (14, 3), (14, 11), (7, 11), (4, 14), (4, 11), (2, 11), (2, 3)])
    elif name == "caminhao": L([(1, 4), (10, 4), (10, 11), (1, 11), (1, 4)]); L([(10, 7), (13, 7), (15, 9.5), (15, 11), (10, 11)]); O(4.5, 12.5, 1.5); O(12, 12.5, 1.5)
    elif name == "link": L([(6, 10), (10, 6)]); L([(7, 4), (9, 2), (12, 2), (14, 4), (14, 7), (12, 9)]); L([(9, 12), (7, 14), (4, 14), (2, 12), (2, 9), (4, 7)])
    elif name == "nota": L([(3, 1.5), (13, 1.5), (13, 14.5), (11, 13), (9, 14.5), (7, 13), (5, 14.5), (3, 13), (3, 1.5)]); L([(5.5, 5.5), (10.5, 5.5)]); L([(5.5, 8.5), (10.5, 8.5)])
    elif name == "transferir": L([(2, 5), (13, 5)]); L([(10, 2), (13, 5), (10, 8)]); L([(14, 11), (3, 11)]); L([(6, 8), (3, 11), (6, 14)])
    elif name == "lixo": L([(2, 4), (14, 4)]); L([(4, 4), (5, 14.5), (11, 14.5), (12, 4)]); L([(6, 4), (6, 2), (10, 2), (10, 4)])
    elif name == "lapis": L([(2, 14), (3, 10.5), (11, 2.5), (13.5, 5), (5.5, 13), (2, 14)])
    elif name == "olho": L([(1, 8), (4, 4.5), (8, 3), (12, 4.5), (15, 8), (12, 11.5), (8, 13), (4, 11.5), (1, 8)]); O(8, 8, 2)
    elif name == "upload": L([(8, 11), (8, 2)]); L([(4.5, 5.5), (8, 2), (11.5, 5.5)]); L([(2, 11), (2, 14), (14, 14), (14, 11)])
    elif name == "whats": O(8, 8, 6.5); L([(2.2, 14.6), (3.2, 11.4)]); L([(5.6, 5.4), (5.2, 6.6), (6.2, 8.8), (8.2, 10.6), (10.4, 11.0), (11.0, 10.2), (10.0, 9.4)])
    elif name == "calendario": L([(2, 3), (14, 3), (14, 14), (2, 14), (2, 3)]); L([(2, 6.5), (14, 6.5)]); L([(5, 1.5), (5, 4)]); L([(11, 1.5), (11, 4)])
    elif name == "filtro": L([(2, 3), (14, 3), (9.5, 8.5), (9.5, 13), (6.5, 14.5), (6.5, 8.5), (2, 3)])
    elif name == "mais-circ": O(8, 8, 6.5); L([(8, 5), (8, 11)]); L([(5, 8), (11, 8)])
    elif name == "pontos": O(3, 8, 0.6); O(8, 8, 0.6); O(13, 8, 0.6)
    elif name == "voltar": L([(6, 3), (2, 7), (6, 11)]); L([(2, 7), (11, 7), (14, 10), (14, 14)])
    elif name == "nuvem": L([(4, 13), (2, 11), (2, 8.5), (4, 6.5), (6, 6.5), (7.5, 3.5), (11, 3), (13, 5.5), (13, 7.5), (15, 9), (15, 11.5), (13, 13), (4, 13)])
    elif name == "chave": O(5, 11, 3); L([(7, 9), (14, 2)]); L([(11, 5), (13, 7)])
    elif name == "casa": L([(1.5, 8), (8, 2), (14.5, 8)]); L([(3.5, 6.5), (3.5, 14.5), (12.5, 14.5), (12.5, 6.5)]); L([(6.5, 14.5), (6.5, 10), (9.5, 10), (9.5, 14.5)])
    elif name == "sacola": L([(2.5, 5.5), (13.5, 5.5), (12.5, 14.5), (3.5, 14.5), (2.5, 5.5)]); L([(5.5, 5.5), (5.5, 4), (8, 1.8), (10.5, 4), (10.5, 5.5)])
    elif name == "pin": O(8, 6.5, 2); L([(8, 15), (3.5, 9), (3, 6.5), (5, 2.5), (8, 1.5), (11, 2.5), (13, 6.5), (12.5, 9), (8, 15)])
    else: O(8, 8, 6)

# ---------- controles ----------
def button(d, p, x, y, label, app=DEFAULT_APP, kind="secondary", w=None, h=40, key=None, icon_name=None, align="center", disabled=False, sub=None):
    """kind: primary (cor do app), dark (tinta), secondary (cartão + hairline), ghost, danger."""
    tw = fc.text_width(label, 14, 500)
    kw = (fc.text_width(key, 11, 500, mono=True) + 10 + 8) if key else 0
    iw = 24 if icon_name else 0
    w = w or int(tw + kw + iw + 32 + 3) // 4 * 4
    fill, fg, stroke = {
        "primary": (acc(app), "#ffffff", None),
        "dark": (C["ink"], "#f4f3ef", None),
        "secondary": (C["card"], C["ink"], C["line"]),
        "ghost": (None, C["text2"], None),
        "danger": (C["card"], C["neg"], C["neg"]),
    }[kind]
    b = d.frame(p, f"Botão {label}", x, y, w, h, fill=fill, stroke=stroke,
                stroke_opacity=(0.35 if kind == "danger" else LINE_A), radius=R_CTL,
                opacity=0.45 if disabled else 1.0)
    cx = (w - (tw + kw + iw)) / 2 if align == "center" else 16
    if icon_name:
        icon(d, b, icon_name, cx, (h - 16) / 2, 16, fg if kind != "secondary" else C["text2"]); cx += iw
    ly = (h - 20) / 2 - (9 if sub else 0)
    T(d, b, label, cx, ly, size=14, weight=500, color=fg, lh=20)
    if key:
        keycap(d, b, cx + tw + 8, ly, key, dark=kind in ("primary", "dark"))
    if sub:
        T(d, b, sub, w / 2, ly + 22, size=12, color=fg, lh=16, align="center", opacity=0.78)
    return b, w

def field(d, p, x, y, w, label=None, value="", placeholder="", focused=False, app=DEFAULT_APP, h=40,
          mono=False, suffix=None, error=None, chevron=False, prefix_icon=None, readonly=False, big=False):
    yy = y
    if label:
        T(d, p, label, x, y, size=13, color=C["text2"], lh=16); yy = y + 20
    f = d.frame(p, f"Campo {label or placeholder or value}"[:40], x, yy, w, h,
                fill=C["raised"] if readonly else C["card"],
                stroke=acc(app) if focused else (C["neg"] if error else C["line"]),
                stroke_opacity=1.0 if (focused or error) else 0.16, stroke_w=2 if focused else 1, radius=R_CTL)
    tx = 12
    if prefix_icon:
        icon(d, f, prefix_icon, 12, (h - 16) / 2, 16); tx = 36
    size = 18 if big else 14
    if value:
        T(d, f, value, tx, (h - (24 if big else 20)) / 2, size=size, color=C["ink"], mono=mono, lh=24 if big else 20)
    elif placeholder:
        T(d, f, placeholder, tx, (h - 20) / 2, size=14, color=C["muted"], lh=20)
    if focused and not chevron:
        vx = tx + (fc.text_width(value, size, 400, mono) if value else 0) + 1
        d.frame(f, "Cursor", vx, (h - 20) / 2, 1.5, 20, fill=C["ink"])
    if suffix:
        T(d, f, suffix, w - 12, (h - 20) / 2, size=13, color=C["muted"], align="right", lh=20, mono=True)
    if chevron:
        icon(d, f, "seta-baixo", w - 28, (h - 16) / 2, 16)
    if error:
        T(d, p, error, x, yy + h + 4, size=12, color=C["neg"], lh=16)
    return f, (yy - y) + h

def toggle(d, p, x, y, on=True, label=None, app=DEFAULT_APP, sub=None):
    t = d.frame(p, "Chave", x, y, 36, 20, fill=acc(app) if on else C["raised"], stroke=None if on else C["line"],
                stroke_opacity=0.18, radius=10)
    d.ellipse(t, 18 if on else 2, 2, 16, "#ffffff", name="Botão da chave")
    if label:
        T(d, p, label, x + 48, y, size=14, lh=20)
        if sub: T(d, p, sub, x + 48, y + 20, size=12, color=C["muted"], lh=16)

def checkbox(d, p, x, y, on=False, label=None, app=DEFAULT_APP):
    b = d.frame(p, "Marcação", x, y, 18, 18, fill=acc(app) if on else C["card"], stroke=None if on else C["ink"],
                stroke_opacity=0.3, radius=4)
    if on: icon(d, b, "ok", 1, 1, 16, "#ffffff")
    if label: T(d, p, label, x + 28, y - 1, size=14, lh=20)

def radio(d, p, x, y, on=False, label=None, app=DEFAULT_APP):
    d.ellipse(p, x, y, 18, C["card"], name="Opção", stroke=acc(app) if on else C["muted"])
    if on: d.ellipse(p, x + 5, y + 5, 8, acc(app), name="Opção marcada")
    if label: T(d, p, label, x + 28, y - 1, size=14, lh=20)

def tabs(d, p, x, y, items, active=0, app=DEFAULT_APP, h=40, counts=None):
    cx = x
    for i, it in enumerate(items):
        tw = fc.text_width(it, 14, 500 if i == active else 400)
        cnt = counts[i] if counts else None
        cw = (fc.text_width(str(cnt), 12, 400, True) + 8) if cnt is not None else 0
        T(d, p, it, cx, y + 10, size=14, weight=500 if i == active else 400,
          color=C["ink"] if i == active else C["text2"], lh=20)
        if cnt is not None:
            T(d, p, str(cnt), cx + tw + 6, y + 12, size=12, color=C["muted"], mono=True, lh=16)
        if i == active:
            d.frame(p, "Aba ativa", cx, y + h - 2, tw + cw, 2, fill=acc(app))
        cx += tw + cw + 28
    hair(d, p, x, y + h - 1, max(cx - x, 1))
    return cx - x

def chips(d, p, x, y, items, active=0, app=DEFAULT_APP, wrap_w=None):
    """Filtros arredondados com a contagem num círculo à direita (spec, HOST › Clientes)."""
    cx, cy = x, y
    for i, (lab, n) in enumerate(items):
        tw = fc.text_width(lab, 13, 500 if i == active else 400)
        nw = max(20, fc.text_width(str(n), 11, 500, True) + 10) if n is not None else 0
        w = int(tw + 24 + (nw + 6 if n is not None else 0) + 3) // 4 * 4
        if wrap_w and cx + w > x + wrap_w:
            cx, cy = x, cy + 40
        on = i == active
        c = d.frame(p, f"Filtro {lab}", cx, cy, w, 32, fill=C["ink"] if on else C["card"],
                    stroke=None if on else C["line"], stroke_opacity=0.14, radius=16)
        T(d, c, lab, 12, 6, size=13, weight=500 if on else 400, color="#f4f3ef" if on else C["ink"], lh=20)
        if n is not None:
            b = d.frame(c, "Contagem", w - nw - 6, 6, nw, 20, fill="#ffffff" if on else C["raised"], radius=10,
                        fill_opacity=0.16 if on else 1.0)
            T(d, b, str(n), nw / 2, 2, size=11, weight=500, mono=True, color="#f4f3ef" if on else C["text2"], align="center", lh=16)
        cx += w + 8
    return cy - y + 32

def status(d, p, x, y, label, tone="ok", align="left"):
    col = {"ok": C["pos"], "neg": C["neg"], "warn": C["warn"], "info": C["info"], "muted": C["muted"]}[tone]
    tw = fc.text_width(label, 13, 400)
    if align == "right": x = x - tw - 14
    d.ellipse(p, x, y + 6, 8, col, name=f"Situação {label}")
    T(d, p, label, x + 14, y, size=13, color=C["text2"] if tone == "muted" else C["ink"], lh=20)
    return tw + 14

def banner(d, p, x, y, w, title, text=None, tone="warn", action=None, app=DEFAULT_APP):
    col = {"ok": C["pos"], "neg": C["neg"], "warn": C["warn"], "info": C["info"]}[tone]
    aw = (fc.text_width(action, 14, 500) + 32 + 16) if action else 0
    tw = w - 60 - aw
    nl = max(1, -(-int(fc.text_width(text, 13)) // int(tw))) if text else 0
    h = (64 + 20 * (nl - 1)) if text else 44
    b = d.frame(p, f"Aviso {title}"[:40], x, y, w, h, fill=C["card"], stroke=col, stroke_opacity=0.35, radius=R_CTL)
    d.frame(b, "Faixa", 0, 0, 3, h, fill=col, radius=[R_CTL, 0, 0, R_CTL])
    icon(d, b, "aviso" if tone in ("warn", "neg") else "dica", 16, 12 if text else 14, 16, col)
    T(d, b, title, 44, 10 if text else 12, size=14, weight=500, lh=20, w=w - 60 - aw)
    if text: T(d, b, text, 44, 32, size=13, color=C["text2"], lh=20, w=tw)
    if action: button(d, b, w - 16 - (fc.text_width(action, 14, 500) + 32), (h - 32) / 2, action, app=app, h=32)
    return h

def stat(d, p, x, y, w, label, value, note=None, h=104, big=28, tone=None):
    c = box(d, p, x, y, w, h, fill=C["card"], name=f"Quadro {label}")
    T(d, c, label, 20, 16, size=13, color=C["text2"], lh=20)
    T(d, c, value, 20, 42, size=big, weight=500, lh=big + 4, color=C["neg"] if tone == "neg" else C["ink"])
    if note: T(d, c, note, 20, h - 28, size=12, color=C["muted"], lh=16)
    return c

def table(d, p, x, y, w, cols, rows, selected=None, row_h=40, header=True, app=DEFAULT_APP, dim_rows=(), zebra=False,
          max_rows=None, focus_row=None, primary=None):
    """cols: [(titulo, largura|None=resto, 'l'|'r'|'c', mono?)]. rows: listas de str (ou (str, tom))."""
    fixed = sum(c[1] for c in cols if c[1])
    flex = [c for c in cols if not c[1]]
    rest = max(40, (w - 32 - fixed) / max(1, len(flex)))
    widths = [c[1] or rest for c in cols]
    t = d.frame(p, "Tabela", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CARD, clip=True)
    yy = 0
    if header:
        cx = 16
        for ci, ((title, _, al, *_), cw) in enumerate(zip(cols, widths)):
            g = 0 if ci == 0 else 8
            ax = cx + g if al == "l" else (cx + cw - (0 if ci == len(cols) - 1 else 8) if al == "r" else cx + cw / 2)
            T(d, t, title, ax, 10, size=12, color=C["muted"], lh=16, align={"l": "left", "r": "right", "c": "center"}[al])
            cx += cw
        yy = 36; hair(d, t, 0, yy - 1, w)
    rows = rows[:max_rows] if max_rows else rows
    if primary is None:
        primary = next((j for j, c in enumerate(cols) if c[0]), 0)
    for i, r in enumerate(rows):
        if i == selected:
            d.frame(t, "Linha selecionada", 4, yy + 2, w - 8, row_h - 4, fill=C["sel"], stroke=C["ink"], stroke_w=1, radius=6)
        cx = 16
        for j, ((title, _, al, *m), cw) in enumerate(zip(cols, widths)):
            v = r[j] if j < len(r) else ""
            tone = None
            if isinstance(v, tuple): v, tone = v
            if v == "": cx += cw; continue
            g = 0 if j == 0 else 8
            ax = cx + g if al == "l" else (cx + cw - (0 if j == len(cols) - 1 else 8) if al == "r" else cx + cw / 2)
            if tone in ("ok", "neg", "warn", "info", "muted") and title.lower() in ("situação", "status", "estado"):
                status(d, t, ax, yy + (row_h - 20) / 2, v, tone, align="right" if al == "r" else "left")
            else:
                col = {"neg": C["neg"], "ok": C["pos"], "warn": C["warn"], "muted": C["muted"], "b": C["ink"]}.get(tone, C["ink"] if j == primary or al == "r" else C["text2"])
                if i in dim_rows: col = C["muted"]
                T(d, t, v, ax, yy + (row_h - 20) / 2, size=13, weight=500 if tone == "b" else 400, color=col, lh=20,
                  mono=bool(m and m[0]), align={"l": "left", "r": "right", "c": "center"}[al],
                  w=(cw - 16 if al == "l" and fc.text_width(v, 13, 400, bool(m and m[0])) > cw - 16 else None))
            cx += cw
        yy += row_h
        if i < len(rows) - 1 and i != selected and i + 1 != selected: hair(d, t, 16, yy, w - 32)
    d.nodes[t]["height"] = float(yy + 4)
    return t, yy + 4

def card(d, p, x, y, w, h, title=None, action=None, app=DEFAULT_APP, fill=None, pad=20):
    c = box(d, p, x, y, w, h, fill=fill or C["card"], name=f"Cartão {title or ''}".strip())
    if title:
        T(d, c, title, pad, pad - 2, size=15, weight=500, lh=20)
        if action: T(d, c, action, w - pad, pad - 1, size=13, color=acc(app), align="right", lh=20)
    return c

def kv(d, p, x, y, w, rows, size=13, gap=28, mono_values=True, bold_last=False):
    for i, (k, v) in enumerate(rows):
        tone = None
        if isinstance(v, tuple): v, tone = v
        last = bold_last and i == len(rows) - 1
        T(d, p, k, x, y + i * gap, size=size, color=C["text2"], lh=20, weight=500 if last else 400)
        T(d, p, v, x + w, y + i * gap, size=size, color={"neg": C["neg"], "ok": C["pos"], "warn": C["warn"]}.get(tone, C["ink"]),
          lh=20, align="right", mono=mono_values, weight=500 if last else 400)
    return len(rows) * gap

def tile(d, p, x, y, s, label, hue="#2b2a26", h=None):
    """Bloco com sigla no lugar de foto (use d.image quando houver a imagem real)."""
    w, h = s, (h or s)
    m = min(w, h)
    t = d.frame(p, f"Foto {label}", x, y, w, h, fill=hue, radius=max(4, min(12, m // 6)))
    fs = max(9, int(m * 0.26)); lh = int(fs * 1.3)
    T(d, t, label[:3].upper(), w / 2, (h - lh) / 2, size=fs, weight=600, color="#f4f3ef", align="center", lh=lh, mono=True)
    return t

product_tile = tile

def avatar(d, p, x, y, s, name):
    a = d.frame(p, f"Inicial {name}", x, y, s, s, fill=C["raised"], radius=s / 2)
    ini = "".join(w[0] for w in name.split()[:2]).upper()
    T(d, a, ini, s / 2, (s - 16) / 2, size=12, weight=500, color=C["text2"], align="center", lh=16)

# ---------- moldura das telas ----------
def altura(d, f, h):
    """Tela que rola: aumenta o quadro ANTES de desenhar topo, menu lateral e barra de baixo,
    que se posicionam pela altura do quadro. Devolva o mesmo h na função da tela."""
    d.nodes[f]["height"] = float(h)
    return h

def screen(d, page, name, device, x, y, h=None, app=DEFAULT_APP):
    w, hh = DEVICES[device]
    f = d.frame(page, name, x, y, w, h or hh, fill=C["page"], clip=True)
    return f, w, h or hh

def topbar(d, f, device, app=DEFAULT_APP, title=None, subtitle=None, right=None):
    """Logo (se houver em APPS[app]["logo"], arquivo em marca/) ou só o nome; navegação entre aplicativos
    quando há mais de um; texto curto à direita (ex.: "Usuário: Ana")."""
    w = DEVICES[device][0]
    h = 56 if device != "mobile" else 52
    bar = d.frame(f, "Barra superior", 0, 0, w, h, fill=C["card"])
    hair(d, bar, 0, h - 1, w)
    pad = PAD[device]
    tx = pad
    logo = APPS[app].get("logo")
    if logo and os.path.exists(os.path.join(HERE, "marca", logo)):
        d.image(bar, os.path.join(HERE, "marca", logo), pad, 8, 41, 36, name="Logo")
        tx = pad + 52
    T(d, bar, title or APPS[app]["nome"], tx, 9 if subtitle else 18, size=14, weight=500, lh=20)
    if subtitle:
        T(d, bar, subtitle, tx, 27, size=12, color=C["muted"], lh=16)
    if len(APPS) > 1 and device != "mobile":
        nx = tx + 200
        for key, a in APPS.items():
            on = key == app
            tw = fc.text_width(a["nome"], 14, 500 if on else 400)
            tab = d.frame(bar, f"App {a['nome']}", nx, 10, tw + 36, 36, fill=C["raised"] if on else None, radius=R_CTL)
            d.ellipse(tab, 12, 14, 8, a["acc"], name=f"Cor {a['sigla']}")
            T(d, tab, a["nome"], 26, 8, size=14, weight=500 if on else 400, color=C["ink"] if on else C["text2"], lh=20)
            nx += tw + 36 + 4
    if right:
        T(d, bar, right, w - pad, 16 if device == "mobile" else 18, size=13, color=C["text2"], align="right", lh=20)
    return h

def footer(d, f, device, app=DEFAULT_APP, keys=(), status_text="Conectado", status_ok=True):
    """Rodapé com atalhos (teclas desenhadas) e uma situação à direita. No tablet as teclas viram botões de toque.
    No celular não há rodapé: use mobile_bar."""
    w, hh = DEVICES[device]
    H = d.nodes[f]["height"]
    if device == "mobile":
        return 0
    h = 40 if device == "desktop" or not keys else 56
    bar = d.frame(f, "Rodapé", 0, H - h, w, h, fill=C["deep"])
    hair(d, bar, 0, 0, w)
    pad = PAD[device]; cx = pad
    for k, lab in keys:
        if device == "desktop":
            kw = keycap(d, bar, cx, 10, k)
            T(d, bar, lab, cx + kw + 6, 10, size=12, color=C["text2"], lh=20)
            cx += kw + 6 + fc.text_width(lab, 12) + 20
        else:
            bw = fc.text_width(lab, 13, 500) + fc.text_width(k, 11, 500, True) + 10 + 32
            b = d.frame(bar, f"Toque {lab}", cx, 8, bw, 40, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CTL)
            kw = keycap(d, b, 10, 10, k)
            T(d, b, lab, 10 + kw + 8, 10, size=13, weight=500, lh=20)
            cx += bw + 8
    if status_text:
        d.ellipse(bar, w - pad - fc.text_width(status_text, 12) - 16, h / 2 - 4, 8, C["pos"] if status_ok else C["neg"], name="Situação")
        T(d, bar, status_text, w - pad, h / 2 - 10, size=12, color=C["text2"], align="right", lh=20)
    return h

def mobile_bar(d, f, value, caption=None, app=DEFAULT_APP, label="Continuar", key=None):
    """Celular: barra fixa embaixo com um valor (ex.: total) e o botão principal."""
    w, hh = DEVICES["mobile"]
    H = d.nodes[f]["height"]
    bar = d.frame(f, "Barra de ação", 0, H - 88, w, 88, fill=C["card"])
    hair(d, bar, 0, 0, w)
    if caption: T(d, bar, caption, 16, 14, size=12, color=C["muted"], lh=16)
    if value: T(d, bar, value, 16, 32, size=28, weight=500, lh=36)
    bw = 148 if value else w - 32
    button(d, bar, w - 16 - bw, 22, label, app=app, kind="primary", w=bw, h=44, key=key)
    return 88

def overlay(d, f):
    w = d.nodes[f]["width"]; h = d.nodes[f]["height"]
    return d.frame(f, "Fundo da janela", 0, 0, w, h, fill=C["overlay"], fill_opacity=0.32)

def window(d, f, device, title, w, h, app=DEFAULT_APP, footer_buttons=None, close=True):
    """Janela no padrão da spec: título com fechar, conteúdo e botões no rodapé. No celular vira folha de baixo."""
    W, H = d.nodes[f]["width"], d.nodes[f]["height"]
    overlay(d, f)
    if device == "mobile":
        w = W; h = min(h, H - 48)
        x, y = 0, H - h
        win = d.frame(f, f"Janela {title}", x, y, w, h, fill=C["card"], radius=[R_WIN, R_WIN, 0, 0])
        d.frame(win, "Puxador", w / 2 - 18, 8, 36, 4, fill=C["ink"], fill_opacity=0.16, radius=2)
    else:
        x, y = (W - w) / 2, max(40, (H - h) / 2)
        win = d.frame(f, f"Janela {title}", x, y, w, h, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_WIN,
                      shadow=shadow(0.10, 12, 32))
    T(d, win, title, 24, 22, size=17, weight=500, lh=24)
    if close:
        cb = d.frame(win, "Fechar", w - 24 - 52, 20, 52, 28, fill=None, radius=R_CTL)
        icon(d, cb, "fechar", 0, 6, 16, C["muted"])
        keycap(d, cb, 22, 4, "Esc")
    hair(d, win, 0, 64, w)
    fb = 0
    if footer_buttons:
        fb = 72
        hair(d, win, 0, h - fb, w)
        bx = w - 24
        for btn in reversed(footer_buttons):
            lab, kind, key = btn[:3]; dis = len(btn) > 3 and btn[3]
            bw = int(fc.text_width(lab, 14, 500) + (fc.text_width(key, 11, 500, True) + 18 if key else 0) + 32 + 3) // 4 * 4
            if device == "mobile" and len(footer_buttons) <= 2:
                bw = (w - 48 - 8 * (len(footer_buttons) - 1)) / len(footer_buttons)
            bx -= bw
            button(d, win, bx, h - fb + 16, lab, app=app, kind=kind, w=bw, h=40, key=key, disabled=dis)
            bx -= 8
    return win, w, h, 64, h - fb  # janela, largura, altura, topo do conteúdo, base do conteúdo

def confirm(d, f, device, question, lines=(), app=DEFAULT_APP, yes="Sim", no="Não", danger=False):
    """Janela Sim/Não com interrogação azul (spec): S ou Enter confirma, N ou Esc volta."""
    w = 440 if device != "mobile" else DEVICES["mobile"][0]
    tw = w - 96
    qn = max(1, -(-int(fc.text_width(question, 15, 500)) // int(tw)))
    ln_n = [max(1, -(-int(fc.text_width(ln, 13, 400, True)) // int(tw))) for ln in lines]
    h = 64 + 24 + 22 * qn + 12 + sum(20 * n + 8 for n in ln_n) + 24 + 72
    win, w, h, top, bot = window(d, f, device, "Confirmar", w, h, app=app,
                                 footer_buttons=[(no, "secondary", "N"), (yes, "danger" if danger else "dark", "S")], close=True)
    q = d.frame(win, "Interrogação", 24, top + 24, 32, 32, fill=C["info"], radius=16)
    T(d, q, "?", 16, 4, size=18, weight=500, color="#ffffff", align="center", lh=24)
    T(d, win, question, 72, top + 28, size=15, weight=500, lh=22, w=tw)
    yy = top + 28 + 22 * qn + 12
    for ln, n in zip(lines, ln_n):
        T(d, win, ln, 72, yy, size=13, color=C["text2"], lh=20, mono=True, w=tw)
        yy += 20 * n + 8
    return win

GRUPOS_EXEMPLO = [
    (None, [("Início", "grafico"), ("Clientes", "pessoas"), ("Relatórios", "doc")]),
    ("Sistema", [("Configurações", "engrenagem")]),
]

def sidebar(d, f, device, active, groups=None, foot=(), app=DEFAULT_APP):
    """Menu lateral de 248 (216 no tablet). groups: [(titulo|None, [(rótulo, ícone), ...])]. No celular não desenha."""
    H = d.nodes[f]["height"]
    if device == "mobile":
        return 0
    groups = groups or GRUPOS_EXEMPLO
    w = 248 if device == "desktop" else 216
    top = 56
    s = d.frame(f, "Menu lateral", 0, top, w, H - top, fill=C["deep"])
    d.frame(s, "Divisa", w - 1, 0, 1, H - top, fill=C["line"], fill_opacity=LINE_A)
    y = 16
    for g, items in groups:
        if g:
            y += 16
            T(d, s, g, 20, y, size=12, color=C["muted"], lh=16); y += 24
        for lab, ic in items:
            on = lab == active
            row = d.frame(s, f"Menu {lab}", 8, y, w - 16, 34, fill=C["card"] if on else None,
                          stroke=C["line"] if on else None, stroke_opacity=LINE_A, radius=R_CTL)
            if on: d.frame(row, "Marca", 0, 9, 3, 16, fill=APPS[app]["acc"], radius=2)
            icon(d, row, ic, 12, 9, 16, C["ink"] if on else C["muted"])
            T(d, row, lab, 38, 7, size=14, weight=500 if on else 400, color=C["ink"] if on else C["text2"], lh=20)
            y += 36
    for i, ln in enumerate(foot):
        T(d, s, ln, 20, H - top - 32 - 20 * (len(foot) - 1 - i), size=12, color=C["muted"], lh=16)
    return w

def page_head(d, p, x, y, w, title, sub=None, actions=(), app=DEFAULT_APP, device="desktop"):
    T(d, p, title, x, y, size=24 if device != "mobile" else 20, weight=500, lh=32 if device != "mobile" else 28)
    if sub: T(d, p, sub, x, y + (36 if device != "mobile" else 30), size=13, color=C["text2"], lh=20)
    if device == "mobile":
        return 64 if sub else 40
    bx = x + w
    for lab, kind, key, ic in reversed(actions):
        b, bw = button(d, p, 0, y, lab, app=app, kind=kind, key=key, icon_name=ic)
        bx -= bw
        d.nodes[b]["transform"][4] = float(bx)
        bx -= 8
    return 64 if sub else 48

# ---------- bobina impressa (recibo, cupom) ----------
def receipt(d, p, x, y, w, lines, title=None):
    """Bobina térmica impressa (pré-visualização): Menlo 12, papel, serrilha embaixo."""
    lh = 18
    h = 24 + len(lines) * lh + 24
    r = d.frame(p, title or "Cupom impresso", x, y, w, h, fill=C["paper"], stroke=C["line"], stroke_opacity=LINE_A,
                shadow=shadow(0.06, 8, 24))
    yy = 24
    for ln in lines:
        style = "l"
        if isinstance(ln, tuple): ln, style = ln
        if style == "hr":
            T(d, r, "-" * int((w - 32) / 7.2), 16, yy, size=12, color=C["muted"], mono=True, lh=lh)
        elif style == "c":
            T(d, r, ln, w / 2, yy, size=12, mono=True, lh=lh, align="center")
        elif style == "cb":
            T(d, r, ln, w / 2, yy, size=13, weight=600, mono=True, lh=lh, align="center")
        elif style == "lr":
            a, b = ln
            T(d, r, a, 16, yy, size=12, mono=True, lh=lh)
            T(d, r, b, w - 16, yy, size=12, mono=True, lh=lh, align="right")
        elif style == "lrb":
            a, b = ln
            T(d, r, a, 16, yy, size=13, weight=600, mono=True, lh=lh)
            T(d, r, b, w - 16, yy, size=13, weight=600, mono=True, lh=lh, align="right")
        elif style == "qr":
            q = d.frame(r, "QR Code", w / 2 - 56, yy, 112, 112, fill="#ffffff", stroke=C["ink"], stroke_opacity=0.2)
            import random
            rnd = random.Random(7)
            for gy in range(21):
                for gx in range(21):
                    corner = (gx < 7 and gy < 7) or (gx > 13 and gy < 7) or (gx < 7 and gy > 13)
                    on = rnd.random() < 0.48 if not corner else (gx % 6 == 0 or gy % 6 == 0 or (gx % 7 in (2, 3, 4) and gy % 7 in (2, 3, 4))) if gx < 7 or gx > 13 else (gx in (14, 20) or gy in (0, 6) or (gx in (16, 17, 18) and gy in (2, 3, 4)))
                    if on: d.frame(q, "m", 3 + gx * 5, 3 + gy * 5, 5, 5, fill=C["ink"])
            yy += 112 - lh + 8
        else:
            T(d, r, ln, 16, yy, size=12, mono=True, lh=lh, w=w - 32)
            yy += lh * (max(1, -(-int(fc.text_width(ln, 12, 400, True)) // int(w - 32))) - 1)
        yy += lh
    d.nodes[r]["height"] = float(yy + 16)
    pts = []
    for i in range(int(w // 8) + 1):
        pts.append((i * 8, 0)); pts.append((i * 8 + 4, 5))
    serr = d.frame(p, "Serrilha", x, y + yy + 16, w, 6, fill=None, clip=True)
    d.polyline(serr, pts, C["ink"], weight=1, x=0, y=0, name="Serrilha")
    d.nodes[serr]["opacity"] = 0.18
    return r, yy + 16

# ---------- moldura do HOST e listas do celular ----------
def app_shell(d, f, device, active, groups=None, app=DEFAULT_APP, right=None, subtitle=None, foot=()):
    """Topo + menu lateral (computador/tablet) ou topo + linha "☰ seção" (celular).
    Devolve (x, y, largura, base) da área de conteúdo."""
    W, H = DEVICES[device]
    top = topbar(d, f, device, app, right=right, subtitle=subtitle)
    sw = sidebar(d, f, device, active, groups=groups, foot=foot, app=app)
    pad = PAD[device]
    if device == "mobile":
        icon(d, f, "menu", pad, top + 14, 16, C["text2"])
        T(d, f, active, pad + 24, top + 12, size=13, color=C["text2"], lh=20, name="Menu")
        return pad, top + 44, W - 2 * pad, H - pad
    return sw + 32, top + 28, W - sw - 32 - (32 if device == "desktop" else 20), H - 24

def mobile_rows(d, p, x, y, w, rows, selected=None, row_h=64):
    """Celular: a tabela vira cartões de duas linhas. rows: (titulo, sub, direita, direita_sub, tom)."""
    c = d.frame(p, "Lista", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CARD, clip=True)
    yy = 4
    for i, r in enumerate(rows):
        title, sub, right, rsub, tone = (list(r) + [None] * 5)[:5]
        tw = w - 32 - (fc.text_width(right or "", 14, 500, True) + 12)
        nl = max(1, -(-int(fc.text_width(title, 14, 500)) // int(tw)))
        rh = row_h + 20 * (nl - 1)
        if i == selected:
            d.frame(c, "Linha selecionada", 4, yy, w - 8, rh - 4, fill=C["sel"], stroke=C["ink"], radius=6)
        T(d, c, title, 16, yy + 10, size=14, weight=500, lh=20, w=tw)
        if sub: T(d, c, sub, 16, yy + 12 + 20 * nl, size=12, color=C["muted"], lh=16, w=w - 32 - 96)
        if right: T(d, c, right, w - 16, yy + 10, size=14, weight=500, lh=20, align="right", mono=True,
                    color=C["neg"] if (tone == "neg" and not rsub) else C["ink"])
        if rsub:
            if tone in ("ok", "neg", "warn", "info", "muted"):
                status(d, c, w - 16, yy + 10 + 20 * nl, rsub, tone, align="right")
            else:
                T(d, c, rsub, w - 16, yy + 12 + 20 * nl, size=12, color=C["muted"], lh=16, align="right")
        yy += rh
        if i < len(rows) - 1 and i != selected and i + 1 != selected: hair(d, c, 16, yy - 2, w - 32)
    d.nodes[c]["height"] = float(yy + 4)
    return c, yy + 4

def subtabs(d, f, device, items, active=0, app=DEFAULT_APP, top=None):
    """Faixa de abas logo abaixo do topo. Devolve o novo topo do conteúdo."""
    W = DEVICES[device][0]; pad = PAD[device]
    top = top if top is not None else (56 if device != "mobile" else 52)
    bar = d.frame(f, "Abas", 0, top, W, 44, fill=C["card"])
    hair(d, bar, 0, 43, W)
    tabs(d, bar, pad, 2, items, active=active, app=app, h=42)
    return top + 44

# =====================================================================
# Componentes da marca Smoke House (e-commerce)
# =====================================================================
import telas._dados as DADOS

def brush(d, p, x, y, parts, size=40, align="left", name=None):
    """Título pincelado em duas cores: parts = [("MAIS", "ink"), ("VENDIDOS", "green")]. Devolve a largura."""
    full = " ".join(t for t, _ in parts)
    wt = fc.text_width(full, size, family=DISPLAY)
    cx = x - wt if align == "right" else (x - wt / 2 if align == "center" else x)
    for t, tone in parts:
        col = {"ink": C["ink"], "green": C["green"], "white": "#ffffff", "yellow": C["yellow"]}[tone]
        d.text(p, t, cx, y, size=size, family=DISPLAY, color=col, lh=int(size * 1.1), name=name or full[:40])
        cx += fc.text_width(t + " ", size, family=DISPLAY)
    return wt

def marca_cor(marca):
    return DADOS.CORES_MARCA.get(marca, ("#1b1d1a", "#55584f"))

def foto_produto(d, p, x, y, w, h, marca, radius=12):
    """Sem foto real: bloco na cor da marca com o nome em pincel (como o protótipo, sem gradiente)."""
    c1, c2 = marca_cor(marca)
    t = d.frame(p, f"Foto {marca}", x, y, w, h, fill=c2, radius=radius, clip=True)
    d.frame(t, "Sombra da marca", 0, h * 0.55, w, h * 0.45, fill=c1, fill_opacity=0.55)
    nome = DADOS.NOME_MARCA.get(marca, marca).upper()
    fs = max(14, min(int(w * 0.17), int(h * 0.22)))
    while fc.text_width(nome, fs, family=DISPLAY) > w - 16 and fs > 12: fs -= 2
    d.text(t, nome, w / 2, (h - fs * 1.1) / 2, size=fs, family=DISPLAY, color="#ffffff", align="center", lh=int(fs * 1.1))
    return t

def brl2(v):
    return brl(v)

def card_produto(d, p, x, y, w, prod, compact=False):
    """Cartão da vitrine: foto, nome, preço no Pix (5%), preço no cartão e Adicionar ao carrinho. Devolve a altura."""
    pid, cat, marca, nome, preco, antigo, hot, hl = prod
    ih = int(w * (0.9 if not compact else 0.86))
    c = d.frame(p, f"Produto {nome}"[:40], x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=R_CARD)
    pad = 10 if compact else 12
    foto_produto(d, c, pad, pad, w - 2 * pad, ih - pad, marca, radius=8)
    if antigo:
        off = round((1 - preco / antigo) * 100)
        b = d.frame(c, "Selo", pad + 8, pad + 8, 44, 20, fill=C["yellow"], radius=4)
        T(d, b, f"-{off}%", 22, 2, size=11, weight=700, align="center", lh=16)
    yy = ih + 10
    fs = 12 if compact else 13
    T(d, c, nome, pad, yy, size=fs, weight=500, lh=18, w=w - 2 * pad)
    nl = max(1, -(-int(fc.text_width(nome, fs, 500)) // int(w - 2 * pad)))
    yy += 18 * min(nl, 3) + 8
    pix = preco * 0.95
    T(d, c, brl(pix), pad, yy, size=15 if compact else 17, weight=700, lh=22)
    T(d, c, "no Pix", pad + fc.text_width(brl(pix), 15 if compact else 17, 700) + 4, yy + 5, size=10, color=C["pos"], lh=14, weight=600)
    yy += 22
    cartao = f"ou 3x de {brl(preco / 3)} sem juros" if preco >= 60 else f"ou {brl(preco)} no cartão"  # app.js: até 3x a partir de R$ 60
    T(d, c, cartao, pad, yy, size=11, color=C["muted"], lh=16, w=w - 2 * pad); yy += 24
    button(d, c, pad, yy, "Adicionar ao carrinho" if w >= 200 else "Adicionar", app="loja", kind="dark", w=w - 2 * pad, h=36 if compact else 40)
    yy += (36 if compact else 40) + pad
    d.nodes[c]["height"] = float(yy)
    return yy

def circulo_cat(d, p, x, y, s, label, img):
    o = d.frame(p, f"Categoria {label}", x, y, s, s, fill=C["black"], radius=s / 2, clip=True)
    d.image(o, os.path.join(HERE, "marca", img + ".png"), s * 0.14, s * 0.14, s * 0.72, s * 0.72, name=label, mode="fit")
    T(d, p, label, x + s / 2, y + s + 8, size=12 if s < 80 else 13, weight=600, align="center", lh=18)

def ticker(d, f, device, y=0):
    W = DEVICES[device][0]
    b = d.frame(f, "Faixa de avisos", 0, y, W, 32, fill=C["green"], clip=True)
    cx = 16
    for a, t in DADOS.TICKER:
        d.ellipse(b, cx, 13, 6, C["yellow"], name="Estrela")
        T(d, b, a, cx + 12, 7, size=12, weight=700, color=C["yellow"], lh=18)
        cx += 12 + fc.text_width(a, 12, 700) + 6
        T(d, b, t, cx, 7, size=12, color="#ffffff", lh=18)
        cx += fc.text_width(t, 12) + 28
        if cx > W: break
    return 32

def loja_header(d, f, device, cart_n=0, cart_total=None, store="pnz", busca=""):
    """Topo da vitrine: avisos, barra preta com logo, loja, busca, conta e carrinho; categorias embaixo.
    Celular: logo, loja e ícones; busca em linha própria; categorias vão para a barra de baixo."""
    W = DEVICES[device][0]; pad = PAD[device] if device != "desktop" else 32
    y = ticker(d, f, device)
    mob = device == "mobile"
    hh = 64 if not mob else 104
    bar = d.frame(f, "Topo da loja", 0, y, W, hh, fill=C["black"])
    d.image(bar, os.path.join(HERE, "marca", "logo-branco.png"), pad, 8, 48 if not mob else 44, 42 if not mob else 38, name="Logo")
    code, cidade, _ = DADOS.LOJAS[store]
    px = pad + 64
    pill = d.frame(bar, "Loja escolhida", px, 14 if not mob else 10, 150 if not mob else 132, 36 if not mob else 32, fill="#ffffff", fill_opacity=0.08, radius=18)
    b = d.frame(pill, "Código", 6, 6 if not mob else 5, 34, 24 if not mob else 22, fill=C["green"], radius=12)
    T(d, b, code, 17, 3, size=10, weight=700, color="#ffffff", align="center", lh=16)
    T(d, pill, "Comprando em", 46, 3, size=9, color="#b9bbb4", lh=13)
    T(d, pill, cidade.split(" · ")[0], 46, 16, size=11, weight=600, color="#ffffff", lh=16)
    ix = W - pad
    if mob:
        for ic in ("sacola", "pessoa", "busca"):
            icon(d, bar, ic, ix - 20, 18, 20, "#ffffff"); ix -= 36
        if cart_n:
            bd = d.frame(bar, "Contador", W - pad - 10, 10, 16, 16, fill=C["yellow"], radius=8)
            T(d, bd, str(cart_n), 8, 0, size=10, weight=700, align="center", lh=16)
        sf, _ = field(d, bar, pad, 56, W - 2 * pad, placeholder="Seda, isqueiro, Tattoo Supply", value=busca, prefix_icon="busca", h=40, app="loja")
        y += hh
        return y
    sw = 420 if device == "desktop" else 330
    sx = px + 170
    ph = "O que você procura? Seda, isqueiro, Tattoo Supply" if device == "desktop" else "Seda, isqueiro, Tattoo Supply"
    field(d, bar, sx, 12, sw, placeholder=ph, value=busca, prefix_icon="busca", h=40, app="loja")
    links = [("sacola", "Carrinho", brl(cart_total) if cart_total is not None else "R$ 0,00"), ("pessoa", "Minha conta", "Entrar"), ("pessoas", "Sou colaborador", "Área do vendedor")]
    if device == "tablet": links = links[:2]
    for ic, a, t in links:
        lw = max(fc.text_width(a, 12, 600), fc.text_width(t, 10)) + 28
        ix -= lw
        icon(d, bar, ic, ix, 22, 18, "#ffffff")
        T(d, bar, a, ix + 26, 14, size=12, weight=600, color="#ffffff", lh=18)
        T(d, bar, t, ix + 26, 32, size=10, color="#b9bbb4", lh=14)
        if a == "Carrinho" and cart_n:
            bd = d.frame(bar, "Contador", ix + 6, 8, 16, 16, fill=C["yellow"], radius=8)
            T(d, bd, str(cart_n), 8, 0, size=10, weight=700, align="center", lh=16)
        ix -= 20
    y += hh
    cb = d.frame(f, "Categorias", 0, y, W, 44, fill=C["bar"], clip=True)
    allb = d.frame(cb, "Todas categorias", pad, 0, 168, 44, fill=C["green"])
    icon(d, allb, "menu", 14, 14, 16, "#ffffff")
    T(d, allb, "Todas categorias", 38, 12, size=13, weight=600, color="#ffffff", lh=20)
    cx = pad + 168 + 20
    for m in DADOS.MENU:
        T(d, cb, m, cx, 12, size=13, weight=500, color=C["yellow"] if m == "Ofertas" else "#ffffff", lh=20)
        cx += fc.text_width(m, 13, 500) + 22
    return y + 44

def bottom_nav(d, f, active="Início", cart_n=0, items=None):
    """Celular: barra fixa embaixo (Início, Categorias, Buscar, Carrinho). Resolve a barra de categorias que cobria o checkout."""
    W, _ = DEVICES["mobile"]; H = d.nodes[f]["height"]
    items = items or [("Início", "casa"), ("Categorias", "menu"), ("Buscar", "busca"), ("Carrinho", "sacola")]
    b = d.frame(f, "Barra de navegação", 0, H - 64, W, 64, fill=C["black"])
    iw = W / len(items)
    for i, (lab, ic) in enumerate(items):
        on = lab == active
        col = C["yellow"] if on else "#d6d7d2"
        icon(d, b, ic, i * iw + iw / 2 - 10, 12, 20, col)
        T(d, b, lab, i * iw + iw / 2, 36, size=11, weight=600 if on else 400, color=col, align="center", lh=16)
        if lab == "Carrinho" and cart_n:
            bd = d.frame(b, "Contador", i * iw + iw / 2 + 4, 6, 16, 16, fill=C["yellow"], radius=8)
            T(d, bd, str(cart_n), 8, 0, size=10, weight=700, align="center", lh=16)
    return 64

def whats_fab(d, f, device, bottom_gap=None):
    """Botão do WhatsApp: no celular fica acima da barra de baixo, sem cobrir botões."""
    W, H = DEVICES[device]; H = d.nodes[f]["height"]
    g = bottom_gap if bottom_gap is not None else (80 if device == "mobile" else 24)
    s = 52
    o = d.frame(f, "WhatsApp", W - s - 16, H - g - s, s, s, fill=C["green"], radius=s / 2, shadow=shadow(0.18, 6, 16))
    icon(d, o, "whats", 16, 16, 20, "#ffffff")

def painel_header(d, f, device, area, user, tabs, active, badges=None, app="colab"):
    """Topo escuro dos painéis (colaborador e donos). Computador e tablet: abas embaixo do topo.
    Celular: só o topo; as abas vão para painel_nav (barra de baixo), porque cortavam à direita.
    No computador logo e abas alinham com o conteúdo (1200 centralizado)."""
    W = DEVICES[device][0]; pad = (W - 1200) / 2 if device == "desktop" else (32 if device == "tablet" else PAD[device])
    mob = device == "mobile"
    bar = d.frame(f, "Topo do painel", 0, 0, W, 60, fill=C["black"])
    d.image(bar, os.path.join(HERE, "marca", "logo-branco.png"), pad, 9, 48, 42, name="Logo")
    tag = d.frame(bar, "Área", pad + 60, 18, fc.text_width(area, 11, 600) + 20, 24, fill=C["yellow"] if app == "donos" else C["green"], radius=12)
    T(d, tag, area, 10, 3, size=11, weight=600, color=C["ink"] if app == "donos" else "#ffffff", lh=18)
    if not mob:
        bx = W - pad
        for lab in ("Sair", "Ver loja"):
            bw = fc.text_width(lab, 12, 600) + 28; bx -= bw
            o = d.frame(bar, lab, bx, 14, bw, 32, stroke="#ffffff", stroke_opacity=0.3, radius=16)
            T(d, o, lab, bw / 2, 6, size=12, weight=600, color="#ffffff", align="center", lh=20)
            bx -= 8
        nm, sub = user
        T(d, bar, nm, bx - 12, 12, size=13, weight=600, color="#ffffff", align="right", lh=18)
        T(d, bar, sub, bx - 12, 30, size=11, color="#b9bbb4", align="right", lh=16)
        tb = d.frame(f, "Abas", 0, 60, W, 48, fill=C["bar"])
        cx = pad
        for i, t in enumerate(tabs):
            on = t == active
            T(d, tb, t, cx, 14, size=13, weight=600 if on else 500, color="#ffffff" if on else "#c9cac4", lh=20)
            tw = fc.text_width(t, 13, 600 if on else 500)
            if badges and badges.get(t):
                bd = d.frame(tb, "Contador", cx + tw + 6, 15, 18, 18, fill=C["yellow"], radius=9)
                T(d, bd, str(badges[t]), 9, 1, size=10, weight=700, align="center", lh=16)
                tw += 24
            if on: d.frame(tb, "Aba ativa", cx, 45, tw, 3, fill=C["yellow"])
            cx += tw + 28
        return 108
    nm, sub = user
    o = d.frame(bar, "Inicial", W - pad - 32, 14, 32, 32, fill=C["green"], radius=16)
    T(d, o, nm[0], 16, 6, size=13, weight=700, color="#ffffff", align="center", lh=20)
    return 60

def painel_nav(d, f, tabs, active, icons, badges=None):
    """Celular: as abas do painel viram barra fixa embaixo (até 5; o resto em "Mais")."""
    W, _ = DEVICES["mobile"]; H = d.nodes[f]["height"]
    items = list(zip(tabs, icons))
    if len(items) > 5: items = items[:4] + [("Mais", "pontos")]
    b = d.frame(f, "Barra do painel", 0, H - 64, W, 64, fill=C["black"])
    iw = W / len(items)
    for i, (lab, ic) in enumerate(items):
        on = lab == active
        col = C["yellow"] if on else "#d6d7d2"
        icon(d, b, ic, i * iw + iw / 2 - 10, 12, 20, col)
        T(d, b, lab, i * iw + iw / 2, 36, size=11, weight=600 if on else 400, color=col, align="center", lh=16)
        if badges and badges.get(lab):
            bd = d.frame(b, "Contador", i * iw + iw / 2 + 4, 6, 16, 16, fill=C["yellow"], radius=8)
            T(d, bd, str(badges[lab]), 8, 0, size=10, weight=700, align="center", lh=16)
    return 64
