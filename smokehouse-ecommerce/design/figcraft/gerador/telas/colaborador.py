"""Responsivo · Área do colaborador (C01 a C07). Colaboradora de exemplo: Carla, loja PNZ Petrolina.
Regras e textos de src/app.js (svLogin, svShell, svHome, svOrders, svStock, svLink, svComm, svPos)."""
import os, random
import fc, ui
from ui import C, T, DEVICES, hair, brl

PAGE = "Responsivo · Área do colaborador"
APP = "colab"

ABAS = ["Início", "Pedidos", "Estoque", "Meu link", "Comissões"]
ICONES = ["grafico", "doc", "caixa", "link", "moeda"]
BADGES = {"Pedidos": 1, "Estoque": 8}
USER = ("Carla", "Loja Petrolina · PE")
AREA = "Área do colaborador · PNZ"
TAXA = 0.05
VERDE = ui.APPS[APP]["acc"]
SOFT = ui.APPS[APP]["soft"]
URL = "https://claude.ai/artifact/QdDp8sUNuQNAtzXsiPgX7c#pnz-vendedor-carla"

# selos (svOrderCard pill, estoque e extrato): fundo suave + texto escuro do mesmo tom
SELO = {"novo": ("#fff1c7", "#7a5600"), "confirmado": ("#e3ebf7", "#2f5d8a"), "separado": ("#ece6f8", "#5a3d99"),
        "pronto": ("#e2efe7", "#256d45"), "a_caminho": ("#e2efe7", "#256d45"), "concluido": ("#e2efe7", "#256d45"),
        "cancelado": ("#f8e1e1", "#c62f32"), "ok": ("#e2efe7", "#256d45"), "warn": ("#fff1c7", "#7a5600"),
        "neg": ("#f8e1e1", "#c62f32"), "info": ("#e3ebf7", "#2f5d8a")}
STL = {"novo": "Novo", "confirmado": "Confirmado", "separado": "Separado", "pronto": "Pronto p/ retirada",
       "a_caminho": "Saiu p/ entrega", "concluido": "Concluído", "cancelado": "Cancelado"}

# pedidos da Carla (os mesmos números em todas as telas)
PEDIDOS = [
    {"id": "PNZ-1048", "nome": "Mariana Alves", "quando": "hoje, 16:24", "tipo": "Retirada", "origem": "Site", "st": "novo",
     "itens": [(1, "Dichavador de metal 4 partes 55 mm", 79.0), (1, "Bandeja Raw média", 69.0),
               (4, "Seda Raw KS Slim Organic Hemp", 12.0), (2, "OCB King Size Slim Premium", 8.0)],
     "whats": "(87) 98812-4470", "slot": "O quanto antes", "pag": "Cartão de crédito em 2x sem juros"},
    {"id": "PNZ-1047", "nome": "Rafael Souza", "quando": "hoje, 09:52", "tipo": "Entrega", "origem": "Site", "st": "confirmado",
     "itens": [(5, "Seda Zomo King Size Brown", 5.0), (2, "Seda Papelito King Size Brown Large", 7.0), (1, "Isqueiro Clipper Grande", 18.0)],
     "whats": "(87) 99134-2208", "slot": "", "pag": "Pix"},
    {"id": "PNZ-1039", "nome": "Juliana Costa", "quando": "23/11, 09:56", "tipo": "Retirada", "origem": "Balcão", "st": "separado",
     "itens": [(1, "Kit presente Smoke House", 99.0), (1, "Incenso Massala sortido · 15 varetas", 12.0)],
     "whats": "", "slot": "Balcão", "pag": "Dinheiro"},
]
TOTAIS = {"PNZ-1048": 212.0, "PNZ-1047": 57.0, "PNZ-1039": 100.0}

def wrap(dev):
    W = DEVICES[dev][0]
    cw = 1200 if dev == "desktop" else (W - 64 if dev == "tablet" else W - 32)
    return (W - cw) / 2, cw

