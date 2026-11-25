"""Responsivo · Painel dos donos (O01 a O08).

Regras de hoje em src/app.js (owLogin, owHome, owFin, owOrders, owOrderModal, owTeam, owAgenda, owCfg).
O que muda no responsivo:
- Celular: abas vão para ui.painel_nav (4 primeiras + Mais); tabela de pedidos vira cartões; KPIs em 1 + 2 colunas;
  filtros de loja e período em duas linhas; pedido aberto vira folha de baixo.
- Tablet: 1180 de verdade, controles com 40 de altura; agenda com calendário na largura toda.
- Computador: conteúdo até 1200, centralizado.
- Um gráfico principal por tela; O02 mantém as duas séries de hoje (PNZ verde, LEM amarelo); roscas viraram barras neutras.
"""
import os
import fc, ui
from ui import C, T, DEVICES, brl, hair

PAGE = "Responsivo · Painel dos donos"
APP = "donos"

TABS = ["Visão geral", "Financeiro", "Pedidos", "Equipe", "Agenda", "Ajustes"]
ICONS = ["grafico", "moeda", "caixa", "pessoas", "calendario", "engrenagem"]
BADGES = {"Pedidos": 3}
USER = ("Donos", "Comissões a pagar: R$ 96,28")
LOJAS = ["Duas lojas", "PNZ", "LEM"]
PERIODOS = ["Hoje", "7 dias", "Este mês", "30 dias"]

EV = {  # tipo: (rótulo, fundo, texto)
    "captacao": ("Captação de conteúdo", "#ece6f9", "#5b3aa0"),
    "reuniao": ("Reunião", "#e3ebf8", "#2f5d8a"),
    "fornecedor": ("Fornecedor", "#fbefc9", "#7a5800"),
    "pagamento": ("Pagamento", "#fbe4e4", "#a8262a"),
    "campanha": ("Campanha", "#e2efe7", "#256d45"),
    "folga": ("Folga/escala", "#ddf0f3", "#1f6672"),
}
EVENTOS = {  # dia de novembro/2026: [(hora, título, tipo, loja, responsável)]
    2: [("08:30", "Reunião de equipe", "reuniao", "Duas lojas", "Todos")],
    9: [("08:30", "Reunião de equipe", "reuniao", "Duas lojas", "Todos")],
    10: [("10:00", "Captação de conteúdo · Conexão", "captacao", "Loja PNZ", "Equipe PNZ")],
    12: [("14:00", "Entrega do distribuidor de sedas", "fornecedor", "Loja PNZ", "João")],
    14: [("", "Folga · Carla", "folga", "Loja PNZ", "Carla")],
    16: [("08:30", "Reunião de equipe", "reuniao", "Duas lojas", "Todos")],
    18: [("15:00", "Captação Tattoo Supply · Conexão", "captacao", "Loja LEM", "Bia")],
    20: [("09:00", "Dia da Consciência Negra · card institucional", "campanha", "Duas lojas", "Conexão")],
    23: [("08:30", "Reunião de equipe", "reuniao", "Duas lojas", "Todos")],
    27: [("08:00", "Black Friday (se aprovada)", "campanha", "Duas lojas", "Todos")],
    30: [("08:30", "Reunião de equipe", "reuniao", "Duas lojas", "Todos"),
         ("17:00", "Pagamento de comissões", "pagamento", "Duas lojas", "Donos")],
}
SEMANA = ["dom.", "seg.", "ter.", "qua.", "qui.", "sex.", "sáb."]
HOJE, DIA_SEL = 25, 30  # 25/11/2026 é quarta; 1/11/2026 é domingo

ST_TOM = {"Novo": "warn", "Confirmado": "info", "Separado": "muted", "Concluído": "ok", "Cancelado": "neg"}
PEDIDOS = [  # número, quando, loja, cliente, colaborador, canal, total, status
    ("PNZ-1001", "hoje, 16:24", "PNZ", "Mariana Lima", "Carla", "Site", 212.00, "Novo"),
    ("PNZ-1028", "hoje, 14:54", "PNZ", "Rafael Souza", "João", "Site", 149.00, "Confirmado"),
    ("LEM-1001", "hoje, 13:57", "LEM", "Juliana Prado", "Bia", "Site", 138.00, "Novo"),
    ("LEM-1002", "hoje, 12:03", "LEM", "Diego Matos", None, "Site", 189.00, "Novo"),
    ("PNZ-1027", "hoje, 10:43", "PNZ", "Camila Rocha", "João", "Site", 298.00, "Confirmado"),
    ("PNZ-1002", "hoje, 09:52", "PNZ", "Thiago Alves", "Carla", "Balcão", 57.00, "Confirmado"),
    ("PNZ-1035", "21/11, 13:49", "PNZ", "Larissa Melo", "João", "Site", 30.00, "Concluído"),
    ("PNZ-1017", "21/11, 11:06", "PNZ", "Bruno Carvalho", "Carla", "Site", 90.25, "Concluído"),
    ("PNZ-1034", "21/11, 08:49", "PNZ", "Patrícia Nunes", "João", "Site", 115.20, "Concluído"),
    ("PNZ-1016", "20/11, 11:14", "PNZ", "Felipe Araújo", "Carla", "Site", 100.00, "Concluído"),
    ("PNZ-1009", "19/11, 11:21", "PNZ", "Renata Gomes", "Carla", "Balcão", 209.00, "Concluído"),
    ("LEM-1004", "18/11, 15:16", "LEM", "Gustavo Pires", "Bia", "Site", 144.00, "Concluído"),
    ("LEM-1003", "18/11, 09:40", "LEM", "Aline Costa", "Bia", "Site", 28.50, "Separado"),
    ("PNZ-1032", "18/11, 14:37", "PNZ", "Vinícius Lopes", "João", "Site", 176.00, "Concluído"),
    ("PNZ-1008", "16/11, 13:45", "PNZ", "Natália Ribeiro", "Carla", "Balcão", 107.00, "Cancelado"),
    ("LEM-1016", "17/11, 13:17", "LEM", "Eduardo Freitas", "Bia", "Site", 120.00, "Concluído"),
]

# faturamento diário de novembro por loja (como o gráfico de hoje), escalado para os totais da tela
_PNZ = [0, 270, 330, 0, 770, 480, 150, 200, 110, 20, 60, 0, 40, 180, 0, 0, 270, 180, 200, 70, 230, 0, 0, 0, 720]
_LEM = [0, 0, 190, 0, 0, 0, 230, 190, 140, 0, 150, 120, 0, 0, 240, 0, 120, 140, 0, 0, 0, 0, 0, 0, 330]
PNZ = [v * 4384.15 / sum(_PNZ) for v in _PNZ]
LEM = [v * 2042.15 / sum(_LEM) for v in _LEM]


# ---------------------------------------------------------------- base
def _wrap(dev):
    W = DEVICES[dev][0]
    cw = 1200 if dev == "desktop" else (W - 64 if dev == "tablet" else W - 32)
    return (W - cw) / 2, cw

def _pad(dev): return 16 if dev == "mobile" else 20

