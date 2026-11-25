"""HOST (Retaguarda), parte B: contas a receber, formas de pagamento, configurações,
usuários, chamados, fornecedores, integrações, relatórios e fiscal (H13 a H25).

Regras da especificação v1.2.02 (seções Venda a prazo e contas a receber, Dar baixa,
Recibo, Desfazer baixa, Extrato e cobrança, Formas de pagamento, Configurações do caixa,
Usuários e permissões, Chamados, Fornecedores e integrações, Relatórios).

Exemplo de baixa usado em H14, H15 e H16 (cliente Rafael Coelho Nunes, hoje 24/11/2026):
  DAV 004517 · parcela 3 de 3 · venc. 18/10 · 37 dias · 110,00 + multa 2,20 + juros 1,36 = 113,56
  DAV 004702 · parcela 2 de 3 · venc. 06/11 · 18 dias · 200,00 + multa 4,00 + juros 1,20 = 205,20
  Devido 318,76; pago 300,00 (PIX 200,00 + Dinheiro 100,00). Primeiro multa e juros, depois o
  principal, da mais antiga para a mais nova: a 3 de 3 fica quitada (compra quitada) e a 2 de 3
  fica com R$ 18,76 em aberto.
"""
import fc, ui
from ui import C, T, brl, PAD, DEVICES, hair

PAGE = "03b · Retaguarda (HOST) · financeiro, cadastros, configurações e fiscal"
APP = "host"
ACC = ui.APPS["host"]["acc"]

def v(x):
    """Valor sem o R$ (tabelas)."""
    return brl(x)[3:]

# ---------- dados do exemplo ----------
CLI = ("Rafael Coelho Nunes", "(87) 99102-7754", "987.654.321-00")
PARC = [  # dav, compra, parcela, vencimento, atraso, valor, pago, multa, juros, total hoje, situação
    ("004517", "03/08/2026", "3 de 3", "18/10/2026", 37, 110.00, 0.0, 2.20, 1.36, 113.56, "Vencida"),
    ("004702", "06/09/2026", "2 de 3", "06/11/2026", 18, 200.00, 0.0, 4.00, 1.20, 205.20, "Vencida"),
    ("004702", "06/09/2026", "3 de 3", "06/12/2026", 0, 200.00, 0.0, 0.0, 0.0, 200.00, "Em aberto"),
    ("004988", "10/11/2026", "1 de 1", "10/12/2026", 0, 184.80, 0.0, 0.0, 0.0, 184.80, "Em aberto"),
]
DEVIDO, PAGO, RESTA = 318.76, 300.00, 18.76
SALDO_DEPOIS = 18.76 + 200.00 + 184.80   # 403,56
LIMITE, ABERTO, VENCIDO = 1000.00, 694.80, 310.00

def _cnpj(base12):
    """CNPJ com os dígitos verificadores conferidos (regra do cadastro)."""
    n = [int(c) for c in base12]
    for pesos in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        s = sum(a * b for a, b in zip(n, pesos)) % 11
        n.append(0 if s < 2 else 11 - s)
    s = "".join(map(str, n))
    return f"{s[:2]}.{s[2:5]}.{s[5:8]}/{s[8:12]}-{s[12:]}"

# ---------- ajudantes locais (sugestões para o ui.py) ----------
def _shell(d, f, dev, active, h=None):
    """host_shell que aceita tela mais alta (o menu lateral acompanha a altura)."""
    if h and h > DEVICES[dev][1]:
        d.nodes[f]["height"] = float(h)
    x, y, w, base = ui.host_shell(d, f, dev, active)
    H = d.nodes[f]["height"]
    return x, y, w, H - (PAD[dev] if dev == "mobile" else 24)

def _fit(d, f, dev, h):
    """Ajusta a altura da tela que rola e leva junto o menu lateral (loja e versão no pé)."""
    h = float(max(DEVICES[dev][1], h))
    d.nodes[f]["height"] = h
    for cid in d.nodes[f].get("children", []):
        n = d.nodes[cid]
        if n.get("name") == "Menu lateral":
            n["height"] = h - 56
            kids = n.get("children", [])
            texts = [k for k in kids if d.nodes[k]["type"] == "text"]
            for k in kids:
                if d.nodes[k].get("name") == "Divisa":
                    d.nodes[k]["height"] = h - 56
            if len(texts) >= 2:
                d.nodes[texts[-2]]["transform"][5] = h - 56 - 52
                d.nodes[texts[-1]]["transform"][5] = h - 56 - 32
    return h

def _crumb(d, p, x, y, label):
    """Volta para a tela anterior: seta, nome e Esc."""
    ui.icon(d, p, "seta-esq", x - 4, y + 2, 16, C["text2"])
    T(d, p, label, x + 16, y, size=13, color=C["text2"], lh=20)
    ui.keycap(d, p, x + 16 + fc.text_width(label, 13) + 8, y, "Esc")
    return 28

def _head(d, f, x, y, w, title, sub, actions, dev):
    """page_head + no celular uma linha de botões (o page_head do celular não desenha ações).
    actions: (rótulo, tipo, tecla, ícone[, rótulo curto no celular])."""
    hh = ui.page_head(d, f, x, y, w, title, sub, actions=[a[:4] for a in actions], app=APP, device=dev)
    if dev != "mobile" or not actions:
        return hh + 8
    y2 = y + hh + 4
    n = len(actions)
    bw = (w - 8 * (n - 1)) / n
    for i, a in enumerate(actions):
        lab = a[4] if len(a) > 4 else a[0]
        ui.button(d, f, x + i * (bw + 8), y2, lab, app=APP, kind=a[1], w=bw, icon_name=a[3] if n < 3 else None)
    return hh + 4 + 40 + 16

def _cols_x(cols, w):
    """Mesma conta de larguras do ui.table: devolve (x, largura) de cada coluna dentro da tabela."""
    fixed = sum(c[1] for c in cols if c[1])
    flex = [c for c in cols if not c[1]]
    rest = max(40, (w - 32 - fixed) / max(1, len(flex)))
    out, cx = [], 16
    for c in cols:
        cw = c[1] or rest
        out.append((cx, cw)); cx += cw
    return out

def _sec(d, p, x, y, w, h, title, action=None):
    """Cartão de seção com título (Configurações, Fiscal, Integrações)."""
    c = ui.card(d, p, x, y, w, h, title=title)
    return c

def _row_toggle(d, p, x, y, w, label, on, sub=None, lock=False):
    """Linha de configuração: rótulo à esquerda, chave à direita."""
    T(d, p, label, x, y, size=14, lh=20, w=w - 60)
    if lock:
        ui.icon(d, p, "cadeado", x + fc.text_width(label, 14) + 8, y + 2, 14, C["muted"])
    if sub:
        T(d, p, sub, x, y + 20, size=12, color=C["muted"], lh=16, w=w - 60)
    ui.toggle(d, p, x + w - 36, y, on=on, app=APP)
    return 44 if sub else 36

def _row_value(d, p, x, y, w, label, value, vw=None, suffix=None, focused=False, sub=None):
    vw = vw or (120 if w > 340 else 96)
    """Linha de configuração: rótulo à esquerda, campo curto à direita."""
    T(d, p, label, x, y + 10, size=14, lh=20, w=w - vw - 16)
    if sub:
        T(d, p, sub, x, y + 30, size=12, color=C["muted"], lh=16, w=w - vw - 16)
    ui.field(d, p, x + w - vw, y, vw, value=value, suffix=suffix, mono=True, app=APP, focused=focused)
    return 52 if not sub else 60

def _check_rows(d, p, x, y, w, rows, checked=(), selected=None, row_h=68):
    """Celular: lista de cartões de duas linhas com marcação à esquerda (parcelas)."""
    c = d.frame(p, "Lista", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CARD, clip=True)
    yy = 4
    for i, (title, sub, right, rsub, tone) in enumerate(rows):
        if i == selected:
            d.frame(c, "Linha selecionada", 4, yy, w - 8, row_h - 4, fill=C["sel"], stroke=C["ink"], radius=6)
        ui.checkbox(d, c, 14, yy + 12, on=i in checked, app=APP)
        T(d, c, title, 44, yy + 10, size=14, weight=500, lh=20)
        T(d, c, sub, 44, yy + 32, size=12, color=C["neg"] if tone == "neg" else C["muted"], lh=16)
        T(d, c, right, w - 16, yy + 10, size=14, weight=500, lh=20, align="right", mono=True)
        if rsub:
            ui.status(d, c, w - 16, yy + 30, rsub, tone or "muted", align="right")
        yy += row_h
        if i < len(rows) - 1 and i != selected and i + 1 != selected:
            hair(d, c, 16, yy - 2, w - 32)
    d.nodes[c]["height"] = float(yy + 4)
    return c, yy + 4

def _bar(d, f, x, y, w, left, total, label, dev):
    """Barra das parcelas marcadas: quantidade, total de hoje e o botão principal."""
    if dev == "mobile":
        W = DEVICES["mobile"][0]
        H = d.nodes[f]["height"]
        b = d.frame(f, "Barra das parcelas marcadas", 0, H - 88, W, 88, fill=C["card"])
        hair(d, b, 0, 0, W)
        T(d, b, left, 16, 14, size=12, color=C["muted"], lh=16)
        T(d, b, total, 16, 32, size=28, weight=500, lh=36)
        ui.button(d, b, W - 16 - 148, 22, label, app=APP, kind="primary", w=148, h=44)
        return 88
    b = d.frame(f, "Barra das parcelas marcadas", x, y, w, 64, fill=C["card"], stroke=C["ink"], stroke_opacity=0.24, radius=ui.R_CARD,
                shadow=ui.shadow(0.06, 8, 24))
    T(d, b, left, 20, 22, size=14, color=C["text2"], lh=20)
    tx = 20 + fc.text_width(left, 14) + 24
    T(d, b, "Total hoje", tx, 22, size=14, color=C["text2"], lh=20)
    T(d, b, total, tx + fc.text_width("Total hoje", 14) + 12, 18, size=20, weight=500, lh=28, mono=True)
    ui.button(d, b, w - 16 - 148, 12, label, app=APP, kind="primary", w=148, key="Enter")
    return 64