def nl(s, size, weight, w, family=None):
    tw = fc.text_width(s, size, weight) if not family else fc.text_width(s, size, weight, family=family)
    return max(1, -(-int(tw) // int(max(1, w * 0.93))))  # folga: a quebra real acontece antes da conta

def corta(s, size, w, mono=True):
    """Encurta no meio com reticências até caber em w."""
    if fc.text_width(s, size, 400, mono) <= w: return s
    a, b = s[:len(s) // 2], s[len(s) // 2:]
    while fc.text_width(a + "…" + b, size, 400, mono) > w and len(a) > 4:
        a = a[:-1]; b = b[1:] if len(b) > 12 else b
    return a + "…" + b

# ---------------------------------------------------------------- componentes do módulo
def _selo(d, p, x, y, label, tone, align="left"):
    bg, fg = SELO[tone]
    w = fc.text_width(label, 12, 600) + 30
    if align == "right": x -= w
    b = d.frame(p, f"Selo {label}", x, y, w, 24, fill=bg, radius=12)
    d.ellipse(b, 10, 9, 6, fg, name="Ponto")
    T(d, b, label, 20, 3, size=12, weight=600, color=fg, lh=18)
    return w

def _painel(d, p, x, y, w, title=None, action=None, sub=None, fill=None, name=None):
    c = d.frame(p, name or f"Painel {title or ''}".strip(), x, y, w, 10, fill=fill or C["card"],
                stroke=C["line"], stroke_opacity=0.08, radius=12)
    if title:
        T(d, c, title, 20, 18, size=15, weight=600, lh=22)
        if action: T(d, c, action, w - 20, 19, size=13, weight=600, color=VERDE, align="right", lh=20)
        elif sub: T(d, c, sub, w - 20, 20, size=12, color=C["muted"], align="right", lh=18)
    return c

def _fecha(d, c, h):
    d.nodes[c]["height"] = float(h)
    return h

def _cabeca(d, f, dev, y, parts, sub, acao=None):
    """Título pincelado + linha de apoio; ação à direita (computador/tablet) ou botão de largura total (celular)."""
    x, cw = wrap(dev); mob = dev == "mobile"
    size = {"desktop": 48, "tablet": 44, "mobile": 34}[dev]
    ui.brush(d, f, x, y, parts, size=size)
    y0 = y
    y += int(size * 1.1) + 2
    sw = cw if (mob or not acao) else cw - 260
    fs = 14 if not mob else 13
    T(d, f, sub, x, y, size=fs, color=C["text2"], lh=20, w=sw)
    y += 20 * nl(sub, fs, 400, sw)
    if acao:
        lab, ic = acao
        if mob:
            y += 16
            ui.button(d, f, x, y, lab, app=APP, kind="primary", w=cw, h=44, icon_name=ic)
            y += 44
        else:
            bw = int(fc.text_width(lab, 14, 500) + 24 + 40)
            ui.button(d, f, x + cw - bw, y0 + 18, lab, app=APP, kind="primary", w=bw, h=44, icon_name=ic)
    return y + 24

def _chips(d, p, x, y, items, active, dev, wrap_w=None):
    """Filtros arredondados: 40 de altura no toque (tablet e celular), 36 no computador."""
    h = 36 if dev == "desktop" else 40
    cx, cy = x, y
    for i, (lab, n) in enumerate(items):
        on = i == active
        tw = fc.text_width(lab, 13, 600)
        nw = fc.text_width(str(n), 12, 600) + 6
        w = int(tw + nw + 34)
        if wrap_w and cx + w > x + wrap_w:
            cx, cy = x, cy + h + 8
        c = d.frame(p, f"Filtro {lab}", cx, cy, w, h, fill=C["black"] if on else C["card"],
                    stroke=None if on else C["line"], stroke_opacity=0.14, radius=h / 2)
        T(d, c, lab, 14, (h - 20) / 2, size=13, weight=600, color="#ffffff" if on else C["ink"], lh=20)
        T(d, c, str(n), 14 + tw + 6, (h - 20) / 2 + 1, size=12, weight=600, color="#b9bbb4" if on else C["muted"], lh=18)
        cx += w + 8
    return cy - y + h

def _kpis(d, f, dev, y, items):
    x, cw = wrap(dev); mob = dev == "mobile"
    cols = 2 if mob else 4; gap = 12 if mob else 16
    w = (cw - gap * (cols - 1)) / cols
    pad = 14 if mob else 18
    iw = w - 2 * pad
    def alt(lab, note): return 16 + 18 * nl(lab, 12, 500, iw) + 6 + 32 + 6 + 16 * nl(note, 12, 400, iw) + 16
    h = max(alt(l, n) for l, v, n, dk in items)
    for i, (lab, val, note, dark) in enumerate(items):
        cx = x + (i % cols) * (w + gap); cy = y + (i // cols) * (h + gap)
        c = d.frame(f, f"Indicador {lab}", cx, cy, w, h, fill=C["black"] if dark else C["card"],
                    stroke=None if dark else C["line"], stroke_opacity=0.08, radius=12)
        T(d, c, lab, pad, 16, size=12, weight=500, color="#c9cac4" if dark else C["text2"], lh=18, w=iw)
        vy = 16 + 18 * nl(lab, 12, 500, iw) + 6
        vs = 28
        while fc.text_width(val, vs, 700) > iw and vs > 18: vs -= 2
        T(d, c, val, pad, vy + (32 - vs * 1.15) / 2, size=vs, weight=700, color=C["yellow"] if dark else C["ink"], lh=int(vs * 1.15))
        T(d, c, note, pad, vy + 38, size=12, color="#b9bbb4" if dark else C["muted"], lh=16, w=iw)
    rows = -(-len(items) // cols)
    return y + rows * h + (rows - 1) * gap

def _linha_mini(d, p, x, y, w, title, sub=None, selo=None):
    """Linha clara dentro de painel (Precisam de você, Estoque baixo). Devolve a altura."""
    sw = (fc.text_width(selo[0], 12, 600) + 30 + 12) if selo else 0
    tw = w - 24 - sw
    n = nl(title, 13, 600, tw)
    h = 10 + 18 * n + (18 if sub else 0) + 10
    r = d.frame(p, f"Linha {title}"[:40], x, y, w, h, fill=C["page"], radius=8)
    T(d, r, title, 12, 10, size=13, weight=600, lh=18, w=tw)
    if sub: T(d, r, sub, 12, 12 + 18 * n, size=11, color=C["muted"], lh=16, w=tw)
    if selo: _selo(d, r, w - 12, (h - 24) / 2, selo[0], selo[1], align="right")
    return h

def _foto(d, p, x, y, s, marca):
    """Miniatura de produto (40 a 44): bloco na cor da marca com a sigla em pincel, sem cortar o nome."""
    c1, c2 = ui.marca_cor(marca)
    t = d.frame(p, f"Foto {marca}", x, y, s, s, fill=c2, radius=8, clip=True)
    d.frame(t, "Sombra da marca", 0, s * 0.55, s, s * 0.45, fill=c1, fill_opacity=0.55)
    nome = ui.DADOS.NOME_MARCA.get(marca, marca).upper().split()[0]
    fs = 16
    while fc.text_width(nome, fs, family=ui.DISPLAY) > s - 8 and fs > 12: fs -= 1
    if fc.text_width(nome, fs, family=ui.DISPLAY) > s - 8: nome = nome[:3]
    d.text(t, nome, s / 2, (s - fs * 1.1) / 2, size=fs, family=ui.DISPLAY, color="#ffffff", align="center", lh=int(fs * 1.1))

def _stepper(d, p, x, y, v, h=36, w=116, mudou=False):
    s = d.frame(p, "Quantidade", x, y, w, h, fill=C["card"], stroke=C["ink"] if mudou else C["line"],
                stroke_opacity=0.5 if mudou else 0.16, radius=h / 2)
    ui.icon(d, s, "menos", 12, (h - 16) / 2, 16, C["ink"])
    T(d, s, str(v), w / 2, (h - 20) / 2, size=14, weight=600, align="center", lh=20)
    ui.icon(d, s, "mais", w - 28, (h - 16) / 2, 16, C["ink"])
    return w

def _avatar(d, p, x, y, s, nome, cor, ink=False):
    a = d.frame(p, f"Inicial {nome}", x, y, s, s, fill=cor, radius=s / 2)
    fs = 13 if s < 40 else 17
    T(d, a, nome[0], s / 2, (s - fs * 1.4) / 2, size=fs, weight=700, color=C["ink"] if ink else "#ffffff", align="center", lh=int(fs * 1.4))

def _qr(d, p, x, y, s):
    """QR code desenhado (módulos em faixas horizontais, padrões de posição nos cantos)."""
    q = d.frame(p, "QR code", x, y, s, s, fill="#ffffff", radius=10)
    n = 25; m = (s - 24) / n; o = 12
    rnd = random.Random(42)
    def finder(gx, gy):
        for cx, cy in ((0, 0), (n - 7, 0), (0, n - 7)):
            if cx <= gx < cx + 7 and cy <= gy < cy + 7:
                a, b = gx - cx, gy - cy
                return a in (0, 6) or b in (0, 6) or (2 <= a <= 4 and 2 <= b <= 4)
            if cx - 1 <= gx <= cx + 7 and cy - 1 <= gy <= cy + 7:
                return False
        return None
    for gy in range(n):
        run = None
        for gx in range(n + 1):
            on = False
            if gx < n:
                fz = finder(gx, gy)
                on = fz if fz is not None else rnd.random() < 0.5
            if on and run is None: run = gx
            if not on and run is not None:
                d.frame(q, "m", o + run * m, o + gy * m, (gx - run) * m + 0.3, m + 0.3, fill=C["black"])
                run = None
    return q

def _moldura(d, f, dev, ativa):
    return ui.painel_header(d, f, dev, AREA, USER, ABAS, ativa, badges=BADGES, app=APP)

def _fim(d, f, dev, ativa, y, nav=True):
    if dev == "mobile":
        total = max(DEVICES[dev][1], y + (64 + 24 if nav else 24))
        ui.altura(d, f, total)
        if nav: ui.painel_nav(d, f, ABAS, ativa, ICONES, badges=BADGES)
    else:
        total = max(DEVICES[dev][1], y + 48)
        ui.altura(d, f, total)
    return total

# ---------------------------------------------------------------- C01 entrar
def c01(d, f, dev, app):
    W, H = DEVICES[dev]; mob = dev == "mobile"
    d.nodes[f]["fills"] = [fc.paint(C["black"])]
    cw = 420 if not mob else W - 32
    x0 = (W - cw) / 2
    lw = 150 if not mob else 120; lh = lw * 286 / 325
    content_h = lh + 24 + 56 + 32 + 128 + 32 + 20 + 12 + 64 + 36 + 20
    y = max(48, (H - content_h) / 2 - (0 if not mob else 10))
    d.image(f, os.path.join(ui.HERE, "marca", "logo-branco.png"), W / 2 - lw / 2, y, lw, lh, name="Logo")
    y += lh + 24
    size = 52 if not mob else 36
    ui.brush(d, f, W / 2, y, [("ÁREA DO", "white"), ("COLABORADOR", "green")], size=size, align="center")
    y += int(size * 1.1) + 6
    T(d, f, "Escolha seu nome e digite o PIN de 4 dígitos", W / 2, y, size=14 if not mob else 13, color="#c9cac4", align="center", lh=20)
    y += 20 + 28
    team = [("Carla", "Loja PNZ", C["green"], False), ("João", "Loja PNZ", C["yellow"], True), ("Bia", "Loja LEM", "#c62f32", False)]
    gap = 12; bw = (cw - 2 * gap) / 3 if mob else 124
    bx = W / 2 - (3 * bw + 2 * gap) / 2
    for i, (nm, loja, cor, ink) in enumerate(team):
        on = i == 0
        b = d.frame(f, f"Colaborador {nm}", bx + i * (bw + gap), y, bw, 128, fill="#16261c" if on else "#1b1d1a",
                    stroke=C["green"] if on else "#ffffff", stroke_opacity=1.0 if on else 0.12, stroke_w=2 if on else 1, radius=14)
        _avatar(d, b, bw / 2 - 22, 18, 44, nm, cor, ink)
        T(d, b, nm, bw / 2, 72, size=15, weight=700, color="#ffffff", align="center", lh=22)
        T(d, b, loja, bw / 2, 96, size=12, color="#b9bbb4", align="center", lh=16)
        if on:
            ok = d.frame(b, "Escolhido", bw - 26, 8, 18, 18, fill=C["green"], radius=9)
            ui.icon(d, ok, "ok", 3, 3, 12, "#ffffff")
    y += 128 + 32
    T(d, f, "PIN da Carla", W / 2, y, size=12, weight=600, color="#b9bbb4", align="center", lh=18)
    y += 20 + 12
    pw, ph, pg = (56, 64, 12)
    px = W / 2 - (4 * pw + 3 * pg) / 2
    for i in range(4):
        foco = i == 2
        c = d.frame(f, f"Dígito {i + 1}", px + i * (pw + pg), y, pw, ph, fill="#1b1d1a",
                    stroke=C["green"] if foco else "#ffffff", stroke_opacity=1.0 if foco else 0.16, stroke_w=2 if foco else 1, radius=12)
        if i < 2: d.ellipse(c, pw / 2 - 6, ph / 2 - 6, 12, "#ffffff", name="Dígito digitado")
        if foco: d.frame(c, "Cursor", pw / 2 - 1, 20, 2, 24, fill=C["green"])
    y += ph + 36
    lab = "Voltar para a loja"
    T(d, f, lab, W / 2, y, size=13, weight=500, color="#d6d7d2", align="center", lh=20)
    tw = fc.text_width(lab, 13, 500)
    d.frame(f, "Sublinhado", W / 2 - tw / 2, y + 21, tw, 1, fill="#d6d7d2", fill_opacity=0.6)
    return H

# ---------------------------------------------------------------- C02 início
VALS14 = [0, 58, 172, 0, 133, 0, 0, 0, 208, 100, 94, 0, 0, 269]
DIAS14 = [f"{12 + i}/11" for i in range(14)]

def _p_meta(d, f, x, y, w):
    c = _painel(d, f, x, y, w, "Meta do mês")
    T(d, c, "73%", w - 20, 20, size=13, weight=600, color=C["muted"], align="right", lh=20)
    d.frame(c, "Trilho", 20, 56, w - 40, 10, fill=C["deep"], radius=5)
    d.frame(c, "Progresso", 20, 56, (w - 40) * 0.73, 10, fill=C["green"], radius=5)
    T(d, c, "R$ 1.836,75", 20, 78, size=13, weight=700, lh=20)
    T(d, c, "de R$ 2.500,00", 20 + fc.text_width("R$ 1.836,75", 13, 700) + 6, 78, size=13, color=C["text2"], lh=20)
    T(d, c, "Faltam R$ 663,25", w - 20, 78, size=13, color=C["text2"], align="right", lh=20)
    return _fecha(d, c, 116)

def _p_grafico(d, f, x, y, w, dev):
    c = _painel(d, f, x, y, w, "Vendas dos últimos 14 dias")
    gx, gy, gw, gh = 20, 56, w - 40, 176 if dev != "mobile" else 150
    pl, pb, top = 34, 24, 300
    for v in (0, 150, 300):
        yy = gy + gh - pb - (v / top) * (gh - pb - 10)
        hair(d, c, gx + pl, yy, gw - pl)
        T(d, c, str(v), gx + pl - 8, yy - 9, size=11, color=C["muted"], align="right", lh=16)
    bw = (gw - pl) / 14
    step = 2 if dev != "mobile" else 3
    for i, v in enumerate(VALS14):
        bx = gx + pl + i * bw
        if v:
            bh = (v / top) * (gh - pb - 10)
            d.frame(c, f"Barra {DIAS14[i]}", bx + bw * 0.16, gy + gh - pb - bh, bw * 0.68, bh, fill=C["green"], radius=[3, 3, 0, 0])
        if (13 - i) % step == 0:
            T(d, c, DIAS14[i], bx + bw / 2, gy + gh - 18, size=11, color=C["muted"], align="center", lh=16)
    return _fecha(d, c, gy + gh + 16)

def _p_precisam(d, f, x, y, w):
    c = _painel(d, f, x, y, w, "Precisam de você", action="Ver pedidos")
    yy = 56
    for o in PEDIDOS:
        yy += _linha_mini(d, c, 20, yy, w - 40, f"{o['id']} · {o['nome']}", f"{o['quando']} · {o['tipo']} · {brl(TOTAIS[o['id']])}",
                          (STL[o['st']], o['st'])) + 8
    return _fecha(d, c, yy + 12)

def _p_tarefas(d, f, x, y, w):
    c = _painel(d, f, x, y, w, "Suas tarefas", sub="enviadas pelos donos")
    yy = 56
    for txt, done in (("Conferir validade das pomadas Tattoo Supply", False), ("Repor vitrine de isqueiros", True)):
        tw = w - 40 - 52
        n = nl(txt, 13, 400, tw)
        h = 20 * n + 22
        r = d.frame(c, f"Tarefa {txt}"[:40], 20, yy, w - 40, h, fill=C["page"], radius=8)
        ui.checkbox(d, r, 14, (h - 18) / 2, on=done, app=APP)
        T(d, r, txt, 44, 11, size=13, color=C["muted"] if done else C["ink"], lh=20, w=tw)
        if done: d.frame(r, "Riscado", 44, 21, fc.text_width(txt, 13), 1, fill=C["muted"])
        yy += h + 8
    return _fecha(d, c, yy + 12)

def _p_ranking(d, f, x, y, w):
    c = _painel(d, f, x, y, w, "Ranking da loja PNZ")
    yy = 56
    for i, (nm, v, cor, ink, me) in enumerate((("João", "R$ 2.547,40", C["yellow"], True, False), ("Carla (você)", "R$ 1.836,75", C["green"], False, True))):
        r = d.frame(c, f"Posição {i + 1}", 20, yy, w - 40, 48, fill="#eef5f0" if me else None, radius=8)
        d.text(r, f"{i + 1}º", 12, 12, size=22, family=ui.DISPLAY, color=C["green"], lh=24)
        _avatar(d, r, 44, 8, 32, nm, cor, ink)
        T(d, r, nm, 86, 14, size=13, weight=600 if me else 400, lh=20)
        T(d, r, v, w - 52, 14, size=13, weight=700, align="right", lh=20)
        yy += 52
    return _fecha(d, c, yy + 12)

def _p_estoque(d, f, x, y, w):
    c = _painel(d, f, x, y, w, "Estoque baixo", action="Ver estoque")
    yy = 56
    for nm, cat, sel in (("Isqueiro Zippo Clássico", "Isqueiros", ("Esgotado", "neg")), ("Vinho tinto seco 750 ml", "Vinhos", ("Esgotado", "neg")),
                         ("Vinho branco suave 750 ml", "Vinhos", ("Esgotado", "neg")), ("Bandeja Raw média", "Acessórios", ("2 un.", "warn")),
                         ("Papelito Marrom c/ Piteira + Bandeja", "Sedas", ("3 un.", "warn"))):
        yy += _linha_mini(d, c, 20, yy, w - 40, nm, cat, sel) + 8
    return _fecha(d, c, yy + 12)

def _p_link(d, f, x, y, w):
    c = d.frame(f, "Painel Seu link de venda", x, y, w, 10, fill=C["green"], radius=12)
    T(d, c, "Seu link de venda", 20, 18, size=15, weight=600, color="#ffffff", lh=22)
    txt = "Cada pedido feito pelo seu link conta para a sua meta e gera comissão"
    n = nl(txt, 13, 400, w - 40)
    T(d, c, txt, 20, 48, size=13, color="#ffffff", lh=20, w=w - 40, opacity=0.92)
    yy = 48 + 20 * n + 14
    b, bw = ui.button(d, c, 20, yy, "Copiar meu link", app=APP, kind="primary", h=40, icon_name="link")
    d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
    for ch in d.nodes[b]["children"]:
        nd = d.nodes[ch]
        if nd["type"] == "text": nd["fills"] = [fc.paint(C["ink"])]
        if nd["type"] == "vector": nd["strokes"] = [fc.paint(C["ink"])]
    return _fecha(d, c, yy + 40 + 20)

def c02(d, f, dev, app):
    mob = dev == "mobile"
    y = _moldura(d, f, dev, "Início") + (32 if not mob else 24)
    x, cw = wrap(dev)
    y = _cabeca(d, f, dev, y, [("BOA TARDE,", "ink"), ("CARLA", "green")], "Seu resumo de novembro na loja PNZ")
    y = _kpis(d, f, dev, y, [("Vendas no mês", "R$ 1.836,75", "16 pedidos · R$ 1.467,75 concluídos", True),
                             ("Comissão a receber", "R$ 38,01", "5% sobre pedidos concluídos", False),
                             ("Pedidos em andamento", "3", "1 novo aguardando você", False),
                             ("Ticket médio", "R$ 114,80", "no mês", False)]) + 16
    g = 16 if not mob else 12
    if mob:
        for fn in (_p_precisam, _p_meta, lambda d, f, x, y, w: _p_grafico(d, f, x, y, w, dev), _p_tarefas, _p_estoque, _p_ranking, _p_link):
            y += fn(d, f, x, y, cw) + g
    else:
        lw = round(cw * (0.6 if dev == "desktop" else 0.57)) - g // 2
        rw = cw - lw - g
        ly = y
        for fn in (_p_meta, lambda d, f, x, y, w: _p_grafico(d, f, x, y, w, dev), _p_precisam):
            ly += fn(d, f, x, ly, lw) + g
        ry = y
        for fn in (_p_tarefas, _p_ranking, _p_estoque, _p_link):
            ry += fn(d, f, x + lw + g, ry, rw) + g
        y = max(ly, ry)
    return _fim(d, f, dev, "Início", y)

# ---------------------------------------------------------------- C03 pedidos
def _passos(o):
    return ["novo", "confirmado", "separado", "a_caminho" if o["tipo"] == "Entrega" else "pronto", "concluido"]

def _pedido(d, p, x, y, w, o, dev, aberto=False):
    mob = dev == "mobile"
    c = d.frame(p, f"Pedido {o['id']}", x, y, w, 10, fill=C["card"], stroke=C["ink"] if aberto else C["line"],
                stroke_opacity=0.35 if aberto else 0.08, radius=12)
    total = TOTAIS[o["id"]]
    qn = sum(q for q, _, _ in o["itens"])
    sub = f"{o['nome']} · {o['quando']} · {qn} {'itens' if qn > 1 else 'item'} · {o['tipo']}"
    T(d, c, o["id"], 18, 16, size=15, weight=700, lh=22)
    tx = 18 + fc.text_width(o["id"], 15, 700) + 10
    tg = d.frame(c, "Origem", tx, 18, fc.text_width(o["origem"], 11, 600) + 16, 20, fill=C["page"], radius=10)
    T(d, tg, o["origem"], 8, 1, size=11, weight=600, color=C["text2"], lh=18)
    _selo(d, c, w - 18, 15, STL[o["st"]], o["st"], align="right")
    if not mob:
        T(d, c, sub, 18, 44, size=13, color=C["text2"], lh=20, w=w - 220)
        T(d, c, brl(total), w - 18, 44, size=15, weight=700, align="right", lh=20)
        ax = w - 18 - fc.text_width(brl(total), 15, 700) - 26
        if aberto: d.polyline(c, [(ax + 3, 56), (ax + 8, 51), (ax + 13, 56)], C["muted"], name="Ícone recolher")
        else: ui.icon(d, c, "seta-baixo", ax, 46, 16, C["muted"])
        yy = 80
    else:
        n = nl(sub, 13, 400, w - 36)
        T(d, c, sub, 18, 46, size=13, color=C["text2"], lh=20, w=w - 36)
        yy = 46 + 20 * n + 6
        T(d, c, brl(total), 18, yy, size=16, weight=700, lh=22)
        if aberto: d.polyline(c, [(w - 31, yy + 14), (w - 26, yy + 9), (w - 21, yy + 14)], C["muted"], name="Ícone recolher")
        else: ui.icon(d, c, "seta-baixo", w - 34, yy + 3, 16, C["muted"])
        yy += 22 + 14
    if not aberto:
        return _fecha(d, c, yy)
    hair(d, c, 0, yy, w)
    yy += 20
    passos = _passos(o); cur = passos.index(o["st"])
    if not mob:
        sw = (w - 36) / len(passos)
        d.frame(c, "Trilha", 18 + sw / 2, yy + 7, sw * (len(passos) - 1), 2, fill=C["deep"])
        d.frame(c, "Trilha feita", 18 + sw / 2, yy + 7, sw * cur, 2, fill=C["green"])
        for i, s in enumerate(passos):
            cx = 18 + sw * i + sw / 2
            d.ellipse(c, cx - 8, yy, 16, C["green"] if i <= cur else C["deep"], name=f"Etapa {s}")
            T(d, c, STL[s].replace(" p/ retirada", "").replace(" p/ entrega", ""), cx, yy + 22, size=12,
              weight=600 if i == cur else 400, color=C["ink"] if i <= cur else C["muted"], align="center", lh=18)
        yy += 22 + 18 + 24
    else:
        sw = (w - 36 - 4 * 4) / 5
        for i in range(5):
            d.frame(c, f"Etapa {i + 1}", 18 + i * (sw + 4), yy, sw, 6, fill=C["green"] if i <= cur else C["deep"], radius=3)
        T(d, c, f"Etapa {cur + 1} de 5 · {STL[o['st']]}", 18, yy + 14, size=12, weight=600, lh=18)
        T(d, c, f"Próxima: {STL[passos[cur + 1]].replace(' p/ retirada', '')}", w - 18, yy + 14, size=12, color=C["muted"], align="right", lh=18)
        yy += 14 + 18 + 20
    # itens + dados
    meta = [("Cliente", o["nome"] + ("\n" + o["whats"] if o["whats"] else "")), (o["tipo"], o["slot"] or "Na loja"),
            ("Pagamento", o["pag"]), ("Sua comissão", f"{brl(total * TAXA)} · prevista")]
    iw = w - 36 if mob else (w - 36) * 0.5 - 12
    ib = d.frame(c, "Itens", 18, yy, iw, 10, fill=C["page"], radius=10)
    iy = 12
    for q, nm, pr in o["itens"]:
        t = f"{q}× {nm}"
        n = nl(t, 13, 400, iw - 24 - 90)
        T(d, ib, t, 12, iy, size=13, lh=20, w=iw - 24 - 90)
        T(d, ib, brl(q * pr), iw - 12, iy, size=13, align="right", lh=20)
        iy += 20 * n + 8
    hair(d, ib, 12, iy, iw - 24); iy += 10
    T(d, ib, "Total", 12, iy, size=14, weight=700, lh=20)
    T(d, ib, brl(total), iw - 12, iy, size=14, weight=700, align="right", lh=20)
    iy += 20 + 12
    _fecha(d, ib, iy)
    if mob:
        yy += iy + 16
        mx, mw, cols = 18, w - 36, 2
    else:
        mx, mw, cols = 18 + iw + 24, (w - 36) - iw - 24, 2
    colw = (mw - 16) / cols
    my = yy if mob else yy
    rowh = []
    for i, (k, v) in enumerate(meta):
        cx = mx + (i % cols) * (colw + 16)
        n = sum(nl(seg, 13, 500, colw) for seg in v.split("\n"))
        cy = my + sum(rowh[:i // cols]) if i % cols == 0 else my + sum(rowh[:i // cols])
        T(d, c, k, cx, cy, size=11, weight=600, color=C["muted"], lh=16)
        T(d, c, v, cx, cy + 18, size=13, weight=500, lh=20, w=colw)
        if i % cols == cols - 1 or i == len(meta) - 1:
            hs = [18 + 20 * sum(nl(seg, 13, 500, colw) for seg in meta[j][1].split("\n")) + 16 for j in range(i - i % cols, i + 1)]
            rowh.append(max(hs))
    mh = sum(rowh)
    yy = (yy + mh) if mob else yy + max(iy, mh)
    yy += 8
    # ações
    acts = [("Confirmar pedido", "primary", "ok"), ("Avisar no WhatsApp", "dark", "whats"), ("Cancelar", "danger", None)]
    if mob:
        ui.button(d, c, 18, yy, acts[0][0], app=APP, kind="primary", w=w - 36, h=44, icon_name="ok")
        yy += 52
        hw = (w - 36 - 8) / 2
        ui.button(d, c, 18, yy, "WhatsApp", app=APP, kind="dark", w=hw, h=44, icon_name="whats")
        ui.button(d, c, 18 + hw + 8, yy, "Cancelar", app=APP, kind="danger", w=hw, h=44)
        yy += 44 + 18
    else:
        bx = 18
        for lab, kind, ic in acts:
            _, bw = ui.button(d, c, bx, yy, lab, app=APP, kind=kind, h=44, icon_name=ic)
            bx += bw + 8
        yy += 44 + 18
    return _fecha(d, c, yy)

def c03(d, f, dev, app, aberto=True):
    mob = dev == "mobile"
    y = _moldura(d, f, dev, "Pedidos") + (32 if not mob else 24)
    x, cw = wrap(dev)
    y = _cabeca(d, f, dev, y, [("SEUS", "ink"), ("PEDIDOS", "green")], "Pedidos feitos pelo seu link e vendas registradas no balcão",
                acao=("Venda no balcão", "mais"))
    y += _chips(d, f, x, y, [("Em andamento", 3), ("Sem atendente", 0), ("Concluídos", 21), ("Cancelados", 2), ("Todos", 26)], 0, dev,
                wrap_w=cw if mob else None) + 16
    for i, o in enumerate(PEDIDOS):
        y += _pedido(d, f, x, y, cw, o, dev, aberto=aberto and i == 0) + 12
    return _fim(d, f, dev, "Pedidos", y)

# ---------------------------------------------------------------- C04 venda no balcão
BUSCA = [(5, "PAPELITO", "Papelito Marrom c/ Piteira + Bandeja", 15.0, 3), (7, "OCB", "OCB King Size Slim Premium", 8.0, 17),
         (11, "RAW", "Seda Raw King Size Classic", 10.0, 11), (20, "ZOMO", "Caixa c/50 Seda Zomo KS Brown", 120.0, 6),
         (40, "CLIPPER", "Isqueiro Clipper Grande", 18.0, 10), (70, "VINHO", "Vinho tinto seco 750 ml", 59.0, 0)]
CARRINHO = [("Papelito Marrom c/ Piteira + Bandeja", 15.0, 1), ("OCB King Size Slim Premium", 8.0, 1)]
PAGS = ["Pix", "Crédito", "Débito", "Carteira", "Boleto", "Dinheiro"]

def _resultado(d, p, x, y, w, item, no_carrinho=False, h=56):
    pid, marca, nm, pr, est = item
    esg = est <= 0
    bw = 36
    tw = w - 60 - 80 - bw - 12
    n = nl(nm, 13, 500, tw)
    h = max(h, 20 * n + 16 + 20)
    r = d.frame(p, f"Resultado {nm}"[:40], x, y, w, h, fill=SOFT if no_carrinho else C["card"],
                stroke=VERDE if no_carrinho else C["line"], stroke_opacity=0.6 if no_carrinho else 0.1, radius=10,
                opacity=0.5 if esg else 1.0)
    _foto(d, r, 8, (h - 40) / 2, 40, marca)
    ty = (h - 20 * n - 16) / 2
    T(d, r, nm, 58, ty, size=13, weight=500, lh=20, w=tw)
    T(d, r, "Esgotado" if esg else f"{est} em estoque" + (" · no carrinho" if no_carrinho else ""), 58, ty + 20 * n, size=11,
      weight=600 if esg else 400, color=C["neg"] if esg else C["muted"], lh=16)
    T(d, r, brl(pr), w - 12 - bw - 10, (h - 20) / 2, size=13, weight=700, align="right", lh=20)
    a = d.frame(r, "Adicionar", w - 10 - bw, (h - bw) / 2, bw, bw, fill=C["deep"] if esg else C["black"], radius=bw / 2)
    ui.icon(d, a, "mais", (bw - 16) / 2, (bw - 16) / 2, 16, C["muted"] if esg else "#ffffff")
    return h

def _item_carrinho(d, p, x, y, w, nm, pr, q, fill=None):
    sw = 104
    tw = w - 24 - sw - 12 - 76
    n = nl(nm, 13, 500, tw)
    h = max(56, 10 + 20 * n + 16 + 10)
    r = d.frame(p, f"Item {nm}"[:40], x, y, w, h, fill=fill or C["page"], radius=10,
                stroke=C["line"] if fill else None, stroke_opacity=0.08)
    T(d, r, nm, 12, 10, size=13, weight=500, lh=20, w=tw)
    T(d, r, f"{brl(pr)} cada", 12, 10 + 20 * n, size=11, color=C["muted"], lh=16)
    _stepper(d, r, w - 12 - 76 - sw, (h - 36) / 2, q, h=36, w=sw)
    T(d, r, brl(pr * q), w - 12, (h - 20) / 2, size=13, weight=700, align="right", lh=20)
    return h

def _pagamento(d, p, x, y, w, dev, ativo=0):
    h = 40 if dev != "mobile" else 44
    cols = 3; g = 8
    bw = (w - g * (cols - 1)) / cols
    for i, lab in enumerate(PAGS):
        on = i == ativo
        b = d.frame(p, f"Pagamento {lab}", x + (i % cols) * (bw + g), y + (i // cols) * (h + g), bw, h,
                    fill=SOFT if on else C["card"], stroke=VERDE if on else C["line"], stroke_opacity=1.0 if on else 0.16,
                    stroke_w=2 if on else 1, radius=8)
        T(d, b, lab, bw / 2, (h - 20) / 2, size=13, weight=600 if on else 500, color=C["ink"], align="center", lh=20)
    return 2 * h + g

def _resumo(d, p, x, y, w):
    rows = [("Subtotal", "R$ 23,00", None), ("Desconto Pix (5%)", "-R$ 1,15", C["pos"])]
    yy = y
    for k, v, col in rows:
        T(d, p, k, x, yy, size=13, color=col or C["text2"], lh=20)
        T(d, p, v, x + w, yy, size=13, color=col or C["ink"], align="right", lh=20)
        yy += 26
    hair(d, p, x, yy, w); yy += 10
    T(d, p, "Total", x, yy + 2, size=16, weight=700, lh=24)
    T(d, p, "R$ 21,85", x + w, yy, size=20, weight=700, align="right", lh=28)
    return yy + 28 - y

NOTA = "A venda entra como concluída, baixa o estoque e conta para a sua comissão"

def c04(d, f, dev, app):
    if dev == "mobile":
        return _c04_celular(d, f, dev)
    c03(d, f, dev, app, aberto=False)
    ww = 960 if dev == "desktop" else 920
    wh = 64 + 24 + 476 + 24 + 72
    win, ww, wh, top, bot = ui.window(d, f, dev, "Venda no balcão", ww, wh, app=APP,
                                      footer_buttons=[("Cancelar", "secondary", None), ("Registrar venda · R$ 21,85", "primary", None)])
    fbw = fc.text_width("Cancelar", 14, 500) + 32 + fc.text_width("Registrar venda · R$ 21,85", 14, 500) + 32 + 8 + 24
    nw = ww - 48 - fbw - 16
    n = nl(NOTA, 12, 400, nw)
    T(d, win, NOTA, 24, bot + (72 - 16 * n) / 2, size=12, color=C["muted"], lh=16, w=nw)
    g = 24
    lw = round((ww - 48 - g) * 0.52); rw = ww - 48 - g - lw
    lx, rx = 24, 24 + lw + g
    y = top + 24
    ui.field(d, win, lx, y, lw, label="Buscar produto", placeholder="Nome, marca ou categoria", focused=True, app=APP, prefix_icon="busca", h=44)
    y += 20 + 44 + 16
    T(d, win, "Destaques da loja", lx, y, size=12, weight=600, color=C["muted"], lh=18)
    y += 26
    for i, it in enumerate(BUSCA):
        y += _resultado(d, win, lx, y, lw, it, no_carrinho=i in (0, 1)) + 6
    d.frame(win, "Divisa", lx + lw + g / 2, top, 1, bot - top, fill=C["line"], fill_opacity=0.08)
    y = top + 24
    T(d, win, "Itens da venda", rx, y, size=13, weight=600, lh=20)
    T(d, win, "2 itens", rx + rw, y, size=12, color=C["muted"], align="right", lh=20)
    y += 28
    for nm, pr, q in CARRINHO:
        y += _item_carrinho(d, win, rx, y, rw, nm, pr, q) + 8
    y += 8
    hw = (rw - 12) / 2
    ui.field(d, win, rx, y, hw, label="Cliente (opcional)", value="Lucas Andrade", app=APP, h=40)
    ui.field(d, win, rx + hw + 12, y, hw, label="WhatsApp (opcional)", placeholder="(87) 99999-9999", app=APP, h=40)
    y += 60 + 16
    T(d, win, "Pagamento", rx, y, size=13, color=C["text2"], lh=16)
    y += 22
    y += _pagamento(d, win, rx, y, rw, dev) + 18
    _resumo(d, win, rx, y, rw)
    return d.nodes[f]["height"]

def _c04_celular(d, f, dev):
    W = DEVICES[dev][0]
    x, cw = wrap(dev)
    bar = d.frame(f, "Topo da venda", 0, 0, W, 60, fill=C["black"])
    ui.icon(d, bar, "seta-esq", 16, 20, 20, "#ffffff")
    d.text(bar, "VENDA NO BALCÃO", 48, 16, size=26, family=ui.DISPLAY, color="#ffffff", lh=28)
    T(d, bar, "PNZ", W - 16, 20, size=12, weight=600, color="#b9bbb4", align="right", lh=20)
    y = 60 + 16
    ui.field(d, f, x, y, cw, placeholder="Buscar nome, marca ou categoria", focused=True, app=APP, prefix_icon="busca", h=44)
    y += 44 + 16
    T(d, f, "Destaques da loja", x, y, size=12, weight=600, color=C["muted"], lh=18)
    y += 26
    for i, it in enumerate(BUSCA[:4]):
        y += _resultado(d, f, x, y, cw, it, no_carrinho=i in (0, 1), h=60) + 6
    y += 16
    T(d, f, "Itens da venda", x, y, size=14, weight=600, lh=20)
    T(d, f, "2 itens", x + cw, y, size=12, color=C["muted"], align="right", lh=20)
    y += 28
    for nm, pr, q in CARRINHO:
        y += _item_carrinho(d, f, x, y, cw, nm, pr, q, fill=C["card"]) + 8
    y += 12
    ui.field(d, f, x, y, cw, label="Cliente (opcional)", value="Lucas Andrade", app=APP, h=44)
    y += 64 + 12
    ui.field(d, f, x, y, cw, label="WhatsApp (opcional)", placeholder="(87) 99999-9999", app=APP, h=44)
    y += 64 + 16
    T(d, f, "Pagamento", x, y, size=13, color=C["text2"], lh=16)
    y += 22
    y += _pagamento(d, f, x, y, cw, dev) + 16
    c = _painel(d, f, x, y, cw, name="Resumo")
    rh = _resumo(d, c, 16, 16, cw - 32)
    _fecha(d, c, rh + 32)
    y += rh + 32 + 12
    T(d, f, NOTA, x, y, size=12, color=C["muted"], lh=16, w=cw)
    y += 16 * nl(NOTA, 12, 400, cw) + 24
    total = max(DEVICES[dev][1], y + 88)
    ui.altura(d, f, total)
    ui.mobile_bar(d, f, "R$ 21,85", caption="Total no Pix", app=APP, label="Registrar venda")
    return total

# ---------------------------------------------------------------- C05 estoque
SEDAS = [(1, "ZOMO", "Seda Zomo King Size Brown", 5.0, 9), (2, "ZOMO", "Seda Zomo King Size Rosa", 5.0, 16),
         (3, "ALEDA", "Seda Aleda KS Clássica Vermelha", 6.0, 6), (4, "PAPELITO", "Seda Papelito King Size Brown Large", 7.0, 13),
         (5, "PAPELITO", "Papelito Marrom c/ Piteira + Bandeja", 15.0, 3), (6, "BEM BOLADO", "Seda Bem Bolado KS Large Hemp", 8.0, 10),
         (7, "OCB", "OCB King Size Slim Premium", 8.0, 17), (8, "OCB", "OCB King Size Slim Ultimate", 10.0, 7),
         (9, "SMOKING", "Seda Smoking King Size Deluxe", 8.0, 14), (10, "LION", "Lion Rolling Circus KS Alfafa", 9.0, 4),
         (11, "RAW", "Seda Raw King Size Classic", 10.0, 11), (12, "RAW", "Seda Raw KS Slim Organic Hemp", 12.0, 18),
         (13, "PURE HEMP", "Seda Pure Hemp King Size", 9.0, 8)]
EDITS = {5: 15, 10: 12}

def _situ(q):
    return ("Esgotado", "neg") if q <= 0 else (("Baixo", "warn") if q < 5 else ("Ok", "ok"))

def _savebar(d, f, dev, bottom):
    W = DEVICES[dev][0]; x, cw = wrap(dev); mob = dev == "mobile"
    h = 64 if not mob else 60
    bx, bw = (x, cw) if not mob else (12, W - 24)
    b = d.frame(f, "Barra salvar estoque", bx, bottom - h, bw, h, fill=C["bar"], radius=12, shadow=ui.shadow(0.2, 8, 24))
    lab = "2 produtos alterados" if not mob else "2 alterados"
    T(d, b, lab, 18, (h - 20) / 2, size=14, weight=600, color="#ffffff", lh=20)
    sl = "Salvar estoque" if not mob else "Salvar"
    sw = fc.text_width(sl, 14, 600) + 36
    s = d.frame(b, "Salvar", bw - 12 - sw, (h - 40) / 2, sw, 40, fill=C["yellow"], radius=20)
    T(d, s, sl, sw / 2, 10, size=14, weight=600, align="center", lh=20)
    uw = fc.text_width("Desfazer", 14, 500) + 32
    u = d.frame(b, "Desfazer", bw - 12 - sw - 8 - uw, (h - 40) / 2, uw, 40, stroke="#ffffff", stroke_opacity=0.3, radius=20)
    T(d, u, "Desfazer", uw / 2, 10, size=14, weight=500, color="#ffffff", align="center", lh=20)

def c05(d, f, dev, app):
    mob = dev == "mobile"
    y = _moldura(d, f, dev, "Estoque") + (32 if not mob else 24)
    x, cw = wrap(dev)
    y = _cabeca(d, f, dev, y, [("ESTOQUE", "ink"), ("PNZ", "green")],
                "O que você salvar aqui aparece na hora na vitrine da loja PNZ. Estoque mínimo: 5 unidades")
    y += _chips(d, f, x, y, [("Todos", 34), ("Estoque baixo", 5), ("Esgotados", 3)], 0, dev, wrap_w=cw if mob else None) + 12
    if mob:
        ui.field(d, f, x, y, cw, placeholder="Buscar produto", prefix_icon="busca", app=APP, h=44)
        y += 44 + 8
        ui.field(d, f, x, y, cw, value="Sedas", chevron=True, app=APP, h=44)
        y += 44 + 12
    else:
        sw = 260
        ui.field(d, f, x, y, cw - sw - 12, placeholder="Buscar produto", prefix_icon="busca", app=APP, h=44)
        ui.field(d, f, x + cw - sw, y, sw, value="Sedas", chevron=True, app=APP, h=44)
        y += 44 + 12
    T(d, f, "13 produtos em Sedas", x, y, size=12, color=C["muted"], lh=18)
    y += 26
    if not mob:
        t = d.frame(f, "Tabela de estoque", x, y, cw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12, clip=True)
        cols = [("Produto", None), ("Preço", 140), ("Quantidade", 240 if dev == "desktop" else 220), ("Situação", 140)]
        fixed = sum(c[1] for c in cols if c[1]); pw = cw - 40 - fixed
        xs = [20, 20 + pw, 20 + pw + 140, 20 + pw + 140 + cols[2][1]]
        for (lab, _), cx in zip(cols, xs):
            T(d, t, lab, cx, 12, size=12, weight=600, color=C["muted"], lh=16)
        hair(d, t, 0, 40, cw)
        yy = 41
        rh = 64
        for i, (pid, marca, nm, pr, q) in enumerate(SEDAS):
            mud = pid in EDITS; v = EDITS.get(pid, q)
            if mud: d.frame(t, "Alterado", 0, yy, cw, rh, fill="#fff8e1")
            _foto(d, t, 20, yy + 12, 40, marca)
            T(d, t, nm, 72, yy + 12, size=13, weight=600, lh=20, w=pw - 72)
            T(d, t, "Sedas", 72, yy + 32, size=11, color=C["muted"], lh=16)
            T(d, t, brl(pr), xs[1], yy + 22, size=13, lh=20)
            _stepper(d, t, xs[2], yy + 12, v, h=40, w=124, mudou=mud)
            if mud: T(d, t, f"antes {q}", xs[2] + 134, yy + 22, size=12, color=C["muted"], lh=20)
            lab, tone = _situ(v)
            _selo(d, t, xs[3], yy + 20, lab, tone)
            yy += rh
            if i < len(SEDAS) - 1: hair(d, t, 20, yy, cw - 40)
        _fecha(d, t, yy + 4)
        y += yy + 4 + 24
        total = max(DEVICES[dev][1], y + 64 + 48)
        ui.altura(d, f, total)
        _savebar(d, f, dev, total - 24)
        return total
    # celular: lista em cartões, quantidade com alvo de 40
    lst = d.frame(f, "Lista de estoque", x, y, cw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12, clip=True)
    yy = 0
    for i, (pid, marca, nm, pr, q) in enumerate(SEDAS):
        mud = pid in EDITS; v = EDITS.get(pid, q)
        lab, tone = _situ(v)
        pw_ = fc.text_width(lab, 12, 600) + 30
        tw = cw - 68 - 14 - pw_ - 8
        n = nl(nm, 14, 600, tw)
        rh = 14 + max(44, 20 * n + 18) + 10 + 40 + 14
        if mud: d.frame(lst, "Alterado", 0, yy, cw, rh, fill="#fff8e1")
        _foto(d, lst, 14, yy + 14, 44, marca)
        T(d, lst, nm, 68, yy + 14, size=14, weight=600, lh=20, w=tw)
        T(d, lst, f"Sedas · {brl(pr)}", 68, yy + 14 + 20 * n, size=12, color=C["muted"], lh=18)
        _selo(d, lst, cw - 14, yy + 14, lab, tone, align="right")
        sy = yy + 14 + max(44, 20 * n + 18) + 10
        _stepper(d, lst, 68, sy, v, h=40, w=136, mudou=mud)
        if mud: T(d, lst, f"antes {q}", 68 + 146, sy + 10, size=12, color=C["muted"], lh=20)
        yy += rh
        if i < len(SEDAS) - 1: hair(d, lst, 14, yy, cw - 28)
    _fecha(d, lst, yy)
    y += yy + 16
    total = max(DEVICES[dev][1], y + 60 + 16 + 64 + 16)
    ui.altura(d, f, total)
    _savebar(d, f, dev, total - 64 - 12)
    ui.painel_nav(d, f, ABAS, "Estoque", ICONES, badges=BADGES)
    return total

# ---------------------------------------------------------------- C06 link e QR
MSGS = [("Para clientes no WhatsApp", "Oi! Aqui é Carla, da Smoke House PNZ. Agora você pode ver o estoque e fazer seu pedido pelo site, com entrega ou retirada na loja:"),
        ("Para o status do Instagram", "Sedas, isqueiros, Tattoo Supply e muito mais. Peça pelo meu link e retire na loja ou receba em casa:"),
        ("Para tatuadores", "Oi! Aqui é Carla, da Smoke House PNZ. A linha Tattoo Supply está no site: confere o estoque e pede por aqui que eu separo pra você:")]

def _p_seulink(d, f, x, y, w, dev):
    mob = dev == "mobile"
    c = _painel(d, f, x, y, w, "Seu link de venda")
    yy = 56
    bw = 148
    lw = w - 40 if mob else w - 40 - bw - 8
    lb = d.frame(c, "Link", 20, yy, lw, 44, fill=C["page"], stroke=C["line"], stroke_opacity=0.12, radius=8, clip=True)
    ui.icon(d, lb, "link", 12, 14, 16, C["muted"])
    T(d, lb, corta(URL, 13, lw - 48), 36, 12, size=13, mono=True, lh=20)
    if mob:
        yy += 52
        ui.button(d, c, 20, yy, "Copiar link", app=APP, kind="primary", w=w - 40, h=44, icon_name="link")
    else:
        ui.button(d, c, 20 + lw + 8, yy, "Copiar link", app=APP, kind="primary", w=bw, h=44, icon_name="link")
    yy += 44 + 16
    kw = (w - 40 - 12) / 2
    ks = (("Pedidos pelo link", "16", "desde o início"), ("Vendas pelo link", "R$ 2.348,40", "pedidos não cancelados"))
    kh = max(38 + 32 + 4 + 16 * nl(nt, 12, 400, kw - 28) + 14 for _, _, nt in ks)
    for i, (lab, val, note) in enumerate((("Pedidos pelo link", "16", "desde o início"), ("Vendas pelo link", "R$ 2.348,40", "pedidos não cancelados"))):
        k = d.frame(c, f"Indicador {lab}", 20 + i * (kw + 12), yy, kw, kh, fill=C["card"], stroke=C["line"], stroke_opacity=0.1, radius=10)
        T(d, k, lab, 14, 14, size=12, weight=500, color=C["text2"], lh=18, w=kw - 28)
        vs = 26
        while fc.text_width(val, vs, 700) > kw - 28 and vs > 18: vs -= 2
        T(d, k, val, 14, 38, size=vs, weight=700, lh=32)
        T(d, k, note, 14, 74, size=12, color=C["muted"], lh=16, w=kw - 28)
    yy += kh + 20
    return _fecha(d, c, yy)

def _p_msgs(d, f, x, y, w, dev):
    c = _painel(d, f, x, y, w, "Mensagens prontas")
    yy = 56
    iw = w - 40 - 28
    for tit, txt in MSGS:
        n = nl(txt, 13, 400, iw)
        h = 14 + 20 + 8 + 20 * n + 4 + 18 + 12 + 36 + 14
        b = d.frame(c, f"Mensagem {tit}"[:40], 20, yy, w - 40, h, fill=C["page"], radius=10)
        T(d, b, tit, 14, 14, size=13, weight=600, color=VERDE, lh=20)
        T(d, b, txt, 14, 42, size=13, lh=20, w=iw)
        T(d, b, corta(URL, 12, iw), 14, 42 + 20 * n + 4, size=12, mono=True, color=C["text2"], lh=18)
        ui.button(d, b, 14, h - 14 - 36, "Copiar mensagem", app=APP, kind="dark", h=36)
        yy += h + 10
    return _fecha(d, c, yy + 10)

def _p_qr(d, f, x, y, w, dev):
    mob = dev == "mobile"
    c = d.frame(f, "QR do balcão", x, y, w, 10, fill=C["black"], radius=12)
    ui.brush(d, c, w / 2, 24, [("QR DO", "white"), ("BALCÃO", "green")], size=32 if not mob else 28, align="center")
    s = 232 if not mob else 220
    _qr(d, c, (w - s) / 2, 78, s)
    cap = "Imprima e deixe no caixa: o cliente aponta a câmera e compra pelo seu link"
    cw = min(w - 48, 320)
    n = nl(cap, 13, 400, cw)
    T(d, c, cap, w / 2 - cw / 2, 78 + s + 18, size=13, color="#c9cac4", align="center", lh=20, w=cw)
    return _fecha(d, c, 78 + s + 18 + 20 * n + 24)

def c06(d, f, dev, app):
    mob = dev == "mobile"
    y = _moldura(d, f, dev, "Meu link") + (32 if not mob else 24)
    x, cw = wrap(dev)
    y = _cabeca(d, f, dev, y, [("MEU", "ink"), ("LINK", "green")], "Todo pedido feito por este link fica registrado no seu nome e gera 5% de comissão")
    g = 16 if not mob else 12
    if mob:
        y += _p_seulink(d, f, x, y, cw, dev) + g
        y += _p_qr(d, f, x, y, cw, dev) + g
        y += _p_msgs(d, f, x, y, cw, dev) + g
    else:
        lw = round(cw * (0.6 if dev == "desktop" else 0.6)) - g // 2
        rw = cw - lw - g
        ly = y + _p_seulink(d, f, x, y, lw, dev) + g
        ly += _p_msgs(d, f, x, ly, lw, dev) + g
        ry = y + _p_qr(d, f, x + lw + g, y, rw, dev) + g
        y = max(ly, ry)
    return _fim(d, f, dev, "Meu link", y)

# ---------------------------------------------------------------- C07 comissões
EXTRATO = [("25/11/2026", "PNZ-1048", "Mariana Alves", 212.00, "p"), ("25/11/2026", "PNZ-1047", "Rafael Souza", 57.00, "p"),
           ("23/11/2026", "PNZ-1039", "Juliana Costa", 100.00, "p"), ("21/11/2026", "PNZ-1044", "Thiago Ramos", 90.25, "r"),
           ("20/11/2026", "PNZ-1043", "Beatriz Lima", 100.00, "r"), ("19/11/2026", "PNZ-1041", "Pedro Henrique Matos", 209.00, "r"),
           ("16/11/2026", "PNZ-1036", "Larissa Melo", 133.00, "r"), ("14/11/2026", "PNZ-1034", "Gustavo Nunes", 172.00, "r"),
           ("13/11/2026", "PNZ-1031", "Camila Rocha", 56.00, "r"), ("10/11/2026", "PNZ-1027", "Diego Ferreira", 93.00, "g"),
           ("07/11/2026", "PNZ-1024", "Ana Paula Dias", 54.00, "g"), ("06/11/2026", "PNZ-1022", "Felipe Barros", 158.65, "g"),
           ("03/11/2026", "PNZ-1019", "Renata Cruz", 143.00, "g")]
SIT = {"p": ("Prevista", "info"), "r": ("A receber", "warn"), "g": ("Paga", "ok")}

def c07(d, f, dev, app):
    mob = dev == "mobile"
    y = _moldura(d, f, dev, "Comissões") + (32 if not mob else 24)
    x, cw = wrap(dev)
    y = _cabeca(d, f, dev, y, [("SUAS", "ink"), ("COMISSÕES", "green")],
                "Taxa de 5% sobre o total dos pedidos concluídos. Os donos fecham e pagam pelo painel deles")
    y = _kpis(d, f, dev, y, [("A receber", "R$ 38,01", "6 pedidos concluídos", True), ("Prevista", "R$ 18,45", "3 pedidos em andamento", False),
                             ("Já paga", "R$ 106,60", "15 pedidos", False), ("Total no mês", "R$ 73,39", "concluídos no mês", False)]) + 16
    c = _painel(d, f, x, y, cw, "Extrato", sub="13 de 24 lançamentos")
    yy = 56
    if not mob:
        iw = cw - 40
        cols = [("Data", 0.14, "l"), ("Pedido", 0.14, "l"), ("Cliente", 0.30, "l"), ("Valor", 0.13, "r"), ("Comissão", 0.13, "r"), ("Situação", 0.16, "l")]
        xs = []; cx = 20
        for lab, frac, al in cols:
            xs.append((cx, iw * frac, al)); cx += iw * frac
        for (lab, _, al), (cx, cwid, _) in zip(cols, xs):
            T(d, c, lab, cx + (cwid - 16 if al == "r" else 0), yy, size=12, weight=600, color=C["muted"], align="right" if al == "r" else "left", lh=16)
        yy += 26; hair(d, c, 20, yy, iw); yy += 1
        for i, (dt, pid, nm, v, s) in enumerate(EXTRATO):
            vals = [dt, pid, nm, brl(v), brl(v * TAXA)]
            for j, val in enumerate(vals):
                cx, cwid, al = xs[j]
                T(d, c, val, cx + (cwid - 16 if al == "r" else 0), yy + 14, size=13, weight=700 if j in (1, 4) else 400,
                  color=C["ink"] if j != 2 else C["text2"], align="right" if al == "r" else "left", lh=20)
            _selo(d, c, xs[5][0], yy + 12, *SIT[s])
            yy += 48
            if i < len(EXTRATO) - 1: hair(d, c, 20, yy, iw)
    else:
        iw = cw - 32
        for i, (dt, pid, nm, v, s) in enumerate(EXTRATO):
            T(d, c, f"{pid} · {nm}", 16, yy + 12, size=14, weight=600, lh=20, w=iw - 100)
            n = nl(f"{pid} · {nm}", 14, 600, iw - 100)
            T(d, c, f"{dt[:5]} · pedido de {brl(v)}", 16, yy + 14 + 20 * n, size=12, color=C["muted"], lh=16)
            T(d, c, brl(v * TAXA), cw - 16, yy + 12, size=14, weight=700, align="right", lh=20)
            lab, tone = SIT[s]
            _selo(d, c, cw - 16, yy + 36, lab, tone, align="right")
            rh = max(12 + 20 * n + 18 + 12, 72)
            yy += rh
            if i < len(EXTRATO) - 1: hair(d, c, 16, yy, iw)
    yy += 8
    b, bw = ui.button(d, c, 0, yy, "Ver lançamentos anteriores", app=APP, kind="secondary", h=40, w=None if not mob else cw - 32)
    d.nodes[b]["transform"][4] = float((cw - bw) / 2)
    yy += 40 + 20
    _fecha(d, c, yy)
    y += yy
    return _fim(d, f, dev, "Comissões", y + 16)

SCREENS = [
    ("C01", "Colaborador · entrar", c01),
    ("C02", "Colaborador · início", c02),
    ("C03", "Colaborador · pedidos", c03),
    ("C04", "Colaborador · venda no balcão", c04),
    ("C05", "Colaborador · estoque", c05),
    ("C06", "Colaborador · link e QR", c06),
    ("C07", "Colaborador · comissões", c07),
]
