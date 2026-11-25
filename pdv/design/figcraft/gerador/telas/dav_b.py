"""DAV (Frente de caixa), parte B: clientes, DAVs emitidos, movimentos e fechamento.

Telas D13 a D24. As telas de fundo (venda e caixa livre) vêm de telas.dav_a.
"""
import math
import fc, ui
from ui import C, T, brl, PAD, DEVICES, hair, LINE_A, R_CTL, R_CARD
from telas.dav_a import d04, d02, ITENS, TOTAL, NITENS

PAGE = "01b · Frente de caixa (DAV) · clientes, movimentos e fechamento"
APP = "dav"

def v(x):
    """Valor sem o prefixo R$ (tabelas e bobina)."""
    return brl(x)[3:] if x >= 0 else "-" + brl(-x)[3:]

# ======================================================================
# componentes locais (candidatos ao ui.py)
# ======================================================================
def _fit(s, size, maxw, weight=400, mono=False):
    """Corta o texto com reticências para caber em maxw."""
    if fc.text_width(s, size, weight, mono) <= maxw:
        return s
    while s and fc.text_width(s + "…", size, weight, mono) > maxw:
        s = s[:-1]
    return s.rstrip() + "…"

def _tag(d, p, x, y, label, h=22):
    """Etiqueta do cliente (VIP, Recorrente…): neutra, sem cor."""
    tw = fc.text_width(label, 12, 500)
    w = int(tw + 16 + 3) // 4 * 4
    t = d.frame(p, f"Etiqueta {label}", x, y, w, h, fill=C["raised"], stroke=C["line"], stroke_opacity=0.12, radius=4)
    T(d, t, label, 8, (h - 16) / 2, size=12, weight=500, color=C["text2"], lh=16)
    return w

def _bolo(d, p, x, y, s=16, color=None):
    """Bolinho de aniversário desenhado com linhas (não é emoji)."""
    c = color or C["text2"]; k = s / 16
    def L(pts): d.polyline(p, [(x + a * k, y + b * k) for a, b in pts], c, weight=1.5, name="Bolinho")
    L([(2, 9), (14, 9), (14, 15), (2, 15), (2, 9)])
    L([(2, 12), (5, 11), (8, 12), (11, 11), (14, 12)])
    L([(8, 9), (8, 5.5)])
    d.ellipse(p, x + 6.6 * k, y + 1.2 * k, 2.8 * k, C["warn"], name="Chama do bolinho")

def _aviso_bolo(d, p, x, y, w, title, text):
    """Aviso de aniversário na ficha: igual ao banner, com o bolinho no lugar do ícone."""
    h = 60
    b = d.frame(p, "Aviso de aniversário", x, y, w, h, fill=C["card"], stroke=C["warn"], stroke_opacity=0.35, radius=R_CTL)
    d.frame(b, "Faixa", 0, 0, 3, h, fill=C["warn"], radius=[R_CTL, 0, 0, R_CTL])
    _bolo(d, b, 16, 12, 16)
    T(d, b, title, 44, 9, size=14, weight=500, lh=20)
    T(d, b, text, 44, 31, size=13, color=C["text2"], lh=20, w=w - 60)
    return h

def _grade(d, p, x, y, w, cells, cols=None, h=60, vsize=16, name="Números"):
    """Quadro de números em linha (ou grade no celular): rótulo pequeno em cima, valor em Menlo."""
    n = len(cells); cols = cols or n; rows = math.ceil(n / cols)
    b = d.frame(p, name, x, y, w, h * rows, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CTL)
    cw = w / cols
    for i, (lab, val, *tone) in enumerate(cells):
        r, c = divmod(i, cols)
        cx, cy = c * cw, r * h
        if c: d.frame(b, "Divisa", cx, cy + 12, 1, h - 24, fill=C["line"], fill_opacity=LINE_A)
        if r and c == 0: hair(d, b, 12, cy, w - 24)
        T(d, b, lab, cx + 14, cy + 10, size=12, color=C["muted"], lh=16)
        col = {"neg": C["neg"], "ok": C["pos"], "warn": C["warn"]}.get(tone[0] if tone else None, C["ink"])
        T(d, b, _fit(val, vsize, cw - 24, 500, True), cx + 14, cy + 30, size=vsize, weight=500, lh=vsize + 6, mono=True, color=col)
    return h * rows

def _area(d, p, x, y, w, h, label, value="", app="dav", focused=False, error=None):
    """Campo de várias linhas (justificativa, observação)."""
    if label:
        T(d, p, label, x, y, size=13, color=C["text2"], lh=16)
    fr = d.frame(p, f"Campo {label}", x, y + 20, w, h, fill=C["card"],
                 stroke=ui.acc(app) if focused else (C["neg"] if error else C["line"]),
                 stroke_opacity=1.0 if (focused or error) else 0.16, stroke_w=2 if focused else 1, radius=R_CTL)
    if value:
        T(d, fr, value, 12, 10, size=14, lh=20, w=w - 24)
    if focused:
        lw_ = fc.text_width(value.split("\n")[-1], 14) if value else 0
        d.frame(fr, "Cursor", 12 + lw_ + 1, 10, 1.5, 20, fill=C["ink"])
    if error:
        T(d, p, error, x, y + 20 + h + 4, size=12, color=C["neg"], lh=16)
    return 20 + h

def _opcoes(d, p, x, y, w, items, active, app="dav", h=40, name="Opções"):
    """Escolha única em botões lado a lado; o escolhido usa a seleção da spec (cinza claro + borda preta)."""
    n = len(items); gap = 8; bw = (w - gap * (n - 1)) / n
    for i, lab in enumerate(items):
        on = i == active
        b = d.frame(p, f"{name} {lab}", x + i * (bw + gap), y, bw, h, fill=C["sel"] if on else C["card"],
                    stroke=C["ink"] if on else C["line"], stroke_opacity=1.0 if on else 0.16, radius=R_CTL)
        T(d, b, lab, bw / 2, (h - 20) / 2, size=14, weight=500 if on else 400, color=C["ink"] if on else C["text2"],
          align="center", lh=20)
    return h

def _menu_ctx(d, p, x, y, w, items, sel=0):
    """Menu de contexto (⋯ ou clique direito). items: (rótulo, ícone, habilitado, perigoso)."""
    rh = 36
    h = 8 + rh * len(items)
    m = d.frame(p, "Menu da venda", x, y, w, h, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CARD,
                shadow=ui.shadow(0.10, 12, 32))
    for i, (lab, ic, on, danger) in enumerate(items):
        ry = 4 + i * rh
        if i == sel:
            d.frame(m, "Linha selecionada", 4, ry, w - 8, rh, fill=C["sel"], stroke=C["ink"], radius=6)
        col = C["neg"] if danger and on else (C["ink"] if on else C["muted"])
        op = 1.0 if on else 0.55
        ui.icon(d, m, ic, 16, ry + 10, 16, C["neg"] if danger and on else (C["text2"] if on else C["muted"]))
        T(d, m, lab, 44, ry + 8, size=14, color=col, lh=20, opacity=op)
    return h

def _win_foot(d, win, w, h, dev, buttons, app="dav", keys=()):
    """Rodapé da janela com botões (rótulo, tipo, tecla, desabilitado) e, à esquerda, teclas de lista."""
    hair(d, win, 0, h - 72, w)
    if dev == "mobile":
        n = len(buttons); bw = (w - 32 - 8 * (n - 1)) / n; bx = 16
        for lab, kind, key, dis in buttons:
            need = fc.text_width(lab, 14, 500) + (fc.text_width(key, 11, 500, True) + 18 if key else 0) + 24
            ui.button(d, win, bx, h - 56, lab, app=app, kind=kind, w=bw, key=key if need <= bw else None, disabled=dis)
            bx += bw + 8
        return h - 72
    bx = w - 24
    for lab, kind, key, dis in reversed(buttons):
        bw = int(fc.text_width(lab, 14, 500) + (fc.text_width(key, 11, 500, True) + 18 if key else 0) + 32 + 3) // 4 * 4
        bx -= bw
        ui.button(d, win, bx, h - 56, lab, app=app, kind=kind, w=bw, key=key, disabled=dis)
        bx -= 8
    kx = 24
    for k, lab in keys:
        for kk in k.split(" "):
            kx += ui.keycap(d, win, kx, h - 46, kk) + 4
        T(d, win, lab, kx + 2, h - 46, size=12, color=C["text2"], lh=20)
        kx += fc.text_width(lab, 12) + 20
    return h - 72

def _autoriza(d, p, x, y, w, app="dav", titulo="Senha do supervisor", quem="Carla · Supervisora de caixa",
              label="Quem autoriza", stacked=False, focused=True, error=None, chevron=True):
    """Bloco de autorização: quem autoriza e a senha dele."""
    T(d, p, titulo, x, y, size=15, weight=500, lh=20)
    y += 32
    if stacked:
        ui.field(d, p, x, y, w, label=label, value=quem, chevron=chevron, readonly=not chevron, app=app)
        ui.field(d, p, x, y + 72, w, label="Senha", value="••••", focused=focused, app=app, mono=True, error=error)
        return 32 + 72 + 60 + (20 if error else 0)
    hw = (w - 16) / 2
    ui.field(d, p, x, y, hw, label=label, value=quem, chevron=chevron, readonly=not chevron, app=app)
    ui.field(d, p, x + hw + 16, y, hw, label="Senha", value="••••", focused=focused, app=app, mono=True, error=error)
    return 32 + 60 + (20 if error else 0)

def _barras(d, p, x, y, w, h, vals, labs, hi, app="dav", hi_label=None):
    """Gráfico de barras simples: neutro, com a cor de destaque só na barra hi (mês atual)."""
    n = len(vals); gap = 6 if w > 260 else 4
    bw = (w - gap * (n - 1)) / n; mx = max(vals); base = h - 20
    top_pad = 22 if hi_label else 4
    for i, val in enumerate(vals):
        bh = max(4, (base - top_pad) * val / mx)
        bx = x + i * (bw + gap)
        on = i == hi
        d.frame(p, f"Barra {labs[i]}", bx, y + base - bh, bw, bh, fill=ui.acc(app) if on else "#d9d6ce", radius=[3, 3, 0, 0])
        T(d, p, labs[i], bx + bw / 2, y + h - 16, size=11, color=C["ink"] if on else C["muted"], align="center", lh=16)
        if on and hi_label:
            T(d, p, hi_label, bx + bw, y, size=11, color=C["ink"], align="right", lh=16, mono=True)
    hair(d, p, x, y + base, w)
    return h

def _abas(d, f, dev, active):
    """Abas da Frente de caixa: Venda, DAVs emitidos e Fechamento de caixa (spec)."""
    W = DEVICES[dev][0]; pad = PAD[dev]
    top = 56 if dev != "mobile" else 52
    bar = d.frame(f, "Abas da frente de caixa", 0, top, W, 44, fill=C["card"])
    hair(d, bar, 0, 43, W)
    ui.tabs(d, bar, pad, 2, ["Venda", "DAVs emitidos", "Fechamento de caixa"], active=active, app="dav", h=42)
    return top + 44

