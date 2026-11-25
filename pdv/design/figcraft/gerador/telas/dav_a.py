"""DAV (Frente de caixa), parte A: abertura, caixa livre, busca, venda, pagamento.

Telas de referência para os demais módulos: D02, D03, D04 e D07.
"""
import fc, ui
from ui import C, T, brl, PAD, DEVICES, hair

PAGE = "01 · Frente de caixa (DAV)"
APP = "dav"

ITENS = [  # (cadastro, nome, qtde, unitário)
    ("006264", "Seda Zomo King Size Brown", 2, 5.00),
    ("004120", "Papelito Marrom c/ Piteira + Bandeja", 1, 15.00),
    ("002210", "Isqueiro Clipper Largo Estampado", 1, 14.00),
    ("005514", "Essência Zomo Love 66 50 g", 2, 18.00),
    ("007702", "Piteira de vidro Squadafum 6 mm", 1, 25.00),
]
TOTAL = sum(q * u for _, _, q, u in ITENS)
NITENS = sum(q for *_, q, _ in ITENS)

def vendas_bar(d, p, x, y, w, ativa=0, app=APP, device="desktop"):
    """Barra de vendas simultâneas (F7/F8) acima do cupom: Venda n, itens, total e primeiro nome do cliente."""
    vendas = [("Venda 1", f"{NITENS} itens · {brl(TOTAL)}", "Mariana"), ("Venda 2", "2 itens · R$ 23,00", None)]
    cx = x
    for i, (nome, info, cli) in enumerate(vendas):
        on = i == ativa
        label = nome + (f" · {cli}" if cli else "")
        tw = max(fc.text_width(label, 13, 500), fc.text_width(info, 12, 400, True)) + 28
        b = d.frame(p, f"Aba {nome}", cx, y, tw, 48, fill=C["card"] if on else C["deep"], stroke=C["ink"] if on else C["line"],
                    stroke_opacity=1.0 if on else ui.LINE_A, radius=ui.R_CTL)
        T(d, b, label, 14, 6, size=13, weight=500 if on else 400, color=C["ink"] if on else C["text2"], lh=18)
        T(d, b, info, 14, 25, size=12, color=C["muted"], lh=16, mono=True)
        cx += tw + 8
    if device == "desktop":
        T(d, p, "F7 nova · F8 trocar", x + w, y + 14, size=12, color=C["muted"], align="right", lh=20, mono=True)
    return 48

def busca(d, p, x, y, w, value="", focused=True, app=APP, h=48):
    f, _ = ui.field(d, p, x, y, w - h - 8, value=value, focused=focused, app=app, h=h, prefix_icon="busca", big=True)
    m = d.frame(p, "Menu principal", x + w - h, y, h, h, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CTL)
    ui.icon(d, m, "menu", (h - 18) / 2, (h - 18) / 2, 18, C["text2"])
    return h