def _stats(d, f, x, y, w, items, dev, h=None):
    """Quadros de número. Celular: 2 por linha, número menor."""
    if dev == "mobile":
        cw = (w - 8) / 2
        for i, it in enumerate(items):
            lab, val, note, tone = (list(it) + [None, None])[:4]
            ui.stat(d, f, x + (i % 2) * (cw + 8), y + (i // 2) * 88, cw, lab, val, note=None, h=80, big=18, tone=tone)
        return ((len(items) + 1) // 2) * 88 - 8
    n = len(items)
    cw = (w - 16 * (n - 1)) / n
    hh = h or (104 if any(len(it) > 2 and it[2] for it in items) else 88)
    for i, it in enumerate(items):
        lab, val, note, tone = (list(it) + [None, None])[:4]
        ui.stat(d, f, x + i * (cw + 16), y, cw, lab, val, note=note, h=hh, big=28 if dev == "desktop" else 24, tone=tone)
    return hh

# ======================================================================
# H13 · Contas a receber
# ======================================================================
CR_ROWS = [  # cliente, limite, aberto, vencido, próximo, uso %, situação, tom
    ("Rafael Coelho Nunes", 1000.00, 694.80, 310.00, "06/12/2026", 69, "Em atraso", "neg"),
    ("Mariana Albuquerque", 800.00, 240.00, 0.0, "28/11/2026", 30, "Vence esta semana", "warn"),
    ("Tabacaria do Porto Ltda", 3000.00, 1842.50, 612.50, "05/12/2026", 61, "Em atraso", "neg"),
    ("João Victor Sampaio", 500.00, 158.00, 0.0, "15/12/2026", 32, "Em dia", "ok"),
    ("Larissa Menezes", 600.00, 89.90, 0.0, "26/11/2026", 15, "Vence esta semana", "warn"),
    ("Pedro Henrique Brandão", 400.00, 386.00, 386.00, "02/11/2026", 97, "Bloqueado", "muted"),
    ("Carlos Eduardo Ribeiro", 1200.00, 520.00, 0.0, "18/12/2026", 43, "Em dia", "ok"),
    ("Distribuidora Vale Fumo ME", 2000.00, 1210.00, 0.0, "30/11/2026", 61, "Vence esta semana", "warn"),
    ("Bianca Torres Lima", 300.00, 75.00, 0.0, "01/12/2026", 25, "Em dia", "ok"),
]

def h13(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Contas a receber")
    y += _head(d, f, x, y, w, "Contas a receber", "Clientes a prazo · Loja PNZ · hoje, 24/11/2026", [], dev)
    y += _stats(d, f, x, y, w, [("Em aberto", "R$ 8.426,30", "23 clientes"), ("Vencido", "R$ 1.912,40", "7 clientes", "neg"),
                                ("Vence em 7 dias", "R$ 1.164,80", "9 parcelas"), ("Recebido em 30 dias", "R$ 5.380,15", "41 baixas")], dev) + 24
    chips = [("Todos", 23), ("Em atraso", 7), ("Vence esta semana", 5), ("Bloqueados", 2)]
    if dev == "mobile":
        y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
        ui.field(d, f, x, y, w, placeholder="Nome, CPF, CNPJ ou telefone", prefix_icon="busca", app=APP); y += 52
        rows = [(r[0], f"Vencido {brl(r[3])} · próx. {r[4][:5]}" if r[3] else f"Próximo vencimento {r[4][:5]}", brl(r[2]), r[6], r[7]) for r in CR_ROWS]
        _, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=0)
        return max(DEVICES[dev][1], y + hh + 24)
    ui.chips(d, f, x, y, chips, 0, app=APP)
    sw = 340 if dev == "desktop" else 260
    ui.field(d, f, x + w - sw, y - 4, sw, placeholder="Nome, CPF, CNPJ ou telefone" if dev == "desktop" else "Buscar cliente", prefix_icon="busca", app=APP)
    y += 52
    if dev == "desktop":
        cols = [("Cliente", None, "l"), ("Limite", 104, "r", True), ("Em aberto", 104, "r", True), ("Vencido", 104, "r", True),
                ("Próximo vencimento", 156, "r", True), ("Uso do limite", 150, "l"), ("Situação", 160, "l")]
        rows = [[r[0], v(r[1]), v(r[2]), (v(r[3]), "neg") if r[3] else "0,00", r[4], "", (r[6], r[7])] for r in CR_ROWS]
        ucol = 5
    else:
        cols = [("Cliente", None, "l"), ("Limite", 96, "r", True), ("Em aberto", 100, "r", True), ("Vencido", 96, "r", True),
                ("Uso do limite", 128, "l"), ("Situação", 156, "l")]
        rows = [[r[0], v(r[1]), v(r[2]), (v(r[3]), "neg") if r[3] else "0,00", "", (r[6], r[7])] for r in CR_ROWS]
        ucol = 4
    t, th = ui.table(d, f, x, y, w, cols, rows, selected=0, app=APP)
    ux, uw = _cols_x(cols, w)[ucol]
    bw = uw - 8 - 52
    for i, r in enumerate(CR_ROWS):
        ry = 36 + i * 40
        d.frame(t, "Uso do limite", ux + 8, ry + 18, bw, 4, fill=C["raised"], radius=2)
        d.frame(t, "Uso", ux + 8, ry + 18, max(2, bw * r[5] / 100), 4, fill=C["warn"] if r[5] >= 90 else C["text2"], radius=2)
        T(d, t, f"{r[5]}%", ux + 8 + bw + 10, ry + 10, size=13, color=C["text2"], lh=20, mono=True)

# ======================================================================
# H14 · Ficha do cliente a prazo (abas Parcelas, Compras a prazo, Pagamentos e recibos)
# ======================================================================
def _ficha_top(d, f, dev, aba):
    x, y, w, base = _shell(d, f, dev, "Contas a receber", h=None)
    if dev != "mobile":
        y += _crumb(d, f, x, y, "Contas a receber")
    acts = [("Cobrar no WhatsApp", "secondary", None, "whats", "WhatsApp"), ("Extrato", "secondary", None, "doc", "Extrato"),
            ("Limite e bloqueio", "secondary", None, "cadeado", "Limite")]
    y += _head(d, f, x, y, w, CLI[0], f"CPF {CLI[2]} · {CLI[1]}", acts, dev)
    y += _stats(d, f, x, y, w, [("Limite", brl(LIMITE)), ("Em aberto", brl(ABERTO)), ("Vencido", brl(VENCIDO), None, "neg"),
                                ("Disponível", brl(LIMITE - ABERTO))], dev, h=88) + 20
    tabs = ["Parcelas", "Compras a prazo", "Pagamentos e recibos"] if dev != "mobile" else ["Parcelas", "Compras", "Recibos"]
    ui.tabs(d, f, x, y, tabs, aba, app=APP)
    return x, y + 56, w, base

def h14(d, f, dev, app):
    x, y, w, base = _ficha_top(d, f, dev, 0)
    chips = [("Em aberto", 4), ("Vencidas", 2), ("Quitadas", 3), ("Todas", 7)]
    marc = (0, 1)
    if dev == "mobile":
        y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
        rows = []
        for p in PARC:
            sub = f"Venc. {p[3][:5]} · {p[4]} dias de atraso" if p[4] else f"Venc. {p[3]}"
            rows.append((f"Parcela {p[2]} · DAV {p[0]}", sub, brl(p[9]), p[10], "neg" if p[4] else "muted"))
        _, hh = _check_rows(d, f, x, y, w, rows, checked=marc, selected=1)
        total = y + hh + 24 + 88
        d.nodes[f]["height"] = float(max(DEVICES[dev][1], total))
        _bar(d, f, x, 0, w, "2 parcelas marcadas", brl(DEVIDO), "Dar baixa", dev)
        return max(DEVICES[dev][1], total)
    ui.chips(d, f, x, y, chips, 0, app=APP)
    y += 48
    if dev == "desktop":
        cols = [("", 36, "l"), ("Venda", 84, "l", True), ("Compra", 100, "l", True), ("Parcela", 76, "l"), ("Vencimento", None, "l", True),
                ("Atraso", 84, "l"), ("Valor", 88, "r", True), ("Pago", 72, "r", True), ("Multa", 72, "r", True), ("Juros", 72, "r", True),
                ("Total hoje", 100, "r", True), ("", 112, "r")]
        rows = [["", p[0], p[1], p[2], p[3], (f"{p[4]} dias", "neg") if p[4] else "—", v(p[5]), v(p[6]), v(p[7]), v(p[8]), (v(p[9]), "b"), ""] for p in PARC]
    else:
        cols = [("", 36, "l"), ("Venda", 80, "l", True), ("Parcela", 68, "l"), ("Vencimento", None, "l", True), ("Atraso", 76, "l"),
                ("Valor", 84, "r", True), ("Multa", 68, "r", True), ("Juros", 68, "r", True), ("Total hoje", 96, "r", True), ("", 108, "r")]
        rows = [["", p[0], p[2], p[3], (f"{p[4]} dias", "neg") if p[4] else "—", v(p[5]), v(p[7]), v(p[8]), (v(p[9]), "b"), ""] for p in PARC]
    t, th = ui.table(d, f, x, y, w, cols, rows, selected=1, app=APP, primary=1)
    px, pw = _cols_x(cols, w)[-1]
    for i in range(len(PARC)):
        ry = 36 + i * 40
        ui.checkbox(d, t, 16, ry + 11, on=i in marc, app=APP)
        ui.button(d, t, px + pw - 96, ry + 6, "Produtos", app=APP, kind="secondary", w=96, h=28)
    _bar(d, f, x, base - 64, w, "2 parcelas marcadas", brl(DEVIDO), "Dar baixa", dev)

COMPRAS = [  # mês, dav, data, itens [(q, nome, valor)], total, parcelas [(n, venc, valor, situação, tom)], cancelada
    ("Novembro de 2026", "004988", "10/11/2026", [(2, "Kit presente Smoke House", 159.80), (1, "Piteira de vidro Squadafum 6 mm", 25.00)], 184.80,
     [("1 de 1", "10/12/2026", 184.80, "Em aberto", "muted")], False),
    ("Novembro de 2026", "004931", "02/11/2026", [(1, "Bandeja Bem Bolado média", 39.90)], 39.90,
     [("1 de 1", "02/12/2026", 39.90, "Cancelada", "muted")], True),
    ("Setembro de 2026", "004702", "06/09/2026", [(3, "Caixa c/50 Seda Zomo KS Brown", 360.00), (2, "Dichavador metal 4 partes 50 mm", 90.00),
                                               (6, "Piteira de vidro Squadafum 6 mm", 150.00)], 600.00,
     [("1 de 3", "06/10/2026", 200.00, "Quitada", "ok"), ("2 de 3", "06/11/2026", 200.00, "Vencida", "neg"), ("3 de 3", "06/12/2026", 200.00, "Em aberto", "muted")], False),
    ("Agosto de 2026", "004517", "03/08/2026", [(1, "Isqueiro Zippo Classic Brushed Chrome", 289.00), (2, "Essência Zomo Love 66 50 g", 36.00),
                                             (1, "Seda Zomo King Size Brown", 5.00)], 330.00,
     [("1 de 3", "18/08/2026", 110.00, "Quitada", "ok"), ("2 de 3", "18/09/2026", 110.00, "Quitada", "ok"), ("3 de 3", "18/10/2026", 110.00, "Vencida", "neg")], False),
]

def h14b(d, f, dev, app):
    """Aba Compras a prazo: cada compra por mês, com produtos e a situação de cada parcela."""
    H0 = 3000
    d.nodes[f]["height"] = float(H0)
    x, y, w, base = _ficha_top(d, f, dev, 1)
    mes = None
    for m, dav, data, itens, total, parcs, canc in COMPRAS:
        if m != mes:
            T(d, f, m, x, y, size=13, color=C["muted"], lh=20); y += 28; mes = m
        if dev == "mobile":
            h = 60 + len(itens) * 40 + 32 + len(parcs) * 40 + 12
            c = ui.card(d, f, x, y, w, h)
            T(d, c, f"DAV {dav} · {data}", 16, 14, size=14, weight=500, lh=20, color=C["muted"] if canc else C["ink"])
            T(d, c, brl(total), w - 16, 14, size=14, weight=500, lh=20, mono=True, align="right", color=C["muted"] if canc else C["ink"])
            yy = 48
            for q, nome, val in itens:
                T(d, c, nome, 16, yy, size=13, lh=18, w=w - 32 - 80, color=C["text2"])
                T(d, c, f"{q} × {v(val / q)}", 16, yy + 18, size=12, color=C["muted"], lh=16, mono=True)
                T(d, c, v(val), w - 16, yy, size=13, lh=18, mono=True, align="right")
                yy += 40
            hair(d, c, 16, yy + 4, w - 32); yy += 16
            for n, venc, val, sit, tone in parcs:
                T(d, c, f"{n} · {venc[:5]}", 16, yy, size=13, lh=20, mono=True, color=C["text2"])
                ui.status(d, c, w - 16, yy, sit, tone, align="right")
                yy += 32
            d.nodes[c]["height"] = float(yy + 8)
            y += yy + 8 + 12
            continue
        lw = w * 0.56
        h = 56 + max(len(itens) * 32, len(parcs) * 32) + 16
        c = ui.card(d, f, x, y, w, h)
        T(d, c, f"DAV {dav}", 20, 16, size=15, weight=500, lh=20, mono=True, color=C["muted"] if canc else C["ink"])
        T(d, c, f"Compra de {data} · {len(parcs)} parcela{'s' if len(parcs) > 1 else ''}", 20 + fc.text_width(f"DAV {dav}", 15, 500, True) + 12, 17,
          size=13, color=C["text2"], lh=20)
        if canc:
            ui.status(d, c, lw - 20, 16, "Compra cancelada", "neg", align="right")
        else:
            T(d, c, brl(total), lw - 20, 16, size=15, weight=500, lh=20, mono=True, align="right")
        hair(d, c, 20, 48, w - 40)
        d.frame(c, "Divisa", lw, 60, 1, h - 72, fill=C["line"], fill_opacity=ui.LINE_A)
        yy = 60
        for q, nome, val in itens:
            T(d, c, f"{q} ×", 20, yy + 2, size=12, color=C["muted"], lh=16, mono=True)
            T(d, c, nome, 56, yy, size=13, lh=20, color=C["muted"] if canc else C["text2"])
            T(d, c, v(val), lw - 20, yy, size=13, lh=20, mono=True, align="right", color=C["muted"] if canc else C["ink"])
            yy += 32
        yy = 60
        for n, venc, val, sit, tone in parcs:
            T(d, c, f"Parcela {n}", lw + 24, yy, size=13, lh=20, color=C["text2"])
            T(d, c, venc, lw + 24 + 108, yy, size=13, lh=20, mono=True, color=C["text2"])
            T(d, c, v(val), lw + 24 + 108 + 96 + (60 if dev == "desktop" else 16), yy, size=13, lh=20, mono=True, align="right")
            ui.status(d, c, w - 20, yy, sit, tone, align="right")
            yy += 32
        y += h + 12
    return _fit(d, f, dev, y + 12)

RECIBOS = [  # nº, data, parcelas, forma, valor, quem, situação, tom, pode desfazer
    ("0143", "24/11/2026 14:32", "004517 3/3 · 004702 2/3", "PIX + Dinheiro", 300.00, "Lucas", "Substitui o 0142", "ok", True),
    ("0142", "24/11/2026 14:05", "004517 3/3 · 004702 2/3", "Dinheiro", 300.00, "Lucas", "Baixa desfeita", "neg", False),
    ("0128", "06/10/2026 10:14", "004702 1/3", "PIX", 200.00, "Carla", "Válido", "ok", False),
    ("0117", "18/09/2026 17:40", "004517 2/3", "Débito", 110.00, "Carla", "Válido", "ok", False),
    ("0098", "19/08/2026 09:52", "004517 1/3", "Dinheiro", 110.00, "Lucas", "Válido", "ok", False),
]

def h14c(d, f, dev, app):
    """Aba Pagamentos e recibos: Recibo e Desfazer baixa (Desfazer só no mesmo dia)."""
    x, y, w, base = _ficha_top(d, f, dev, 2)
    if dev == "mobile":
        rows = [(f"Recibo {r[0]} · {brl(r[4])}", f"{r[1][:5]} · {r[3]} · {r[5]}", None, r[6], r[7]) for r in RECIBOS]
        _, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=0)
        y += hh + 12
        ui.button(d, f, x, y, "Recibo", app=APP, kind="secondary", w=(w - 8) / 2, icon_name="nota")
        ui.button(d, f, x + (w + 8) / 2, y, "Desfazer baixa", app=APP, kind="secondary", w=(w - 8) / 2, icon_name="voltar")
        return max(DEVICES[dev][1], y + 64)
    if dev == "desktop":
        cols = [("Recibo", 80, "l", True), ("Data", 148, "l", True), ("Parcelas pagas (DAV)", None, "l"), ("Forma", 120, "l"), ("Valor", 96, "r", True),
                ("Baixa por", 88, "l"), ("Situação", 156, "l"), ("", 224, "r")]
        rows = [[r[0], r[1], r[2], r[3], v(r[4]), r[5], (r[6], r[7]), ""] for r in RECIBOS]
    else:
        cols = [("Recibo", 72, "l", True), ("Data", 108, "l", True), ("Forma", None, "l"), ("Valor", 88, "r", True),
                ("Situação", 148, "l"), ("", 220, "r")]
        rows = [[r[0], r[1][:10], r[3], v(r[4]), (r[6], r[7]), ""] for r in RECIBOS]
    t, th = ui.table(d, f, x, y, w, cols, rows, selected=0, app=APP, row_h=48)
    px, pw = _cols_x(cols, w)[-1]
    for i, r in enumerate(RECIBOS):
        ry = 36 + i * 48
        ui.button(d, t, px + pw - 212, ry + 8, "Recibo", app=APP, kind="secondary", w=80, h=32)
        if r[6] != "Baixa desfeita":
            ui.button(d, t, px + pw - 124, ry + 8, "Desfazer", app=APP, kind="secondary", w=124, h=32, icon_name="voltar", disabled=not r[8])
    y += th + 12
    T(d, f, "Desfazer só no mesmo dia da baixa, com motivo e senha do administrador", x, y, size=12, color=C["muted"], lh=16)

# ======================================================================
# H15 · Dar baixa
# ======================================================================
def h15(d, f, dev, app):
    Hm = 1500
    x, y, w, base = _shell(d, f, dev, "Contas a receber", h=Hm if dev == "mobile" else None)
    if dev != "mobile":
        y += _crumb(d, f, x, y, CLI[0])
    y += _head(d, f, x, y, w, "Dar baixa", f"{CLI[0]} · data da baixa 24/11/2026 (hoje)", [], dev)
    a, b = PARC[0], PARC[1]
    fica = [("Quitada", "ok"), (f"Paga R$ 186,44 · resta R$ 18,76", "warn")]
    if dev == "mobile":
        rows = [(f"Parcela {p[2]} · DAV {p[0]}", f"Venc. {p[3][:5]} · {p[4]} dias de atraso", brl(p[9]),
                 ("Quitada" if i == 0 else "Resta R$ 18,76"), "ok" if i == 0 else "warn") for i, p in enumerate((a, b))]
        _, hh = ui.mobile_rows(d, f, x, y, w, rows)
        y += hh + 16
    else:
        if dev == "desktop":
            cols = [("Venda", 96, "l", True), ("Parcela", 80, "l"), ("Vencimento", 112, "l", True), ("Atraso", 80, "l"), ("Valor", 96, "r", True),
                    ("Multa 2%", 88, "r", True), ("Juros 1% a.m.", 112, "r", True), ("Total hoje", 104, "r", True), ("Como fica", None, "l")]
            rows = [[p[0], p[2], p[3], (f"{p[4]} dias", "neg"), v(p[5]), v(p[7]), v(p[8]), (v(p[9]), "b"), ""] for i, p in enumerate((a, b))]
        else:
            cols = [("Parcela", None, "l"), ("Vencimento", 104, "l", True), ("Atraso", 72, "l"), ("Valor", 80, "r", True), ("Multa", 60, "r", True),
                    ("Juros", 56, "r", True), ("Total hoje", 88, "r", True), ("Como fica", 236, "l")]
            rows = [[f"{p[2]} · DAV {p[0]}", p[3], (f"{p[4]} dias", "neg"), v(p[5]), v(p[7]), v(p[8]), (v(p[9]), "b"), ""] for i, p in enumerate((a, b))]
        t, th = ui.table(d, f, x, y, w, cols, rows, app=APP)
        # "Como fica" com ponto de situação
        cx_, cw_ = _cols_x(cols, w)[-1]
        for i, (lab, tone) in enumerate(fica):
            ui.status(d, t, cx_ + 8, 36 + i * 40 + 10, lab, tone)
        y += th + 20
    # quadros Valores de hoje e Pagamento
    if dev == "mobile":
        cw = w; h1 = 292; h2 = 436
        c1x, c1y, c2x, c2y = x, y, x, y + h1 + 12
    else:
        cw = (w - 16) / 2
        h1 = h2 = 388
        c1x, c1y, c2x, c2y = x, y, x + cw + 16, y
    p = 20
    c1 = ui.card(d, f, c1x, c1y, cw, h1, title="Valores de hoje")
    yy = 56
    yy += ui.kv(d, c1, p, yy, cw - 2 * p, [("Valor das parcelas", "310,00"), ("Multa 2%", "6,20"), ("Juros 1% ao mês, por dia", "2,56")])
    T(d, c1, "Desconto", p, yy + 10, size=13, color=C["text2"], lh=20)
    ui.field(d, c1, cw - p - 120, yy, 120, value="0,00", mono=True, app=APP)
    yy += 52
    T(d, c1, "Dispensar multa e juros", p, yy, size=13, color=C["text2"], lh=20)
    ui.icon(d, c1, "cadeado", p + fc.text_width("Dispensar multa e juros", 13) + 8, yy + 2, 14, C["muted"])
    ui.toggle(d, c1, cw - p - 36, yy, on=False, app=APP)
    yy += 36
    hair(d, c1, p, yy, cw - 2 * p); yy += 16
    T(d, c1, "Total devido", p, yy + 6, size=14, weight=500, lh=20)
    T(d, c1, brl(DEVIDO), cw - p, yy, size=24, weight=500, lh=32, align="right", mono=True)
    c2 = ui.card(d, f, c2x, c2y, cw, h2, title="Pagamento")
    yy = 56
    ui.field(d, c2, p, yy, cw - 2 * p, label="Valor que o cliente está pagando", value="R$ 300,00", focused=True, app=APP, mono=True)
    yy += 72
    T(d, c2, "Fica em aberto", p, yy, size=13, color=C["text2"], lh=20)
    T(d, c2, brl(RESTA), cw - p, yy, size=13, weight=500, lh=20, align="right", mono=True, color=C["warn"])
    yy += 36
    hair(d, c2, p, yy, cw - 2 * p); yy += 16
    formas = [("PIX", "200,00", "Conta PIX"), ("Dinheiro", "100,00", "Caixa da loja")]
    for nome, val, conta in formas:
        if dev == "mobile":
            ui.field(d, c2, p, yy, 150, value=nome, chevron=True, app=APP)
            ui.field(d, c2, p + 158, yy, cw - 2 * p - 158 - 36, value=val, mono=True, app=APP)
            ui.icon(d, c2, "fechar", cw - p - 20, yy + 12, 16, C["muted"])
            T(d, c2, f"Entra em {conta}", p, yy + 44, size=12, color=C["muted"], lh=16)
            yy += 72
        else:
            fw, vw = (176, 120) if dev == "desktop" else (120, 100)
            ui.field(d, c2, p, yy, fw, value=nome, chevron=True, app=APP)
            ui.field(d, c2, p + fw + 8, yy, vw, value=val, mono=True, app=APP)
            T(d, c2, f"Entra em {conta}", p + fw + 8 + vw + 12, yy + 10, size=12, color=C["muted"], lh=20)
            ui.icon(d, c2, "fechar", cw - p - 16, yy + 12, 16, C["muted"])
            yy += 48
    ui.button(d, c2, p, yy, "Dividir em outra forma", app=APP, kind="ghost", icon_name="mais", w=212, align="left")
    yy += 52
    hair(d, c2, p, yy, cw - 2 * p); yy += 16
    T(d, c2, "Soma das formas", p, yy, size=13, color=C["text2"], lh=20)
    sw_ = fc.text_width("300,00", 13, 400, True)
    T(d, c2, "300,00", cw - p, yy, size=13, lh=20, mono=True, align="right")
    ui.icon(d, c2, "ok", cw - p - sw_ - 24, yy + 2, 16, C["pos"])
    # botões
    if dev == "mobile":
        by = c2y + h2 + 16
        ui.button(d, f, x, by, "Cancelar", app=APP, kind="secondary", w=(w - 8) / 2)
        ui.button(d, f, x + (w + 8) / 2, by, "Confirmar baixa", app=APP, kind="primary", w=(w - 8) / 2)
        return _fit(d, f, dev, by + 40 + 24)
    bx = x + w
    by = y + h1 + 24
    b, bw = ui.button(d, f, 0, by, "Confirmar baixa", app=APP, kind="primary", key="Enter")
    bx -= bw; d.nodes[b]["transform"][4] = float(bx)
    b, bw2 = ui.button(d, f, 0, by, "Cancelar", app=APP, kind="secondary", key="Esc")
    d.nodes[b]["transform"][4] = float(bx - 8 - bw2)

# ======================================================================
# H16 · Recibo
# ======================================================================
RECIBO_LINHAS = [
    ("SMOKE HOUSE TABACARIA", "cb"), ("Loja PNZ · Petrolina-PE", "c"), ("CNPJ a informar", "c"), ("", "hr"),
    ("RECIBO Nº 0143", "cb"), ("24/11/2026 14:32 · baixa por Lucas", "c"),
    ("SUBSTITUI O RECIBO Nº 0142 (DESFEITO)", "cb"), ("", "hr"),
    ("Cliente: Rafael Coelho Nunes", "l"), ("", "hr"),
    ("COMPRA DAV 004517 · 03/08/2026", "l"),
    (("1 ISQ ZIPPO CLASSIC CHROME", "289,00"), "lr"), (("2 ESS ZOMO LOVE 66 50G", "36,00"), "lr"), (("1 SEDA ZOMO KS BROWN", "5,00"), "lr"),
    (("Total da compra", "330,00"), "lr"),
    (("PAGO AGORA: PARCELA 3 DE 3", "110,00"), "lrb"),
    ("COMPRA QUITADA", "cb"), ("", "hr"),
    ("COMPRA DAV 004702 · 06/09/2026", "l"),
    (("3 CX C/50 SEDA ZOMO KS", "360,00"), "lr"), (("2 DICHAVADOR METAL 50MM", "90,00"), "lr"), (("6 PITEIRA VIDRO SQUADAFUM", "150,00"), "lr"),
    (("Total da compra", "600,00"), "lr"),
    (("PAGO AGORA: PARCELA 2 DE 3", "181,24"), "lrb"),
    (("Resta da parcela 2", "18,76"), "lr"),
    (("FALTA DESTA COMPRA", "218,76"), "lrb"), ("", "hr"),
    (("Multa e juros", "8,76"), "lr"), (("Desconto", "0,00"), "lr"),
    (("TOTAL PAGO", "300,00"), "lrb"), (("PIX", "200,00"), "lr"), (("Dinheiro", "100,00"), "lr"), ("", "hr"),
    (("SALDO DEVEDOR TOTAL", "403,56"), "lrb"),
]

def h16(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Contas a receber", h=H0)
    if dev != "mobile":
        y += _crumb(d, f, x, y, "Pagamentos e recibos")
    acts = [("Desfazer baixa", "secondary", None, "voltar", "Desfazer"), ("WhatsApp", "secondary", None, "whats"), ("Imprimir", "primary", None, "impressora")]
    y += _head(d, f, x, y, w, "Recibo Nº 0143", f"{CLI[0]} · 24/11/2026 14:32", acts, dev)
    rw = 384 if dev != "mobile" else w
    r, rh = ui.receipt(d, f, x, y, rw, RECIBO_LINHAS, title="Recibo impresso")
    rbot = y + rh + 6
    if dev == "mobile":
        y += rh + 32
        cx, cw = x, w
    else:
        cx, cw = x + rw + 32, w - rw - 32
        cw = min(cw, 520)
    c = ui.card(d, f, cx, y, cw, 236, title="Para onde foi o dinheiro")
    ui.kv(d, c, 20, 56, cw - 40, [("PIX · Conta PIX", "200,00"), ("Dinheiro · Caixa da loja", "100,00"), ("Total pago", "300,00")], bold_last=True)
    hair(d, c, 20, 148, cw - 40)
    T(d, c, "Desfazer baixa", 20, 164, size=13, color=C["text2"], lh=20)
    ui.status(d, c, cw - 20, 164, "Liberado até 23:59 de hoje", "ok", align="right")
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela
    y2 = y + 236 + 16
    c2 = ui.card(d, f, cx, y2, cw, 220, title="Recibo Nº 0142")
    ui.status(d, c2, cw - 20, 18, "Baixa desfeita", "neg", align="right")
    ui.kv(d, c2, 20, 56, cw - 40, [("Desfeito por", "Lucas · 14:28"), ("Motivo", "Forma errada"), ("No recibo", "SUBSTITUÍDO PELO 0143")], mono_values=False)
    T(d, c2, "Lançado em Dinheiro, o cliente pagou em PIX e dinheiro", 20, 148, size=12, color=C["muted"], lh=16, w=cw - 40)
    ui.button(d, c2, 20, 172, "Ver recibo 0142", app=APP, kind="secondary", h=32)
    return _fit(d, f, dev, max(y2 + 220, rbot) + 24)

# ======================================================================
# H17 · Formas de pagamento (+ janela Nova forma de pagamento)
# ======================================================================
FORMAS = [  # tipo, nome, conta, taxa, recebe, troco, parcelar, ativa, nova
    ("Dinheiro", "Dinheiro", "Caixa da loja", "0,00%", "Na hora", "Sim", "Não", True, False),
    ("PIX", "PIX", "Conta PIX", "0,00%", "Na hora", "Não", "Não", True, False),
    ("Débito", "Débito", "Maquininha Terminal 01", "1,39%", "1 dia", "Não", "Não", True, False),
    ("Crédito", "Crédito à vista", "Maquininha Terminal 01", "3,19%", "30 dias", "Não", "Não", True, False),
    ("Crédito", "Crédito parcelado", "Maquininha Terminal 01", "4,59%", "30 dias", "Não", "Até 3x", True, False),
    ("Crédito", "Crédito Terminal 02", "Maquininha Terminal 02", "3,49%", "30 dias", "Não", "Até 3x", True, True),
    ("Vale", "Vale-presente", "Caixa da loja", "0,00%", "Na hora", "Não", "Não", False, False),
]

def h17(d, f, dev, app, sem_nova=False):
    x, y, w, base = _shell(d, f, dev, "Formas de pagamento")
    y += _head(d, f, x, y, w, "Formas de pagamento", "Aparecem no F3 do DAV e da NFC-e e na baixa do Contas a receber",
               [("Adicionar", "primary", None, "mais")], dev) if dev != "mobile" else \
         _head(d, f, x, y, w, "Formas de pagamento", "No F3 do caixa e na baixa", [("Adicionar", "primary", None, "mais")], dev)
    sel = 5
    formas = [fm for fm in FORMAS if not (sem_nova and fm[8])]
    if sem_nova: sel = None
    if dev == "mobile":
        rows = [(fm[1], f"{fm[2]} · {fm[3]}", None, "Ativa" if fm[7] else "Inativa", "ok" if fm[7] else "muted") for fm in formas]
        lst, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=sel)
        for i, fm in enumerate(formas):
            if fm[8]:
                T(d, lst, "Nova", 16 + fc.text_width(fm[1], 14, 500) + 10, 4 + i * 64 + 11, size=12, color=C["muted"], lh=18)
        y += hh + 24
        T(d, f, "Formas fixas do sistema", x, y, size=15, weight=500, lh=20); y += 32
        _, hh = ui.mobile_rows(d, f, x, y, w, [("PRAZO", "Só com a venda a prazo ligada", None, "Fixa", "muted"),
                                                ("Crédito do cliente", "Só quando o cliente tem saldo", None, "Fixa", "muted")])
        return max(DEVICES[dev][1], y + hh + 24)
    if dev == "desktop":
        cols = [("Tipo", 100, "l"), ("Nome no caixa", None, "l"), ("Maquininha ou conta", 208, "l"), ("Taxa", 80, "r", True), ("Recebe em", 112, "l"),
                ("Troco", 72, "l"), ("Parcelamento", 116, "l"), ("Ativa", 72, "l")]
        rows = [[fm[0], fm[1], fm[2], fm[3], fm[4], fm[5], fm[6], ""] for fm in formas]
    else:
        cols = [("Tipo", 88, "l"), ("Nome no caixa", None, "l"), ("Maquininha ou conta", 196, "l"), ("Taxa", 72, "r", True), ("Recebe em", 92, "l"),
                ("Parcelamento", 108, "l"), ("Ativa", 60, "l")]
        rows = [[fm[0], fm[1], fm[2], fm[3], fm[4], fm[6], ""] for fm in formas]
    t, th = ui.table(d, f, x, y, w, cols, rows, selected=sel, app=APP, primary=1)
    cx = _cols_x(cols, w)
    for i, fm in enumerate(formas):
        ry = 36 + i * 40
        ui.toggle(d, t, cx[-1][0] + 8, ry + 10, on=fm[7], app=APP)
        if fm[8]:
            T(d, t, "Nova", cx[1][0] + 8 + fc.text_width(fm[1], 13) + 10, ry + 11, size=12, color=C["muted"], lh=18)
    y += th + 32
    T(d, f, "Formas fixas do sistema", x, y, size=15, weight=500, lh=20); y += 32
    cols2 = [("Forma", 220, "l"), ("Quando aparece no caixa", None, "l"), ("Entra em", 260, "l")]
    ui.table(d, f, x, y, w, cols2, [["PRAZO", "Só com a venda a prazo ligada em Regras do caixa", "Contas a receber do cliente"],
                                     ["Crédito do cliente", "Só quando o cliente identificado tem saldo", "Abate o saldo do cliente"]], app=APP)

def h17b(d, f, dev, app):
    h17(d, f, dev, app, sem_nova=True)
    win, w, h, top, bot = ui.window(d, f, dev, "Nova forma de pagamento", 640, 532 if dev != "mobile" else 620, app=APP,
                                    footer_buttons=[("Cancelar", "secondary", "Esc"), ("Salvar", "primary", "Enter")])
    p = 24
    y = top + 20
    T(d, win, "Tipo", p, y, size=13, color=C["text2"], lh=16); y += 28
    tipos = ["Crédito", "Débito", "PIX", "Dinheiro", "Vale", "Outro"]
    cx = p
    per_row = 3 if dev == "mobile" else 6
    for i, t in enumerate(tipos):
        if i and i % per_row == 0:
            cx = p; y += 32
        ui.radio(d, win, cx, y, on=i == 0, label=t, app=APP)
        cx += (w - 2 * p) / 3 if dev == "mobile" else 28 + fc.text_width(t, 14) + 28
    y += 44
    if dev == "mobile":
        fw = w - 2 * p
        ui.field(d, win, p, y, fw, label="Nome no caixa", value="Crédito Terminal 02", focused=True, app=APP); y += 72
        ui.field(d, win, p, y, fw, label="Maquininha ou conta", value="Maquininha Terminal 02", chevron=True, app=APP); y += 72
        ui.field(d, win, p, y, (fw - 12) / 2, label="Taxa", value="3,49", suffix="%", mono=True, app=APP)
        ui.field(d, win, p + (fw + 12) / 2, y, (fw - 12) / 2, label="Recebe em", value="30 dias", chevron=True, app=APP); y += 80
    else:
        fw = (w - 2 * p - 16) / 2
        ui.field(d, win, p, y, fw, label="Nome no caixa", value="Crédito Terminal 02", focused=True, app=APP)
        ui.field(d, win, p + fw + 16, y, fw, label="Maquininha ou conta", value="Maquininha Terminal 02", chevron=True, app=APP); y += 76
        ui.field(d, win, p, y, fw, label="Taxa", value="3,49", suffix="%", mono=True, app=APP)
        ui.field(d, win, p + fw + 16, y, fw, label="Recebe em", value="30 dias", chevron=True, app=APP); y += 84
    hair(d, win, p, y, w - 2 * p); y += 20
    y += _row_toggle(d, win, p, y, w - 2 * p, "Aceita troco", False)
    _row_toggle(d, win, p, y, w - 2 * p, "Permite parcelar", True)
    ui.field(d, win, w - p - 36 - 16 - 96, y - 10, 96, value="Até 3x", chevron=True, app=APP)
    y += 44
    y += _row_toggle(d, win, p, y, w - 2 * p, "Mostrar no caixa", True)

# ======================================================================
# H18 · Configurações
# ======================================================================
def _cfg_empresa(d, p, x, y, w, dev):
    one = dev == "mobile"
    fw = w - 40 if one else (w - 40 - 16) / 2
    c = _sec(d, p, x, y, w, 10, "Empresa")
    yy = 56
    pos = [("Razão social", "Smoke House Tabacaria Ltda", False, None), ("Nome fantasia", "Smoke House", False, None),
           ("CNPJ", "", True, "CNPJ a informar"), ("Inscrição estadual", "", True, "A informar"),
           ("Regime", "Simples Nacional", False, "chev"), ("Tabela IBPT", "26.1.A · até 31/01/2027", False, "ro")]
    for i, (lab, val, mono, extra) in enumerate(pos):
        col = 0 if one else i % 2
        fx = 20 + col * (fw + 16)
        ui.field(d, c, fx, yy, fw, label=lab, value=val, mono=mono, app=APP, chevron=extra == "chev", readonly=extra == "ro",
                 placeholder=extra if extra not in ("chev", "ro") else "")
        if one or col == 1:
            yy += 72
    ui.button(d, c, 20, yy, "Importar tabela IBPT", app=APP, kind="secondary", icon_name="upload", h=36)
    d.nodes[c]["height"] = float(yy + 56)
    return yy + 56

def _cfg_regras(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Regras do caixa")
    yy = 56; iw = w - 40
    yy += _row_toggle(d, c, 20, yy, iw, "Fechamento cego", False)
    yy += _row_value(d, c, 20, yy, iw, "Fundo de troco sugerido", "150,00", suffix="R$", sub=None)
    yy += _row_value(d, c, 20, yy, iw, "Desconto máximo sem senha", "5", suffix="%")
    yy += _row_toggle(d, c, 20, yy, iw, "Cancelar item ou cupom pede senha", False)
    yy += _row_toggle(d, c, 20, yy, iw, "Importar o DAV no NFC-e ao finalizar", False) + 4
    hair(d, c, 20, yy, iw); yy += 16
    T(d, c, "Venda a prazo", 20, yy, size=13, color=C["muted"], lh=20); yy += 28
    yy += _row_toggle(d, c, 20, yy, iw, "Venda a prazo", True)
    yy += _row_value(d, c, 20, yy, iw, "Vencimento padrão", "30", suffix="dias", sub="De 1 a 120 dias")
    T(d, c, "Parcelas", 20, yy, size=14, lh=20); yy += 28
    cx = 20
    for i, lab in enumerate(["Vencimento único", "Até 2x", "Até 3x"]):
        ui.radio(d, c, cx, yy, on=i == 2, label=lab, app=APP)
        if dev == "mobile":
            yy += 32
        else:
            cx += 28 + fc.text_width(lab, 14) + 24
    yy += 36 if dev != "mobile" else 8
    yy += _row_value(d, c, 20, yy, iw, "Multa por atraso", "2", suffix="%", sub="Máximo 2%")
    yy += _row_value(d, c, 20, yy, iw, "Juros de atraso ao mês", "1", suffix="%", sub="Contados por dia · máximo 10%")
    d.nodes[c]["height"] = float(yy + 8)
    return yy + 8

def _cfg_equip(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Equipamentos")
    yy = 56
    for lab, val in [("Impressora do cupom", "Térmica 80 mm · USB001"), ("Impressora do DANFE", "Térmica 80 mm · USB001"),
                     ("Gaveta", "Ligada à impressora do cupom")]:
        if dev == "mobile":
            ui.field(d, c, 20, yy, w - 40 - 48, label=lab, value=val, chevron=True, app=APP)
            b = d.frame(c, f"Botão Testar {lab}", w - 20 - 40, yy + 20, 40, 40, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CTL)
            ui.icon(d, b, "impressora" if lab != "Gaveta" else "caixa", 12, 12, 16, C["text2"])
        else:
            ui.field(d, c, 20, yy, w - 40 - 136, label=lab, value=val, chevron=True, app=APP)
            ui.button(d, c, w - 20 - 124, yy + 20, "Testar", app=APP, kind="secondary", w=124, icon_name="impressora" if lab != "Gaveta" else "caixa")
        yy += 72
    d.nodes[c]["height"] = float(yy + 4)
    return yy + 4

def _cfg_backup(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Cópia de segurança")
    if dev == "mobile":
        T(d, c, "Última cópia baixada", 20, 56, size=13, color=C["text2"], lh=20)
        T(d, c, "20/11/2026 18:02 · Lucas", 20, 76, size=13, lh=20, mono=True)
        T(d, c, "Nuvem: todo dia às 03:00, 7 cópias", 20, 104, size=13, color=C["text2"], lh=20)
        T(d, c, "Em Integrações", 20, 124, size=12, color=C["muted"], lh=16)
        ui.button(d, c, 20, 156, "Fazer backup", app=APP, kind="secondary", icon_name="upload")
        d.nodes[c]["height"] = 216.0
        return 216
    T(d, c, "Última cópia baixada", 20, 56, size=13, color=C["text2"], lh=20)
    T(d, c, "20/11/2026 18:02 · Lucas", w - 20, 56, size=13, lh=20, mono=True, align="right")
    T(d, c, "Nuvem: todo dia às 03:00, 7 cópias", 20, 84, size=13, color=C["text2"], lh=20)
    T(d, c, "Em Integrações", w - 20, 84, size=13, color=C["muted"], lh=20, align="right")
    ui.button(d, c, 20, 120, "Fazer backup", app=APP, kind="secondary", icon_name="upload")
    T(d, c, "Arquivo com os dados, sem as senhas", 20 + 156, 130, size=12, color=C["muted"], lh=20) if w > 400 else None
    d.nodes[c]["height"] = 176.0
    return 176

def h18(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Configurações", h=H0)
    y += _head(d, f, x, y, w, "Configurações", "Loja PNZ · Petrolina-PE", [("Salvar alterações", "primary", None, "ok")], dev) if dev != "mobile" else \
         _head(d, f, x, y, w, "Configurações", "Loja PNZ · Petrolina-PE", [], dev)
    if dev == "mobile":
        for fn in (_cfg_empresa, _cfg_regras, _cfg_equip, _cfg_backup):
            y += fn(d, f, x, y, w, dev) + 16
        y += 8
        ui.button(d, f, x, y, "Salvar alterações", app=APP, kind="primary", w=w, h=44)
        return _fit(d, f, dev, y + 44 + 24)
    cw = (w - 24) / 2
    if dev == "tablet":
        y += _cfg_empresa(d, f, x, y, w, dev) + 16
        y1 = y + _cfg_equip(d, f, x + cw + 24, y, cw, dev) + 16
        y1 += _cfg_backup(d, f, x + cw + 24, y1, cw, dev) + 16
        y2 = y + _cfg_regras(d, f, x, y, cw, dev) + 16
        return _fit(d, f, dev, max(y1, y2) + 8)
    y1 = y + _cfg_empresa(d, f, x, y, cw, dev) + 16
    y1 += _cfg_equip(d, f, x, y1, cw, dev) + 16
    y1 += _cfg_backup(d, f, x, y1, cw, dev) + 16
    y2 = y + _cfg_regras(d, f, x + cw + 24, y, cw, dev) + 16
    return _fit(d, f, dev, max(y1, y2) + 8)

# ======================================================================
# H19 · Usuários e permissões
# ======================================================================
USERS = [("Lucas", "Administrador", "Nenhum", "Ativo", "ok"), ("Marcos", "Gerente", "Nenhum", "Ativo", "ok"),
         ("Carla", "Supervisor de caixa", "Nenhum", "Ativo", "ok"), ("Arthur", "Operador de caixa", "Terminal 01", "Ativo", "ok"),
         ("Ana", "Operador de caixa", "Terminal 02", "Ativo", "ok"), ("Júlia", "Faturista", "Nenhum", "Inativo", "muted")]
PERFIS = ["Administrador", "Gerente", "Supervisor de caixa", "Operador de caixa", "Faturista"]
FUNCOES = [  # função, [adm, ger, sup, op, fat]
    ("Cancelar item e cupom", [1, 1, 1, 1, 0]),
    ("Cancelar venda finalizada", [1, 1, 1, 0, 0]),
    ("Sangria e suprimento", [1, 1, 1, 1, 0]),
    ("Troca e devolução", [1, 1, 1, 0, 0]),
    ("Lançar crédito do cliente", [1, 0, 0, 0, 0]),
    ("Dar baixa em parcelas", [1, 1, 0, 0, 1]),
    ("Desfazer baixa", [1, 0, 0, 0, 0]),
    ("Limite e bloqueio do cliente", [1, 0, 0, 0, 0]),
    ("Entrada, saída e transferência", [1, 1, 0, 0, 1]),
    ("Produtos e preços", [1, 1, 0, 0, 1]),
    ("Relatórios", [1, 1, 1, 0, 1]),
    ("Configurações e fiscal", [1, 0, 0, 0, 0]),
]
DESC = ["Sem limite", "15%", "10%", "5%", "0%"]

def h19(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Usuários", h=H0)
    y += _head(d, f, x, y, w, "Usuários e permissões", "Administrador principal: Lucas, com tudo liberado sempre",
               [("Novo usuário", "primary", None, "mais")], dev)
    if dev == "mobile":
        rows = [(u[0], f"{u[1]} · {u[2]}", None, u[3], u[4]) for u in USERS]
        _, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=3)
        y += hh + 24
        T(d, f, "Permissões por perfil", x, y, size=15, weight=500, lh=20); y += 32
        y += ui.chips(d, f, x, y, [(p_, None) for p_ in PERFIS], 3, app=APP, wrap_w=w) + 16
        c = ui.card(d, f, x, y, w, 10)
        yy = 16
        yy += _row_value(d, c, 16, yy, w - 32, "Limite de desconto", "5", vw=96, suffix="%")
        for fn_, vals in FUNCOES:
            hair(d, c, 16, yy - 4, w - 32)
            T(d, c, fn_, 16, yy + 8, size=14, lh=20)
            ui.toggle(d, c, w - 16 - 36, yy + 8, on=bool(vals[3]), app=APP)
            yy += 40
        d.nodes[c]["height"] = float(yy + 8)
        return _fit(d, f, dev, y + yy + 32)
    if dev == "desktop":
        lw = 440
        cols = [("Nome", None, "l"), ("Perfil", 140, "l"), ("Terminal fixo", 96, "l"), ("Situação", 80, "l")]
        T(d, f, "Usuários", x, y, size=15, weight=500, lh=20)
        t, th = ui.table(d, f, x, y + 32, lw, cols, [[u[0], u[1], u[2], (u[3], u[4])] for u in USERS], selected=0, app=APP)
        T(d, f, "Ana e Arthur estão com o caixa aberto e não podem ser desativados", x, y + 32 + th + 12, size=12, color=C["muted"], lh=16, w=lw)
        px, pw = x + lw + 24, w - lw - 24
        py = y
    else:
        cols = [("Nome", None, "l"), ("Perfil", 176, "l"), ("Terminal fixo", 120, "l"), ("Situação", 100, "l")]
        T(d, f, "Usuários", x, y, size=15, weight=500, lh=20)
        t, th = ui.table(d, f, x, y + 32, w, cols, [[u[0], u[1], u[2], (u[3], u[4])] for u in USERS], selected=0, app=APP)
        px, pw = x, w
        py = y + 32 + th + 32
    # permissões
    T(d, f, "Permissões", px, py, size=15, weight=500, lh=20)
    ui.tabs(d, f, px + 120, py - 10, ["Por perfil", "Por usuário"], 0, app=APP)
    c = ui.card(d, f, px, py + 40, pw, 10)
    pcw = [96, 68, 80, 80, 68]
    fw = pw - 40 - sum(pcw)
    ccx, acc_ = [], 20 + fw
    for cw_ in pcw:
        ccx.append(acc_); acc_ += cw_
    for i, pf in enumerate(PERFIS):
        T(d, c, pf, ccx[i] + 2, 14 if " " in pf else 22, size=12, color=C["ink"] if i == 0 else C["text2"], lh=16, align="center", w=pcw[i] - 4)
    T(d, c, "Função", 20, 22, size=12, color=C["muted"], lh=16)
    yy = 52
    hair(d, c, 0, yy, pw); yy += 6
    T(d, c, "Limite de desconto", 20, yy + 8, size=13, lh=20)
    for i, dv in enumerate(DESC):
        T(d, c, dv, ccx[i] + pcw[i] / 2, yy + 8, size=12, lh=20, mono=True, align="center", color=C["text2"])
    yy += 36
    for fn_, vals in FUNCOES:
        hair(d, c, 20, yy, pw - 40)
        T(d, c, fn_, 20, yy + 8, size=13, lh=20, color=C["text2"])
        for i, on in enumerate(vals):
            ui.checkbox(d, c, ccx[i] + pcw[i] / 2 - 9, yy + 9, on=bool(on), app=APP)
            if i == 0:
                d.nodes[d.nodes[c]["children"][-1]]["opacity"] = 0.5
        yy += 36
    hair(d, c, 20, yy, pw - 40)
    T(d, c, "Administrador: tudo liberado sempre", 20, yy + 12, size=12, color=C["muted"], lh=16)
    d.nodes[c]["height"] = float(yy + 40)
    return _fit(d, f, dev, py + 40 + yy + 40 + 24)

# ======================================================================
# H20 · Chamados
# ======================================================================
CHAMADOS = [  # categoria, título, de, para, quando, coluna
    ("Estoque", "Essência Zomo Strong Mint zerada na frente de loja", "Arthur", "Lucas", "hoje 09:12", 0),
    ("Caixa", "Divergência de R$ 12,00 no caixa de Ana ontem", "Carla", "Lucas", "ontem 22:47", 0),
    ("Cliente", "Rafael Coelho pediu aumento do limite a prazo", "Carla", "Lucas", "22/11 16:05", 0),
    ("Sistema", "Impressora do Terminal 02 cortando o cupom", "Ana", "Lucas", "21/11 11:30", 1),
    ("Estoque", "Conferir a entrada da nota 18.442 do fornecedor", "Lucas", "Marcos", "20/11 15:10", 1),
]

def _chamado_card(d, p, x, y, w, ch, sel=False):
    h = 112
    c = d.frame(p, f"Chamado {ch[1][:24]}", x, y, w, h, fill=C["sel"] if sel else C["card"], stroke=C["ink"] if sel else C["line"],
                stroke_opacity=1.0 if sel else ui.LINE_A, radius=ui.R_CTL + 2)
    T(d, c, ch[0], 16, 14, size=12, color=C["muted"], lh=16)
    T(d, c, ch[4], w - 16, 14, size=12, color=C["muted"], lh=16, align="right", mono=True)
    T(d, c, ch[1], 16, 36, size=14, weight=500, lh=20, w=w - 32)
    T(d, c, f"{ch[2]} para {ch[3]}", 16, h - 28, size=12, color=C["text2"], lh=16)
    return h

def h20(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Chamados")
    y += _head(d, f, x, y, w, "Chamados", "Só os chamados de Lucas", [("Novo chamado", "primary", None, "mais")], dev)
    ui.tabs(d, f, x, y, ["Abertos", "Concluídos"], 0, app=APP, counts=[5, 38])
    y += 56
    cats = [("Todas", 5), ("Estoque", 2), ("Caixa", 1), ("Cliente", 1), ("Sistema", 1)]
    if dev == "mobile":
        ui.field(d, f, x, y, w, placeholder="Buscar chamado", prefix_icon="busca", app=APP); y += 52
        y += ui.chips(d, f, x, y, cats, 0, app=APP, wrap_w=w) + 16
        for ci, (nome, tone) in enumerate((("Aberto", "info"), ("Em andamento", "warn"))):
            grp = [ch for ch in CHAMADOS if ch[5] == ci]
            ui.status(d, f, x, y, nome, tone)
            T(d, f, str(len(grp)), x + fc.text_width(nome, 13) + 22, y, size=12, color=C["muted"], lh=20, mono=True)
            y += 28
            rows = [(ch[1], f"{ch[2]} para {ch[3]} · {ch[4]}", None, ch[0], None) for ch in grp]
            _, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=0 if ci == 0 else None)
            y += hh + 20
        return max(DEVICES[dev][1], y + 4)
    sw = 280 if dev == "desktop" else 220
    ui.field(d, f, x, y, sw, placeholder="Buscar chamado", prefix_icon="busca", app=APP)
    ui.chips(d, f, x + sw + 16, y + 4, cats, 0, app=APP)
    # quadro / lista
    seg = d.frame(f, "Quadro ou lista", x + w - 168, y, 168, 40, fill=C["raised"], radius=ui.R_CTL)
    d.frame(seg, "Quadro ativo", 4, 4, 80, 32, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=6)
    T(d, seg, "Quadro", 44, 10, size=13, weight=500, lh=20, align="center")
    T(d, seg, "Lista", 126, 10, size=13, color=C["text2"], lh=20, align="center")
    y += 64
    detail = dev == "desktop"
    bw = w - (392 + 24 if detail else 0)
    colw = (bw - 16) / 2
    for ci, (nome, n) in enumerate([("Aberto", 3), ("Em andamento", 2)]):
        cx = x + ci * (colw + 16)
        col = d.frame(f, f"Coluna {nome}", cx, y, colw, base - y, fill=C["deep"], radius=ui.R_CARD)
        ui.status(d, col, 16, 14, nome, "info" if ci == 0 else "warn")
        T(d, col, str(n), 16 + fc.text_width(nome, 13) + 22, 14, size=12, color=C["muted"], lh=20, mono=True)
        yy = 48
        for i, ch in enumerate(CHAMADOS):
            if ch[5] != ci: continue
            yy += _chamado_card(d, col, 8, yy, colw - 16, ch, sel=i == 0) + 8
    if detail:
        ch = CHAMADOS[0]
        dx = x + bw + 24; dw = 392
        c = ui.card(d, f, dx, y, dw, base - y)
        T(d, c, ch[0], 20, 20, size=12, color=C["muted"], lh=16)
        ui.status(d, c, dw - 20, 18, "Aberto", "info", align="right")
        T(d, c, ch[1], 20, 44, size=17, weight=500, lh=24, w=dw - 40)
        ui.kv(d, c, 20, 108, dw - 40, [("Aberto por", "Arthur · Terminal 01"), ("Para", "Lucas"), ("Quando", "24/11/2026 09:12")], mono_values=False)
        hair(d, c, 20, 200, dw - 40)
        T(d, c, "Cliente pediu a Strong Mint e a frente está zerada. O fundo tem 14. Pode transferir?", 20, 216, size=14, lh=22, w=dw - 40)
        hair(d, c, 20, 300, dw - 40)
        T(d, c, "Histórico", 20, 316, size=13, color=C["text2"], lh=20)
        for i, (hora, txt) in enumerate([("09:12", "Arthur abriu o chamado"), ("09:40", "Lucas viu")]):
            T(d, c, hora, 20, 344 + i * 28, size=12, color=C["muted"], lh=20, mono=True)
            T(d, c, txt, 72, 344 + i * 28, size=13, color=C["text2"], lh=20)
        hb = base - y
        ui.field(d, c, 20, hb - 20 - 40 - 12 - 40, dw - 40, placeholder="Responder", app=APP)
        ui.button(d, c, 20, hb - 20 - 40, "Em andamento", app=APP, kind="secondary", w=(dw - 48) / 2)
        ui.button(d, c, 20 + (dw - 48) / 2 + 8, hb - 20 - 40, "Concluir", app=APP, kind="primary", w=(dw - 48) / 2)

# ======================================================================
# H21 · Fornecedores
# ======================================================================
FORN = [  # razão social, cnpj base, contato, telefone, e-mail, cidade, uf
    ("Zomo Distribuidora de Tabacaria Ltda", "123456780001", "Rogério", "(11) 3456-7788", "pedidos@distzomo.com.br", "São Paulo", "SP"),
    ("Papelito Indústria de Papéis Ltda", "234567890001", "Fernanda", "(47) 3321-9087", "comercial@papelito.ind.br", "Blumenau", "SC"),
    ("Clipper Isqueiros do Brasil Ltda", "345678900001", "Marcelo", "(11) 4122-3300", "vendas@clipperbr.com.br", "Barueri", "SP"),
    ("Vale Fumo Distribuidora ME", "456789010001", "Joelma", "(87) 3862-1450", "joelma@valefumo.com.br", "Petrolina", "PE"),
    ("Bem Bolado Acessórios Ltda", "567890120001", "Thiago", "(21) 3090-4471", "pedidos@bembolado.com.br", "Rio de Janeiro", "RJ"),
    ("Squadafum Comércio de Vidros Ltda", "678901230001", "Paula", "(41) 3233-8010", "loja@squadafum.com.br", "Curitiba", "PR"),
    ("Nordeste Tabacos e Conveniência Ltda", "789012340001", "Sérgio", "(74) 3611-2290", "sergio@nordestetabacos.com.br", "Juazeiro", "BA"),
]

def h21(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Fornecedores")
    y += _head(d, f, x, y, w, "Fornecedores", "7 fornecedores", [("Novo fornecedor", "primary", None, "mais", "Novo fornecedor")], dev)
    sel = 3
    if dev == "mobile":
        ui.field(d, f, x, y, w, placeholder="Razão social, CNPJ ou cidade", prefix_icon="busca", app=APP); y += 52
        rows = [(fo[0], f"{_cnpj(fo[1])} · {fo[5]}-{fo[6]}", None, None, None) for fo in FORN]
        _, hh = ui.mobile_rows(d, f, x, y, w, rows, selected=sel)
        return max(DEVICES[dev][1], y + hh + 24)
    pw = 400 if dev == "desktop" else 344
    lw = w - pw - 16
    ui.field(d, f, x, y, lw, placeholder="Razão social, CNPJ ou cidade", prefix_icon="busca", app=APP); y += 56
    if dev == "desktop":
        cols = [("Razão social", None, "l"), ("CNPJ", 172, "l", True), ("Contato", 88, "l"), ("Cidade", 140, "l")]
        rows = [[fo[0], _cnpj(fo[1]), fo[2], f"{fo[5]}-{fo[6]}"] for fo in FORN]
    else:
        cols = [("Razão social", None, "l"), ("Cidade", 132, "l")]
        rows = [[fo[0], f"{fo[5]}-{fo[6]}"] for fo in FORN]
    ui.table(d, f, x, y, lw, cols, rows, selected=sel, app=APP)
    fo = FORN[sel]
    py = y - 56
    c = ui.card(d, f, x + lw + 16, py, pw, base - py, title="Editar fornecedor")
    yy = 56; iw = pw - 40
    for lab, val, mono in [("Razão social", fo[0], False), ("CNPJ", _cnpj(fo[1]), True), ("Contato", fo[2], False),
                           ("Telefone", fo[3], True), ("E-mail", fo[4], False)]:
        ui.field(d, c, 20, yy, iw, label=lab, value=val, mono=mono, app=APP, focused=lab == "Contato")
        yy += 68
    ui.field(d, c, 20, yy, iw - 88, label="Cidade", value=fo[5], app=APP)
    ui.field(d, c, 20 + iw - 76, yy, 76, label="UF", value=fo[6], chevron=True, app=APP)
    yy += 68
    T(d, c, "Ligado a 38 produtos", 20, yy + 4, size=12, color=C["muted"], lh=16)
    hb = base - py
    ui.button(d, c, 20, hb - 60, "Excluir", app=APP, kind="danger", icon_name="lixo")
    b, bw = ui.button(d, c, 0, hb - 60, "Salvar", app=APP, kind="primary", key="Enter")
    d.nodes[b]["transform"][4] = float(pw - 20 - bw)

# ======================================================================
# H22 · Integrações
# ======================================================================
INTEG = [  # título, ícone, situação, tom, linhas, botão ativo
    ("Central do fornecedor", "caminhao", "Configurada", "ok", [("E-mail de pedidos", "compras@smokehouse.com.br"), ("Pedido automático no mínimo", "Ligado")], True),
    ("Central do cliente", "pessoas", "Configurada", "ok", [("Mostra as compras", "Ligado"), ("Mostra o crédito disponível", "Ligado")], True),
    ("PIX", "moeda", "Configurada", "ok", [("Tipo de chave", "CNPJ"), ("Conta", "Conta PIX")], True),
    ("Envio para a contabilidade", "doc", "Falta configurar", "warn", [("E-mail do contador", "a informar"), ("Dia do envio", "5 de cada mês")], True),
    ("Backup na nuvem", "nuvem", "Configurada", "ok", [("Horário", "03:00"), ("Cópias guardadas", "7"), ("Última cópia", "hoje 03:00")], True),
    ("Notas fiscais (MD-e)", "nota", "Aguarda integração fiscal", "muted", [("Importação e manifestação das notas de compra", None)], False),
]

def h22(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Integrações", h=H0)
    y += _head(d, f, x, y, w, "Integrações", "Configurar abre as opções e atualiza a situação do cartão", [], dev)
    ncol = {"desktop": 3, "tablet": 2, "mobile": 1}[dev]
    cw = (w - 16 * (ncol - 1)) / ncol
    ch = 228
    my = y
    for i, (tit, ic, sit, tone, lines, ativo) in enumerate(INTEG):
        cx = x + (i % ncol) * (cw + 16); cy = y + (i // ncol) * (ch + 16)
        if dev == "mobile":
            ch = 76 + 26 * len(lines) + 16 + 36 + 20
            cy = my; my += ch + 12
        c = ui.card(d, f, cx, cy, cw, ch)
        q = d.frame(c, "Ícone", 20, 20, 32, 32, fill=C["raised"], radius=ui.R_CTL)
        ui.icon(d, q, ic, 8, 8, 16, C["text2"])
        T(d, c, tit, 64, 18, size=15, weight=500, lh=20, w=cw - 84)
        ui.status(d, c, 64, 40, sit, tone)
        yy = 76
        for k, val in lines:
            T(d, c, k, 20, yy, size=13, color=C["text2"], lh=20)
            if val is None:
                yy += 26; continue
            T(d, c, val, cw - 20, yy, size=13, lh=20, align="right", color=C["muted"] if val == "a informar" else C["ink"])
            yy += 26
        ui.button(d, c, 20, ch - 20 - 36, "Configurar", app=APP, kind="secondary", h=36, disabled=not ativo)
    if dev == "mobile":
        return _fit(d, f, dev, my + 12)
    return _fit(d, f, dev, y + ((6 + ncol - 1) // ncol) * (ch + 16) + 8)

# ======================================================================
# H23 · Relatórios
# ======================================================================
RELS = [
    ("Vendas", ["Vendas por período", "Produtos vendidos"]),
    ("Caixa", ["Fechamento", "Sangrias e suprimentos"]),
    ("Produtos e estoque", ["Listagem de produtos", "Estoque mínimo e reposição", "Produtos com alteração no preço", "Histórico de custo",
                            "Entrada e saída manual de estoque", "Transferências de estoque"]),
    ("Clientes", ["Listagem de clientes", "Contas a receber"]),
    ("Financeiro", ["Contas a pagar", "DRE", "Balancete", "Caixa geral", "Fluxo de caixa"]),
]

def _rel_card(d, p, x, y, w, cat, items, sel=None):
    h = 56 + len(items) * 40 + 8
    c = ui.card(d, p, x, y, w, h, title=cat)
    T(d, c, str(len(items)), w - 20, 18, size=12, color=C["muted"], lh=20, mono=True, align="right")
    yy = 52
    for i, it in enumerate(items):
        if it == sel:
            d.frame(c, "Linha selecionada", 8, yy, w - 16, 40, fill=C["sel"], stroke=C["ink"], radius=6)
        elif i:
            hair(d, c, 20, yy, w - 40)
        T(d, c, it, 20, yy + 10, size=14, lh=20, color=C["ink"] if it == sel else C["text2"])
        ui.icon(d, c, "seta-dir", w - 36, yy + 12, 16, C["ink"] if it == sel else C["muted"])
        yy += 40
    return h

def h23(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Relatórios", h=H0)
    y += _head(d, f, x, y, w, "Relatórios", "Dados reais e custo real do produto · emitido por Lucas",
               [("Pré-visualizar", "primary", "Enter", "olho")], dev)
    # filtros: período e operador
    if dev == "mobile":
        fw = (w - 8) / 2
        ui.field(d, f, x, y, fw, label="De", value="01/11/2026", mono=True, app=APP)
        ui.field(d, f, x + fw + 8, y, fw, label="Até", value="24/11/2026", mono=True, app=APP); y += 68
        ui.field(d, f, x, y, w, label="Operador", value="Todos", chevron=True, app=APP); y += 76
    else:
        ui.field(d, f, x, y, 160, label="De", value="01/11/2026", mono=True, app=APP)
        ui.field(d, f, x + 172, y, 160, label="Até", value="24/11/2026", mono=True, app=APP)
        ui.field(d, f, x + 344, y, 220, label="Operador", value="Todos", chevron=True, app=APP)
        sh = ["Hoje", "7 dias", "Este mês", "Mês passado"]
        bx = x + 580
        for i, s in enumerate(sh):
            if dev == "tablet" and i > 1: break
            b, bw = ui.button(d, f, bx, y + 20, s, app=APP, kind="secondary" if i != 2 else "dark", h=40)
            bx += bw + 8
        y += 84
    sel = "Vendas por período"
    if dev == "mobile":
        for cat, items in RELS:
            y += _rel_card(d, f, x, y, w, cat, items, sel) + 12
        return _fit(d, f, dev, y + 12)
    ncol = 3 if dev == "desktop" else 2
    cw = (w - 16 * (ncol - 1)) / ncol
    layout = [[0, 1], [2], [3, 4]] if ncol == 3 else [[0, 1, 3], [2, 4]]
    yend = y
    for ci, idxs in enumerate(layout):
        yy = y
        for i in idxs:
            yy += _rel_card(d, f, x + ci * (cw + 16), yy, cw, RELS[i][0], RELS[i][1], sel) + 16
        yend = max(yend, yy)
    return _fit(d, f, dev, yend + 8)

# ======================================================================
# H24 · Pré-visualizar relatório (Vendas por período)
# ======================================================================
PAGTOS = [("Dinheiro", 214, 12480.50, "21,4%"), ("PIX", 388, 24910.30, "42,7%"), ("Débito", 121, 7844.20, "13,4%"),
          ("Crédito", 96, 10236.90, "17,5%"), ("PRAZO", 18, 2316.40, "4,0%"), ("Crédito do cliente", 9, 590.00, "1,0%")]
VENDAS = [
    ("01/11 08:12", "DAV 004902", "Consumidor", "Arthur", "PIX", 37.00), ("01/11 08:31", "NFC-e 1.104", "Mariana Albuquerque", "Arthur", "Crédito", 289.00),
    ("01/11 09:05", "DAV 004903", "Consumidor", "Ana", "Dinheiro", 15.00), ("01/11 09:18", "DAV 004904", "João Victor Sampaio", "Ana", "PIX", 79.90),
    ("01/11 09:44", "DAV 004905", "Consumidor", "Arthur", "Débito", 46.00), ("01/11 10:02", "NFC-e 1.105", "Consumidor", "Arthur", "PIX", 12.00),
    ("01/11 10:27", "DAV 004906", "Tabacaria do Porto Ltda", "Ana", "PRAZO", 480.00), ("01/11 10:55", "DAV 004907", "Consumidor", "Ana", "Dinheiro", 25.00),
    ("01/11 11:13", "DAV 004908", "Larissa Menezes", "Arthur", "PIX", 63.90), ("01/11 11:40", "DAV 004909", "Consumidor", "Arthur", "Dinheiro", 10.00),
    ("01/11 12:06", "NFC-e 1.106", "Rafael Coelho Nunes", "Ana", "Débito", 120.00), ("01/11 12:31", "DAV 004910", "Consumidor", "Ana", "PIX", 32.00),
    ("01/11 13:02", "DAV 004911", "Consumidor", "Arthur", "Crédito", 45.00), ("01/11 13:20", "DAV 004912", "Pedro Henrique Brandão", "Arthur", "PIX", 18.00),
    ("01/11 13:48", "DAV 004913", "Consumidor", "Ana", "Dinheiro", 7.00), ("01/11 14:15", "DAV 004914", "Consumidor", "Ana", "PIX", 39.90),
    ("01/11 14:37", "NFC-e 1.107", "Carlos Eduardo Ribeiro", "Arthur", "Crédito", 334.00), ("01/11 15:01", "DAV 004915", "Consumidor", "Arthur", "Dinheiro", 20.00),
    ("01/11 15:26", "DAV 004916", "Consumidor", "Ana", "PIX", 8.00), ("01/11 15:52", "DAV 004917", "Bianca Torres Lima", "Ana", "Crédito do cliente", 50.00),
]

def _sheet(d, f, x, y, w, h, dev):
    """Folha A4 do relatório (a 100% no computador e no tablet; ajustada à largura no celular)."""
    s = d.frame(f, "Folha A4 · página 1 de 3", x, y, w, h, fill="#ffffff", stroke=C["line"], stroke_opacity=ui.LINE_A,
                shadow=ui.shadow(0.06, 8, 24), clip=True)
    m = 56 if dev != "mobile" else 16
    iw = w - 2 * m
    yy = m - 8 if dev != "mobile" else 16
    small = dev == "mobile"
    T(d, s, "Smoke House Tabacaria", m, yy, size=16 if not small else 13, weight=500, lh=22 if not small else 18)
    T(d, s, "Loja PNZ · Petrolina-PE · CNPJ a informar", m, yy + (24 if not small else 20), size=11, color=C["muted"], lh=16)
    if not small:
        T(d, s, "Vendas por período", m + iw, yy, size=16, weight=500, lh=22, align="right")
        T(d, s, "01/11/2026 a 24/11/2026 · Operador: Todos", m + iw, yy + 24, size=11, color=C["text2"], lh=16, align="right")
        T(d, s, "Emitido por Lucas em 24/11/2026 14:40", m + iw, yy + 40, size=11, color=C["muted"], lh=16, align="right")
        yy += 72
    else:
        T(d, s, "Vendas por período", m, yy + 44, size=13, weight=500, lh=18)
        T(d, s, "01/11 a 24/11/2026 · Operador: Todos", m, yy + 64, size=11, color=C["text2"], lh=16)
        T(d, s, "Emitido por Lucas em 24/11/2026 14:40", m, yy + 80, size=11, color=C["muted"], lh=16)
        yy += 108
    d.frame(s, "Linha", m, yy, iw, 1, fill=C["ink"])
    yy += 16
    T(d, s, "Faturado por forma de pagamento", m, yy, size=12, weight=500, lh=16); yy += 24
    def row(cells, xs, aligns, yy, bold=False, color=None):
        for cval, cx_, al in zip(cells, xs, aligns):
            T(d, s, cval, cx_, yy, size=11, lh=16, mono=al == "right", align=al, weight=500 if bold else 400, color=color or C["ink"])
    if not small:
        xs = [m, m + 300, m + 460, m + iw]; al = ["left", "right", "right", "right"]
        row(["Forma", "Pagamentos", "Valor", "%"], xs, al, yy, color=C["muted"]); yy += 20
        for fm, n, val, pc in PAGTOS:
            hair(d, s, m, yy - 2, iw)
            row([fm, str(n), v(val), pc], xs, al, yy + 2); yy += 22
        d.frame(s, "Linha", m, yy - 2, iw, 1, fill=C["ink"])
        row(["Total", "846", "58.378,30", "100,0%"], xs, al, yy + 2, bold=True); yy += 40
        T(d, s, "Vendas", m, yy, size=12, weight=500, lh=16); yy += 24
        xs = [m, m + 92, m + 196, m + 396, m + 476, m + iw]; al = ["left", "left", "left", "left", "left", "right"]
        row(["Data", "Documento", "Cliente", "Operador", "Forma", "Total"], xs, al, yy, color=C["muted"]); yy += 20
        for vd in VENDAS:
            hair(d, s, m, yy - 2, iw)
            row([vd[0], vd[1], vd[2], vd[3], vd[4], v(vd[5])], xs, al, yy + 2); yy += 22
    else:
        xs = [m, m + iw]; al = ["left", "right"]
        for fm, n, val, pc in PAGTOS:
            row([f"{fm} · {pc}", v(val)], xs, al, yy); yy += 20
        d.frame(s, "Linha", m, yy, iw, 1, fill=C["ink"]); yy += 6
        row(["Total", "58.378,30"], xs, al, yy, bold=True); yy += 32
        T(d, s, "Vendas", m, yy, size=12, weight=500, lh=16); yy += 22
        for vd in VENDAS:
            if yy > h - 52: break
            row([f"{vd[0][:5]} {vd[1]}", v(vd[5])], xs, al, yy); yy += 20
    if h < 1200:
        T(d, s, "Página 1 de 3", m + iw, h - m + 16 if dev != "mobile" else h - 28, size=11, color=C["muted"], lh=16, align="right")

def h24(d, f, dev, app):
    W, H = DEVICES[dev]
    top = ui.topbar(d, f, dev, APP, user="Lucas")
    pad = PAD[dev]
    tb = d.frame(f, "Barra da pré-visualização", 0, top, W, 64 if dev != "mobile" else 112, fill=C["card"])
    th = d.nodes[tb]["height"]
    hair(d, tb, 0, th - 1, W)
    d.frame(f, "Fundo", 0, top + th, W, H - top - th, fill=C["deep"])
    if dev == "mobile":
        T(d, tb, "Vendas por período", pad, 10, size=15, weight=500, lh=20)
        T(d, tb, "01/11 a 24/11/2026 · Todos", pad, 30, size=12, color=C["muted"], lh=16)
        cb = d.frame(tb, "Fechar", W - pad - 52, 12, 52, 28, radius=ui.R_CTL)
        ui.icon(d, cb, "fechar", 0, 6, 16, C["muted"]); ui.keycap(d, cb, 22, 4, "Esc")
        yy = 60
        ui.icon(d, tb, "seta-esq", pad, yy + 12, 16, C["muted"])
        T(d, tb, "1 de 3", pad + 24, yy + 10, size=13, lh=20, mono=True)
        ui.icon(d, tb, "seta-dir", pad + 80, yy + 12, 16, C["text2"])
        bx = W - pad
        for lab, kind in (("Imprimir", "primary"), ("Excel", "secondary"), ("PDF", "secondary")):
            b, bw = ui.button(d, tb, 0, yy, lab, app=APP, kind=kind, h=40)
            bx -= bw; d.nodes[b]["transform"][4] = float(bx); bx -= 8
        sw = W - 2 * pad
        _sheet(d, f, pad, top + th + 16, sw, int(sw * 1.414), dev)
        T(d, f, "Ajustado à largura", W / 2, top + th + 16 + int(sw * 1.414) + 12, size=12, color=C["muted"], lh=16, align="center")
        return
    ui.icon(d, tb, "seta-esq", pad, 24, 16, C["text2"])
    T(d, tb, "Vendas por período", pad + 24, 12, size=15, weight=500, lh=20)
    T(d, tb, "01/11/2026 a 24/11/2026 · Operador: Todos", pad + 24, 32, size=12, color=C["muted"], lh=16)
    # páginas e zoom no centro
    cx = W / 2 - (150 if dev == "desktop" else 190)
    pg = d.frame(tb, "Páginas", cx, 12, 132, 40, fill=C["raised"], radius=ui.R_CTL)
    ui.icon(d, pg, "seta-esq", 12, 12, 16, C["muted"])
    T(d, pg, "1 de 3", 66, 10, size=13, lh=20, mono=True, align="center")
    ui.icon(d, pg, "seta-dir", 104, 12, 16, C["text2"])
    zm = d.frame(tb, "Zoom", cx + 144, 12, 132, 40, fill=C["raised"], radius=ui.R_CTL)
    ui.icon(d, zm, "menos", 12, 12, 16, C["text2"])
    T(d, zm, "100%", 66, 10, size=13, lh=20, mono=True, align="center")
    ui.icon(d, zm, "mais", 104, 12, 16, C["text2"])
    bx = W - pad
    cb = d.frame(tb, "Fechar", bx - 52, 18, 52, 28, radius=ui.R_CTL)
    ui.icon(d, cb, "fechar", 0, 6, 16, C["muted"]); ui.keycap(d, cb, 22, 4, "Esc")
    bx -= 52 + 16
    for lab, kind, ic in (("Imprimir", "primary", "impressora"), ("Excel", "secondary", "doc"), ("PDF", "secondary", "doc")):
        b, bw = ui.button(d, tb, 0, 12, lab, app=APP, kind=kind, icon_name=ic if dev == "desktop" else None)
        bx -= bw; d.nodes[b]["transform"][4] = float(bx); bx -= 8
    sw = 794
    _sheet(d, f, (W - sw) / 2, top + th + 24, sw, 1123, dev)

# ======================================================================
# H25 · Fiscal (configuração do que a NFC-e precisa, por loja)
# ======================================================================
def _fs_cert(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Certificado A1")
    ui.status(d, c, w - 20, 18, "Válido", "ok", align="right")
    yy = 56
    yy += ui.kv(d, c, 20, yy, w - 40, [("Titular", "SMOKE HOUSE TABACARIA LTDA"), ("CNPJ", "a informar"), ("Validade", "12/03/2027"),
                                         ("Dias restantes", "108")], mono_values=False)
    ui.button(d, c, 20, yy + 8, "Trocar certificado", app=APP, kind="secondary", icon_name="upload")
    d.nodes[c]["height"] = float(yy + 64)
    return yy + 64

def _fs_csc(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "CSC da loja")
    ui.status(d, c, w - 20, 18, "Cadastrado", "ok", align="right")
    yy = 56
    ui.field(d, c, 20, yy, 104, label="Id do CSC", value="000001", mono=True, app=APP)
    f_, _ = ui.field(d, c, 136, yy, w - 156, label="Código (CSC)", value="•••• •••• •••• •••• ••••" if w > 400 else "•••• •••• ••••", mono=True, app=APP, readonly=True)
    ui.icon(d, f_, "olho", w - 156 - 28, 12, 16, C["muted"])
    yy += 72
    T(d, c, "Cadastrado em 03/11/2026 por Lucas", 20, yy, size=12, color=C["muted"], lh=16)
    d.nodes[c]["height"] = float(yy + 36)
    return yy + 36

def _fs_amb(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Ambiente da SEFAZ")
    yy = 60
    ui.radio(d, c, 20, yy, on=False, label="Homologação", app=APP)
    ui.radio(d, c, 20 + 28 + fc.text_width("Homologação", 14) + 32, yy, on=True, label="Produção", app=APP)
    yy += 8
    d.nodes[c]["height"] = float(yy + 36)
    return yy + 36

def _fs_series(d, p, x, y, w, dev):
    T(d, p, "Séries da NFC-e por terminal", x, y, size=15, weight=500, lh=20)
    if dev == "mobile":
        _, hh = ui.mobile_rows(d, p, x, y + 32, w, [("Terminal 01 · série 1", "Próximo número 1.248", None, "Em uso", "ok"),
                                                    ("Terminal 02 · série 2", "Próximo número 873", None, "Em uso", "ok")])
        return 32 + hh
    cols = [("Terminal", None, "l"), ("Série", 56, "r", True), ("Próximo número", 132, "r", True), ("Situação", 100, "l")]
    nm = ("Terminal 01 · Arthur", "Terminal 02 · Ana") if dev == "desktop" else ("Terminal 01", "Terminal 02")
    t, th = ui.table(d, p, x, y + 32, w, cols, [[nm[0], "1", "000.001.248", ("Em uso", "ok")],
                                                 [nm[1], "2", "000.000.873", ("Em uso", "ok")]], app=APP)
    return 32 + th

def _fs_regime(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Regime e IBS/CBS")
    yy = 56
    ui.field(d, c, 20, yy, w - 40, label="Regime tributário", value="Simples Nacional", chevron=True, app=APP); yy += 72
    T(d, c, "Recolhimento do IBS e da CBS", 20, yy, size=13, color=C["text2"], lh=16); yy += 28
    ui.radio(d, c, 20, yy, on=True, label="Dentro do Simples Nacional", app=APP); yy += 32
    ui.radio(d, c, 20, yy, on=False, label="Por fora, no regime regular", app=APP); yy += 36
    hair(d, c, 20, yy, w - 40); yy += 16
    T(d, c, "Tabela de cClassTrib", 20, yy, size=14, lh=20)
    ui.status(d, c, w - 20, yy, "Atualizada", "ok", align="right")
    T(d, c, "Versão da tabela 1.03 · 15/10/2026", 20, yy + 22, size=12, color=C["muted"], lh=16)
    yy += 48
    ui.button(d, c, 20, yy, "Atualizar tabela", app=APP, kind="secondary", h=36)
    d.nodes[c]["height"] = float(yy + 56)
    return yy + 56

def _fs_cont(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Contingência")
    ui.status(d, c, w - 20, 18, "3 pendentes", "warn", align="right")
    yy = 56
    yy += ui.kv(d, c, 20, yy, w - 40, [("Notas pendentes de transmissão", "3"), ("Mais antiga", "24/11 08:14"), ("Prazo para transmitir", "25/11 08:14")])
    ui.button(d, c, 20, yy + 8, "Transmitir agora", app=APP, kind="secondary", icon_name="upload")
    d.nodes[c]["height"] = float(yy + 64)
    return yy + 64

def _fs_inut(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Inutilização de numeração")
    yy = 56
    if dev == "mobile":
        fw = (w - 40 - 16) / 3
    else:
        fw = (w - 40 - 16) / 3
    for i, (lab, val) in enumerate([("Série", "1"), ("Do número", "1.190"), ("Até o número", "1.190")]):
        ui.field(d, c, 20 + i * (fw + 8), yy, fw, label=lab, value=val, mono=True, app=APP)
    yy += 72
    ui.field(d, c, 20, yy, w - 40, label="Justificativa", value="Número pulado por rejeição da SEFAZ", app=APP); yy += 72
    T(d, c, "Última: série 2, nº 851 · 12/11/2026", 20, yy + 12, size=12, color=C["muted"], lh=16) if w > 400 else None
    b, bw = ui.button(d, c, 0, yy, "Inutilizar", app=APP, kind="secondary")
    d.nodes[b]["transform"][4] = float(w - 20 - bw)
    d.nodes[c]["height"] = float(yy + 60)
    return yy + 60

def h25(d, f, dev, app):
    H0 = 3000
    x, y, w, base = _shell(d, f, dev, "Fiscal", h=H0)
    y += _head(d, f, x, y, w, "Fiscal", "O que a NFC-e precisa, separado por loja", [("Salvar alterações", "primary", None, "ok")], dev) if dev != "mobile" else \
         _head(d, f, x, y, w, "Fiscal", "Configuração separada por loja", [], dev)
    ui.tabs(d, f, x, y, ["Loja PNZ · PE", "Loja LEM · BA"] if dev == "mobile" else ["Loja PNZ · Petrolina-PE", "Loja LEM · Luís Eduardo Magalhães-BA"], 0, app=APP)
    y += 60
    if dev == "mobile":
        for fn in (_fs_cert, _fs_csc, _fs_amb, _fs_series, _fs_regime, _fs_cont, _fs_inut):
            y += fn(d, f, x, y, w, dev) + 16
        ui.button(d, f, x, y + 8, "Salvar alterações", app=APP, kind="primary", w=w, h=44)
        return _fit(d, f, dev, y + 8 + 44 + 24)
    cw = (w - 24) / 2
    y1 = y
    for fn in (_fs_cert, _fs_csc, _fs_amb, _fs_cont):
        y1 += fn(d, f, x, y1, cw, dev) + 16
    y2 = y
    for fn in (_fs_series, _fs_regime, _fs_inut):
        y2 += fn(d, f, x + cw + 24, y2, cw, dev) + 16
    return _fit(d, f, dev, max(y1, y2) + 8)

SCREENS = [
    ("H13", "Contas a receber", h13),
    ("H14", "Ficha do cliente a prazo · Parcelas", h14),
    ("H14b", "Ficha do cliente a prazo · Compras a prazo", h14b),
    ("H14c", "Ficha do cliente a prazo · Pagamentos e recibos", h14c),
    ("H15", "Dar baixa", h15),
    ("H16", "Recibo", h16),
    ("H17", "Formas de pagamento", h17),
    ("H17b", "Nova forma de pagamento", h17b),
    ("H18", "Configurações", h18),
    ("H19", "Usuários e permissões", h19),
    ("H20", "Chamados", h20),
    ("H21", "Fornecedores", h21),
    ("H22", "Integrações", h22),
    ("H23", "Relatórios", h23),
    ("H24", "Pré-visualizar relatório", h24),
    ("H25", "Fiscal", h25),
]
