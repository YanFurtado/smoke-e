"""Componentes do PDV Smoke House, na direção visual de pdv/02-direcao-visual.md.

Regras que valem para todas as telas (não mude sem mudar o documento):
- Grade de 4 px. Raio: tecla 4, controle 8, cartão 12, janela 16.
- Neutros levemente quentes; a cor do aplicativo (DAV verde, NFC-e azul-petróleo,
  HOST azul-petróleo escuro) só no botão principal, no foco e numa marca do topo.
- Inter 400/500 (600 raro). Menlo para cupom, códigos, teclas e valores de tabela.
- Seleção em lista: fundo cinza claro + borda fina preta (spec, "Seleção em listas").
- Sem emoji, sem gradiente, sem brilho, sem texto em caixa alta espaçada,
  sem ponto final em rótulo/botão, sem exclamação.
- Assinatura: teclas (keycaps). Momento: o cupom em papel térmico e o TOTAL.
"""
import os
import fc

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- tokens ----------
C = {
    "page": "#f4f3ef",      # fundo da tela
    "deep": "#ebe9e3",      # faixa lateral / barra de vendas
    "card": "#ffffff",
    "raised": "#eeece6",    # campo, linha ativa
    "sel": "#e6e4de",       # linha selecionada (spec: cinza claro)
    "ink": "#1c1b18",       # texto principal e borda da seleção
    "text2": "#55534d",     # texto secundário
    "muted": "#77746c",     # meta, legenda, ícone
    "line": "#1c1b18",      # hairline = ink a 9%
    "paper": "#fffdf8",     # bobina térmica
    "pos": "#256d45",       # positivo
    "neg": "#b4332f",       # erro, cancelado
    "warn": "#9a6400",      # aviso
    "info": "#1b6670",      # interrogação das janelas Sim/Não
    "overlay": "#1c1b18",
}
LINE_A = 0.10
APPS = {
    "dav":  {"nome": "Frente de caixa", "sigla": "DAV",   "acc": "#256d45", "soft": "#e3efe7", "logo": "logo-verde.png"},
    "nfce": {"nome": "Cupom fiscal",    "sigla": "NFC-e", "acc": "#1b6670", "soft": "#e1eef0", "logo": "logo-verde.png"},
    "host": {"nome": "Retaguarda",      "sigla": "HOST",  "acc": "#134a52", "soft": "#e0eaec", "logo": "logo-verde.png"},
}
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
    elif name == "whats": O(8, 8, 6.5); L([(3, 14.5), (3.8, 11.8)])
    elif name == "calendario": L([(2, 3), (14, 3), (14, 14), (2, 14), (2, 3)]); L([(2, 6.5), (14, 6.5)]); L([(5, 1.5), (5, 4)]); L([(11, 1.5), (11, 4)])
    elif name == "filtro": L([(2, 3), (14, 3), (9.5, 8.5), (9.5, 13), (6.5, 14.5), (6.5, 8.5), (2, 3)])
    elif name == "mais-circ": O(8, 8, 6.5); L([(8, 5), (8, 11)]); L([(5, 8), (11, 8)])
    elif name == "pontos": O(3, 8, 0.6); O(8, 8, 0.6); O(13, 8, 0.6)
    elif name == "voltar": L([(6, 3), (2, 7), (6, 11)]); L([(2, 7), (11, 7), (14, 10), (14, 14)])
    elif name == "nuvem": L([(4, 13), (2, 11), (2, 8.5), (4, 6.5), (6, 6.5), (7.5, 3.5), (11, 3), (13, 5.5), (13, 7.5), (15, 9), (15, 11.5), (13, 13), (4, 13)])
    elif name == "chave": O(5, 11, 3); L([(7, 9), (14, 2)]); L([(11, 5), (13, 7)])
    elif name == "pin": O(8, 6.5, 2); L([(8, 15), (3.5, 9), (3, 6.5), (5, 2.5), (8, 1.5), (11, 2.5), (13, 6.5), (12.5, 9), (8, 15)])
    else: O(8, 8, 6)

# ---------- controles ----------
def button(d, p, x, y, label, app="dav", kind="secondary", w=None, h=40, key=None, icon_name=None, align="center", disabled=False, sub=None):
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