def _nl(s, size, w, weight=400):
    return max(1, -(-int(fc.text_width(s, size, weight)) // int(max(1, w * 0.92))))

def _corta(s, size, weight, maxw):
    if fc.text_width(s, size, weight) <= maxw: return s
    while s and fc.text_width(s + "…", size, weight) > maxw: s = s[:-1]
    return s.rstrip() + "…"

def _shell(d, f, dev, aba, total):
    ui.altura(d, f, total)
    return ui.painel_header(d, f, dev, "Painel dos donos", USER, TABS, aba, badges=BADGES, app="donos")

def _fim(d, f, dev, aba, total):
    ui.altura(d, f, total)
    if dev == "mobile":
        ui.painel_nav(d, f, TABS, aba if TABS.index(aba) < 4 else "Mais", ICONS, badges=BADGES)
    return total

def _inicio(dev):
    return (60 + 24) if dev == "mobile" else (108 + 36)

def _titulo(d, f, dev, x, y, cw, parts, sub, acao=None):
    """Título pincelado + linha de apoio. acao = (rótulo, ícone): botão à direita (celular: embaixo, largura toda)."""
    mob = dev == "mobile"
    size = 34 if mob else 44
    ui.brush(d, f, x, y, parts, size=size)
    yy = y + int(size * 1.1) + 2
    aw = 0
    if acao and not mob:
        lab, ic = acao
        b, aw = ui.button(d, f, 0, y + 10, lab, app="donos", kind="primary", icon_name=ic, h=40)
        d.nodes[b]["transform"][4] = float(x + cw - aw)
        aw += 24
    tw = cw - aw
    T(d, f, sub, x, yy, size=13, color=C["text2"], lh=20, w=tw)
    yy += 20 * _nl(sub, 13, tw) + 20
    if acao and mob:
        lab, ic = acao
        ui.button(d, f, x, yy - 4, lab, app="donos", kind="primary", icon_name=ic, w=cw, h=44)
        yy += 44 + 12
    return yy

def _seg(d, p, x, y, items, active, h):
    """Controle segmentado (como o de hoje): pílula branca com a opção ativa em preto."""
    ws = [int(fc.text_width(t, 13, 600) + 28 + 3) // 4 * 4 for t in items]
    w = sum(ws) + 8
    s = d.frame(p, "Filtro " + " / ".join(items), x, y, w, h, fill=C["card"], stroke=C["line"], stroke_opacity=0.12, radius=h / 2)
    cx = 4
    for i, (t, iw) in enumerate(zip(items, ws)):
        on = i == active
        if on: d.frame(s, "Ativo", cx, 4, iw, h - 8, fill=C["black"], radius=(h - 8) / 2)
        T(d, s, t, cx + iw / 2, (h - 20) / 2, size=13, weight=600 if on else 500, color="#ffffff" if on else C["text2"], align="center", lh=20)
        cx += iw
    return w

def _filtros(d, f, dev, x, y, cw, loja=0, periodo=2, com_periodo=True):
    h = 36 if dev == "desktop" else 40
    w1 = _seg(d, f, x, y, LOJAS, loja, h)
    if not com_periodo: return h + 20
    if dev == "mobile":
        _seg(d, f, x, y + h + 8, PERIODOS, periodo, h)
        return 2 * h + 8 + 20
    _seg(d, f, x + w1 + 12, y, PERIODOS, periodo, h)
    return h + 20

def _painel(d, f, x, y, w, dev, titulo, extra=None, link=None):
    """Cartão branco com título; devolve (cartão, padding, topo do conteúdo). Feche com _fecha."""
    pd = _pad(dev)
    c = d.frame(f, f"Painel {titulo}"[:40], x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
    T(d, c, titulo, pd, pd - 2, size=15, weight=600, lh=22)
    if link: T(d, c, link, w - pd, pd, size=13, weight=600, color=C["pos"], align="right", lh=20)
    elif extra: T(d, c, extra, w - pd, pd + 1, size=12, color=C["muted"], align="right", lh=20)
    return c, pd, pd + 38

def _fecha(d, c, h):
    d.nodes[c]["height"] = float(h)
    return h

def _colunas(d, f, dev, x, y, cw, esq, dir_, ordem_mob=None, gap=16):
    """Duas colunas (60/40) no computador e no tablet; uma só no celular. Cada painel: fn(d, f, x, y, w, dev) -> altura."""
    if dev == "mobile":
        yy = y
        for fn in (ordem_mob or esq + dir_):
            yy += fn(d, f, x, yy, cw, dev) + 12
        return yy - 12
    lw = round((cw - gap) * 0.6); rw = cw - gap - lw
    ly = y
    for fn in esq: ly += fn(d, f, x, ly, lw, dev) + gap
    ry = y
    for fn in dir_: ry += fn(d, f, x + lw + gap, ry, rw, dev) + gap
    return max(ly, ry) - gap

def _kpis(d, f, dev, x, y, cw, items):
    """items: (rótulo, valor, nota, tom_nota, escuro, tom_valor). Celular: o 1º na largura toda, o resto em 2 colunas."""
    mob = dev == "mobile"
    pos = []
    if mob:
        pos.append((x, y, cw, 92))
        cy = y + 92 + 10; w2 = (cw - 10) / 2; rest = items[1:]
        for i in range(len(rest)):
            last_odd = i == len(rest) - 1 and len(rest) % 2 == 1
            pos.append((x + (i % 2) * (w2 + 10), cy + (i // 2) * 100, cw if last_odd else w2, 90))
        total = 92 + 10 + ((len(rest) + 1) // 2) * 100 - 10
    else:
        n = len(items); g = 16; w = (cw - g * (n - 1)) / n
        for i in range(n): pos.append((x + i * (w + g), y, w, 108))
        total = 108
    pd = 16 if mob else 18
    big = 20 if mob else 24
    if mob:  # altura pela nota (pode quebrar em 2 linhas no cartão estreito)
        alt = [pd + 20 + big + 10 + 16 * _nl((n or "").replace(" vs período anterior", " vs anterior"), 11, kw - 2 * pd, 600) + pd
               for (_, _, n, *_), (_, _, kw, _) in zip(items, pos)]
        hs = [alt[0]] + [max(alt[1 + (i // 2) * 2: 3 + (i // 2) * 2]) for i in range(len(items) - 1)]
        cy = y + hs[0] + 10; ny = []
        for i in range(len(items) - 1):
            ny.append(cy)
            if i % 2 == 1: cy += hs[1 + i] + 10
        if (len(items) - 1) % 2 == 1: cy += hs[-1] + 10
        pos = [(pos[0][0], y, pos[0][2], hs[0])] + [(px, ny[i], pw, hs[1 + i]) for i, (px, _, pw, _) in enumerate(pos[1:])]
        total = cy - 10 - y
    for (lab, val, nota, tn, dark, tv), (kx, ky, kw, kh) in zip(items, pos):
        c = d.frame(f, f"Indicador {lab}", kx, ky, kw, kh, fill=C["black"] if dark else C["card"],
                    stroke=None if dark else C["line"], stroke_opacity=0.08, radius=12)
        T(d, c, lab, pd, pd - 2, size=12, weight=500, color="#b9bbb4" if dark else C["text2"], lh=18)
        vc = {"neg": "#ff8a8c" if dark else C["neg"], "pos": C["pos"]}.get(tv, C["yellow"] if dark else C["ink"])
        T(d, c, val, pd, pd + 20, size=big, weight=700, color=vc, lh=big + 6)
        if nota:
            if mob: nota = nota.replace(" vs período anterior", " vs anterior")
            nc = {"up": "#5fd08f" if dark else C["pos"], "dn": "#ff8a8c" if dark else C["neg"]}.get(tn, "#b9bbb4" if dark else C["muted"])
            T(d, c, nota, pd, pd + 20 + big + 10, size=11 if mob else 12, weight=600 if tn else 400, color=nc, lh=16, w=kw - 2 * pd)
    return total + 16

def _barras(d, c, x, y, w, rows, pct=None, destaque=None):
    """Barras horizontais. rows: (rótulo, valor, fração 0..1). Tinta neutra; destaque=i pinta só essa em verde."""
    for i, (lab, val, fr) in enumerate(rows):
        vx = x + w - (40 if pct else 0)
        T(d, c, _corta(lab, 13, 400, w - (40 if pct else 0) - fc.text_width(brl(val), 13, 600) - 16), x, y, size=13, color=C["ink"], lh=20)
        T(d, c, brl(val), vx, y, size=13, weight=600, align="right", lh=20)
        if pct: T(d, c, f"{pct[i]}%", x + w, y + 1, size=12, color=C["muted"], align="right", lh=18)
        d.frame(c, "Trilho", x, y + 26, w, 6, fill=C["raised"], radius=3)
        d.frame(c, "Barra", x, y + 26, max(6, w * fr), 6, fill=C["green"] if i == destaque else C["ink"],
                fill_opacity=1.0 if i == destaque or destaque is None else 0.75, radius=3)
        y += 46
    return len(rows) * 46

def _pill(d, p, x, y, label, bg, fg, h=20):
    w = fc.text_width(label, 11, 600) + 16
    b = d.frame(p, f"Selo {label}", x, y, w, h, fill=bg, radius=h / 2)
    T(d, b, label, w / 2, (h - 16) / 2, size=11, weight=600, color=fg, align="center", lh=16)
    return w

def _evento(d, p, x, y, w, dia, ev, excluir=False):
    """Compromisso: hora, título, selo do tipo e dia · loja · responsável. Devolve a altura."""
    hora, tit, tipo, loja, quem = ev
    lab, bg, fg = EV[tipo]
    box = d.frame(p, f"Compromisso {tit}"[:40], x, y, w, 10, fill=C["page"], radius=10)
    T(d, box, hora or "Dia todo", 12, 12, size=13, weight=700, lh=20)
    tx = 72; tw = w - tx - (40 if excluir else 12)
    nl = _nl(tit, 13, tw, 600)
    T(d, box, tit, tx, 10, size=13, weight=600, lh=20, w=tw)
    yy = 10 + 20 * nl + 4
    pw = _pill(d, box, tx, yy, lab, bg, fg)
    meta = f"{SEMANA[(dia - 1) % 7]}, {dia:02d}/11 · {loja} · {quem}"
    if pw + 8 + fc.text_width(meta, 11) <= tw:
        T(d, box, meta, tx + pw + 8, yy + 2, size=11, color=C["muted"], lh=16)
        yy += 20
    else:
        T(d, box, meta, tx, yy + 24, size=11, color=C["muted"], lh=16, w=tw)
        yy += 24 + 16 * _nl(meta, 11, tw)
    h = yy + 12
    if excluir:
        ui.icon(d, box, "fechar", w - 28, 14, 14, C["muted"])
    return _fecha(d, box, h)


# ---------------------------------------------------------------- O01 entrar
def o01(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    d.nodes[f]["fills"] = [fc.paint(C["black"])]
    lw = 120 if mob else 140
    lh = lw * 286 / 325
    top = (H - (lh + 24 + 44 + 16 + 24 + 32 + 72 + 16 + 20 + 40 + 20)) / 2 - (20 if mob else 0)
    d.image(f, os.path.join(ui.HERE, "marca", "logo-branco.png"), (W - lw) / 2, top, lw, lh, name="Logo")
    y = top + lh + 24
    size = 36 if mob else 44
    ui.brush(d, f, W / 2, y, [("PAINEL DOS", "white"), ("DONOS", "green")], size=size, align="center")
    y += int(size * 1.1) + 12
    sw = min(440, W - 48)
    T(d, f, "Financeiro, pedidos, equipe e agenda das duas lojas", W / 2 - sw / 2, y, size=14, color="#c9cac4", align="center", lh=22, w=sw)
    y += 22 * _nl("Financeiro, pedidos, equipe e agenda das duas lojas", 14, sw) + 32
    bw, bh, g = (64, 72, 12) if mob else (60, 68, 12)
    x0 = (W - (4 * bw + 3 * g)) / 2
    for i in range(4):
        foc = i == 2
        b = d.frame(f, f"Dígito {i + 1} do PIN", x0 + i * (bw + g), y, bw, bh, fill="#1b1d1a",
                    stroke=C["green"] if foc else "#ffffff", stroke_opacity=1.0 if foc else 0.16, stroke_w=2 if foc else 1, radius=12)
        if i < 2: d.ellipse(b, bw / 2 - 6, bh / 2 - 6, 12, "#ffffff", name="Dígito digitado")
        if foc: d.frame(b, "Cursor", bw / 2 - 1, bh / 2 - 14, 2, 28, fill=C["green"])
    y += bh + 16
    T(d, f, "Digite o PIN de 4 números dos donos", W / 2, y, size=12, color="#8d8f87", align="center", lh=20)
    y += 20 + 36
    lab = "Voltar para a loja"
    tw = fc.text_width(lab, 13, 500)
    T(d, f, lab, W / 2, y, size=13, weight=500, color="#e7e7e2", align="center", lh=20)
    d.frame(f, "Sublinhado", W / 2 - tw / 2, y + 21, tw, 1, fill="#e7e7e2", fill_opacity=0.6)
    return H


# ---------------------------------------------------------------- O02 visão geral
def _p_fat(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Faturamento por dia")
    mob = dev == "mobile"
    leg = [("Loja PNZ", C["green"]), ("Loja LEM", C["yellow"])]  # as duas séries de hoje (STORE_COLOR)
    if mob:
        lx = pd
        for lab, col in leg:
            d.frame(c, "Legenda", lx, yy + 8, 16, 4, fill=col, radius=2)
            T(d, c, lab, lx + 22, yy + 1, size=12, weight=600, color=C["text2"], lh=18)
            lx += 22 + fc.text_width(lab, 12, 600) + 20
        yy += 30
    else:
        lx = w - pd
        for lab, col in reversed(leg):
            lx -= fc.text_width(lab, 12, 600)
            T(d, c, lab, lx, pd + 1, size=12, weight=600, color=C["text2"], lh=18)
            d.frame(c, "Legenda", lx - 22, pd + 8, 16, 4, fill=col, radius=2)
            lx -= 22 + 20
    ch = {"desktop": 220, "tablet": 210, "mobile": 170}[dev]
    x0, x1 = pd + 36, w - pd - 4
    y0, y1 = yy + 8, yy + ch - 24
    top = 1000
    for v in (0, 250, 500, 750, 1000):
        gy = y1 - v / top * (y1 - y0)
        hair(d, c, x0, gy, x1 - x0)
        T(d, c, "1 mil" if v == 1000 else str(v), x0 - 8, gy - 8, size=10, color=C["muted"], align="right", lh=16)
    n = len(PNZ)
    X = lambda i: x0 + i * (x1 - x0) / (n - 1)
    Y = lambda v: y1 - min(v, top) / top * (y1 - y0)
    for nome, serie, col in (("Loja LEM", LEM, C["yellow"]), ("Loja PNZ", PNZ, C["green"])):
        d.polyline(c, [(X(i), Y(v)) for i, v in enumerate(serie)], col, weight=2.5, name=nome)
        r = 5 if not mob else 4
        for i, v in enumerate(serie):
            d.ellipse(c, X(i) - r / 2, Y(v) - r / 2, r, col, name=f"{nome} {i + 1}/11")
    step = 6 if mob else 4
    for i in range(0, n, step):
        T(d, c, f"{i + 1}/11", X(i), y1 + 6, size=10, color=C["muted"], align="center", lh=16)
    return _fecha(d, c, yy + ch + pd - 4)

def _p_lojas(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Comparativo das lojas")
    g = 12; bw = (w - 2 * pd - g) / 2
    hh = 0
    for i, (lj, v, sub, fr) in enumerate([("Loja PNZ", 4384.15, "34 pedidos · ticket R$ 128,95", "68% do total"),
                                          ("Loja LEM", 2042.15, "17 pedidos · ticket R$ 120,13", "32% do total")]):
        nl = _nl(sub, 12, bw - 28)
        h = 16 + 18 + 4 + 28 + 6 + 18 * nl + 2 + 18 + 14
        b = d.frame(c, lj, pd + i * (bw + g), yy, bw, h, fill=C["page"], radius=10)
        T(d, b, lj, 14, 14, size=12, weight=600, color=C["text2"], lh=18)
        T(d, b, brl(v), 14, 36, size=20 if dev == "mobile" else 22, weight=700, lh=28)
        T(d, b, sub, 14, 70, size=12, color=C["muted"], lh=18, w=bw - 28)
        T(d, b, fr, 14, 72 + 18 * nl, size=12, weight=600, color=C["text2"], lh=18)
        hh = max(hh, h)
    return _fecha(d, c, yy + hh + pd)

def _p_top(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Mais vendidos no período")
    rows = [("Caixa c/50 Seda Zomo KS Brown", 1080), ("Caixa c/25 Seda Zomo Monster KS", 550), ("Caixa c/50 Seda Zomo KS Branca", 500),
            ("Bandeja Raw média", 483), ("OCB King Size Slim Ultimate", 310), ("Kit presente Smoke House", 297)]
    if dev == "mobile": rows = rows[:5]
    h = _barras(d, c, pd, yy, w - 2 * pd, [(a, v, v / 1080) for a, v in rows])
    return _fecha(d, c, yy + h + pd - 12)

def _p_pag(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Formas de pagamento", extra="51 pedidos")
    rows = [("Débito", 1865.00, 29), ("Crédito", 1481.00, 23), ("Dinheiro", 1418.00, 22), ("Pix", 1379.30, 21), ("Carteira digital", 283.00, 4)]
    h = _barras(d, c, pd, yy, w - 2 * pd, [(a, v, v / 1865) for a, v, _ in rows], pct=[p for *_, p in rows])
    return _fecha(d, c, yy + h + pd - 12)

def _p_canal(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Canal de venda")
    iw = w - 2 * pd
    a = 0.69
    d.frame(c, "Site e link", pd, yy, iw * a - 2, 12, fill=C["ink"], radius=[6, 0, 0, 6])
    d.frame(c, "Balcão", pd + iw * a + 2, yy, iw * (1 - a) - 2, 12, fill=C["ink"], fill_opacity=0.25, radius=[0, 6, 6, 0])
    yy += 24
    for i, (lab, v, p, op) in enumerate([("Site e link", 4412.40, "69%", 1.0), ("Balcão", 2013.90, "31%", 0.25)]):
        d.frame(c, "Cor", pd, yy + 5, 10, 10, fill=C["ink"], fill_opacity=op, radius=3)
        T(d, c, lab, pd + 18, yy, size=13, lh=20)
        T(d, c, brl(v), w - pd - 44, yy, size=13, weight=600, align="right", lh=20)
        T(d, c, p, w - pd, yy + 1, size=12, color=C["muted"], align="right", lh=18)
        yy += 28
    return _fecha(d, c, yy + pd - 8)

def _p_prox(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Próximos compromissos", link="Abrir agenda")
    for dia in (27, 30):
        for ev in EVENTOS[dia]:
            yy += _evento(d, c, pd, yy, w - 2 * pd, dia, ev) + 8
    return _fecha(d, c, yy + pd - 8)

def _p_estoque(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Estoque baixo", extra="20 itens")
    rows = [("Isqueiro Zippo Clássico", "PNZ", 0), ("Vinho tinto seco 750 ml", "PNZ", 0), ("Seda Aleda KS Clássica Vermelha", "LEM", 0),
            ("Seda Raw KS Slim Organic Hemp", "LEM", 2), ("Pomada cicatrizante 50 g", "LEM", 3)]
    iw = w - 2 * pd
    for i, (n, lj, q) in enumerate(rows):
        T(d, c, _corta(n, 13, 600, iw - 100), pd, yy, size=13, weight=600, lh=20)
        T(d, c, "Loja " + lj, pd, yy + 20, size=11, color=C["muted"], lh=16)
        lab = "Esgotado" if not q else f"{q} un."
        pw = fc.text_width(lab, 11, 600) + 16
        _pill(d, c, w - pd - pw, yy + 8, lab, "#fbe4e4" if not q else "#fbefc9", "#a8262a" if not q else "#7a5800", h=22)
        yy += 44
        if i < len(rows) - 1: hair(d, c, pd, yy - 6, iw)
    ui.button(d, c, pd, yy + 4, "Ver os 20 itens no estoque", app="donos", kind="secondary", w=iw, h=40)
    return _fecha(d, c, yy + 44 + pd)

def o02(d, f, dev, app):
    total = {"desktop": 1900, "tablet": 1900, "mobile": 3200}[dev]
    _shell(d, f, dev, "Visão geral", total)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("VISÃO", "ink"), ("GERAL", "green")], "Duas lojas · este mês")
    y += _filtros(d, f, dev, x, y, cw)
    y += _kpis(d, f, dev, x, y, cw, [
        ("Faturamento", "R$ 6.426,30", "+83% vs período anterior", "up", True, None),
        ("Pedidos", "51", "+132% vs período anterior", "up", False, None),
        ("Ticket médio", "R$ 126,01", "-21% vs período anterior", "dn", False, None),
        ("Em andamento agora", "9", "3 novos sem confirmação", None, False, None),
        ("Comissões a pagar", "R$ 96,28", "5% sobre concluídos", None, False, None)])
    y = _colunas(d, f, dev, x, y, cw, [_p_fat, _p_lojas, _p_top], [_p_pag, _p_canal, _p_prox, _p_estoque],
                 ordem_mob=[_p_fat, _p_lojas, _p_prox, _p_estoque, _p_top, _p_pag, _p_canal])
    total = y + (40 if dev != "mobile" else 24 + 64)
    return _fim(d, f, dev, "Visão geral", total)


# ---------------------------------------------------------------- O03 financeiro
DRE = [("Vendas brutas", "51 pedidos", "R$ 6.386,00", ""), ("(-) Descontos", "3 por 2 e Pix", "-R$ 70,70", "neg"),
       ("Receita líquida de produtos", None, "R$ 6.315,30", "sub"),
       ("(-) Custo dos produtos", "estimado com margem de 45%", "-R$ 3.473,42", "neg"),
       ("Lucro bruto", None, "R$ 2.841,88", "sub"), ("(+) Taxas de entrega", None, "R$ 111,00", ""),
       ("(-) Comissões da equipe", "5%", "-R$ 321,32", "neg"), ("(-) Despesas", "9 lançamentos", "-R$ 13.201,00", "neg"),
       ("Resultado", None, "-R$ 10.569,43", "res")]
CONTAS = [("Aluguel da loja", "Aluguel · Loja PNZ · vence 10/11", 3500, 15), ("Aluguel da loja", "Aluguel · Loja LEM · vence 10/11", 3200, 15),
          ("Reposição de sedas (distribuidor)", "Fornecedor · Loja PNZ · vence 10/11", 2150, 15),
          ("Reposição Tattoo Supply", "Fornecedor · Loja LEM · vence 12/11", 1780, 13),
          ("Energia", "Energia · Loja PNZ · vence 15/11", 640, 10), ("Energia", "Energia · Loja LEM · vence 15/11", 580, 10),
          ("Internet e sistema", "Internet · Loja PNZ · vence 20/11", 189, 5), ("Tráfego pago (Meta Ads)", "Marketing · Loja PNZ · vence hoje", 1076, 0)]

def _p_dre(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Demonstrativo do período")
    iw = w - 2 * pd
    for i, (lab, small, val, k) in enumerate(DRE):
        wt = 600 if k in ("sub", "res") else 400
        col = C["neg"] if k == "neg" else C["ink"]
        vw = fc.text_width(val, 13, 600) + 16
        duas = small and fc.text_width(lab, 13, wt) + 6 + fc.text_width(small, 11) > iw - vw - 8
        rh = 52 if duas else 40
        if k == "sub": d.frame(c, "Subtotal", pd, yy, iw, rh, fill=C["page"], radius=6)
        if k == "res":
            hair(d, c, pd, yy, iw)
        lx = pd + 8
        ly = yy + (8 if duas else 10)
        T(d, c, lab, lx, ly, size=15 if k == "res" else 13, weight=wt, color=col, lh=20)
        if small:
            if duas: T(d, c, small, lx, ly + 20, size=11, color=C["muted"], lh=16)
            else: T(d, c, small, lx + fc.text_width(lab, 13, wt) + 6, ly + 2, size=11, color=C["muted"], lh=16)
        vc = C["neg"] if (k == "neg" or (k == "res" and val.startswith("-"))) else C["ink"]
        T(d, c, val, pd + iw - 8, yy + (rh - 20) / 2, size=15 if k == "res" else 13, weight=700 if k == "res" else 600, color=vc, align="right", lh=20)
        yy += rh
        if k not in ("sub", "res") and i + 1 < len(DRE) and DRE[i + 1][3] not in ("sub", "res"): hair(d, c, pd, yy, iw)
    nota = "O custo dos produtos é estimado pela margem definida em Ajustes. Com o custo real de cada item cadastrado, o cálculo fica exato"
    T(d, c, nota, pd, yy + 12, size=12, color=C["muted"], lh=18, w=iw)
    yy += 12 + 18 * _nl(nota, 12, iw)
    return _fecha(d, c, yy + pd)

def _p_despesa(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Lançar despesa")
    iw = w - 2 * pd; g = 12
    h = 44 if dev != "desktop" else 40
    if dev == "mobile":
        ui.field(d, c, pd, yy, iw, label="Descrição", placeholder="Ex.: conta de energia", h=h, app="donos"); yy += 20 + h + 12
        hw = (iw - g) / 2
        ui.field(d, c, pd, yy, hw, label="Categoria", value="Energia", chevron=True, h=h, app="donos")
        ui.field(d, c, pd + hw + g, yy, hw, label="Loja", value="PNZ", chevron=True, h=h, app="donos"); yy += 20 + h + 12
        ui.field(d, c, pd, yy, hw, label="Valor (R$)", placeholder="0,00", h=h, app="donos")
        ui.field(d, c, pd + hw + g, yy, hw, label="Vencimento", value="25/11/2026", h=h, app="donos"); yy += 20 + h + 16
        ui.button(d, c, pd, yy, "Lançar despesa", app="donos", kind="primary", w=iw, h=44); yy += 44
    else:
        dw = iw * 0.62
        ui.field(d, c, pd, yy, dw, label="Descrição", placeholder="Ex.: conta de energia", h=h, app="donos")
        ui.field(d, c, pd + dw + g, yy, iw - dw - g, label="Categoria", value="Energia", chevron=True, h=h, app="donos")
        yy += 20 + h + 12
        bw = 120
        cw3 = (iw - bw - 3 * g) / 3
        ui.field(d, c, pd, yy, cw3, label="Loja", value="PNZ", chevron=True, h=h, app="donos")
        ui.field(d, c, pd + cw3 + g, yy, cw3, label="Valor (R$)", placeholder="0,00", h=h, app="donos")
        ui.field(d, c, pd + 2 * (cw3 + g), yy, cw3, label="Vencimento", value="25/11/2026", h=h, app="donos")
        ui.button(d, c, pd + iw - bw, yy + 20, "Lançar", app="donos", kind="primary", w=bw, h=h)
        yy += 20 + h
    return _fecha(d, c, yy + pd)

def _p_contas(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Contas a pagar", extra="R$ 13.115,00 em 8 contas")
    iw = w - 2 * pd
    rows = CONTAS[:4] if dev == "mobile" else CONTAS
    for tit, sub, v, atraso in rows:
        tw = iw - 24 - 96
        nl = _nl(tit, 13, tw, 600)
        sl = _nl(sub, 11, tw)
        h = max(12 + 20 * nl + 16 * sl + (18 if atraso else 0) + 12, 84)
        b = d.frame(c, f"Conta {tit}"[:40], pd, yy, iw, h, fill=C["page"], radius=10)
        T(d, b, tit, 12, 12, size=13, weight=600, lh=20, w=tw)
        T(d, b, sub, 12, 12 + 20 * nl, size=11, color=C["muted"], lh=16, w=tw)
        if atraso: T(d, b, f"Atrasada há {atraso} dias", 12, 14 + 20 * nl + 16 * sl, size=11, weight=600, color=C["neg"], lh=16)
        T(d, b, brl(v), iw - 12, 12, size=13, weight=700, align="right", lh=20)
        ui.button(d, b, iw - 12 - 80, 40, "Pagar", app="donos", kind="dark", w=80, h=32 if dev == "desktop" else 36)
        yy += h + 8
    if dev == "mobile":
        ui.button(d, c, pd, yy, "Ver as 8 contas", app="donos", kind="secondary", w=iw, h=44); yy += 52
    return _fecha(d, c, yy + pd - 8)

def _p_cat(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Despesas por categoria", extra="R$ 13.201,00")
    rows = [("Aluguel", 6700), ("Fornecedor", 3930), ("Energia", 1220), ("Marketing", 1076), ("Internet", 189), ("Manutenção", 86)]
    h = _barras(d, c, pd, yy, w - 2 * pd, [(a, v, v / 6700) for a, v in rows], destaque=0)
    return _fecha(d, c, yy + h + pd - 12)

def _p_receb(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Recebimentos por forma", extra="42 concluídos")
    rows = [("Débito", 1467.00, 28), ("Pix", 1293.80, 25), ("Crédito", 1131.00, 22), ("Dinheiro", 1062.00, 20), ("Carteira digital", 283.00, 5)]
    h = _barras(d, c, pd, yy, w - 2 * pd, [(a, v, v / 1467) for a, v, _ in rows], pct=[p for *_, p in rows])
    return _fecha(d, c, yy + h + pd - 12)

def o03(d, f, dev, app):
    total = {"desktop": 1900, "tablet": 1900, "mobile": 3200}[dev]
    _shell(d, f, dev, "Financeiro", total)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("FINANCEIRO", "ink")], "Duas lojas · este mês")
    y += _filtros(d, f, dev, x, y, cw)
    y += _kpis(d, f, dev, x, y, cw, [
        ("Resultado estimado", "-R$ 10.569,43", "depois de custos, comissões e despesas", None, True, "neg"),
        ("Entradas (concluídos)", "R$ 5.236,80", "42 pedidos recebidos", None, False, None),
        ("Saídas pagas", "R$ 86,00", "despesas e comissões pagas", None, False, None),
        ("Saldo de caixa", "R$ 5.150,80", "entradas menos saídas", None, False, "pos")])
    y = _colunas(d, f, dev, x, y, cw, [_p_cat, _p_dre, _p_despesa], [_p_contas, _p_receb],
                 ordem_mob=[_p_cat, _p_contas, _p_dre, _p_receb, _p_despesa])
    total = y + (40 if dev != "mobile" else 24 + 64)
    return _fim(d, f, dev, "Financeiro", total)


# ---------------------------------------------------------------- O04 pedidos
def o04(d, f, dev, app, vista=False):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    n = {"desktop": 14, "tablet": 13, "mobile": 9}[dev]
    total = H if vista else {"desktop": 1200, "tablet": 1250, "mobile": 1500}[dev]
    _shell(d, f, dev, "Pedidos", total)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("PEDIDOS", "ink")], "54 pedidos · R$ 6.426,30 em vendas")
    y += _filtros(d, f, dev, x, y, cw)
    h = 40 if dev == "desktop" else 44
    if mob:
        ui.field(d, f, x, y, cw, placeholder="Número, cliente, produto ou colaborador", prefix_icon="busca", h=h, app="donos"); y += h + 8
        hw = (cw - 8) / 2
        ui.field(d, f, x, y, hw, value="Todos os status", chevron=True, h=h, app="donos")
        ui.field(d, f, x + hw + 8, y, hw, value="Todos os colab.", chevron=True, h=h, app="donos"); y += h + 16
        y += _cartoes_pedidos(d, f, x, y, cw, PEDIDOS[:n]) + 12
        ui.button(d, f, x, y, "Carregar mais pedidos", app="donos", kind="secondary", w=cw, h=44); y += 44
    else:
        s1, s2 = (200, 240) if dev == "desktop" else (190, 220)
        ui.field(d, f, x, y, cw - s1 - s2 - 16, placeholder="Buscar por número, cliente, produto ou colaborador", prefix_icon="busca", h=h, app="donos")
        ui.field(d, f, x + cw - s1 - s2 - 8, y, s1, value="Todos os status", chevron=True, h=h, app="donos")
        ui.field(d, f, x + cw - s2, y, s2, value="Todos os colaboradores", chevron=True, h=h, app="donos")
        y += h + 16
        if dev == "desktop":
            cols = [("Pedido", 120, "l", False), ("Data", 130, "l", False), ("Loja", 64, "l", False), ("Cliente", None, "l", False),
                    ("Colaborador", 140, "l", False), ("Canal", 90, "l", False), ("Total", 110, "r", False), ("Status", 150, "l", False)]
        else:
            cols = [("Pedido", 116, "l", False), ("Data", 128, "l", False), ("Cliente", None, "l", False),
                    ("Colaborador", 140, "l", False), ("Canal", 84, "l", False), ("Total", 110, "r", False), ("Status", 140, "l", False)]
        rows = []
        for num, qd, lj, cli, sel, canal, tot, st in PEDIDOS[:n]:
            r = [(num, "b"), qd] + ([lj] if dev == "desktop" else []) + [cli, sel or ("Sem atendente", "neg"), canal, (brl(tot), "b"), (st, ST_TOM[st])]
            rows.append(r)
        t, th = ui.table(d, f, x, y, cw, cols, rows, row_h=44 if dev == "desktop" else 48, app="donos", selected=0 if vista else None)
        y += th + 16
        T(d, f, f"Mostrando {n} de 54 pedidos", x, y + 10, size=13, color=C["text2"], lh=20)
        b, bw = ui.button(d, f, 0, y, "Carregar mais", app="donos", kind="secondary", h=h)
        d.nodes[b]["transform"][4] = float(x + cw - bw)
        y += h
    if not vista:
        total = y + (40 if not mob else 24 + 64)
    return _fim(d, f, dev, "Pedidos", total)


def _cartoes_pedidos(d, f, x, y, w, pedidos):
    """Celular: a tabela de pedidos vira lista de cartões (número e cliente, total, quando, colaborador, situação)."""
    c = d.frame(f, "Lista de pedidos", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12, clip=True)
    yy = 0
    for i, (num, qd, lj, cli, sel, canal, tot, st) in enumerate(pedidos):
        T(d, c, num, 16, yy + 12, size=14, weight=700, lh=20)
        T(d, c, cli, 16 + fc.text_width(num, 14, 700) + 8, yy + 12, size=14, color=C["text2"], lh=20)
        T(d, c, brl(tot), w - 16, yy + 12, size=14, weight=700, align="right", lh=20)
        T(d, c, f"{qd} · {canal}", 16, yy + 36, size=12, color=C["muted"], lh=16)
        sx = 16 + fc.text_width(f"{qd} · {canal} · ", 12)
        T(d, c, "· " + (sel or "Sem atendente"), sx - fc.text_width("· ", 12), yy + 36, size=12,
          weight=600 if not sel else 400, color=C["neg"] if not sel else C["muted"], lh=16)
        ui.status(d, c, w - 16, yy + 34, st, ST_TOM[st], align="right")
        yy += 66
        if i < len(pedidos) - 1: hair(d, c, 16, yy, w - 32)
    return _fecha(d, c, yy + 2)


# ---------------------------------------------------------------- O05 pedido aberto
def o05(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    o04(d, f, dev, app, vista=True)
    itens = [("3× Seda Smoking King Size Deluxe", 24.00), ("2× Bandeja Raw média", 138.00), ("5× Seda Raw King Size Classic", 50.00)]
    meta = [("Cliente", "Mariana Lima\n(87) 98812-4410"), ("Retirada na loja", "O quanto antes"),
            ("Pagamento", "Cartão de crédito"), ("Comissão de Carla", "R$ 10,60 · prevista")]
    ww = W if mob else 560
    hh = 64 + 20 + 20 + 16 + len(itens) * 28 + 12 + 28 + 20 + 2 * 72 + 4 + 20 + 44 + 24 + 72
    win, ww, hh, top, bot = ui.window(d, f, dev, "Pedido PNZ-1001", ww, hh, app="donos",
                                      footer_buttons=[("Fechar", "secondary", None), ("Falar com o cliente", "dark", None)], close=not mob)
    pd = 24
    iw = ww - 2 * pd
    y = top + 20
    sw = ui.status(d, win, pd, y, "Novo", "warn")
    T(d, win, "hoje, 16:24 · Loja PNZ · Site", pd + sw + 12, y, size=13, color=C["muted"], lh=20)
    y += 36
    for lab, v in itens:
        T(d, win, lab, pd, y, size=13, lh=20)
        T(d, win, brl(v), pd + iw, y, size=13, align="right", lh=20)
        y += 28
    hair(d, win, pd, y, iw); y += 12
    T(d, win, "Total", pd, y, size=15, weight=700, lh=22)
    T(d, win, "R$ 212,00", pd + iw, y, size=15, weight=700, align="right", lh=22)
    y += 22 + 20
    cw2 = (iw - 16) / 2
    for i, (k, v) in enumerate(meta):
        mx = pd + (i % 2) * (cw2 + 16); my = y + (i // 2) * 72
        T(d, win, k, mx, my, size=12, weight=600, color=C["muted"], lh=16)
        T(d, win, v, mx, my + 18, size=13, lh=20, w=cw2)
    y += 2 * 72 + 4
    ui.field(d, win, pd, y, iw, label="Colaborador responsável", value="Carla", chevron=True, h=44, app="donos")
    return H


# ---------------------------------------------------------------- O06 equipe
EQUIPE = [  # nome, loja, cor do avatar, vendas, pedidos, ticket, % meta, vendido no mês, comissão, n concluídos, já pago, tarefas
    ("João", "PNZ", C["yellow"], "R$ 2.547,40", "18", "R$ 141,52", 100, "R$ 2.547,40", "R$ 29,57", 4, "R$ 111,70",
     [("Receber o distribuidor de sedas e conferir a nota", False)]),
    ("Bia", "LEM", "#c8243b", "R$ 2.042,15", "17", "R$ 120,13", 82, "R$ 2.042,15", "R$ 28,70", 4, "R$ 122,64",
     [("Fotografar a seleção de vinhos para o site", False)]),
    ("Carla", "PNZ", C["green"], "R$ 1.836,75", "16", "R$ 114,80", 73, "R$ 1.836,75", "R$ 38,01", 6, "R$ 106,60",
     [("Conferir validade das pomadas Tattoo Supply", False), ("Repor vitrine de isqueiros", True)]),
]

def _membro(d, f, x, y, w, dev, i, m):
    nome, lj, cor, vend, ped, tk, pct, mes, com, nc, pago, tarefas = m
    pd = _pad(dev)
    c = d.frame(f, f"Colaborador {nome}", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
    iw = w - 2 * pd
    av = d.frame(c, "Inicial", pd, pd, 44, 44, fill=cor, radius=22)
    T(d, av, nome[0], 22, 11, size=16, weight=700, color=C["ink"] if cor == C["yellow"] else "#ffffff", align="center", lh=22)
    T(d, c, nome, pd + 56, pd + 2, size=16, weight=600, lh=22)
    T(d, c, f"Loja {lj} · PIN 1234", pd + 56, pd + 24, size=12, color=C["muted"], lh=18)
    T(d, c, f"{i + 1}º", w - pd, pd + 6, size=20, weight=700, color=C["pos"] if i == 0 else C["muted"], align="right", lh=28)
    yy = pd + 44 + 16
    g = 8; mw = (iw - 2 * g) / 3
    for j, (k, v) in enumerate([("Vendas", vend), ("Pedidos", ped), ("Ticket", tk)]):
        b = d.frame(c, k, pd + j * (mw + g), yy, mw, 58, fill=C["page"], radius=8)
        T(d, b, k, 10, 8, size=11, color=C["muted"], lh=16)
        T(d, b, v, 10, 26, size=14, weight=700, lh=22)
    yy += 58 + 16
    T(d, c, f"Meta do mês · {pct}%", pd, yy, size=12, weight=600, lh=18)
    T(d, c, f"{mes} de R$ 2.500,00", w - pd, yy, size=12, color=C["muted"], align="right", lh=18)
    yy += 24
    d.frame(c, "Trilho da meta", pd, yy, iw, 8, fill=C["raised"], radius=4)
    d.frame(c, "Meta", pd, yy, iw * pct / 100, 8, fill=C["green"], radius=4)
    yy += 8 + 16
    fh = 40 if dev == "desktop" else 44
    T(d, c, "Meta mensal (R$)", pd, yy + (fh - 20) / 2, size=13, color=C["text2"], lh=20)
    ui.field(d, c, w - pd - 120, yy, 120, value="2.500", h=fh, app="donos")
    yy += fh + 16
    tw = iw - 24 - 88
    s1 = f"Comissão a pagar: {com}"; s2 = f"{nc} concluídos · já pago {pago}"
    n1, n2 = _nl(s1, 13, tw, 700), _nl(s2, 11, tw)
    bh_ = max(64, 12 + 20 * n1 + 2 + 16 * n2 + 12)
    cb = d.frame(c, "Comissão", pd, yy, iw, bh_, fill=C["page"], radius=10)
    T(d, cb, s1, 12, 12, size=13, weight=700, lh=20, w=tw)
    T(d, cb, s2, 12, 14 + 20 * n1, size=11, color=C["muted"], lh=16, w=tw)
    b, _ = ui.button(d, cb, iw - 12 - 76, (bh_ - 36) / 2, "Pagar", app="donos", kind="primary", w=76, h=36)
    d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
    for ch in d.nodes[b]["children"]:
        if d.nodes[ch]["type"] == "text": d.nodes[ch]["fills"] = [fc.paint(C["ink"])]
    yy += bh_ + 18
    T(d, c, "Tarefas", pd, yy, size=13, weight=700, lh=20)
    yy += 28
    for txt, ok in tarefas:
        tw = iw - 40 - 36
        nl = _nl(txt, 13, tw)
        th = max(44, 12 + 20 * nl + 12)
        tb = d.frame(c, f"Tarefa {txt}"[:40], pd, yy, iw, th, fill=C["page"], radius=8)
        ui.checkbox(d, tb, 12, (th - 18) / 2, on=ok, app="donos")
        T(d, tb, txt, 40, 12, size=13, color=C["muted"] if ok else C["ink"], lh=20, w=tw)
        ui.icon(d, tb, "fechar", iw - 26, (th - 12) / 2, 12, C["muted"])
        yy += th + 8
    bw = 104
    ui.field(d, c, pd, yy, iw - bw - 8, placeholder=f"Nova tarefa para {nome}", h=fh, app="donos")
    ui.button(d, c, pd + iw - bw, yy, "Adicionar", app="donos", kind="dark", w=bw, h=fh)
    yy += fh + pd
    return c, _fecha(d, c, yy)

def o06(d, f, dev, app):
    total = {"desktop": 1100, "tablet": 1080, "mobile": 2400}[dev]
    _shell(d, f, dev, "Equipe", total)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("EQUIPE", "ink")],
                "Desempenho, meta, comissão e tarefas de cada colaborador. As tarefas aparecem na área de cada um",
                acao=("Novo colaborador", "mais"))
    y += _filtros(d, f, dev, x, y, cw)
    if dev == "mobile":
        for i, m in enumerate(EQUIPE):
            _, h = _membro(d, f, x, y, cw, dev, i, m); y += h + 12
        y -= 12
    else:
        g = 16; w = (cw - 2 * g) / 3
        cards = [_membro(d, f, x + i * (w + g), y, w, dev, i, m) for i, m in enumerate(EQUIPE)]
        hm = max(h for _, h in cards)
        for c, _ in cards: d.nodes[c]["height"] = float(hm)
        y += hm
    total = y + (40 if dev != "mobile" else 24 + 64)
    return _fim(d, f, dev, "Equipe", total)


# ---------------------------------------------------------------- O07 agenda
def _p_cal(d, f, x, y, w, dev):
    mob = dev == "mobile"
    pd = _pad(dev)
    c = d.frame(f, "Calendário", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
    ui.brush(d, c, pd, pd, [("NOVEMBRO DE", "ink"), ("2026", "green")], size=26 if mob else 30)
    bh = 36 if dev == "desktop" else 40
    bx = w - pd
    by = pd + 40 if mob else pd - 2
    for lab in ("seta-dir", "Hoje", "seta-esq"):
        bw = bh if lab.startswith("seta") else 64
        bx -= bw
        b = d.frame(c, f"Botão {lab}", bx, by, bw, bh, fill=C["card"], stroke=C["line"], stroke_opacity=0.16, radius=bh / 2)
        if lab.startswith("seta"): ui.icon(d, b, lab, (bw - 16) / 2, (bh - 16) / 2, 16, C["ink"])
        else: T(d, b, lab, bw / 2, (bh - 20) / 2, size=13, weight=600, align="center", lh=20)
        bx -= 6
    yy = by + bh + 16
    g = 4 if mob else 6
    cwid = (w - 2 * pd - 6 * g) / 7
    for i, dn in enumerate(["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]):
        T(d, c, dn, pd + i * (cwid + g) + cwid / 2, yy, size=11, weight=600, color=C["muted"], align="center", lh=16)
    yy += 24
    chh = {"desktop": 84, "tablet": 80, "mobile": 52}[dev]
    for k in range(35):
        dia = k + 1
        fora = dia > 30
        num = dia - 30 if fora else dia
        cx = pd + (k % 7) * (cwid + g); cy = yy + (k // 7) * (chh + g)
        sel = dia == DIA_SEL; hoje = dia == HOJE
        cell = d.frame(c, f"Dia {num}", cx, cy, cwid, chh, fill=C["black"] if sel else C["card"],
                       stroke=C["green"] if hoje else C["line"], stroke_opacity=1.0 if hoje else (0.06 if fora else 0.12),
                       stroke_w=2 if hoje else 1, radius=8, clip=True)
        T(d, cell, str(num), 8, 6, size=12, weight=700, color="#ffffff" if sel else (C["muted"] if fora else C["ink"]),
          lh=18, opacity=0.5 if fora else 1.0)
        evs = [] if fora else EVENTOS.get(dia, [])
        if mob:
            for j, ev in enumerate(evs[:3]):
                d.ellipse(cell, 8 + j * 10, chh - 14, 7, EV[ev[2]][2], name=EV[ev[2]][0])
        else:
            for j, ev in enumerate(evs[:2]):
                _, bg, fg = EV[ev[2]]
                b = d.frame(cell, ev[1][:30], 4, 28 + j * 24, cwid - 8, 20, fill=bg, radius=4)
                txt = (ev[0] + " " if ev[0] else "") + ev[1]
                T(d, b, _corta(txt, 10, 600, cwid - 20), 6, 2, size=10, weight=600, color=fg, lh=16)
    yy += 5 * (chh + g) + 10
    lx, ly = pd, yy
    for k, (lab, bg, fg) in EV.items():
        lw = 18 + fc.text_width(lab, 11) + 16
        if lx + lw > w - pd: lx, ly = pd, ly + 22
        d.frame(c, "Cor", lx, ly + 3, 10, 10, fill=fg if mob else bg, stroke=fg, stroke_opacity=0.4, radius=3)
        T(d, c, lab, lx + 16, ly, size=11, color=C["text2"], lh=16)
        lx += lw
    return _fecha(d, c, ly + 16 + pd)

def _p_dia(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "segunda-feira, 30 de novembro")
    for ev in EVENTOS[DIA_SEL]:
        yy += _evento(d, c, pd, yy, w - 2 * pd, DIA_SEL, ev, excluir=True) + 8
    return _fecha(d, c, yy + pd - 8)

def _p_novo(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Novo compromisso")
    iw = w - 2 * pd; g = 12; hw = (iw - g) / 2
    h = 40 if dev == "desktop" else 44
    ui.field(d, c, pd, yy, iw, label="Título", placeholder="Ex.: captação de Reels", h=h, app="donos"); yy += 20 + h + 12
    ui.field(d, c, pd, yy, hw, label="Data", value="30/11/2026", h=h, app="donos")
    ui.field(d, c, pd + hw + g, yy, hw, label="Horário", placeholder="Opcional", h=h, app="donos"); yy += 20 + h + 12
    ui.field(d, c, pd, yy, hw, label="Tipo", value=_corta("Captação de conteúdo", 14, 400, hw - 48), chevron=True, h=h, app="donos")
    ui.field(d, c, pd + hw + g, yy, hw, label="Loja", value="Duas lojas", chevron=True, h=h, app="donos"); yy += 20 + h + 12
    ui.field(d, c, pd, yy, iw, label="Responsável", placeholder="Opcional", h=h, app="donos"); yy += 20 + h + 16
    if dev == "mobile": ui.button(d, c, pd, yy, "Agendar", app="donos", kind="primary", w=iw, h=44); yy += 44
    else: ui.button(d, c, pd, yy, "Agendar", app="donos", kind="primary", w=140, h=h); yy += h
    return _fecha(d, c, yy + pd)

def o07(d, f, dev, app):
    total = {"desktop": 1100, "tablet": 1500, "mobile": 2000}[dev]
    _shell(d, f, dev, "Agenda", total)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("AGENDA", "ink")], "Captações, fornecedores, reuniões, pagamentos e escala das lojas")
    y += _filtros(d, f, dev, x, y, cw, com_periodo=False)
    if dev == "tablet":
        y += _p_cal(d, f, x, y, cw, dev) + 16
        g = 16; hw = (cw - g) / 2
        y += max(_p_dia(d, f, x, y, hw, dev), _p_novo(d, f, x + hw + g, y, hw, dev))
    else:
        y = _colunas(d, f, dev, x, y, cw, [_p_cal], [_p_dia, _p_novo])
    total = y + (40 if dev != "mobile" else 24 + 64)
    return _fim(d, f, dev, "Agenda", total)


# ---------------------------------------------------------------- O08 ajustes
def _p_regras(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Comissão e custos")
    iw = w - 2 * pd
    h = 40 if dev == "desktop" else 44
    fw = 112
    for lab, v, suf, ro in [("Comissão dos colaboradores", "5", "%", False), ("Margem bruta média estimada", "45", "%", False),
                            ("Estoque mínimo para alerta", "5", "un.", True)]:
        T(d, c, lab, pd, yy + (h - 20) / 2, size=14, lh=20, w=iw - fw - 12)
        ui.field(d, c, pd + iw - fw, yy, fw, value=v, suffix=suf, readonly=ro, h=h, app="donos")
        yy += h + 12
    T(d, c, "A comissão vale para a área do colaborador; a margem estima o custo no Financeiro", pd, yy, size=12, color=C["muted"], lh=18, w=iw)
    yy += 18 * _nl("A comissão vale para a área do colaborador; a margem estima o custo no Financeiro", 12, iw) + 16
    if dev == "mobile": ui.button(d, c, pd, yy, "Salvar ajustes", app="donos", kind="primary", w=iw, h=44); yy += 44
    else: ui.button(d, c, pd, yy, "Salvar ajustes", app="donos", kind="primary", w=160, h=h); yy += h
    return _fecha(d, c, yy + pd)

def _p_dados(d, f, x, y, w, dev):
    c, pd, yy = _painel(d, f, x, y, w, dev, "Dados do protótipo")
    iw = w - 2 * pd
    txt = ("Neste protótipo, pedidos, estoque, despesas e agenda ficam salvos no navegador. No sistema final, tudo fica num banco "
           "de dados compartilhado entre donos e colaboradores, com acesso por login individual")
    nl = _nl(txt, 13, iw - 28)
    b = d.frame(c, "Nota", pd, yy, iw, 20 * nl + 28, fill="#fff3cf", radius=10)
    T(d, b, txt, 14, 14, size=13, color="#4a3a00", lh=20, w=iw - 28)
    yy += 20 * nl + 28 + 16
    h = 40 if dev == "desktop" else 44
    ui.button(d, c, pd, yy, "Restaurar dados de exemplo", app="donos", kind="danger", w=iw if dev == "mobile" else None, h=h)
    return _fecha(d, c, yy + h + pd)

def o08(d, f, dev, app):
    W, H = DEVICES[dev]
    _shell(d, f, dev, "Ajustes", H)
    x, cw = _wrap(dev)
    y = _titulo(d, f, dev, x, _inicio(dev), cw, [("AJUSTES", "ink")], "Regras que valem para o painel, para a área do colaborador e para a vitrine")
    y = _colunas(d, f, dev, x, y, cw, [_p_regras], [_p_dados])
    total = max(H, y + (40 if dev != "mobile" else 24 + 64))
    return _fim(d, f, dev, "Ajustes", total)


SCREENS = [
    ("O01", "Donos · entrar (PIN)", o01),
    ("O02", "Visão geral", o02),
    ("O03", "Financeiro", o03),
    ("O04", "Pedidos", o04),
    ("O05", "Pedido aberto", o05),
    ("O06", "Equipe", o06),
    ("O07", "Agenda", o07),
    ("O08", "Ajustes", o08),
]