def _secao(d, p, x, y, title, right=None, w=None):
    T(d, p, title, x, y, size=15, weight=500, lh=20)
    if right and w:
        T(d, p, right, x + w, y + 1, size=13, color=C["muted"], align="right", lh=20, mono=True)
    return 28

def _alto(d, f, dev, hh):
    """Tela que rola no celular: aumenta o quadro antes de desenhar."""
    d.nodes[f]["height"] = float(hh)
    return hh

# ======================================================================
# dados de exemplo
# ======================================================================
BUSCA_NOME = [  # nome, telefone, aniversário em até 7 dias, extra
    ("Mariana Albuquerque", "(87) 98841-2207", True, None),
    ("Maria Clara Torres", "(87) 98107-3345", False, None),
    ("Marina Gonçalves Lima", "(77) 99812-0034", False, None),
    ("Mário Sérgio Pacheco", "(87) 99630-2218", False, None),
]
ULTIMAS = [("21/11/2026", "001431", 95.00), ("14/11/2026", "001302", 62.00), ("07/11/2026", "001188", 118.40),
           ("02/11/2026", "001095", 37.00), ("31/10/2026", "001067", 45.00)]
TOP5 = [("Seda Zomo King Size Brown", 38), ("Essência Zomo Love 66 50 g", 21), ("Carvão de coco Zomo 1 kg", 12),
        ("Papelito Marrom c/ Piteira", 9), ("Isqueiro Clipper Largo", 6)]
TOP10 = TOP5 + [("Piteira de vidro Squadafum", 5), ("OCB King Size Slim Premium", 5), ("Seda Zomo King Size Rosa", 4),
                ("Bandeja Bem Bolado média", 2), ("Dichavador metal 4 partes", 2)]
GASTO_MES = [182.0, 240.5, 210.0, 265.3, 198.0, 290.1, 305.0, 276.4, 330.2, 298.0, 386.9, 312.4]
MESES = ["D", "J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N"]
COMO_PAGA = [("Pix", 48), ("Crédito", 22), ("Dinheiro", 16), ("Débito", 10), ("Crédito do cliente", 4)]
OBS_MARIANA = "Prefere seda brown. Avisar quando chegar a Zomo Love 66"

# ======================================================================
# D13 · Identificar cliente (F1)
# ======================================================================
def _lista_cli(d, p, x, y, w, rows, sel, rh=56):
    c = d.frame(p, "Resultados", x, y, w, 8 + rh * len(rows), fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A,
                radius=R_CARD, clip=True)
    yy = 4
    for i, (nome, tel, bolo, extra) in enumerate(rows):
        if i == sel:
            d.frame(c, "Linha selecionada", 4, yy, w - 8, rh, fill=C["sel"], stroke=C["ink"], radius=6)
        T(d, c, nome, 16, yy + 9, size=14, weight=500, lh=20)
        if bolo:
            _bolo(d, c, 16 + fc.text_width(nome, 14, 500) + 8, yy + 11, 16)
        T(d, c, tel, 16, yy + 31, size=12, color=C["muted"], lh=16, mono=True)
        if extra == "confere":
            lab = "documento confere"
            tw = fc.text_width(lab, 13)
            ui.icon(d, c, "ok", w - 16 - tw - 22, yy + 20, 16, C["pos"])
            T(d, c, lab, w - 16, yy + 18, size=13, color=C["text2"], align="right", lh=20)
        yy += rh
        if i < len(rows) - 1 and i != sel and i + 1 != sel:
            hair(d, c, 16, yy, w - 32)
    return 8 + rh * len(rows)

def _busca_cli(d, p, x, y, w, value, tag, app, h=44):
    fr, _ = ui.field(d, p, x, y, w, value=value, focused=True, app=app, h=h, prefix_icon="busca", mono=True)
    tw = int(fc.text_width(tag, 12, 500) + 16 + 3) // 4 * 4
    _tag(d, fr, w - tw - 10, (h - 22) / 2, tag)
    return h

def _ficha(d, p, x, y, w, app):
    """Ficha da Mariana ao lado da lista (F1)."""
    ui.avatar(d, p, x, y, 40, "Mariana Albuquerque")
    T(d, p, "Mariana Albuquerque", x + 52, y, size=17, weight=500, lh=24)
    _bolo(d, p, x + 52 + fc.text_width("Mariana Albuquerque", 17, 500) + 8, y + 4, 16)
    T(d, p, "(87) 98841-2207", x + 52, y + 24, size=13, color=C["text2"], lh=16, mono=True)
    tx = x
    for t in ("Recorrente", "Aniversário"):
        tx += _tag(d, p, tx, y + 56, t) + 6
    yy = y + 90
    yy += _aviso_bolo(d, p, x, yy, w, "Aniversário em 3 dias", "Completa 29 anos em 27/11") + 12
    yy += _grade(d, p, x, yy, w, [("Cliente desde", "12/03/2024"), ("Compras", "46"), ("Total gasto", "R$ 3.482,40"),
                                   ("Ticket médio", "R$ 75,70")], h=56, vsize=15) + 12
    # crédito e prazo
    yy += _grade(d, p, x, yy, w, [("Saldo de crédito", "R$ 12,00"), ("A prazo: limite · disponível", "R$ 500,00 · R$ 338,00")],
                 h=56, vsize=15, name="Crédito e prazo") + 20
    # últimas 5 compras e top 5
    cw1 = int(w * 0.46); cw2 = w - cw1 - 24
    T(d, p, "Últimas 5 compras", x, yy, size=13, color=C["text2"], lh=20)
    T(d, p, "Top 5", x + cw1 + 24, yy, size=13, color=C["text2"], lh=20)
    ly = yy + 28
    for i, (dt, dav, tot) in enumerate(ULTIMAS):
        T(d, p, dt[:5], x, ly + i * 24, size=12, color=C["text2"], lh=20, mono=True)
        T(d, p, dav, x + 52, ly + i * 24, size=12, color=C["muted"], lh=20, mono=True)
        T(d, p, v(tot), x + cw1, ly + i * 24, size=12, lh=20, mono=True, align="right")
    for i, (nome, q) in enumerate(TOP5):
        T(d, p, _fit(nome, 13, cw2 - 44), x + cw1 + 24, ly + i * 24, size=13, lh=20)
        T(d, p, str(q), x + w, ly + i * 24, size=12, color=C["text2"], lh=20, mono=True, align="right")
    d.frame(p, "Divisa", x + cw1 + 12, yy, 1, 28 + 5 * 24, fill=C["line"], fill_opacity=LINE_A)
    yy = ly + 5 * 24 + 16
    T(d, p, "Observação", x, yy, size=13, color=C["text2"], lh=20)
    T(d, p, OBS_MARIANA, x, yy + 22, size=14, lh=20, w=w)
    return yy + 44 - y

def d13(d, f, dev, app):
    W, H = DEVICES[dev]
    if dev == "mobile":
        d04(d, f, dev, app)
        win, w, h, top, _ = ui.window(d, f, dev, "Identificar cliente", W, 796, app=app)
        x = 16; cw = w - 32; y = top + 16
        y += _busca_cli(d, win, x, y, cw, "87 9910", "Telefone", app) + 12
        y += _lista_cli(d, win, x, y, cw, [("Rafael Coelho Nunes", "(87) 99102-7754", False, None),
                                           ("Raquel Duarte Moura", "(87) 99104-5521", False, None)], 0) + 20
        T(d, win, "Rafael Coelho Nunes", x, y, size=17, weight=500, lh=24)
        _tag(d, win, x, y + 32, "Recorrente")
        y += 66
        y += ui.banner(d, win, x, y, cw, "Vendas bloqueadas, fale com o gerente", tone="neg") + 12
        y += _grade(d, win, x, y, cw, [("Cliente desde", "05/08/2023"), ("Compras", "23"), ("Total gasto", "R$ 1.204,60"),
                                       ("Ticket médio", "R$ 52,37")], cols=2, h=56, vsize=15) + 12
        _grade(d, win, x, y, cw, [("Saldo de crédito", "R$ 0,00"), ("A prazo: limite · disponível", "R$ 300,00 · R$ 0,00")],
               cols=1, h=56, vsize=15, name="Crédito e prazo")
        _win_foot(d, win, w, h, dev, [("Vender sem cliente", "secondary", None, False), ("Usar na venda", "primary", "Enter", True)], app)
        return
    tablet = dev == "tablet"
    if tablet:
        d02(d, f, dev, app)
    else:
        d04(d, f, dev, app)
    ww = 1040 if not tablet else 1100
    win, w, h, top, _ = ui.window(d, f, dev, "Identificar cliente", ww, 716, app=app)
    lw = 400
    x = 24; y = top + 20
    if tablet:
        _busca_cli(d, win, x, y, lw, "123.456.789-09", "CPF", app)
        _lista_cli(d, win, x, y + 56, lw, [("Mariana Albuquerque", "(87) 98841-2207", True, "confere")], 0)
    else:
        _busca_cli(d, win, x, y, lw, "mari", "Nome", app)
        _lista_cli(d, win, x, y + 56, lw, BUSCA_NOME, 0)
    d.frame(win, "Divisa", x + lw + 23, top, 1, h - 72 - top, fill=C["line"], fill_opacity=LINE_A)
    fx = x + lw + 48
    _ficha(d, win, fx, y, w - fx - 24, app)
    first = ("Vender sem cliente", "secondary", None, False) if tablet else ("Tirar cliente da venda", "secondary", None, False)
    _win_foot(d, win, w, h, dev, [first, ("Novo cadastro", "secondary", "F2", False),
                                  ("Histórico completo", "secondary", "F4", False), ("Usar na venda", "primary", "Enter", False)],
              app, keys=[("↑ ↓", "Escolher")])

# ======================================================================
# D14 · Cadastro rápido (F2)
# ======================================================================
def d14(d, f, dev, app):
    W, H = DEVICES[dev]
    d04(d, f, dev, app)
    mob = dev == "mobile"
    win, w, h, top, _ = ui.window(d, f, dev, "Novo cliente", W if mob else 640, 796 if mob else 600, app=app)
    x = 24 if not mob else 16; cw = w - 2 * x
    y = top + 20
    if mob:
        rows = [
            [dict(label="CPF ou CNPJ", value="123.456.789-00", mono=True, error="CPF com dígito errado")],
            [dict(label="Telefone/WhatsApp", value="(87) 99812-3344", mono=True)],
            [dict(label="Nome", value="", error="Informe o nome")],
            [dict(label="Data de nascimento", value="31/02/1996", mono=True, error="Data inválida")],
            [dict(label="E-mail (opcional)", value="", focused=True)],
            [dict(label="Cidade", value="Juazeiro"), dict(label="Estado", value="BA", chevron=True, w=96)],
        ]
    else:
        rows = [
            [dict(label="CPF ou CNPJ", value="123.456.789-00", mono=True, error="CPF com dígito errado"),
             dict(label="Telefone/WhatsApp", value="(87) 99812-3344", mono=True)],
            [dict(label="Nome", value="", error="Informe o nome")],
            [dict(label="Data de nascimento", value="31/02/1996", mono=True, error="Data inválida"),
             dict(label="E-mail (opcional)", value="", focused=True)],
            [dict(label="Cidade", value="Juazeiro"), dict(label="Estado", value="BA", chevron=True)],
        ]
    for row in rows:
        fixed = sum(c.get("w", 0) for c in row)
        flex = [c for c in row if "w" not in c]
        fw = (cw - fixed - 16 * (len(row) - 1)) / max(1, len(flex))
        cx = x; err = False
        for c in row:
            c = dict(c); ww = c.pop("w", fw)
            ui.field(d, win, cx, y, ww, app=app, **c)
            err = err or bool(c.get("error"))
            cx += ww + 16
        y += 60 + (36 if err else 16)
    ui.checkbox(d, win, x, y + 4, on=True, label="Aceita ofertas pelo WhatsApp", app=app)
    _win_foot(d, win, w, h, dev, [("Salvar e usar na venda", "primary", "Enter", False)], app)