def field(d, p, x, y, w, label=None, value="", placeholder="", focused=False, app="dav", h=40,
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

def toggle(d, p, x, y, on=True, label=None, app="dav", sub=None):
    t = d.frame(p, "Chave", x, y, 36, 20, fill=acc(app) if on else C["raised"], stroke=None if on else C["line"],
                stroke_opacity=0.18, radius=10)
    d.ellipse(t, 18 if on else 2, 2, 16, "#ffffff", name="Botão da chave")
    if label:
        T(d, p, label, x + 48, y, size=14, lh=20)
        if sub: T(d, p, sub, x + 48, y + 20, size=12, color=C["muted"], lh=16)

def checkbox(d, p, x, y, on=False, label=None, app="dav"):
    b = d.frame(p, "Marcação", x, y, 18, 18, fill=acc(app) if on else C["card"], stroke=None if on else C["ink"],
                stroke_opacity=0.3, radius=4)
    if on: icon(d, b, "ok", 1, 1, 16, "#ffffff")
    if label: T(d, p, label, x + 28, y - 1, size=14, lh=20)

def radio(d, p, x, y, on=False, label=None, app="dav"):
    d.ellipse(p, x, y, 18, C["card"], name="Opção", stroke=acc(app) if on else C["muted"])
    if on: d.ellipse(p, x + 5, y + 5, 8, acc(app), name="Opção marcada")
    if label: T(d, p, label, x + 28, y - 1, size=14, lh=20)

def tabs(d, p, x, y, items, active=0, app="dav", h=40, counts=None):
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

def chips(d, p, x, y, items, active=0, app="dav", wrap_w=None):
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

def banner(d, p, x, y, w, title, text=None, tone="warn", action=None, app="dav"):
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

def table(d, p, x, y, w, cols, rows, selected=None, row_h=40, header=True, app="dav", dim_rows=(), zebra=False,
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

def card(d, p, x, y, w, h, title=None, action=None, app="dav", fill=None, pad=20):
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

def product_tile(d, p, x, y, s, label, hue="#2b2a26", h=None):
    """Foto do produto: enquanto não há foto real, bloco com a sigla da marca (igual ao e-commerce)."""
    w, h = s, (h or s)
    m = min(w, h)
    t = d.frame(p, f"Foto {label}", x, y, w, h, fill=hue, radius=max(4, min(12, m // 6)))
    fs = max(9, int(m * 0.26)); lh = int(fs * 1.3)
    T(d, t, label[:3].upper(), w / 2, (h - lh) / 2, size=fs, weight=600, color="#f4f3ef", align="center", lh=lh, mono=True)
    return t

def produto(cod):
    for p in PRODUTOS:
        if p[0] == cod: return p
    return PRODUTOS[0]

def avatar(d, p, x, y, s, name):
    a = d.frame(p, f"Inicial {name}", x, y, s, s, fill=C["raised"], radius=s / 2)
    ini = "".join(w[0] for w in name.split()[:2]).upper()
    T(d, a, ini, s / 2, (s - 16) / 2, size=12, weight=500, color=C["text2"], align="center", lh=16)

# ---------- moldura das telas ----------
def screen(d, page, name, device, x, y, h=None, app="dav"):
    w, hh = DEVICES[device]
    f = d.frame(page, name, x, y, w, h or hh, fill=C["page"], clip=True)
    return f, w, h or hh

def topbar(d, f, device, app="dav", user="Arthur", terminal="Terminal 01", nav=True, right=None):
    """Logo + terminal; navegação entre os três aplicativos; só 'Usuário: nome' à direita (spec, Visão geral)."""
    w = DEVICES[device][0]
    h = 56 if device != "mobile" else 52
    bar = d.frame(f, "Barra superior", 0, 0, w, h, fill=C["card"])
    hair(d, bar, 0, h - 1, w)
    pad = PAD[device]
    d.image(bar, os.path.join(HERE, "marca", APPS[app]["logo"]), pad, 8 if device != "mobile" else 8, 41, 36, name="Logo Smoke House")
    T(d, bar, "Smoke House", pad + 52, 9 if device != "mobile" else 8, size=14, weight=500, lh=20)
    T(d, bar, terminal if app != "host" else "Retaguarda · Loja PNZ", pad + 52, 27 if device != "mobile" else 26, size=12, color=C["muted"], lh=16)
    if nav and device != "mobile":
        nx = pad + 220 if device == "desktop" else pad + 200
        for key in ("dav", "nfce", "host"):
            a = APPS[key]
            label = a["nome"]
            tw = fc.text_width(label, 14, 500 if key == app else 400)
            on = key == app
            tab = d.frame(bar, f"App {label}", nx, 10, tw + 36, 36, fill=C["raised"] if on else None, radius=R_CTL)
            d.ellipse(tab, 12, 14, 8, a["acc"], name=f"Cor {a['sigla']}")
            T(d, tab, label, 26, 8, size=14, weight=500 if on else 400, color=C["ink"] if on else C["text2"], lh=20)
            nx += tw + 36 + 4
    if device == "mobile":
        T(d, bar, f"Usuário: {user}", w - pad, 16, size=13, color=C["text2"], align="right", lh=20)
    else:
        T(d, bar, right or f"Usuário: {user}", w - pad, 18, size=13, color=C["text2"], align="right", lh=20)
    return h

FOOT_KEYS = [("F1", "Cliente"), ("F3", "Pagamento"), ("F6", "Cancelar cupom"), ("F7", "Nova venda"),
             ("F8", "Trocar venda"), ("F10", "Alterar valor"), ("F11", "Menu")]

def footer(d, f, device, app="dav", keys=FOOT_KEYS, server=True, version="Versão 1.2.02"):
    """Rodapé: só as teclas e se o servidor está conectado (spec). No tablet as teclas viram botões de toque."""
    w, hh = DEVICES[device]
    H = d.nodes[f]["height"]
    if device == "mobile":
        return 0
    h = 40 if device == "desktop" else 56
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
    ok = C["pos"] if server else C["neg"]
    lab = "Servidor conectado" if server else "Sem conexão com o servidor"
    d.ellipse(bar, w - pad - fc.text_width(lab, 12) - 16, h / 2 - 4, 8, ok, name="Situação do servidor")
    T(d, bar, lab, w - pad, h / 2 - 10, size=12, color=C["text2"], align="right", lh=20)
    return h

def mobile_bar(d, f, total, itens, app="dav", label="Pagamento", key="F3"):
    """Celular: barra fixa embaixo com o total e o botão principal."""
    w, hh = DEVICES["mobile"]
    H = d.nodes[f]["height"]
    bar = d.frame(f, "Barra do total", 0, H - 88, w, 88, fill=C["card"])
    hair(d, bar, 0, 0, w)
    T(d, bar, f"{itens} itens", 16, 14, size=12, color=C["muted"], lh=16)
    T(d, bar, total, 16, 32, size=28, weight=500, lh=36)
    button(d, bar, w - 16 - 148, 22, label, app=app, kind="primary", w=148, h=44, key=key)
    return 88

def overlay(d, f):
    w = d.nodes[f]["width"]; h = d.nodes[f]["height"]
    return d.frame(f, "Fundo da janela", 0, 0, w, h, fill=C["overlay"], fill_opacity=0.32)

def window(d, f, device, title, w, h, app="dav", footer_buttons=None, close=True):
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

def confirm(d, f, device, question, lines=(), app="dav", yes="Sim", no="Não", danger=False):
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

def sidebar(d, f, device, active="Estoque", user="Lucas", store="Loja PNZ · Petrolina"):
    """HOST: menu lateral de 248. No celular vira menu (☰) e não é desenhado."""
    H = d.nodes[f]["height"]
    if device == "mobile":
        return 0
    w = 248 if device == "desktop" else 216
    top = 56
    s = d.frame(f, "Menu lateral", 0, top, w, H - top, fill=C["deep"])
    d.frame(s, "Divisa", w - 1, 0, 1, H - top, fill=C["line"], fill_opacity=LINE_A)
    groups = [
        (None, [("Início", "grafico"), ("Caixas", "caixa"), ("Clientes", "pessoas"), ("Estoque", "caixa"),
                ("Contas a receber", "moeda"), ("Contas a pagar", "doc"), ("Relatórios", "doc"), ("Chamados", "chat")]),
        ("Cadastros", [("Fornecedores", "caminhao"), ("Formas de pagamento", "moeda"), ("Usuários", "pessoa")]),
        ("Sistema", [("Configurações", "engrenagem"), ("Fiscal", "nota"), ("Integrações", "link")]),
    ]
    y = 16
    for g, items in groups:
        if g:
            y += 16
            T(d, s, g, 20, y, size=12, color=C["muted"], lh=16); y += 24
        for lab, ic in items:
            on = lab == active
            row = d.frame(s, f"Menu {lab}", 8, y, w - 16, 34, fill=C["card"] if on else None,
                          stroke=C["line"] if on else None, stroke_opacity=LINE_A, radius=R_CTL)
            if on: d.frame(row, "Marca", 0, 9, 3, 16, fill=APPS["host"]["acc"], radius=2)
            icon(d, row, ic, 12, 9, 16, C["ink"] if on else C["muted"])
            T(d, row, lab, 38, 7, size=14, weight=500 if on else 400, color=C["ink"] if on else C["text2"], lh=20)
            y += 36
    T(d, s, store, 20, H - top - 52, size=12, color=C["muted"], lh=16)
    T(d, s, "Versão 1.2.02", 20, H - top - 32, size=12, color=C["muted"], lh=16, mono=True)
    return w

def page_head(d, p, x, y, w, title, sub=None, actions=(), app="host", device="desktop"):
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

# ---------- o cupom (momento) ----------
def cupom_tela(d, p, x, y, w, h, itens, cliente=None, doc=None, selecionado=None, app="dav", titulo="Cupom", cancelados=(),
               doc_label="CPF/CNPJ do consumidor"):
    """Cupom à esquerda na tela de venda: papel térmico, item, cadastro e descrição (sem código de barras)."""
    c = d.frame(p, "Cupom na tela", x, y, w, h, fill=C["paper"], stroke=C["line"], stroke_opacity=LINE_A,
                radius=[R_CARD, R_CARD, 0, 0], clip=True)
    T(d, c, titulo, 20, 16, size=13, color=C["muted"], lh=20)
    if cliente:
        T(d, c, cliente, 20, 36, size=15, weight=500, lh=22)
        T(d, c, f"{doc_label}  {doc or '—'}", 20, 58, size=12, color=C["text2"], lh=16, mono=True)
        y0 = 88
    else:
        T(d, c, "Consumidor não identificado", 20, 36, size=14, color=C["text2"], lh=20)
        y0 = 68
    hair(d, c, 20, y0, w - 40)
    compact = w < 420
    if compact:
        T(d, c, "Item  Descrição", 20, y0 + 10, size=11, color=C["muted"], lh=16, mono=True)
        T(d, c, "Total", w - 20, y0 + 10, size=11, color=C["muted"], lh=16, mono=True, align="right")
    else:
        T(d, c, "Item  Cód.    Descrição", 20, y0 + 10, size=11, color=C["muted"], lh=16, mono=True)
        T(d, c, "Qtde × Unit.      Total", w - 20, y0 + 10, size=11, color=C["muted"], lh=16, mono=True, align="right")
    yy = y0 + 36
    rh = 44
    vis = itens[-int((h - yy - 24) // rh):] if itens else []
    start = len(itens) - len(vis)
    for i, it in enumerate(vis):
        n = start + i + 1
        cod, nome, q, unit = it
        last = n == len(itens) and selecionado is None or n == selecionado
        if last:
            d.frame(c, "Último item", 8, yy - 2, w - 16, rh, fill=APPS[app]["soft"], radius=6)
        pre = f"{n:03d}  " if compact else f"{n:03d}  {cod}  "
        px = 20 + fc.text_width(pre, 12, 400, True)
        nw = w - 20 - px - 84
        nl = max(1, -(-int(fc.text_width(nome, 13, 500 if last else 400)) // int(nw)))
        rh_i = rh + 18 * (nl - 1)
        if last:
            d.nodes[d.nodes[c]["children"][-1]]["height"] = float(rh_i)
        T(d, c, pre.strip(), 20, yy + 2, size=12, color=C["text2"], lh=16, mono=True)
        T(d, c, nome, px, yy + 1, size=13, weight=500 if last else 400, lh=18, w=nw)
        T(d, c, (f"{cod} · " if compact else "") + f"{q} × {brl(unit)[3:]}", px, yy + 3 + 18 * nl, size=12, color=C["muted"], lh=16, mono=True)
        T(d, c, brl(q * unit)[3:], w - 20, yy + (rh_i - 18) / 2 - 2, size=13, lh=18, mono=True, align="right", weight=500 if last else 400)
        yy += rh_i
    # serrilha da bobina
    pts = []
    for i in range(int(w // 8) + 1):
        pts.append((i * 8, 0)); pts.append((i * 8 + 4, 5))
    serr = d.frame(p, "Serrilha", x, y + h, w, 6, fill=None, clip=True)
    d.polyline(serr, pts, C["ink"], weight=1, name="Serrilha", x=0, y=0)
    d.nodes[serr]["opacity"] = 0.18
    return c

def total_block(d, p, x, y, w, total, itens, app="dav", device="desktop"):
    big = 72 if device == "desktop" else 52
    T(d, p, "Qtde itens", x, y, size=13, color=C["text2"], lh=20)
    T(d, p, str(itens), x + w, y, size=13, color=C["ink"], lh=20, align="right", mono=True)
    hair(d, p, x, y + 32, w)
    T(d, p, "Total", x, y + 48, size=13, color=C["text2"], lh=20)
    T(d, p, total, x + w, y + 70, size=big, weight=500, lh=big + 8, align="right")
    return 70 + big + 8

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

# ---------- dados de exemplo (plausíveis, da loja) ----------
PRODUTOS = [  # cadastro, gtin, nome, preço, frente, fundo, unidade, sigla, cor
    ("006264", "7898920550018", "Seda Zomo King Size Brown", 5.00, 42, 120, "UN", "ZOM", "#1b1d1a"),
    ("006265", "7898920550025", "Seda Zomo King Size Rosa", 5.00, 18, 60, "UN", "ZOM", "#1b1d1a"),
    ("004118", "7896009401121", "Seda Papelito King Size Brown Large", 7.00, 31, 80, "UN", "PAP", "#4a3216"),
    ("004120", "7896009401206", "Papelito Marrom c/ Piteira + Bandeja", 15.00, 9, 24, "UN", "PAP", "#4a3216"),
    ("003301", "7896066300214", "OCB King Size Slim Premium", 8.00, 27, 50, "UN", "OCB", "#2b2a26"),
    ("003302", "7896066300221", "OCB King Size Slim Ultimate", 10.00, 4, 36, "UN", "OCB", "#2b2a26"),
    ("002210", "7891234100016", "Isqueiro Clipper Largo Estampado", 14.00, 22, 48, "UN", "CLI", "#7d1022"),
    ("002251", "0041689103323", "Isqueiro Zippo Classic Brushed Chrome", 289.00, 3, 2, "UN", "ZIP", "#3a3b37"),
    ("005510", "7898941230104", "Essência Zomo Strong Mint 50 g", 18.00, 0, 14, "UN", "ZOM", "#1b1d1a"),
    ("005514", "7898941230142", "Essência Zomo Love 66 50 g", 18.00, 12, 30, "UN", "ZOM", "#1b1d1a"),
    ("007702", "7899500100227", "Piteira de vidro Squadafum 6 mm", 25.00, 15, 20, "UN", "SQU", "#0f3a40"),
    ("007780", "7899500100753", "Dichavador metal 4 partes 50 mm", 45.00, 7, 10, "UN", "DIC", "#3a3b37"),
    ("008801", "7898953200010", "Bandeja Bem Bolado média", 39.90, 6, 12, "UN", "BEM", "#174a2e"),
    ("009102", "2000000091020", "Kit presente Smoke House", 79.90, 5, 8, "KIT", "SMK", "#256d45"),
    ("006290", "7898920551299", "Caixa c/50 Seda Zomo KS Brown", 120.00, 2, 6, "CX", "ZOM", "#1b1d1a"),
    ("004401", "7891991010474", "Carvão de coco Zomo 1 kg", 32.00, 11, 40, "PCT", "ZOM", "#1b1d1a"),
]
CLIENTES = [
    ("Mariana Albuquerque", "(87) 98841-2207", "123.456.789-09"),
    ("Rafael Coelho Nunes", "(87) 99102-7754", "987.654.321-00"),
    ("Tabacaria do Porto Ltda", "(87) 3861-4410", "12.345.678/0001-90"),
    ("João Victor Sampaio", "(87) 98122-0451", "321.654.987-12"),
    ("Larissa Menezes", "(87) 99643-1180", "456.789.123-45"),
    ("Pedro Henrique Brandão", "(87) 98810-3369", "741.852.963-00"),
]

# ---------- moldura do HOST e listas do celular ----------
def host_shell(d, f, device, active, user="Lucas"):
    """Topo + menu lateral do HOST. Devolve (x, y, largura, base) da área de conteúdo."""
    W, H = DEVICES[device]
    top = topbar(d, f, device, "host", user=user)
    sw = sidebar(d, f, device, active=active, user=user)
    pad = PAD[device]
    if device == "mobile":
        icon(d, f, "menu", pad, top + 14, 16, C["text2"])
        T(d, f, active, pad + 24, top + 12, size=13, color=C["text2"], lh=20, name="Menu do HOST")
        return pad, top + 44, W - 2 * pad, H - pad
    return sw + 32, top + 28, W - sw - 32 - 32 if device == "desktop" else W - sw - 24 - 20, H - 24

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

def caixa_abas(d, f, device, active=0, app="dav"):
    """Abas da frente de caixa logo abaixo do topo (spec: aba DAVs emitidos / Notas emitidas, aba Fechamento de caixa)."""
    W = DEVICES[device][0]; pad = PAD[device]
    top = 56 if device != "mobile" else 52
    items = ["Venda", "DAVs emitidos", "Fechamento de caixa"] if app == "dav" else ["Venda", "Notas emitidas"]
    bar = d.frame(f, "Abas da frente de caixa", 0, top, W, 44, fill=C["card"])
    hair(d, bar, 0, 43, W)
    tabs(d, bar, pad, 2, items, active=active, app=app, h=42)
    return top + 44