def ultimo_item(d, p, x, y, w, it, app=APP, compact=False, h=None):
    """Último item: foto (cadastrada no HOST), nome, quantidade × preço."""
    cod, nome, q, u = it
    pr = ui.produto(cod)
    if compact:
        h = 72
        c = ui.card(d, p, x, y, w, h)
        ui.product_tile(d, c, 12, 12, 48, pr[7], pr[8])
        tx = 72
        T(d, c, "Último item", tx, 12, size=12, color=C["muted"], lh=16)
        T(d, c, nome, tx, 30, size=14, weight=500, lh=20, w=w - tx - 16)
        T(d, c, f"{q} × {brl(u)}", tx, 50, size=12, color=C["text2"], lh=16, mono=True)
        return h
    h = h or 280
    c = ui.card(d, p, x, y, w, h)
    s = min(h - 40, 280)
    ui.product_tile(d, c, 20, 20, s, pr[7], pr[8])
    tx = 20 + s + 24
    T(d, c, "Último item", tx, 24, size=13, color=C["muted"], lh=20)
    T(d, c, nome, tx, 48, size=22, weight=500, lh=30, w=w - tx - 24)
    nl = max(1, -(-int(fc.text_width(nome, 22, 500)) // int(w - tx - 24)))
    T(d, c, f"Cadastro {cod}", tx, 48 + 30 * nl + 8, size=12, color=C["muted"], lh=16, mono=True)
    T(d, c, f"{q} × {brl(u)}", tx, h - 64, size=16, color=C["text2"], lh=24, mono=True)
    T(d, c, brl(q * u), w - 24, h - 64, size=16, weight=500, lh=24, mono=True, align="right")
    return h

# ---------- D04 · Venda em andamento ----------
ALERTA = ("Estoque baixo", "Seda Zomo King Size Rosa ficou com 2 na frente · mínimo 6")

def d04b(d, f, dev, app):
    """P14: faixa discreta de estoque baixo, some na próxima leitura e não interrompe a venda."""
    return d04(d, f, dev, app, alerta=True)

def d04(d, f, dev, app, alerta=False):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    top = ui.caixa_abas(d, f, dev, 0, app)
    if dev == "mobile":
        y = top + 12
        busca(d, f, pad, y, W - 2 * pad, h=44, app=app); y += 56
        vendas_bar(d, f, pad, y, W - 2 * pad, device=dev); y += 60
        ultimo_item(d, f, pad, y, W - 2 * pad, ITENS[-1], compact=True); y += 84
        if alerta:
            y += ui.banner(d, f, pad, y, W - 2 * pad, *ALERTA, tone="warn") + 12
        ui.cupom_tela(d, f, pad, y, W - 2 * pad, H - y - 88 - 18, ITENS, cliente="Mariana Albuquerque", doc="123.456.789-09", app=app)
        ui.mobile_bar(d, f, brl(TOTAL), NITENS)
        return
    foot = 40 if dev == "desktop" else 56
    lw = 560 if dev == "desktop" else 460
    y = top + 16
    vendas_bar(d, f, pad, y, lw, device=dev)
    ui.cupom_tela(d, f, pad, y + 60, lw, H - foot - (y + 60) - 22, ITENS, cliente="Mariana Albuquerque", doc="123.456.789-09", app=app)
    rx = pad + lw + 24; rw = W - rx - pad
    busca(d, f, rx, y, rw, app=app)
    by = H - foot - 24 - 64
    tb_h = 70 + (72 if dev == "desktop" else 52) + 8
    ty = by - 32 - tb_h
    ui_h = ty - 24 - (y + 64)
    if alerta:
        bh = ui.banner(d, f, rx, ty - 24 - 64 + 8, rw, *ALERTA, tone="warn")
        ui_h -= bh + 16
    ultimo_item(d, f, rx, y + 64, rw, ITENS[-1], h=ui_h)
    ui.total_block(d, f, rx, ty, rw, brl(TOTAL), NITENS, device=dev)
    ui.button(d, f, rx, by, "Formas de pagamento", app=app, kind="primary", w=rw - 196 - 12, h=64, key="F3", sub="Finalizar a venda")
    ui.button(d, f, rx + rw - 196, by, "Cancelar cupom", app=app, kind="secondary", w=196, h=64, key="F6")
    ui.footer(d, f, dev, app)

# ---------- D02 · Caixa livre ----------
def d02(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    top = ui.caixa_abas(d, f, dev, 0, app)
    foot = ui.footer(d, f, dev, app) if dev != "mobile" else 0
    if dev == "mobile":
        busca(d, f, pad, top + 12, W - 2 * pad, h=44)
    else:
        busca(d, f, pad, top + 16, W - 2 * pad)
    cy = (top + H - foot) / 2 - 40
    T(d, f, "Operador Arthur · segunda, 24 de novembro de 2026", W / 2, cy - 72, size=14 if dev != "mobile" else 13, color=C["text2"], align="center", lh=20)
    T(d, f, "CAIXA LIVRE", W / 2, cy - 36, size=88 if dev == "desktop" else (72 if dev == "tablet" else 44), weight=500,
      align="center", lh=104 if dev == "desktop" else (88 if dev == "tablet" else 56), ls=-2 if dev != "mobile" else -1)
    T(d, f, "17:42:08", W / 2, cy + (92 if dev == "desktop" else (76 if dev == "tablet" else 40)), size=32 if dev != "mobile" else 24,
      color=C["text2"], align="center", lh=40, mono=True)
    # dois botões pequenos à direita, com ícone em quadradinho: Dicas e Fechar caixa
    bx = W - pad - 2 * 136 - 8 if dev != "mobile" else pad
    by = top + 16 + 64 if dev != "mobile" else H - 64 - 16
    bw = 136 if dev != "mobile" else (W - 2 * pad - 8) / 2
    for i, (lab, ic) in enumerate((("Dicas", "dica"), ("Fechar caixa", "cadeado"))):
        b = d.frame(f, f"Botão {lab}", bx + i * (bw + 8), by, bw, 40, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CTL)
        q = d.frame(b, "Quadradinho", 8, 8, 24, 24, fill=C["raised"], radius=6)
        ui.icon(d, q, ic, 4, 4, 16, C["text2"])
        T(d, b, lab, 40, 10, size=13, weight=500, lh=20)

# ---------- D03 · Busca aberta ----------
import unicodedata
def _sem_acento(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
# a busca lista em ordem alfabética (spec, Barra de busca)
RESULT = sorted([p for p in ui.PRODUTOS if "Zomo" in p[2] or "Essência" in p[2]], key=lambda p: _sem_acento(p[2]))[:7]

def d03(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    top = ui.caixa_abas(d, f, dev, 0, app)
    foot = ui.footer(d, f, dev, app) if dev != "mobile" else 0
    y = top + (16 if dev != "mobile" else 12)
    bh = 48 if dev != "mobile" else 44
    busca(d, f, pad, y, W - 2 * pad, value="zomo", h=bh)
    y += bh + 8
    sel = 1
    if dev == "mobile":
        lst = d.frame(f, "Resultados", pad, y, W - 2 * pad, H - y - 16, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CARD, clip=True)
        yy = 8
        for i, p in enumerate(RESULT):
            cad, gtin, nome, preco, fr, fu, un, sig, cor = p
            nl = _nl(nome, 14, W - 2 * pad - 68 - 92, 500)  # nome longo quebra e a linha cresce
            rh = 64 + 20 * (nl - 1)
            if i == sel:
                d.frame(lst, "Linha selecionada", 4, yy, W - 2 * pad - 8, rh, fill=C["sel"], stroke=C["ink"], radius=6)
            ui.product_tile(d, lst, 12, yy + (rh - 44) / 2, 44, sig, cor)
            T(d, lst, nome, 68, yy + 10, size=14, weight=500, lh=20, w=W - 2 * pad - 68 - 92)
            T(d, lst, f"{cad} · {un} · frente {fr}", 68, yy + 12 + 20 * nl, size=12, color=C["neg"] if fr == 0 else C["muted"], lh=16, mono=True)
            T(d, lst, brl(preco), W - 2 * pad - 12, yy + 10, size=14, weight=500, lh=20, align="right", mono=True)
            yy += rh + 4
        return
    lw = int((W - 2 * pad) * 0.62)
    cols = [("", 56, "l"), ("Produto", None, "l"), ("Preço", 96, "r", True), ("Estoque", 80, "r", True), ("ID", 76, "r", True),
            ("GTIN", 132, "r", True), ("Un.", 48, "c")]
    if dev == "tablet":
        cols = [("", 56, "l"), ("Produto", None, "l"), ("Preço", 92, "r", True), ("Estoque", 76, "r", True), ("ID", 72, "r", True), ("Un.", 44, "c")]
    rows = []
    for p in RESULT:
        cad, gtin, nome, preco, fr, fu, un, sig, cor = p
        r = ["", nome, brl(preco)[3:], (str(fr), "neg") if fr == 0 else str(fr), cad]
        if dev == "desktop": r.append(gtin)
        r.append(un)
        rows.append(r)
    t, th = ui.table(d, f, pad, y, lw, cols, rows, selected=sel, row_h=56)
    th = max(th, 200 + 32 + 48 + 5 * 28 + 24)
    d.nodes[t]["height"] = float(th)
    for i, p in enumerate(RESULT):
        ui.product_tile(d, t, 16, 36 + i * 56 + 8, 40, p[7], p[8])
    # detalhes do produto escolhido
    p = RESULT[sel]
    dx = pad + lw + 16; dw = W - pad - dx
    c = ui.card(d, f, dx, y, dw, th)
    ui.product_tile(d, c, 20, 20, dw - 40, p[7], p[8], h=180)
    yy = 20 + 180 + 20
    T(d, c, p[2], 20, yy, size=17, weight=500, lh=24, w=dw - 40); yy += 32
    T(d, c, brl(p[3]), 20, yy, size=28, weight=500, lh=36); yy += 48
    ui.kv(d, c, 20, yy, dw - 40, [("Cadastro", p[0]), ("GTIN", p[1]), ("Unidade", p[6]),
                                   ("Frente de loja", str(p[4])), ("Fundo de loja", str(p[5]))])

# ---------- D07 · Formas de pagamento (F3) ----------
def d07(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    w = 760 if dev != "mobile" else W
    win, w, h, top, bot = ui.window(d, f, dev, "Formas de pagamento", w, 640 if dev != "mobile" else 760, app=app,
                                    footer_buttons=[("Finalizar", "primary", "Enter")])
    pad = 24
    # cliente (F1) e total
    T(d, win, "Cliente", pad, top + 20, size=12, color=C["muted"], lh=16)
    T(d, win, "Mariana Albuquerque", pad, top + 38, size=15, weight=500, lh=22)
    ui.keycap(d, win, pad + fc.text_width("Mariana Albuquerque", 15, 500) + 10, top + 39, "F1")
    T(d, win, "Total da venda", w - pad, top + 20, size=12, color=C["muted"], lh=16, align="right")
    T(d, win, brl(TOTAL), w - pad, top + 36, size=24, weight=500, lh=32, align="right")
    y = top + 84
    hair(d, win, pad, y, w - 2 * pad); y += 16
    if dev == "mobile":
        ui.field(d, win, pad, y, w - 2 * pad, label="Forma", value="Dinheiro", chevron=True, app=app); y += 68
        ui.field(d, win, pad, y, w - 2 * pad - 88, label="Valor", value="60,00", focused=True, app=app, mono=True)
        ui.button(d, win, w - pad - 80, y + 20, "Ok", app=app, kind="dark", w=80)
        y += 76
    else:
        ui.field(d, win, pad, y, 280, label="Forma", value="Dinheiro", chevron=True, app=app)
        ui.field(d, win, pad + 296, y, 200, label="Valor", value="60,00", focused=True, app=app, mono=True)
        ui.button(d, win, pad + 512, y + 20, "Ok", app=app, kind="dark", w=72)
        y += 80
    T(d, win, "Pagamentos lançados", pad, y, size=13, color=C["text2"], lh=20); y += 28
    pags = [("Pix", "45,00"), ("Dinheiro", "60,00")]
    for nome, v in pags:
        r = d.frame(win, f"Pagamento {nome}", pad, y, w - 2 * pad, 40, fill=C["raised"], radius=ui.R_CTL)
        T(d, r, nome, 12, 10, size=14, lh=20)
        T(d, r, v, w - 2 * pad - 44, 10, size=14, lh=20, mono=True, align="right")
        ui.icon(d, r, "fechar", w - 2 * pad - 28, 12, 16, C["muted"])
        y += 44
    y += 12
    kvw = (w - 2 * pad) if dev == "mobile" else 320
    kx = w - pad - kvw
    ui.kv(d, win, kx, y, kvw, [("Desconto  F8", "- 5,00"), ("Acréscimo", "0,00"), ("Pago", "105,00"), ("Restante", "0,00"),
                               ("Troco", ("10,00", "ok"))], bold_last=True)


# ---------- D07b · Pagamento com crédito de troca (decisão P11) ----------
def d07b(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    w = 760 if dev != "mobile" else W
    win, w, h, top, bot = ui.window(d, f, dev, "Formas de pagamento", w, 500 if dev != "mobile" else 560, app=app,
                                    footer_buttons=[("Finalizar", "primary", "Enter")])
    pad = 24 if dev != "mobile" else 16
    T(d, win, "Cliente", pad, top + 20, size=12, color=C["muted"], lh=16)
    T(d, win, "Mariana Albuquerque", pad, top + 38, size=15, weight=500, lh=22)
    ui.keycap(d, win, pad + fc.text_width("Mariana Albuquerque", 15, 500) + 10, top + 39, "F1")
    T(d, win, "Total da venda", w - pad, top + 20, size=12, color=C["muted"], lh=16, align="right")
    T(d, win, brl(TOTAL), w - pad, top + 36, size=24, weight=500, lh=32, align="right")
    y = top + 84
    hair(d, win, pad, y, w - 2 * pad); y += 16
    T(d, win, "Pagamentos lançados", pad, y, size=13, color=C["text2"], lh=20); y += 28
    r = d.frame(win, "Crédito de troca", pad, y, w - 2 * pad, 52, fill=APPS_SOFT(app), radius=ui.R_CTL)
    T(d, r, "Crédito de troca", 12, 8, size=14, weight=500, lh=20)
    T(d, r, "Ticket T001431 · 2 itens devolvidos", 12, 28, size=12, color=C["muted"], lh=16, mono=True)
    T(d, r, "47,50", w - 2 * pad - 44, 16, size=14, lh=20, mono=True, align="right")
    ui.icon(d, r, "fechar", w - 2 * pad - 28, 18, 16, C["muted"])
    y += 56
    r = d.frame(win, "Pagamento Pix", pad, y, w - 2 * pad, 40, fill=C["raised"], radius=ui.R_CTL)
    T(d, r, "Pix", 12, 10, size=14, lh=20)
    T(d, r, "52,50", w - 2 * pad - 44, 10, size=14, lh=20, mono=True, align="right")
    ui.icon(d, r, "fechar", w - 2 * pad - 28, 12, 16, C["muted"])
    y += 56
    kvw = (w - 2 * pad) if dev == "mobile" else 360
    ui.kv(d, win, w - pad - kvw, y, kvw, [("Pago", "100,00"), ("Restante", "0,00"), ("Troco", "0,00"),
                                          ("Sobra da troca → crédito", "0,00")], bold_last=False)

def APPS_SOFT(app): return ui.APPS[app]["soft"]

# =====================================================================
# Telas D01, D05, D06, D08, D09, D10, D11 e D12
# =====================================================================

# ---------- auxiliares locais (sugestões para o ui.py) ----------
TONE = {"ok": C["pos"], "neg": C["neg"], "warn": C["warn"], "info": C["info"]}

def _nl(s, size, w, weight=400, mono=False):
    """Quantas linhas o texto ocupa na largura w."""
    return max(1, -(-int(fc.text_width(s, size, weight, mono)) // int(max(1, w))))

def _aviso_h(w, title, text=None, action=None):
    tw = w - 60
    h = 12 + 20 * _nl(title, 14, tw, 500)
    if text: h += 4 + 20 * _nl(text, 13, tw)
    if action: h += 12 + 32
    return h + 12

def _aviso(d, p, x, y, w, title, text=None, tone="warn", action=None, app=APP):
    """Aviso com faixa lateral que cresce com o texto (o ui.banner tem altura fixa de uma linha)."""
    col = TONE[tone]; tw = w - 60
    h = _aviso_h(w, title, text, action)
    b = d.frame(p, f"Aviso {title}"[:40], x, y, w, h, fill=C["card"], stroke=col, stroke_opacity=0.35, radius=ui.R_CTL)
    d.frame(b, "Faixa", 0, 0, 3, h, fill=col, radius=[ui.R_CTL, 0, 0, ui.R_CTL])
    ui.icon(d, b, "aviso" if tone in ("warn", "neg") else "dica", 16, 14, 16, col)
    T(d, b, title, 44, 12, size=14, weight=500, lh=20, w=tw)
    yy = 12 + 20 * _nl(title, 14, tw, 500)
    if text:
        T(d, b, text, 44, yy + 4, size=13, color=C["text2"], lh=20, w=tw)
        yy += 4 + 20 * _nl(text, 13, tw)
    if action:
        ui.button(d, b, 44, yy + 12, action, app=app, h=32)
    return h

def _busca_pos(dev):
    """Posição da barra de busca na tela de venda (D04)."""
    W, H = DEVICES[dev]; pad = PAD[dev]
    if dev == "mobile":
        return pad, 52 + 12, W - 2 * pad, 44
    lw = 560 if dev == "desktop" else 460
    x = pad + lw + 24
    return x, 56 + 16, W - x - pad, 48

def _busca_sobre(d, f, dev, app, texto, selecionado=False):
    """Redesenha a busca da tela de venda com um texto digitado (e selecionado, depois de um aviso)."""
    x, y, w, h = _busca_pos(dev)
    busca(d, f, x, y, w, value=texto, h=h)
    if selecionado:
        tw = fc.text_width(texto, 18, 400)
        d.frame(f, "Texto selecionado", x + 34, y + (h - 24) / 2, tw + 4, 24, fill=ui.acc(app), fill_opacity=0.18, radius=2)

def _confirm(d, f, dev, question, body_h, app=APP, yes="Sim", no="Não"):
    """Janela Sim/Não com corpo livre (o ui.confirm só aceita linhas de texto). Devolve (janela, largura, y do corpo)."""
    W = DEVICES[dev][0]
    w = 440 if dev != "mobile" else W
    h = 64 + 24 + 22 + 16 + body_h + 24 + 72
    win, w, h, top, bot = ui.window(d, f, dev, "Confirmar", w, h, app=app,
                                    footer_buttons=[(no, "secondary", "N"), (yes, "dark", "S")])
    q = d.frame(win, "Interrogação", 24, top + 24, 32, 32, fill=C["info"], radius=16)
    T(d, q, "?", 16, 4, size=18, weight=500, color="#ffffff", align="center", lh=24)
    T(d, win, question, 72, top + 28, size=15, weight=500, lh=22, w=w - 96)
    return win, w, top + 24 + 22 + 16 + 4

def _key_hint(d, p, x, y, pares):
    """Linha de teclas desenhadas com o que cada uma faz (ex.: ↑ ↓ escolhe · Enter abre)."""
    cx = x
    for keys, lab in pares:
        for k in keys:
            cx += ui.keycap(d, p, cx, y, k) + 4
        T(d, p, lab, cx + 2, y + 1, size=12, color=C["text2"], lh=18)
        cx += 2 + fc.text_width(lab, 12) + 16
    return cx - x

# ---------- D01 · Abrir caixa ----------
def _caixa_fechado(d, f, dev, app):
    """Fundo do Abrir caixa: o caixa ainda fechado no Terminal 01."""
    W, H = DEVICES[dev]
    top = ui.topbar(d, f, dev, app)
    foot = ui.footer(d, f, dev, app, keys=[]) if dev != "mobile" else 0
    if dev == "mobile":
        cy = top + 96
        T(d, f, "Terminal 01 · 24/11/2026", W / 2, cy - 28, size=13, color=C["text2"], align="center", lh=20)
        T(d, f, "CAIXA FECHADO", W / 2, cy, size=36, weight=500, align="center", lh=44, ls=-1)
        return
    # o título fica acima da janela, que desce para perto do rodapé
    big = 88 if dev == "desktop" else 72
    ty = top + (48 if dev == "desktop" else 32)
    T(d, f, "Terminal 01 · segunda, 24 de novembro de 2026", W / 2, ty, size=14, color=C["text2"], align="center", lh=20)
    T(d, f, "CAIXA FECHADO", W / 2, ty + 32, size=big, weight=500, align="center", lh=big + 16, ls=-2)

def d01(d, f, dev, app):
    _caixa_fechado(d, f, dev, app)
    W, H = DEVICES[dev]
    win, w, h, top, bot = ui.window(d, f, dev, "Abrir caixa", 480 if dev != "mobile" else W, 488, app=app,
                                    footer_buttons=[("Abrir caixa", "primary", "Enter")])
    if dev != "mobile":  # abaixo do CAIXA FECHADO
        tb = 56 + (48 if dev == "desktop" else 32) + 32 + (104 if dev == "desktop" else 88)
        d.nodes[win]["transform"][5] = float(tb + (H - (40 if dev == "desktop" else 56) - tb - h) // 2)
    px = 24; fw = w - 48
    y = top + 20
    T(d, win, "Terminal 01 · 24/11/2026", px, y, size=13, color=C["text2"], lh=20)
    y += 36
    fr, _ = ui.field(d, win, px, y, fw, label="Usuário", value="Arthur", readonly=True, app=app)
    ui.icon(d, fr, "cadeado", fw - 28, 12, 16, C["muted"])
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela
    y += 96
    ui.field(d, win, px, y, fw, label="Senha", value="••••••", error="Senha incorreta", mono=True, app=app)
    y += 96
    ui.field(d, win, px, y, fw, label="Fundo de troco", value="150,00", focused=False, mono=True, app=app)
    T(d, win, "Sugestão de HOST › Configurações › Regras do caixa", px, y + 64, size=12, color=C["muted"], lh=16)

# ---------- D05 · Produto sem estoque na frente ----------
SEM_ESTOQUE = ("005522", "7898941230227", "Essência Zomo Blue Mist 50 g", 18.00, 0, 0, "UN", "ZOM", "#1b1d1a")

def d05(d, f, dev, app):
    """Computador: há no fundo de loja (peça a reposição). Tablet e celular: em falta nos dois."""
    falta = dev != "desktop"
    p = SEM_ESTOQUE if falta else ui.produto("005510")
    cad, gtin, nome, preco, fr, fu = p[:6]
    d04(d, f, dev, app)
    _busca_sobre(d, f, dev, app, str(int(cad)), selecionado=True)
    W, H = DEVICES[dev]
    w = 520 if dev != "mobile" else W
    fw = w - 48
    if falta:
        a1 = ("Em falta na frente e no fundo de loja", "Não há unidades para vender nem para repor")
    else:
        a1 = ("Sem estoque na frente de loja", f"Há {fu} no fundo de loja: peça a reposição")
    a2 = ("Estoque baixo na frente de loja", "Frente de loja zerada, mínimo 6. O produto entrou em Para repor")
    nota = "O produto não entrou na venda"
    h1, h2 = _aviso_h(fw, *a1), _aviso_h(fw, *a2)
    h = 64 + 20 + 56 + 20 + h1 + 16 + 84 + 12 + h2 + 16 + 20 * _nl(nota, 13, fw) + 24 + 72
    win, w, h, top, bot = ui.window(d, f, dev, "Produto sem estoque", w, h, app=app,
                                    footer_buttons=[("Voltar à busca", "primary", "Esc")])
    y = top + 20
    ui.product_tile(d, win, 24, y, 56, p[7], p[8])
    T(d, win, nome, 96, y + 6, size=15, weight=500, lh=22, w=fw - 72)
    T(d, win, f"Cadastro {cad} · {brl(preco)}", 96, y + 32, size=12, color=C["muted"], lh=16, mono=True)
    y += 76
    y += _aviso(d, win, 24, y, fw, *a1, tone="neg") + 16
    ui.kv(d, win, 24, y, fw, [("Frente de loja", (str(fr), "neg")), ("Fundo de loja", (str(fu), "neg") if fu == 0 else str(fu)),
                              ("Mínimo na frente", "6")])
    y += 84 + 12
    y += _aviso(d, win, 24, y, fw, *a2, tone="warn") + 16
    T(d, win, nota, 24, y, size=13, color=C["text2"], lh=20, w=fw)

# ---------- D06 · Cancelar item ----------
def d06(d, f, dev, app):
    d04(d, f, dev, app)
    _busca_sobre(d, f, dev, app, "-2")
    cod, nome, q, u = ITENS[1]
    w = 440 if dev != "mobile" else DEVICES[dev][0]
    bw = w - 96
    nl = _nl(nome, 15, bw - 32, 500)
    box_h = 16 + 16 + 6 + 22 * nl + 6 + 20 + 16
    win, w, by = _confirm(d, f, dev, "Cancelar o item?", box_h + 12 + 16, app=app)
    b = d.frame(win, "Item a cancelar", 72, by, bw, box_h, fill=C["raised"], radius=ui.R_CTL)
    T(d, b, "Item 002", 16, 16, size=12, color=C["muted"], lh=16, mono=True)
    T(d, b, nome, 16, 38, size=15, weight=500, lh=22, w=bw - 32)
    T(d, b, f"{q} × {brl(u)} = {brl(q * u)}", 16, 38 + 22 * nl + 6, size=14, lh=20, mono=True)
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela

# ---------- D08 · Venda a prazo (F3 › PRAZO) ----------
PARCELAS = [("1 de 3", "24/12/2026", "33,34"), ("2 de 3", "24/01/2027", "33,33"), ("3 de 3", "24/02/2027", "33,33")]

def d08(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    w = 800 if not mob else W
    pad = 24; fw = w - 2 * pad
    venc = ("Parcela vencida desde 10/11/2026",
            "R$ 93,33 em atraso há 14 dias. A prazo só com a senha do supervisor" if mob else
            "R$ 93,33 em atraso há 14 dias. Para vender a prazo nesta venda, peça a senha do supervisor",
            "Senha do supervisor")
    if mob:
        hv = _aviso_h(fw, *venc)
        h = 64 + 100 + 80 + 52 + hv + 16 + 24 + 12 + 60 + 16 + 148 + 16 + 72
    else:
        h = 680
    win, w, h, top, bot = ui.window(d, f, dev, "Formas de pagamento", w, h, app=app,
                                    footer_buttons=[("Lançar PRAZO", "primary", "Enter", True)])
    # cliente (F1) e total, como em D07
    T(d, win, "Cliente", pad, top + 20, size=12, color=C["muted"], lh=16)
    T(d, win, "Mariana Albuquerque", pad, top + 38, size=15, weight=500, lh=22)
    ui.keycap(d, win, pad + fc.text_width("Mariana Albuquerque", 15, 500) + 10, top + 39, "F1")
    T(d, win, "Total da venda", w - pad, top + 20, size=12, color=C["muted"], lh=16, align="right")
    T(d, win, brl(TOTAL), w - pad, top + 36, size=24, weight=500, lh=32, align="right")
    y = top + 84
    hair(d, win, pad, y, fw); y += 16
    if mob:
        ui.field(d, win, pad, y, 150, label="Forma", value="PRAZO", chevron=True, app=app)
        ui.field(d, win, pad + 158, y, fw - 158 - 72, label="Valor", value="100,00", app=app, mono=True)
        ui.button(d, win, w - pad - 64, y + 20, "Ok", app=app, kind="dark", w=64)
        y += 60 + 20
        cw = (fw - 16) / 3
        for i, (k, v, tone) in enumerate((("Limite", "800,00", None), ("Em aberto", "280,00", None), ("Disponível", "520,00", "ok"))):
            T(d, win, k, pad + i * (cw + 8), y, size=12, color=C["muted"], lh=16)
            T(d, win, v, pad + i * (cw + 8), y + 18, size=14, lh=20, mono=True, color=C["pos"] if tone else C["ink"])
        y += 40 + 12
        y += _aviso(d, win, pad, y, fw, *venc[:2], tone="neg", action=venc[2], app=app) + 16
        T(d, win, "Parcelas", pad, y + 2, size=13, color=C["text2"], lh=20)
        for i, lab in enumerate(("Único", "2x", "3x")):
            ui.radio(d, win, pad + 88 + i * 84, y + 3, on=lab == "3x", label=lab, app=app)
        y += 24 + 12
        ui.field(d, win, pad, y, 160, label="1º vencimento", value="24/12/2026", focused=True, mono=True, app=app)
        T(d, win, "Depois de hoje, até 24/03/2027 (120 dias)", pad + 176, y + 22, size=12, color=C["muted"], lh=16, w=fw - 176)
        y += 60 + 16
        ui.table(d, win, pad, y, fw, [("Parcela", 80, "l"), ("Vencimento", None, "l", True), ("Valor", 96, "r", True)],
                 [list(r) for r in PARCELAS], row_h=36)
        return
    ui.field(d, win, pad, y, 280, label="Forma", value="PRAZO", chevron=True, app=app)
    ui.field(d, win, pad + 296, y, 200, label="Valor", value="100,00", app=app, mono=True)
    ui.button(d, win, pad + 512, y + 20, "Ok", app=app, kind="dark", w=72)
    y += 84
    hair(d, win, pad, y, fw); y += 20
    lw = 320; rx = pad + lw + 40; rw = w - pad - rx
    # coluna esquerda: limite do cliente e aviso de parcela vencida
    T(d, win, "A prazo · Mariana Albuquerque", pad, y, size=13, color=C["text2"], lh=20)
    ui.kv(d, win, pad, y + 32, lw, [("Limite", "800,00"), ("Em aberto", "280,00"), ("Disponível", ("520,00", "ok")),
                                     ("Nesta venda", "100,00")])
    _aviso(d, win, pad, y + 32 + 112 + 8, lw, *venc[:2], tone="neg", action=venc[2], app=app)
    # coluna direita: vencimento único ou 2x/3x, 1º vencimento e parcelas
    T(d, win, "Parcelas", rx, y, size=13, color=C["text2"], lh=20)
    for i, lab in enumerate(("Único", "2x", "3x")):
        ui.radio(d, win, rx + i * 96, y + 33, on=lab == "3x", label=lab, app=app)
    yy = y + 32 + 20 + 20
    ui.field(d, win, rx, yy, 180, label="1º vencimento", value="24/12/2026", focused=True, mono=True, app=app)
    T(d, win, "Depois de hoje, até 24/03/2027 (120 dias)", rx + 196, yy + 30, size=12, color=C["muted"], lh=16, w=rw - 196)
    yy += 60 + 20
    ui.table(d, win, rx, yy, rw, [("Parcela", 88, "l"), ("Vencimento", None, "l", True), ("Valor", 96, "r", True)],
             [list(r) for r in PARCELAS])

# ---------- D09 · Senha do supervisor ----------
def d09(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    w = 480 if dev != "mobile" else W
    fw = w - 48
    motivo = ("Desconto de 8% acima do limite de 5%", "Venda 1 · desconto de R$ 8,00 em R$ 100,00")
    ha = _aviso_h(fw, *motivo)
    h = 64 + 20 + ha + 24 + 28 + 128 + 8 + 16 + 24 + 60 + 24 + 72
    win, w, h, top, bot = ui.window(d, f, dev, "Senha do supervisor", w, h, app=app,
                                    footer_buttons=[("Autorizar", "primary", "Enter")])
    y = top + 20
    y += _aviso(d, win, 24, y, fw, *motivo, tone="warn") + 24
    T(d, win, "Quem autoriza", 24, y, size=13, color=C["text2"], lh=16); y += 28
    _, lh_ = ui.mobile_rows(d, win, 24, y, fw, [("Carla", "Supervisor de caixa"), ("Lucas", "Administrador")], selected=0, row_h=60)
    y += lh_ + 8
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela
    y += 16 + 24
    ui.field(d, win, 24, y, fw, label="Senha de Carla", value="••••", focused=True, mono=True, app=app)

# ---------- D10 · Pré-visualização do cupom DAV ----------
CANCELADO = ("004401", "Carvão de coco Zomo 1 kg", 1, 32.00)

def _cupom_dav_linhas():
    v = lambda x: brl(x)[3:]
    L = [("SMOKE HOUSE TABACARIA", "cb"), ("Loja PNZ · Petrolina-PE", "c"), ("CNPJ a informar", "c"), ("", "hr"),
         (("DAV 000482", "24/11/2026 17:46"), "lr"), (("Caixa de Arthur", "Terminal 01"), "lr"),
         (("Cliente Mariana Albuquerque", "123.456.789-09"), "lr"), ("", "hr"),
         "ITEM DESCRIÇÃO", (("    CÓD.    QTDE × UNIT.", "TOTAL"), "lr")]
    for i, (cod, nome, q, u) in enumerate(ITENS):
        L.append(f"{i + 1:03d} {nome}")
        L.append(((f"    {cod}  {q} × {v(u)}", v(q * u)), "lr"))
    cod, nome, q, u = CANCELADO
    L += [("", "hr"), "CANCELAMENTOS", f"    {nome}", ((f"    {cod}  {q} × {v(u)}", "-" + v(q * u)), "lr"), ("", "hr"),
          (("Qtde de itens", str(NITENS)), "lr"), (("Subtotal", v(TOTAL)), "lr"), (("Desconto", "-5,00"), "lr"),
          (("TOTAL", brl(TOTAL - 5)), "lrb"), ("", "hr"),
          (("Pix", "45,00"), "lr"), (("Dinheiro", "60,00"), "lr"), (("Troco", "10,00"), "lr"), ("", "hr"),
          "Obs.: embalar para presente", ("PARABÉNS POR SUA COMPRA!", "cb")]
    return L

def d10(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    linhas = _cupom_dav_linhas()
    if dev == "mobile":
        y = top + 16
        ui.status(d, f, pad, y, "Venda finalizada", "ok")
        T(d, f, "DAV 000482 · 17:46", W - pad, y, size=12, color=C["muted"], lh=20, mono=True, align="right")
        y += 32
        T(d, f, "Troco", pad, y + 6, size=13, color=C["text2"], lh=20)
        T(d, f, brl(10), W - pad, y, size=24, weight=500, lh=32, align="right")
        y += 48
        _, rh = ui.receipt(d, f, pad, y, W - 2 * pad, linhas, title="Cupom DAV 000482")
        total_h = y + rh + 6 + 24 + 88
        d.nodes[f]["height"] = float(total_h)
        bar = d.frame(f, "Barra de ações", 0, total_h - 88, W, 88, fill=C["card"])
        hair(d, bar, 0, 0, W)
        bw = (W - 2 * pad - 8) / 2
        ui.button(d, bar, pad, 22, "Caixa livre", app=app, kind="secondary", w=bw, h=44, key="Esc")
        ui.button(d, bar, pad + bw + 8, 22, "Imprimir", app=app, kind="primary", w=bw, h=44, key="Enter")
        return total_h
    foot = ui.footer(d, f, dev, app, keys=[("Enter", "Imprimir"), ("Esc", "Caixa livre")])
    pw = 420 if dev == "desktop" else 380
    px = W - pad - pw
    rw = 360
    area_w = px - 24 - pad
    rx = pad + (area_w - rw) / 2
    ry = top + (24 if dev == "desktop" else 8)
    ui.receipt(d, f, rx, ry, rw, linhas, title="Cupom DAV 000482")
    # painel ao lado: o que o operador precisa para decidir
    ch = H - foot - 24 - (top + 24)
    c = ui.card(d, f, px, top + 24, pw, ch)
    y = 24
    ui.status(d, c, 24, y, "Venda finalizada", "ok"); y += 28
    T(d, c, "DAV 000482 · 24/11/2026 17:46", 24, y, size=12, color=C["muted"], lh=16, mono=True); y += 32
    hair(d, c, 24, y, pw - 48); y += 20
    ui.kv(d, c, 24, y, pw - 48, [("Total da venda", brl(TOTAL - 5)), ("Pix", "45,00"), ("Dinheiro", "60,00"),
                                  ("Qtde itens", str(NITENS))])
    y += 4 * 28 + 12
    hair(d, c, 24, y, pw - 48); y += 20
    T(d, c, "Troco", 24, y, size=13, color=C["text2"], lh=20)
    T(d, c, brl(10), pw - 24, y + 24, size=40, weight=500, lh=48, align="right")
    by = ch - 24 - 64 - 12 - 48 - 28
    ui.button(d, c, 24, by, "Imprimir", app=app, kind="primary", w=pw - 48, h=64, key="Enter", sub="Cupom DAV na impressora")
    ui.button(d, c, 24, by + 76, "Caixa livre sem imprimir", app=app, kind="secondary", w=pw - 48, h=48, key="Esc")
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela

# ---------- D11 · Menu principal (F11) ----------
MENU = [("Suprimento", "mais-circ", None), ("Sangria", "caixa", None), ("Troca", "transferir", None),
        ("Devolução", "voltar", None), ("Identifica cliente", "pessoa", "F1"), ("Crédito do cliente", "moeda", None),
        ("Observação no cupom", "doc", "F9"), ("Nova venda", "mais", "F7"), ("Trocar de venda", "nota", "F8"),
        ("Alterar valor do item", "lapis", "F10"), ("Cancelar cupom", "fechar", "F6"), ("Configurações", "engrenagem", None)]
GRUPOS = (1, 3, 5, 10)  # linha fina depois destes itens

def d11(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    w = 460 if not mob else W
    rh = 40 if not mob else 48
    sel = 1
    h = 64 + 12 + len(MENU) * rh + len(GRUPOS) * 9 + 12 + 56
    win, w, h, top, bot = ui.window(d, f, dev, "Menu principal", w, h, app=app)
    ui.keycap(d, win, 24 + fc.text_width("Menu principal", 17, 500) + 10, 24, "F11")
    y = top + 12
    for i, (lab, ic, key) in enumerate(MENU):
        on = i == sel
        r = d.frame(win, f"Menu {lab}", 12, y, w - 24, rh, fill=C["sel"] if on else None,
                    stroke=C["ink"] if on else None, radius=6)
        ui.icon(d, r, ic, 12, (rh - 16) / 2, 16, C["ink"] if on else C["muted"])
        T(d, r, lab, 40, (rh - 20) / 2, size=14, weight=500 if on else 400, lh=20)
        if key:
            kw = fc.text_width(key, 11, 500, True) + 10
            ui.keycap(d, r, w - 24 - 12 - max(20, kw), (rh - 20) / 2, key)
        if lab == "Configurações":
            s = "Senha do supervisor"
            T(d, r, s, w - 24 - 12, (rh - 16) / 2, size=12, color=C["muted"], lh=16, align="right")
            ui.icon(d, r, "cadeado", w - 24 - 12 - fc.text_width(s, 12) - 22, (rh - 16) / 2, 16, C["muted"])
        y += rh
        if i in GRUPOS:
            hair(d, win, 24, y + 4, w - 48); y += 9
    hair(d, win, 0, h - 56, w)
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela

# ---------- D12 · Alterar valor do item (F10) ----------
def d12(d, f, dev, app):
    d04(d, f, dev, app)
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    w = 560 if not mob else W
    fw = w - 48
    cod, nome, q, u = ITENS[3]
    novo = 16.50
    pct = (u - novo) / u * 100
    pct_s = f"{pct:.1f}".replace(".", ",")
    aviso = (f"Desconto de {pct_s}% passa do máximo sem senha (5%)",
             "Ao confirmar, o caixa pede a senha do supervisor")
    ha = _aviso_h(fw, *aviso)
    h = 64 + 20 + (60 + 16 + 44 if mob else 60) + 24 + 60 + 24 + 5 * 28 + 16 + ha + 24 + 72
    win, w, h, top, bot = ui.window(d, f, dev, "Alterar valor do item", w, h, app=app,
                                    footer_buttons=[("Confirmar", "primary", "Enter")])
    ui.keycap(d, win, 24 + fc.text_width("Alterar valor do item", 17, 500) + 10, 24, "F10")
    y = top + 20
    # 1. número do item
    ui.field(d, win, 24, y, 120, label="1. Número do item", value="4", mono=True, app=app)
    ix, iy = (24, y + 76) if mob else (160, y + 20)
    ui.product_tile(d, win, ix, iy, 40, ui.produto(cod)[7], ui.produto(cod)[8])
    T(d, win, nome, ix + 52, iy, size=14, weight=500, lh=20, w=w - 24 - ix - 52)
    T(d, win, f"Item 004 · {q} × {brl(u)}", ix + 52, iy + 22, size=12, color=C["muted"], lh=16, mono=True)
    y += (60 + 16 + 44) if mob else 60
    y += 24
    # 2. novo preço unitário
    ui.field(d, win, 24, y, 200, label="2. Novo preço unitário", value=brl(novo)[3:], focused=True, mono=True, app=app)
    y += 60 + 24
    v = lambda x: brl(x)[3:]
    ui.kv(d, win, 24, y, fw, [("Preço atual", v(u)), ("Novo preço", v(novo)),
                              ("Desconto por unidade", (f"{v(u - novo)} · {pct_s}%", "warn")),
                              (f"Desconto no item ({q} un.)", v((u - novo) * q)),
                              ("Total da venda", f"{v(TOTAL)} → {v(TOTAL - (u - novo) * q)}")])
    y += 5 * 28 + 16
    _aviso(d, win, 24, y, fw, *aviso, tone="warn")

SCREENS = [
    ("D01", "Abrir caixa", d01),
    ("D02", "Caixa livre", d02),
    ("D03", "Busca de produto", d03),
    ("D04", "Venda em andamento", d04),
    ("D04b", "Alerta de estoque baixo", d04b),
    ("D05", "Produto sem estoque na frente", d05),
    ("D06", "Cancelar item", d06),
    ("D07", "Formas de pagamento", d07),
    ("D07b", "Pagamento com crédito de troca", d07b),
    ("D08", "Venda a prazo", d08),
    ("D09", "Senha do supervisor", d09),
    ("D10", "Pré-visualização do cupom DAV", d10),
    ("D11", "Menu principal", d11),
    ("D12", "Alterar valor do item", d12),
]