# ======================================================================
# D15 · Histórico completo do cliente
# ======================================================================
NOV = [("21/11 17:12", "001431", "7 itens", "Pix + 2", 95.00), ("14/11 10:40", "001302", "3 itens", "Pix", 62.00),
       ("07/11 18:05", "001188", "4 itens", "Crédito", 118.40), ("02/11 16:22", "001095", "2 itens", "Dinheiro", 37.00)]
OUT = [("31/10 15:48", "001067", "2 itens", "Pix", 45.00), ("24/10 11:02", "000952", "3 itens", "Débito", 87.50),
       ("17/10 17:30", "000871", "4 itens", "Pix", 79.90), ("10/10 19:14", "000790", "5 itens", "Crédito", 120.00),
       ("03/10 09:55", "000702", "2 itens", "Pix", 54.50)]

def _mes(d, p, x, y, w, titulo, n, total):
    r = d.frame(p, f"Mês {titulo}", x, y, w, 40, fill=C["raised"], radius=R_CTL)
    ui.icon(d, r, "seta-baixo", 12, 12, 16, C["text2"])
    T(d, r, titulo, 36, 10, size=14, weight=500, lh=20)
    T(d, r, f"{n} compras", 36 + fc.text_width(titulo, 14, 500) + 12, 10, size=13, color=C["muted"], lh=20)
    T(d, r, v(total), w - 14, 10, size=14, weight=500, lh=20, mono=True, align="right")
    return 44

def _compra(d, p, x, y, w, c, sel=False, compact=False):
    dt, dav, it, pg, tot = c
    if sel:
        d.frame(p, "Linha selecionada", x, y, w, 40, fill=C["sel"], stroke=C["ink"], radius=6)
    T(d, p, dt if not compact else dt[:5], x + 12, y + 10, size=13, lh=20, mono=True)
    if compact:
        T(d, p, f"{dav} · {pg}", x + 64, y + 10, size=13, color=C["text2"], lh=20)
    else:
        T(d, p, dav, x + 124, y + 10, size=13, color=C["text2"], lh=20, mono=True)
        T(d, p, it, x + 196, y + 10, size=13, color=C["text2"], lh=20)
        if w > 460: T(d, p, pg, x + 268, y + 10, size=13, color=C["text2"], lh=20)
    T(d, p, v(tot), x + w - 12, y + 10, size=13, lh=20, mono=True, align="right")
    return 40

def _compra_aberta(d, p, x, y, w, compact=False):
    """Itens da compra aberta: código, quantidade, unitário, total; desconto, pagamento e operador."""
    rows = ITENS
    rh_ = 42 if compact else 24
    hh = 28 + rh_ * len(rows) + 8 + (64 if compact else 44)
    b = d.frame(p, "Itens da compra", x, y, w, hh, fill=C["paper"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CTL)
    T(d, b, "Produto" if compact else "Cód.    Produto", 12, 8, size=11, color=C["muted"], lh=16, mono=True)
    T(d, b, "Total" if compact else "Qtde × Unit.    Total", w - 12, 8, size=11, color=C["muted"], lh=16, mono=True, align="right")
    yy = 28
    for cod, nome, q, u in (rows if compact else []):
        T(d, b, _fit(nome, 13, w - 24 - 64), 12, yy, size=13, lh=18)
        T(d, b, f"{cod} · {q} × {v(u)}", 12, yy + 19, size=12, color=C["text2"], lh=16, mono=True)
        T(d, b, v(q * u), w - 12, yy + 8, size=12, lh=20, mono=True, align="right")
        yy += rh_
    for cod, nome, q, u in ([] if compact else rows):
        T(d, b, cod, 12, yy, size=12, color=C["text2"], lh=20, mono=True)
        nx = 12 + fc.text_width("000000  ", 12, 400, True)
        T(d, b, _fit(nome, 13, w - nx - 160), nx, yy, size=13, lh=20)
        T(d, b, f"{q} × {v(u)}", w - 76, yy, size=12, color=C["text2"], lh=20, mono=True, align="right")
        T(d, b, v(q * u), w - 12, yy, size=12, lh=20, mono=True, align="right")
        yy += 24
    hair(d, b, 12, yy + 4, w - 24)
    yy += 12
    pg = "Pix 43,00 · Dinheiro 40,00 · Crédito do cliente 12,00"
    if compact:
        T(d, b, "Desconto 5,00 · Operador Arthur", 12, yy, size=12, color=C["text2"], lh=20)
        T(d, b, pg, 12, yy + 22, size=12, color=C["text2"], lh=20, w=w - 24)
    else:
        T(d, b, "Desconto 5,00 · " + pg + " · Operador Arthur", 12, yy, size=12, color=C["text2"], lh=20, w=w - 24)
    return hh

def _cadastro(d, p, x, y, w):
    y0 = y
    y += _secao(d, p, x, y, "Cadastro")
    y += ui.kv(d, p, x, y, w, [("CPF", "123.456.789-09"), ("Telefone", "(87) 98841-2207"), ("E-mail", "mari.alb@gmail.com"),
                               ("Nascimento", "27/11/1997 · 28 anos"), ("Cidade/UF", "Petrolina-PE"),
                               ("Cliente desde", "12/03/2024")], gap=24)
    y += 4
    b = d.frame(p, "Crédito", x, y, w, 36, fill=C["raised"], radius=R_CTL)
    T(d, b, "Saldo de crédito", 12, 8, size=13, color=C["text2"], lh=20)
    T(d, b, "R$ 12,00", w - 12, 8, size=13, weight=500, lh=20, mono=True, align="right")
    return y + 36 - y0

def _como_paga(d, p, x, y, w):
    y0 = y
    y += _secao(d, p, x, y, "Como paga")
    lw = 128 if w > 280 else 116
    for lab, pct in COMO_PAGA:
        T(d, p, lab, x, y, size=13, color=C["text2"], lh=20)
        bw = w - lw - 44
        d.frame(p, "Trilho", x + lw, y + 7, bw, 6, fill=C["raised"], radius=3)
        d.frame(p, f"Barra {lab}", x + lw, y + 7, max(4, bw * pct / 50), 6, fill=C["text2"], radius=3)
        T(d, p, f"{pct}%", x + w, y, size=12, lh=20, mono=True, align="right")
        y += 26
    return y - y0

def _top10(d, p, x, y, w):
    y0 = y
    y += _secao(d, p, x, y, "10 mais comprados")
    for i, (nome, q) in enumerate(TOP10):
        T(d, p, f"{i + 1:>2}", x, y, size=12, color=C["muted"], lh=20, mono=True)
        T(d, p, _fit(nome, 13, w - 28 - 40), x + 24, y, size=13, lh=20)
        T(d, p, str(q), x + w, y, size=12, color=C["text2"], lh=20, mono=True, align="right")
        y += 24
    return y - y0

def _gasto(d, p, x, y, w, app):
    y0 = y
    y += _secao(d, p, x, y, "Gasto por mês")
    T(d, p, "últimos 12 meses", x + w, y - 27, size=12, color=C["muted"], lh=20, align="right")
    y += _barras(d, p, x, y, w, 132, GASTO_MES, MESES, 11, app, hi_label="312,40")
    return y - y0

def d15(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    if mob:
        HH = _alto(d, f, dev, 2480)
        d04(d, f, dev, app)
        win, w, h, top, _ = ui.window(d, f, dev, "Histórico de Mariana", W, HH - 48, app=app)
        x = 16; cw = w - 32; y = top + 16
        y += _grade(d, win, x, y, cw, [("Compras", "46"), ("Total gasto", "R$ 3.482,40"), ("Ticket médio", "R$ 75,70"),
                                       ("Itens comprados", "158"), ("Compra a cada", "13 dias"), ("Última compra", "21/11/2026")],
                    cols=2, h=56, vsize=15) + 16
        y += ui.chips(d, win, x, y, [("30 dias", None), ("90 dias", None), ("12 meses", None), ("Tudo", None)], active=2,
                      app=app, wrap_w=cw) + 12
        ui.field(d, win, x, y, cw, placeholder="Produto ou número do DAV", prefix_icon="busca", app=app); y += 56
        y += _mes(d, win, x, y, cw, "Novembro de 2026", 4, 312.40)
        y += _compra(d, win, x, y, cw, NOV[0], sel=True, compact=True) + 4
        y += _compra_aberta(d, win, x, y, cw, compact=True) + 4
        for c in NOV[1:]:
            y += _compra(d, win, x, y, cw, c, compact=True)
        y += 8
        y += _mes(d, win, x, y, cw, "Outubro de 2026", 5, 386.90)
        for c in OUT:
            y += _compra(d, win, x, y, cw, c, compact=True)
        y += 12
        for fn in (lambda yy: _cadastro(d, win, x, yy, cw), lambda yy: _gasto(d, win, x, yy, cw, app),
                   lambda yy: _top10(d, win, x, yy, cw), lambda yy: _como_paga(d, win, x, yy, cw)):
            hair(d, win, x, y, cw); y += 20
            y += fn(y) + 12
        need = 48 + y + 24
        if abs(need - HH) > 1:
            d.nodes[f]["height"] = float(need)
            d.nodes[win]["height"] = float(y + 24)
            for c in d.nodes[f]["children"]:
                if d.nodes[c]["name"] == "Fundo da janela":
                    d.nodes[c]["height"] = float(need)
            # barra do total do celular fica escondida atrás da folha
        return int(need)
    d04(d, f, dev, app)
    tablet = dev == "tablet"
    ww = W - 96 if not tablet else W - 80
    win, w, h, top, _ = ui.window(d, f, dev, "Histórico de Mariana Albuquerque", ww, 820 if not tablet else 760, app=app)
    x = 24; cw = w - 48; y = top + 20
    _grade(d, win, x, y, cw, [("Compras", "46"), ("Total gasto", "R$ 3.482,40"), ("Ticket médio", "R$ 75,70"),
                              ("Itens comprados", "158"), ("Compra a cada", "13 dias"), ("Última compra", "21/11/2026")],
           h=60, vsize=17 if not tablet else 15)
    y += 76
    lw = 640 if not tablet else 476
    ytop = y
    ui.chips(d, win, x, y + 4, [("30 dias", None), ("90 dias", None), ("12 meses", None), ("Tudo", None)], active=2, app=app)
    if tablet:
        y += 48
        ui.field(d, win, x, y, lw, placeholder="Produto ou número do DAV", prefix_icon="busca", app=app)
    else:
        ui.field(d, win, x + lw - 240, y, 240, placeholder="Produto ou número do DAV", prefix_icon="busca", app=app)
    y += 56
    # lista por mês (rola)
    lst = d.frame(win, "Compras por mês", x, y, lw, h - 24 - y, fill=None, clip=True)
    ly = 0
    ly += _mes(d, lst, 0, ly, lw, "Novembro de 2026", 4, 312.40)
    ly += _compra(d, lst, 0, ly, lw, NOV[0], sel=True) + 4
    ly += _compra_aberta(d, lst, 0, ly, lw, compact=tablet) + 4
    for c in NOV[1:]:
        ly += _compra(d, lst, 0, ly, lw, c)
    ly += 8
    ly += _mes(d, lst, 0, ly, lw, "Outubro de 2026", 5, 386.90)
    for c in OUT:
        ly += _compra(d, lst, 0, ly, lw, c)
    # lateral em duas colunas
    rx = x + lw + 32
    d.frame(win, "Divisa", rx - 16, ytop, 1, h - 24 - ytop, fill=C["line"], fill_opacity=LINE_A)
    colw = (w - 24 - rx - 24) / 2
    ya = ytop
    ya += _cadastro(d, win, rx, ya, colw) + 24
    _como_paga(d, win, rx, ya, colw)
    bx = rx + colw + 24
    yb = ytop
    yb += _gasto(d, win, bx, yb, colw, app) + 24
    _top10(d, win, bx, yb, colw)

# ======================================================================
# D16 · DAVs emitidos
# ======================================================================
NC = ("Não identificado", "muted")
DAVS = [  # número, hora, cliente, pagamento, vendedor, desconto, total, (situação, tom)
    ("001486", "17:58", NC, "Dinheiro", "Arthur", 0, 18.00, ("Finalizado", "ok")),
    ("001485", "17:41", "Pedro Brandão", "Crédito", "Ana", 0, 289.00, ("Finalizado", "ok")),
    ("001484", "17:30", NC, "Pix", "Arthur", 0, 39.90, ("Cancelado", "neg")),
    ("001483", "17:22", "Tabacaria do Porto", "Débito", "Arthur", 12.00, 228.00, ("Finalizado", "ok")),
    ("001482", "17:12", "Mariana Albuquerque", "Pix + 2", "Arthur", 5.00, 95.00, ("Finalizado", "ok")),
    ("001481", "16:55", "João Sampaio", "PRAZO", "Ana", 10.00, 324.00, ("Finalizado", "ok")),
    ("001480", "16:31", NC, "Dinheiro", "Arthur", 0, 15.00, ("Finalizado", "ok")),
    ("001479", "15:40", "Larissa Menezes", "Pix", "Arthur", 0, 66.00, ("Devolvido", "warn")),
    ("001478", "14:47", "Rafael Coelho", "Débito", "Ana", 0, 52.00, ("Importado", "info")),
    ("001477", "14:20", NC, "Pix", "Arthur", 0, 10.00, ("Finalizado", "ok")),
    ("001476", "13:58", "Mariana Albuquerque", "Crédito", "Arthur", 0, 79.90, ("Finalizado", "ok")),
    ("001475", "13:31", NC, "Dinheiro", "Ana", 0, 32.00, ("Finalizado", "ok")),
    ("001474", "12:50", "Pedro Brandão", "Pix", "Arthur", 6.00, 114.00, ("Finalizado", "ok")),
    ("001473", "12:12", NC, "Débito", "Ana", 0, 45.00, ("Cancelado", "neg")),
]
SEL_DAV = 7
DET_ITENS = [("004401", "Carvão de coco Zomo 1 kg", 1, 32.00), ("005514", "Essência Zomo Love 66 50 g", 1, 18.00),
             ("003301", "OCB King Size Slim Premium", 2, 8.00)]
MENU_ITENS = [("Reimpressão do cupom", "impressora", True, False), ("Enviar por WhatsApp", "whats", True, False),
              ("Imprimir ticket para troca", "nota", True, False), ("Importar no NFC-e", "doc", False, False),
              ("Alterar forma de pagamento", "moeda", False, False),
              ("Cancelar cupom", "fechar", False, True)]
CHIPS_DAV = [("Todos", 42), ("Finalizados", 38), ("Cancelados", 2), ("Importados", 1), ("Devolvidos", 1)]

DETALHES = {
    "001479": dict(st=("Devolvido", "warn"), sub="15:40 · Terminal 01 · Arthur", cli=("Larissa Menezes", "(87) 99643-1180"),
                   itens=DET_ITENS, kv=[("Subtotal", "66,00"), ("Desconto", "0,00"), ("Pix", "66,00"), ("Total", "66,00")],
                   pg=None, dev=True),
    "001482": dict(st=("Finalizado", "ok"), sub="17:12 · Terminal 01 · Arthur", cli=("Mariana Albuquerque", "(87) 98841-2207"),
                   itens=ITENS, kv=[("Subtotal", "100,00"), ("Desconto", "5,00"), ("Total", "95,00")],
                   pg="Pix 43,00 · Dinheiro 40,00 · Crédito do cliente 12,00", dev=False),
}

def _detalhe_dav(d, p, x, y, w, h=None, num="001479"):
    D = DETALHES[num]
    c = ui.card(d, p, x, y, w, h or 600)
    pad = 20; iw = w - 2 * pad
    T(d, c, f"DAV {num}", pad, 18, size=17, weight=500, lh=24, mono=True)
    ui.status(d, c, w - pad, 20, D["st"][0], D["st"][1], align="right")
    T(d, c, D["sub"], pad, 46, size=13, color=C["text2"], lh=20)
    hair(d, c, pad, 80, iw)
    T(d, c, "Cliente", pad, 92, size=12, color=C["muted"], lh=16)
    T(d, c, D["cli"][0], pad, 110, size=14, weight=500, lh=20)
    T(d, c, D["cli"][1], w - pad, 110, size=13, color=C["text2"], lh=20, mono=True, align="right")
    hair(d, c, pad, 144, iw)
    yy = 156
    rh = 48 if len(D["itens"]) < 4 else 42
    for cod, nome, q, u in D["itens"]:
        T(d, c, _fit(nome, 13, iw - 70), pad, yy, size=13, lh=20)
        T(d, c, f"{cod} · {q} × {v(u)}", pad, yy + 20, size=12, color=C["muted"], lh=16, mono=True)
        T(d, c, v(q * u), w - pad, yy, size=13, lh=20, mono=True, align="right")
        yy += rh
    hair(d, c, pad, yy, iw); yy += 12
    yy += ui.kv(d, c, pad, yy, iw, D["kv"], gap=26, bold_last=True) + 4
    if D["pg"]:
        T(d, c, D["pg"], pad, yy, size=12, color=C["text2"], lh=20, w=iw)
        yy += 44
    if D["dev"]:
        yy += 4
        b = d.frame(c, "Devolução", pad, yy, iw, 84, fill=C["raised"], radius=R_CTL)
        d.ellipse(b, 12, 14, 8, C["warn"], name="Situação devolução")
        T(d, b, "Devolução às 16:10", 28, 8, size=13, weight=500, lh=20)
        T(d, b, "Essência Zomo Love 66 · R$ 18,00", 28, 30, size=13, color=C["text2"], lh=20, w=iw - 40)
        T(d, b, "Em dinheiro · autorizada por Carla", 28, 52, size=12, color=C["muted"], lh=20)
        yy += 84
    yy += 20
    if h is None:
        d.nodes[c]["height"] = float(yy)
    return yy

def d16(d, f, dev, app, sel=SEL_DAV, menu=True):
    W, H = DEVICES[dev]; pad = PAD[dev]
    ui.topbar(d, f, dev, app)
    y = _abas(d, f, dev, 1) + (16 if dev != "mobile" else 12)
    if dev == "mobile":
        HH = 1640
        _alto(d, f, dev, HH)
        cw = W - 2 * pad
        y += ui.chips(d, f, pad, y, CHIPS_DAV, active=0, app=app, wrap_w=cw) + 12
        ui.field(d, f, pad, y, cw, placeholder="Número, cliente ou produto", prefix_icon="busca", app=app); y += 48
        ui.field(d, f, pad, y, cw, value="24/11/2026 a 24/11/2026", prefix_icon="calendario", app=app, mono=True); y += 56
        rows = []
        for r in DAVS[:11]:
            cli = r[2][0] if isinstance(r[2], tuple) else r[2]
            rows.append((f"{r[0]} · {cli}", f"{r[1]} · {r[3]} · {r[4]}", v(r[6]), r[7][0], r[7][1]))
        lst, lh = ui.mobile_rows(d, f, pad, y, cw, rows, selected=sel)
        ry = y + 4 + 64 * sel
        y += lh + 24
        T(d, f, "Detalhe da venda", pad, y, size=15, weight=500, lh=20); y += 32
        y += _detalhe_dav(d, f, pad, y, cw, num=DAVS[sel][0]) + 24
        if menu:  # ⋯ aberto na linha escolhida
            _menu_ctx(d, f, W - pad - 264, ry + 60, 264, MENU_ITENS)
        d.nodes[f]["height"] = float(y)
        return y
    foot = ui.footer(d, f, dev, app, keys=[("↑↓", "Escolher"), ("Enter", "Detalhe"), ("Esc", "Voltar")])
    dw = 400 if dev == "desktop" else 320
    lw = W - 2 * pad - 16 - dw
    if dev == "desktop":
        ui.chips(d, f, pad, y + 4, CHIPS_DAV, active=0, app=app)
        ui.field(d, f, W - pad - 240 - 8 - 280, y, 280, placeholder="Número, cliente ou produto", prefix_icon="busca", app=app)
        ui.field(d, f, W - pad - 240, y, 240, value="24/11/2026 a 24/11/2026", prefix_icon="calendario", app=app, mono=True)
        y += 56
        cols = [("Número", 80, "l", True), ("Hora", 60, "l", True), ("Cliente", None, "l"), ("Pagamento", 104, "l"),
                ("Vendedor", 84, "l"), ("Desconto", 84, "r", True), ("Total", 92, "r", True), ("Situação", 116, "l"), ("", 40, "c")]
    else:
        ui.chips(d, f, pad, y, CHIPS_DAV, active=0, app=app)
        y += 44
        ui.field(d, f, pad, y, lw - 248, placeholder="Número, cliente ou produto", prefix_icon="busca", app=app)
        ui.field(d, f, pad + lw - 240, y, 240, value="24/11/2026 a 24/11/2026", prefix_icon="calendario", app=app, mono=True)
        y += 52
        cols = [("Número", 72, "l", True), ("Hora", 56, "l", True), ("Cliente", None, "l"), ("Pagamento", 92, "l"),
                ("Vendedor", 72, "l"), ("Desconto", 76, "r", True), ("Total", 80, "r", True), ("Situação", 104, "l"), ("", 36, "c")]
    nrows = int((H - foot - 24 - y - 40) // 40)
    data = DAVS[:nrows]
    rows = []
    for r in data:
        rows.append([r[0], r[1], r[2], r[3], r[4], v(r[5]) if r[5] else ("0,00", "muted"), v(r[6]), r[7], ""])
    t, th = ui.table(d, f, pad, y, lw, cols, rows, selected=sel)
    for i in range(len(data)):
        ix = lw - 16 - cols[-1][1] / 2 - 8
        if i == sel and menu:
            d.frame(t, "Botão ⋯ aberto", lw - 16 - cols[-1][1] + 6, 36 + i * 40 + 8, 28, 24, fill=C["card"], stroke=C["ink"],
                    stroke_opacity=0.2, radius=6)
        ui.icon(d, t, "pontos", ix, 36 + i * 40 + 12, 16, C["text2"] if i == sel else C["muted"])
    _detalhe_dav(d, f, pad + lw + 16, y, dw, h=H - foot - 24 - y, num=DAVS[sel][0])
    if menu:
        _menu_ctx(d, f, pad + lw - 16 - 264, y + 36 + (sel + 1) * 40 + 2, 264, MENU_ITENS)

# ======================================================================
# D17 · Cancelar venda finalizada
# ======================================================================
RESUMO = [("caixa", "7 unidades voltam para a frente de loja", None),
          ("pessoa", "A compra sai do histórico da cliente", None),
          ("moeda", "Devolver em dinheiro", "R$ 40,00"),
          ("pessoa", "Crédito do cliente que volta", "R$ 12,00"),
          ("transferir", "Estornar no Pix", "R$ 43,00")]

def _passos(d, p, x, y, active):
    for i, lab in enumerate(("Motivo", "Senha do supervisor")):
        on = i == active
        c = d.frame(p, f"Passo {i + 1}", x, y, 20, 20, fill=C["ink"] if on else C["raised"], radius=10)
        T(d, c, str(i + 1), 10, 2, size=11, weight=500, color="#f4f3ef" if on else C["text2"], align="center", lh=16, mono=True)
        T(d, p, lab, x + 28, y, size=13, weight=500 if on else 400, color=C["ink"] if on else C["muted"], lh=20)
        x += 28 + fc.text_width(lab, 13, 500) + 20

def _resumo(d, p, x, y, w):
    b = d.frame(p, "O que acontece", x, y, w, 20 + 28 + 44 * len(RESUMO), fill=C["raised"], radius=R_CARD)
    T(d, b, "O que acontece", 16, 14, size=13, color=C["text2"], lh=20)
    yy = 48
    for ic, lab, val in RESUMO:
        ui.icon(d, b, ic, 16, yy + 2, 16, C["text2"])
        T(d, b, lab, 44, yy, size=14, lh=20, w=w - 44 - (96 if val else 16))
        if val:
            T(d, b, val, w - 16, yy, size=14, weight=500, lh=20, mono=True, align="right")
        yy += 44
        if yy < 20 + 28 + 44 * len(RESUMO) - 4:
            hair(d, b, 44, yy - 12, w - 60)
    return 20 + 28 + 44 * len(RESUMO)

def _motivos(d, p, x, y, w, app):
    T(d, p, "Motivo", x, y, size=13, color=C["text2"], lh=16); y += 28
    for i, m in enumerate(("Cliente desistiu", "Erro de lançamento", "Produto com defeito", "Outro")):
        ui.radio(d, p, x, y, on=i == 0, label=m, app=app); y += 34
    y += 8
    return y + _area(d, p, x, y, w, 72, "Observação", "Levou só a seda, vai voltar amanhã", app=app, focused=True)

def d17(d, f, dev, app):
    W, H = DEVICES[dev]
    d16(d, f, dev, app, sel=4, menu=False)
    if dev == "tablet":
        win, w, h, top, _ = ui.window(d, f, dev, "Senha do supervisor", 520, 420, app=app)
        x = 24; cw = w - 48; y = top + 20
        b = d.frame(win, "Pedido", x, y, cw, 64, fill=C["raised"], radius=R_CTL)
        T(d, b, "Cancelar venda DAV 001482", 14, 10, size=14, weight=500, lh=20)
        T(d, b, "Cliente desistiu · R$ 95,00", 14, 32, size=13, color=C["text2"], lh=20)
        y += 88
        ui.field(d, win, x, y, cw, label="Quem autoriza", value="Carla · Supervisora de caixa", chevron=True, app=app)
        ui.field(d, win, x, y + 72, cw, label="Senha", value="••••", focused=True, app=app, mono=True)
        _passos(d, win, 24, h - 46, 1)
        _win_foot(d, win, w, h, dev, [("Autorizar", "danger", "Enter", False)], app)
        return
    mob = dev == "mobile"
    if mob:
        HH = d.nodes[f]["height"]
        win, w, h, top, _ = ui.window(d, f, dev, "Cancelar venda", W, 796, app=app)
        # a folha fica no alto da tela (quadro alto por causa da lista)
        d.nodes[win]["transform"][5] = 48.0
        x = 16; cw = w - 32; y = top + 16
        T(d, win, "DAV 001482 · 17:12", x, y, size=13, color=C["text2"], lh=20, mono=True)
        T(d, win, "R$ 95,00", w - x, y, size=15, weight=500, lh=20, mono=True, align="right")
        T(d, win, "Mariana Albuquerque", x, y + 22, size=15, weight=500, lh=22)
        y += 60
        y = _motivos(d, win, x, y, cw, app) + 20
        _resumo(d, win, x, y, cw)
        _win_foot(d, win, w, h, dev, [("Cancelar venda", "danger", "Enter", False)], app)
        # o resto do quadro fica coberto pelo fundo escuro: corta a tela no tamanho do celular
        d.nodes[f]["height"] = float(H)
        for c in d.nodes[f]["children"]:
            if d.nodes[c]["name"] == "Fundo da janela":
                d.nodes[c]["height"] = float(H)
        d.nodes[win]["transform"][5] = float(H - h)
        return H
    win, w, h, top, _ = ui.window(d, f, dev, "Cancelar venda DAV 001482", 820, 520, app=app)
    x = 24; y = top + 20
    T(d, win, "Mariana Albuquerque · 24/11/2026 17:12 · Arthur", x, y, size=14, color=C["text2"], lh=20)
    T(d, win, "R$ 95,00", w - 24, y - 4, size=22, weight=500, lh=28, mono=True, align="right")
    y += 44
    hair(d, win, x, y - 12, w - 48)
    lw = 320
    _motivos(d, win, x, y, lw, app)
    _resumo(d, win, x + lw + 32, y, w - 48 - lw - 32)
    _passos(d, win, 24, h - 46, 0)
    _win_foot(d, win, w, h, dev, [("Cancelar venda", "danger", "Enter", False)], app)

# ======================================================================
# D18 · Troca
# ======================================================================
# venda de origem DAV 001431 (mesmos itens da venda da Mariana), desconto de 5%
TROCA_DEV = {2, 3}  # itens devolvidos (índices)
NOVOS = [("008801", "Bandeja Bem Bolado média", 1, 39.90)]

def _itens_origem(d, p, x, y, w, itens, marcados, fator, app, compact=False):
    """Itens da venda de origem com marcação, quantidade e valor pago (já com o desconto da venda)."""
    rh = 56
    c = d.frame(p, "Itens da venda", x, y, w, 8 + rh * len(itens), fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A,
                radius=R_CARD, clip=True)
    yy = 4
    for i, (cod, nome, q, u) in enumerate(itens):
        on = i in marcados
        ui.checkbox(d, c, 14, yy + 19, on=on, app=app)
        if not compact:
            T(d, c, f"{i + 1:03d}", 44, yy + 9, size=12, color=C["muted"], lh=20, mono=True)
        nx = 44 if compact else 44 + 36
        T(d, c, _fit(nome, 14, w - nx - 96, 500 if on else 400), nx, yy + 8, size=14, weight=500 if on else 400, lh=20)
        sub = f"{q} × {v(u)} · pago {v(u * fator)}"
        T(d, c, sub, nx, yy + 30, size=12, color=C["muted"], lh=16, mono=True)
        tot = q * u * fator
        T(d, c, v(tot), w - 16, yy + 18, size=13, weight=500 if on else 400, lh=20, mono=True, align="right",
          color=C["ink"] if on else C["muted"])
        yy += rh
        if i < len(itens) - 1:
            hair(d, c, 16, yy, w - 32)
    return 8 + rh * len(itens)

def d18(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    fator = 0.95
    devolvido = sum(ITENS[i][2] * ITENS[i][3] for i in TROCA_DEV) * fator
    novos = sum(q * u for _, _, q, u in NOVOS)
    sobra = devolvido - novos
    if mob:
        HH = _alto(d, f, dev, 1240)
        d02(d, f, dev, app)
        win, w, h, top, _ = ui.window(d, f, dev, "Troca", W, HH - 48, app=app)
        x = 16; cw = w - 32; y = top + 16
        ui.field(d, win, x, y, cw, label="Ticket", value="T001470", mono=True, app=app); y += 68
        T(d, win, "DAV 001470 · 19/11/2026 · Consumidor não identificado", x, y, size=13, color=C["text2"], lh=20, w=cw)
        T(d, win, "Desconto da venda 5% · troca até 19/12/2026", x, y + 22, size=13, color=C["text2"], lh=20)
        y += 56
        _secao(d, win, x, y, "Itens devolvidos"); y += 28
        y += _itens_origem(d, win, x, y, cw, ITENS, TROCA_DEV, fator, app, compact=True) + 20
        y += ui.kv(d, win, x, y, cw, [("Devolvidos (valor pago)", v(devolvido)), ("Crédito de troca", (v(devolvido), "ok")),
                                      ("Entra na", "Venda 1")], bold_last=False) + 12
        y += ui.banner(d, win, x, y, cw, "Venda sem cliente", "A sobra da troca só vira crédito com o cliente identificado", tone="warn") + 12
        ui.button(d, win, x, y, "Identificar cliente", app=app, kind="secondary", w=cw, key="F1", icon_name="pessoa")
        y += 56
        hh = y + 72
        d.nodes[win]["height"] = float(hh)
        _win_foot(d, win, w, hh, dev, [("Confirmar troca", "primary", "Enter", False)], app)
        HH = 48 + hh
        d.nodes[f]["height"] = float(HH)
        for c in d.nodes[f]["children"]:
            if d.nodes[c]["name"] == "Fundo da janela":
                d.nodes[c]["height"] = float(HH)
        return HH
    d02(d, f, dev, app)
    tablet = dev == "tablet"
    win, w, h, top, _ = ui.window(d, f, dev, "Troca", 1040 if not tablet else 1100, 600, app=app)
    x = 24; y = top + 20
    ui.field(d, win, x, y, 200, label="Ticket", value="T001431", mono=True, app=app)
    T(d, win, "DAV 001431 · 20/11/2026 · Mariana Albuquerque", x + 224, y + 20, size=14, weight=500, lh=20)
    T(d, win, "Desconto da venda 5% · troca até 20/12/2026", x + 224, y + 42, size=13, color=C["text2"], lh=20)
    y += 84
    lw = 540 if not tablet else 560
    _secao(d, win, x, y, "Itens devolvidos", "2 de 5", lw)
    _itens_origem(d, win, x, y + 28, lw, ITENS, TROCA_DEV, fator, app)
    rx = x + lw + 32; rw = w - 24 - rx
    _secao(d, win, rx, y, "Crédito de troca")
    ny = y + 28
    c = ui.card(d, win, rx, ny, rw, 112)
    T(d, c, "Entra na Venda 1 · Mariana", 20, 18, size=13, color=C["text2"], lh=20)
    T(d, c, v(devolvido), 20, 44, size=32, weight=500, lh=40, mono=True)
    ny += 112 + 16
    ny += ui.kv(d, win, rx, ny, rw, [("Devolvidos (valor pago)", v(devolvido)), ("Volta para", "Frente de loja"),
                                      ("Sobra sem produto novo", "Crédito do cliente")]) + 12
    _win_foot(d, win, w, h, dev, [("Confirmar e voltar à venda", "primary", "Enter", False)], app)

def _novos(d, p, x, y, w):
    c = d.frame(p, "Itens novos", x, y, w, 8 + 56 * len(NOVOS), fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A,
                radius=R_CARD)
    yy = 4
    for cod, nome, q, u in NOVOS:
        pr = ui.produto(cod)
        ui.product_tile(d, c, 12, yy + 8, 40, pr[7], pr[8])
        T(d, c, _fit(nome, 14, w - 64 - 80, 500), 64, yy + 8, size=14, weight=500, lh=20)
        T(d, c, f"{cod} · {q} × {v(u)}", 64, yy + 30, size=12, color=C["muted"], lh=16, mono=True)
        T(d, c, v(q * u), w - 16, yy + 18, size=13, weight=500, lh=20, mono=True, align="right")
        yy += 56
    return 8 + 56 * len(NOVOS)

# ======================================================================
# D19 · Devolução
# ======================================================================
DEV_ITENS = [("002251", "Isqueiro Zippo Classic Brushed Chrome", 1, 289.00), ("007780", "Dichavador metal 4 partes 50 mm", 1, 45.00)]
FATOR_PRAZO = 324.0 / 334.0

def d19(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    if mob:
        HH = _alto(d, f, dev, 1100)
        d02(d, f, dev, app)
        win, w, h, top, _ = ui.window(d, f, dev, "Devolução", W, HH - 48, app=app)
        x = 16; cw = w - 32; y = top + 16
        ui.field(d, win, x, y, cw, label="Venda de origem", value="001470", mono=True, app=app); y += 68
        T(d, win, "DAV 001470 · 19/11/2026 · Pix", x, y, size=13, color=C["text2"], lh=20)
        T(d, win, "Consumidor não identificado · desconto 5%", x, y + 22, size=13, color=C["text2"], lh=20)
        y += 56
        _secao(d, win, x, y, "Itens a devolver"); y += 28
        itens = [("006265", "Seda Zomo King Size Rosa", 2, 5.00), ("003301", "OCB King Size Slim Premium", 1, 8.00)]
        y += _itens_origem(d, win, x, y, cw, itens, {0}, 0.95, app, compact=True) + 20
        y += ui.kv(d, win, x, y, cw, [("Valor da devolução", "9,50")], bold_last=True) + 12
        T(d, win, "Forma de reembolso", x, y, size=13, color=C["text2"], lh=16); y += 24
        for i, m in enumerate(("Dinheiro", "Pix", "Crédito do cliente")):
            ui.radio(d, win, x, y + 2, on=i == 2, label=m, app=app); y += 34
        y += 12
        ui.field(d, win, x, y, cw, label="Cliente para o crédito", value="", placeholder="CPF, CNPJ ou telefone",
                 error="Informe um cliente cadastrado", app=app, prefix_icon="pessoa")
        y += 60 + 44
        y += _autoriza(d, win, x, y, cw, app, stacked=True, focused=False) + 16
        hh = y + 72
        d.nodes[win]["height"] = float(hh)
        _win_foot(d, win, w, hh, dev, [("Confirmar devolução", "primary", "Enter", True)], app)
        HH = 48 + hh
        d.nodes[f]["height"] = float(HH)
        for c in d.nodes[f]["children"]:
            if d.nodes[c]["name"] == "Fundo da janela":
                d.nodes[c]["height"] = float(HH)
        return HH
    d02(d, f, dev, app)
    tablet = dev == "tablet"
    win, w, h, top, _ = ui.window(d, f, dev, "Devolução", 1040 if not tablet else 1100, 660, app=app)
    x = 24; y = top + 20
    ui.field(d, win, x, y, 200, label="Venda de origem", value="001455", mono=True, app=app)
    T(d, win, "DAV 001455 · 18/11/2026 · João Victor Sampaio", x + 224, y + 20, size=14, weight=500, lh=20)
    T(d, win, "PRAZO em 2x · subtotal 334,00 · desconto 10,00 · pago 324,00", x + 224, y + 42, size=13, color=C["text2"], lh=20)
    y += 84
    lw = 500 if not tablet else 520
    _secao(d, win, x, y, "Itens a devolver", "1 de 2", lw)
    ih = _itens_origem(d, win, x, y + 28, lw, DEV_ITENS, {1}, FATOR_PRAZO, app)
    yy = y + 28 + ih + 20
    T(d, win, "Volta ao estoque", x, yy, size=13, color=C["text2"], lh=20)
    T(d, win, "Frente de loja", x + lw, yy, size=13, lh=20, align="right")
    yy += 40
    _autoriza(d, win, x, yy, lw, app)
    # reembolso
    rx = x + lw + 32; rw = w - 24 - rx
    d.frame(win, "Divisa", rx - 16, y, 1, h - 72 - 20 - y, fill=C["line"], fill_opacity=LINE_A)
    _secao(d, win, rx, y, "Reembolso")
    ry = y + 28
    b = d.frame(win, "Venda a prazo", rx, ry, rw, 44, fill=C["raised"], radius=R_CTL)
    ui.icon(d, b, "calendario", 14, 14, 16, C["text2"])
    T(d, b, "Venda a prazo: abate das parcelas em aberto", 40, 12, size=13, lh=20, w=rw - 52)
    ry += 60
    cols = [("Parcela", 64, "l", True), ("Vencimento", None, "l", True), ("Em aberto", 92, "r", True), ("Depois", 84, "r", True)]
    t, th = ui.table(d, win, rx, ry, rw, cols, [["1/2", "18/12/2026", "162,00", "162,00"],
                                               ["2/2", "18/01/2027", "162,00", ("118,35", "b")]])
    ry += th + 16
    ry += ui.kv(d, win, rx, ry, rw, [("Valor da devolução", "43,65"), ("Abatido das parcelas", "-43,65"),
                                     ("Volta ao cliente", "0,00")], bold_last=True) + 12
    T(d, win, "Forma de reembolso", rx, ry, size=13, color=C["muted"], lh=16)
    ry += 22
    for m, mw in (("Dinheiro", 120), ("Pix", 80), ("Crédito do cliente", 180)):
        g = d.frame(win, f"Forma {m}", rx, ry, mw, 24, fill=None, opacity=0.45)
        ui.radio(d, g, 0, 3, on=False, label=m, app=app)
        rx += mw
    _win_foot(d, win, w, h, dev, [("Confirmar devolução", "primary", "Enter", False)], app)

# ======================================================================
# D20 · Sangria e suprimento
# ======================================================================
def d20(d, f, dev, app):
    W, H = DEVICES[dev]
    d02(d, f, dev, app)
    mob = dev == "mobile"
    titulo = "Suprimento" if mob else "Sangria"
    win, w, h, top, _ = ui.window(d, f, dev, titulo, W if mob else 560, 520 if mob else 600, app=app)
    x = 24 if not mob else 16; cw = w - 2 * x; y = top + 20
    y += ui.kv(d, win, x, y, cw, [("Caixa", "Caixa de Arthur · Terminal 01"), ("Operador", "Arthur")], gap=28, mono_values=False)
    y += ui.kv(d, win, x, y, cw, [("Data", "24/11/2026 17:45"), ("Dinheiro na gaveta", "R$ 1.559,50")], gap=28) + 12
    hair(d, win, x, y, cw); y += 20
    fr, fh = ui.field(d, win, x, y, cw if mob else 240, label="Valor", value="100,00" if mob else "800,00", focused=True,
                      app=app, mono=True, h=48, big=True)
    y += fh + 20
    y += _area(d, win, x, y, cw, 72, "Justificativa", "Troco em moedas" if mob else "Depósito no banco") + 20
    if not mob:
        ui.field(d, win, x, y, cw, label="Destino", value="Conta do banco", readonly=True, app=app)
    _win_foot(d, win, w, h, dev, [("Confirmar", "primary", "Enter", False)], app)

# ======================================================================
# D20b · Sangria para pagar fornecedor (decisão P9)
# ======================================================================
CONTAS_PAGAR = [("Distribuidora Sertão Tabacaria", "NF-e 001.245", "26/11/2026", 380.00),
                ("Zomo Brasil Comércio", "NF-e 88.412", "02/12/2026", 1240.00),
                ("Papelito Indústria", "NF-e 5.310", "10/12/2026", 615.50)]

def d20b(d, f, dev, app):
    W, H = DEVICES[dev]
    d02(d, f, dev, app)
    mob = dev == "mobile"
    win, w, h, top, _ = ui.window(d, f, dev, "Sangria", W if mob else 640, 780 if mob else 680, app=app)
    x = 24 if not mob else 16; cw = w - 2 * x; y = top + 20
    y += ui.kv(d, win, x, y, cw, [("Caixa", "Caixa de Arthur · Terminal 01"), ("Dinheiro na gaveta", "R$ 1.559,50")],
               gap=28, mono_values=False) + 12
    hair(d, win, x, y, cw); y += 20
    T(d, win, "Destino", x, y, size=13, color=C["text2"], lh=16)
    _opcoes(d, win, x, y + 20, cw, ["Conta do banco", "Pagamento a fornecedor"], 1, app); y += 20 + 40 + 20
    T(d, win, "Conta a pagar", x, y, size=13, color=C["text2"], lh=16); y += 22
    if mob:
        _, th = ui.mobile_rows(d, win, x, y, cw, [(n, f"{doc} · vence {venc}", v(val), None, None) for n, doc, venc, val in CONTAS_PAGAR],
                               selected=0, row_h=60)
    else:
        _, th = ui.table(d, win, x, y, cw, [("Fornecedor", None, "l"), ("Documento", 120, "l", True), ("Vencimento", 104, "l", True),
                                            ("Valor", 96, "r", True)],
                         [[n, doc, venc, v(val)] for n, doc, venc, val in CONTAS_PAGAR], selected=0, app=app)
    y += th + 20
    if mob:
        ui.field(d, win, x, y, cw, label="Valor", value="380,00", focused=True, app=app, mono=True); y += 72
    else:
        ui.field(d, win, x, y, 200, label="Valor", value="380,00", focused=True, app=app, mono=True)
        ui.kv(d, win, x + 232, y + 20, cw - 232, [("Gaveta depois", "R$ 1.179,50")])
        y += 76
    y += _area(d, win, x, y, cw, 56, "Justificativa", "Entregador da Distribuidora Sertão, nota 001.245") + 12
    _win_foot(d, win, w, h, dev, [("Confirmar sangria", "primary", "Enter", False)], app)

# ======================================================================
# D21 · Crédito do cliente lançado no caixa
# ======================================================================
def d21(d, f, dev, app):
    W, H = DEVICES[dev]
    d04(d, f, dev, app)
    mob = dev == "mobile"
    win, w, h, top, _ = ui.window(d, f, dev, "Crédito do cliente", W if mob else 640, 796 if mob else 620, app=app)
    x = 24 if not mob else 16; cw = w - 2 * x; y = top + 20
    T(d, win, "Cliente", x, y, size=13, color=C["text2"], lh=16)
    fr, _ = ui.field(d, win, x, y + 20, cw, value="123.456.789-09", app=app, mono=True, prefix_icon="busca")
    _tag(d, fr, cw - 52, 9, "CPF")
    y += 68
    b = d.frame(win, "Cliente encontrado", x, y, cw, 44, fill=C["raised"], radius=R_CTL)
    ui.icon(d, b, "pessoa", 14, 14, 16, C["text2"])
    T(d, b, "Mariana Albuquerque", 40, 12, size=14, weight=500, lh=20)
    T(d, b, "saldo R$ 12,00", cw - 14, 12, size=13, color=C["text2"], lh=20, align="right", mono=True)
    y += 56 if mob else 60
    if mob:
        ui.field(d, win, x, y, cw, label="Valor", value="50,00", focused=True, app=app, mono=True); y += 72
        T(d, win, "Forma em que recebeu", x, y, size=13, color=C["text2"], lh=16); y += 22
        _opcoes(d, win, x, y, cw, ["Dinheiro", "Pix"], 0, app); y += 48
        _opcoes(d, win, x, y, cw, ["Débito", "Crédito"], -1, app); y += 56
    else:
        ui.field(d, win, x, y, 180, label="Valor", value="50,00", focused=True, app=app, mono=True)
        T(d, win, "Forma em que recebeu", x + 196, y, size=13, color=C["text2"], lh=16)
        _opcoes(d, win, x + 196, y + 20, cw - 196, ["Dinheiro", "Pix", "Débito", "Crédito"], 0, app)
        y += 76
    y += _area(d, win, x, y, cw, 44 if mob else 56, "Observação (opcional)", "Adiantamento da encomenda do Zippo") + 16
    y += ui.kv(d, win, x, y, cw, [("Saldo depois", "R$ 62,00")], bold_last=True) + 8
    hair(d, win, x, y, cw); y += 20
    _autoriza(d, win, x, y, cw, app, titulo="Senha do administrador", quem="Lucas", label="Administrador",
              stacked=mob, focused=False, chevron=False)
    _win_foot(d, win, w, h, dev, [("Lançar crédito", "primary", "Enter", False)], app)

# ======================================================================
# D22 · Fechamento de caixa
# ======================================================================
FORMAS = [("Dinheiro", 1259.50), ("Pix", 2016.00), ("Débito", 1142.80), ("Crédito", 1968.40),
          ("Crédito do cliente", 60.00), ("PRAZO (líquido)", 280.35)]
TOTAL_REC = sum(x for _, x in FORMAS)

def _comprovante(divergencia=True, w=380):
    L = [("SMOKE HOUSE TABACARIA", "cb"), ("CNPJ a informar", "c"), ("FECHAMENTO DE CAIXA", "c"), ("", "hr"),
         (("Caixa de Arthur", "Terminal 01"), "lr"), (("Abertura", "24/11/2026 07:58"), "lr"),
         (("Fechamento", "24/11/2026 18:12"), "lr"), ("", "hr"),
         "DAV", (("  Vendas 38", "4.806,70"), "lr"), (("  Canceladas 1", "45,00"), "lr"),
         "NFC-e", (("  Notas 14", "1.939,00"), "lr"), ("", "hr"),
         "TOTALIZADORES"]
    for n, x in FORMAS:
        L.append(((f"  {n if n != 'Crédito do cliente' else 'Créd. cliente'}", v(x)), "lr"))
    L += [(("  Devoluções", "-68,65"), "lr"), (("TOTAL RECEBIDO", v(TOTAL_REC)), "lrb"), ("", "hr"),
          "RECEBIDO DE CLIENTES", (("  Crédito lançado", "50,00"), "lr"),
          "SANGRIAS E SUPRIMENTOS", (("  Suprimento", "100,00"), "lr"), (("  Sangria", "-800,00"), "lr"),
          "GAVETA", (("  Fundo de troco", "200,00"), "lr"), (("  Dinheiro na gaveta", "759,50"), "lrb")]
    if divergencia:
        L += [("", "hr"), "DIVERGÊNCIA", (("  Dinheiro contado", "754,50"), "lr"), (("  Diferença", "-5,00"), "lr"),
              "  Troco dado a mais · Arthur 18:05"]
    return L

def _fech_corpo(d, f, x, y, w, dev, app, divergencia=True, mob=False):
    gap = 12
    if mob:
        y += _grade(d, f, x, y, w, [("Total recebido", v(TOTAL_REC)), ("Dinheiro na gaveta", "759,50"),
                                    ("Vendido no DAV", "4.806,70"), ("Vendido no NFC-e", "1.939,00")], cols=2, h=60, vsize=16) + 16
    else:
        sw = (w - 3 * gap) / 4
        for i, (lab, val, note) in enumerate([("Total recebido", brl(TOTAL_REC), "Já sem as devoluções"),
                                              ("Vendido no DAV", "R$ 4.806,70", "38 vendas"),
                                              ("Vendido no NFC-e", "R$ 1.939,00", "14 notas"),
                                              ("Dinheiro na gaveta", "R$ 759,50", "Com o fundo de troco")]):
            ui.stat(d, f, x + i * (sw + gap), y, sw, lab, val, note=note, h=100, big=24 if dev == "desktop" else 22)
        y += 100 + 16
    cw = w if mob else (w - 16) / 2
    rows = [(n, v(x_)) for n, x_ in FORMAS] + [("Total", v(TOTAL_REC))]
    hcard = 20 + 28 + 26 * len(rows) + 12
    c1 = ui.card(d, f, x, y, cw, hcard, title="Recebido por forma de pagamento")
    ui.kv(d, c1, 20, 52, cw - 40, rows, gap=26, bold_last=True)
    movs = [("Fundo de troco", "200,00"), ("Suprimentos", "100,00"), ("Sangrias", "-800,00"),
            ("Recebido de clientes", "50,00"), ("Devoluções em dinheiro", "-25,00"), ("Abatido no PRAZO", "-43,65"),
            ("Cancelamentos (1)", "45,00")]
    if mob:
        y += hcard + 16
        c2 = ui.card(d, f, x, y, cw, hcard, title="Movimentos do caixa")
        ui.kv(d, c2, 20, 52, cw - 40, movs, gap=26)
        y += hcard + 16
    else:
        c2 = ui.card(d, f, x + cw + 16, y, cw, hcard, title="Movimentos do caixa")
        ui.kv(d, c2, 20, 52, cw - 40, movs, gap=26)
        y += hcard + 16
    # divergência
    if divergencia:
        dh = 196 if not mob else 404
        c = ui.card(d, f, x, y, w, dh)
        ui.checkbox(d, c, 20, 20, on=True, label="Divergência", app=app)
        T(d, c, "Lançada por Arthur às 18:05", w - 20, 19, size=12, color=C["muted"], lh=20, align="right")
        cy = 56
        if mob:
            iw = w - 40
            ui.field(d, c, 20, cy, iw, label="Forma", value="Dinheiro", chevron=True, app=app); cy += 68
            ui.field(d, c, 20, cy, (iw - 12) / 2, label="Sistema", value="759,50", readonly=True, mono=True, app=app)
            ui.field(d, c, 20 + (iw + 12) / 2, cy, (iw - 12) / 2, label="Contado", value="754,50", focused=True, mono=True, app=app)
            cy += 68
            T(d, c, "Diferença", 20, cy, size=13, color=C["text2"], lh=20)
            T(d, c, "-5,00", w - 20, cy, size=14, weight=500, lh=20, mono=True, align="right", color=C["neg"])
            cy += 32
            ui.field(d, c, 20, cy, iw, label="Motivo", value="Troco dado a mais", chevron=True, app=app); cy += 68
            ui.field(d, c, 20, cy, iw, label="Observação", value="Conferido com a Carla", app=app)
        else:
            iw = w - 40
            fw = [200, 150, 150]
            cx = 20
            ui.field(d, c, cx, cy, fw[0], label="Forma", value="Dinheiro", chevron=True, app=app); cx += fw[0] + 12
            ui.field(d, c, cx, cy, fw[1], label="Sistema", value="759,50", readonly=True, mono=True, app=app); cx += fw[1] + 12
            ui.field(d, c, cx, cy, fw[2], label="Valor contado", value="754,50", focused=True, mono=True, app=app); cx += fw[2] + 12
            T(d, c, "Diferença", cx, cy, size=13, color=C["text2"], lh=16)
            T(d, c, "-5,00", cx, cy + 30, size=16, weight=500, lh=20, mono=True, color=C["neg"])
            cy += 72
            ui.field(d, c, 20, cy, 260, label="Motivo", value="Troco dado a mais", chevron=True, app=app)
            ui.field(d, c, 292, cy, iw - 272, label="Observação", value="Conferido com a Carla", app=app)
        y += dh
    else:
        c = ui.card(d, f, x, y, w, 60)
        ui.checkbox(d, c, 20, 21, on=False, label="Divergência", app=app)
        y += 60
    return y

def d22(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    ui.topbar(d, f, dev, app)
    y = _abas(d, f, dev, 2)
    if dev == "mobile":
        HH = 2480
        _alto(d, f, dev, HH)
        x = pad; cw = W - 2 * pad; y += 16
        y += ui.banner(d, f, x, y, cw, "Há venda em andamento", "Venda 2 do DAV está aberta", tone="neg") + 8
        ui.button(d, f, x, y, "Ir para a venda", app=app, kind="secondary", w=cw); y += 56
        T(d, f, "Fechamento de caixa", x, y, size=20, weight=500, lh=28)
        T(d, f, "Caixa de Arthur · aberto às 07:58 · 24/11/2026", x, y + 30, size=13, color=C["text2"], lh=20, w=cw)
        y += 68
        y = _fech_corpo(d, f, x, y, cw, dev, app, divergencia=False, mob=True) + 24
        T(d, f, "Comprovante", x, y, size=15, weight=500, lh=20); y += 32
        r, rh = ui.receipt(d, f, x, y, cw, _comprovante(False))
        y += rh + 32
        bar = d.frame(f, "Barra do fechamento", 0, y, W, 88, fill=C["card"])
        hair(d, bar, 0, 0, W)
        T(d, bar, "Total recebido", 16, 14, size=12, color=C["muted"], lh=16)
        T(d, bar, brl(TOTAL_REC), 16, 32, size=22, weight=500, lh=32, mono=True)
        ui.button(d, bar, W - 16 - 148, 22, "Fechar caixa", app=app, kind="primary", w=148, h=44, icon_name="cadeado", disabled=True)
        y += 88
        d.nodes[f]["height"] = float(y)
        return y
    foot = ui.footer(d, f, dev, app, keys=[("Esc", "Voltar")])
    y += 20 if dev == "desktop" else 16
    rw = 380 if dev == "desktop" else 328
    lw = W - 2 * pad - 24 - rw
    x = pad
    if dev == "tablet":
        ui.banner(d, f, x, y, W - 2 * pad, "Este caixa fecha sozinho à meia-noite", tone="warn")
        T(d, f, "São 23:34 · fecha com a hora 23:59 de 24/11/2026", W - pad - 16, y + 12, size=13, color=C["text2"], lh=20, align="right")
        y += 44 + 16
    ui.page_head(d, f, x, y, lw, "Fechamento de caixa", "Caixa de Arthur · aberto às 07:58 · 24/11/2026",
                 actions=[("Fechar caixa", "primary", None, "cadeado")], app=app, device=dev)
    y0 = y
    y += 76
    _fech_corpo(d, f, x, y, lw, dev, app, divergencia=dev == "desktop")
    # comprovante ao lado (rola)
    rx = x + lw + 24
    T(d, f, "Comprovante", rx, y0 + 4, size=15, weight=500, lh=20)
    ui.button(d, f, rx + rw - 104, y0, "Imprimir", app=app, kind="secondary", w=104, icon_name="impressora")
    avail = H - foot - 16 - (y0 + 52)
    ah = int((avail - 24) // 18) * 18 + 24 - 1  # corta entre duas linhas da bobina
    area = d.frame(f, "Comprovante (rola)", rx - 8, y0 + 52, rw + 16, ah, fill=None, clip=True)
    r, rh = ui.receipt(d, area, 8, 0, rw, _comprovante(dev == "desktop", rw))
    # barra de rolagem fina: o comprovante continua
    d.frame(f, "Rolagem", rx + rw + 4, y0 + 52, 4, ah, fill=C["ink"], fill_opacity=0.06, radius=2)
    d.frame(f, "Rolagem (posição)", rx + rw + 4, y0 + 52, 4, ah * ah / (rh + 6), fill=C["ink"], fill_opacity=0.25, radius=2)

# ======================================================================
# D23 · Caixa fechado
# ======================================================================
def d23(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    foot = ui.footer(d, f, dev, app, keys=[]) if dev != "mobile" else 0
    from telas.dav_a import busca
    bh = 48 if dev != "mobile" else 44
    busca(d, f, pad, top + (16 if dev != "mobile" else 12), W - 2 * pad, focused=False, h=bh)
    # busca travada: sem foco e apagada
    for c in d.nodes[f]["children"][-2:]:
        d.nodes[c]["opacity"] = 0.45
    cy = (top + H - foot) / 2 - 40
    T(d, f, "Caixa de Arthur · fechado às 18:12 · 24/11/2026", W / 2, cy - 72, size=14 if dev != "mobile" else 13,
      color=C["text2"], align="center", lh=20)
    big = 88 if dev == "desktop" else (72 if dev == "tablet" else 40)
    T(d, f, "CAIXA FECHADO", W / 2, cy - 36, size=big, weight=500, align="center",
      lh=104 if dev == "desktop" else (88 if dev == "tablet" else 52), ls=-2 if dev != "mobile" else -1, color=C["text2"])
    by = cy + (100 if dev == "desktop" else (84 if dev == "tablet" else 40))
    bw = 200 if dev != "mobile" else W - 2 * pad
    ui.button(d, f, (W - bw) / 2, by, "Abrir caixa", app=app, kind="primary", w=bw, h=48, icon_name="cadeado")
    # Dicas continua disponível
    bx = W - pad - 136 if dev != "mobile" else pad
    byy = top + 16 + 64 if dev != "mobile" else H - 64 - 16
    bww = 136 if dev != "mobile" else W - 2 * pad
    b = d.frame(f, "Botão Dicas", bx, byy, bww, 40, fill=C["card"], stroke=C["line"], stroke_opacity=LINE_A, radius=R_CTL)
    q = d.frame(b, "Quadradinho", 8, 8, 24, 24, fill=C["raised"], radius=6)
    ui.icon(d, q, "dica", 4, 4, 16, C["text2"])
    T(d, b, "Dicas", 40, 10, size=13, weight=500, lh=20)

# ======================================================================
# D24 · Dicas
# ======================================================================
DICAS_BUSCA = [("2*006264", "Lança 2 unidades. Só quantidade inteira"),
               ("-1", "Cancela o item 1 do cupom, sem senha. Os itens são renumerados"),
               ("6264", "O cadastro pode ser digitado sem os zeros"),
               ("essencia", "A busca não liga para acento"),
               ("Enter", "Lança direto quando o código de barras ou o cadastro bate"),
               ("Esc", "Depois de um aviso, volta à busca com o texto selecionado")]
DICAS_TECLAS = [("F1", "Identificar cliente"), ("F3", "Formas de pagamento"), ("F6", "Cancelar cupom"),
                ("F7", "Nova venda, guarda a atual (até 4)"), ("F8", "Trocar de venda"), ("F9", "Observação no cupom"),
                ("F10", "Alterar o valor de um item"), ("F11", "Menu principal"), ("Esc", "Volta para a tela anterior")]
DICAS_LISTAS = [("↑ ↓", "Escolhe na lista"), ("Home End", "Primeiro e último"), ("PgUp PgDn", "Pulam 10"),
                ("Enter", "Usa o que está escolhido")]
DICAS_OUTRAS = [("F2", "Novo cadastro, dentro do F1"), ("F4", "Histórico completo, dentro do F1"),
                ("F1", "Cliente, dentro do pagamento"), ("F8", "Desconto e acréscimo, dentro do pagamento")]

def _dica_cod(d, p, x, y, w, cod, txt, kw=112):
    """Exemplo digitado na busca (Menlo, em caixa) ou tecla, e a explicação ao lado."""
    if cod in ("Enter", "Esc"):
        ui.keycap(d, p, x, y + 2, cod)
    else:
        cw_ = fc.text_width(cod, 13, 400, True) + 16
        b = d.frame(p, f"Digitado {cod}", x, y, cw_, 24, fill=C["raised"], stroke=C["line"], stroke_opacity=0.12, radius=4)
        T(d, b, cod, 8, 3, size=13, lh=18, mono=True)
    T(d, p, txt, x + kw, y + 2, size=14, lh=20, w=w - kw)
    nl = max(1, -(-int(fc.text_width(txt, 14)) // int(w - kw)))
    return max(32, 20 * nl + 12)

def _dica_tecla(d, p, x, y, w, keys, txt, kw=96):
    kx = x
    for k in keys.split(" "):
        kx += ui.keycap(d, p, kx, y, k) + 4
    T(d, p, txt, x + kw, y, size=14, lh=20, w=w - kw)
    nl = max(1, -(-int(fc.text_width(txt, 14)) // int(w - kw)))
    return 20 * nl + 10

def _dicas_col1(d, p, x, y, w):
    y0 = y
    y += _secao(d, p, x, y, "Na busca") + 4
    for cod, txt in DICAS_BUSCA:
        y += _dica_cod(d, p, x, y, w, cod, txt)
    y += 16
    y += _secao(d, p, x, y, "Vendas simultâneas") + 4
    for k, txt in (("F7", "Abre outra venda sem esperar a atual terminar"), ("F8", "Troca entre as vendas abertas")):
        y += _dica_tecla(d, p, x, y, w, k, txt, kw=112)
    y += 2
    obs = "Cada venda guarda os seus itens, cliente, desconto e observação"
    T(d, p, obs, x, y, size=13, color=C["text2"], lh=20, w=w)
    y += 20 * max(1, -(-int(fc.text_width(obs, 13)) // int(w))) + 8 + 16
    y += _secao(d, p, x, y, "Cliente e pagamento") + 4
    for k, txt in DICAS_OUTRAS:
        y += _dica_tecla(d, p, x, y, w, k, txt, kw=112)
    return y - y0

def _dicas_col2(d, p, x, y, w):
    y0 = y
    y += _secao(d, p, x, y, "Teclas") + 4
    for k, txt in DICAS_TECLAS:
        y += _dica_tecla(d, p, x, y, w, k, txt)
    y += 16
    y += _secao(d, p, x, y, "Nas listas") + 4
    for k, txt in DICAS_LISTAS:
        y += _dica_tecla(d, p, x, y, w, k, txt)
    return y - y0

def d24(d, f, dev, app):
    W, H = DEVICES[dev]
    if dev == "mobile":
        HH = _alto(d, f, dev, 1500)
        d02(d, f, dev, app)
        win, w, h, top, _ = ui.window(d, f, dev, "Dicas", W, HH - 48, app=app)
        x = 16; cw = w - 32; y = top + 20
        y += _dicas_col1(d, win, x, y, cw) + 20
        hair(d, win, x, y, cw); y += 20
        y += _dicas_col2(d, win, x, y, cw) + 24
        d.nodes[win]["height"] = float(y)
        HH = 48 + y
        d.nodes[f]["height"] = float(HH)
        for c in d.nodes[f]["children"]:
            if d.nodes[c]["name"] == "Fundo da janela":
                d.nodes[c]["height"] = float(HH)
        return HH
    d02(d, f, dev, app)
    win, w, h, top, _ = ui.window(d, f, dev, "Dicas", 1000 if dev == "desktop" else 1080, 740, app=app)
    x = 32; cw = (w - 64 - 48) / 2
    _dicas_col1(d, win, x, top + 24, cw)
    d.frame(win, "Divisa", x + cw + 24, top + 24, 1, h - top - 48, fill=C["line"], fill_opacity=LINE_A)
    _dicas_col2(d, win, x + cw + 48, top + 24, cw)

SCREENS = [
    ("D13", "Identificar cliente (F1)", d13),
    ("D14", "Cadastro rápido (F2)", d14),
    ("D15", "Histórico completo do cliente", d15),
    ("D16", "DAVs emitidos", d16),
    ("D17", "Cancelar venda finalizada", d17),
    ("D18", "Troca", d18),
    ("D19", "Devolução", d19),
    ("D20", "Sangria e suprimento", d20),
    ("D20b", "Sangria para pagar fornecedor", d20b),
    ("D21", "Crédito do cliente no caixa", d21),
    ("D22", "Fechamento de caixa", d22),
    ("D23", "Caixa fechado", d23),
    ("D24", "Dicas", d24),
]
