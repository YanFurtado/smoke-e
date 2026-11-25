"""HOST (Retaguarda), parte A: entrada, início, caixas, clientes e estoque (H01 a H12).

Padrão de página (igual em host_b.py): ui.host_shell + ui.page_head; quadros com ui.stat
(_stats faz a linha e o 2 × 2 do celular); tabelas com ui.table (_table2 põe duas linhas
numa célula); no celular as tabelas viram ui.mobile_rows.
Estoque só tem dois locais: Frente de loja e Fundo de loja.
"""
import fc, ui
from ui import C, T, brl, PAD, DEVICES, hair

PAGE = "03 · Retaguarda (HOST) · início, caixas, clientes e estoque"
APP = "host"
ACC = ui.APPS["host"]["acc"]
HOJE = "24/11/2026"


def _n(v):
    """Valor sem o R$ (para colunas de tabela), sinal à frente."""
    s = brl(abs(v))[3:]
    return ("-" if v < 0 else "") + s


def _q(v):
    """Quantidade com sinal."""
    return f"+{v}" if v > 0 else (f"-{abs(v)}" if v < 0 else "0")


# ---------- dados do estoque ----------
CUSTO = {"006264": 2.60, "006265": 2.60, "004118": 3.90, "004120": 8.40, "003301": 4.30, "003302": 5.60,
         "002210": 7.70, "002251": 182.00, "005510": 9.80, "005514": 9.80, "007702": 12.50, "007780": 22.00,
         "008801": 21.90, "009102": 41.00, "006290": 98.00, "004401": 18.50}
MIN_FR = {"006264": 20, "006265": 20, "004118": 20, "004120": 10, "003301": 15, "003302": 15, "002210": 10,
          "002251": 4, "005510": 10, "005514": 10, "007702": 6, "007780": 6, "008801": 6, "009102": 4,
          "006290": 3, "004401": 12}
MIN_FU = {k: v * 2 for k, v in MIN_FR.items()}
CATEG = {"006264": "Sedas", "006265": "Sedas", "004118": "Sedas", "004120": "Sedas", "003301": "Sedas",
         "003302": "Sedas", "006290": "Sedas", "002210": "Isqueiros", "002251": "Isqueiros", "005510": "Essências",
         "005514": "Essências", "007702": "Piteiras", "007780": "Dichavadores", "008801": "Bandejas",
         "009102": "Kits", "004401": "Carvão"}
CADASTRO = {"006264": "12/03/2025", "006265": "12/03/2025", "004118": "02/05/2025", "004120": "02/05/2025",
            "003301": "19/06/2025", "003302": "19/06/2025", "002210": "12/03/2025", "002251": "07/08/2025",
            "005510": "15/01/2026", "005514": "15/01/2026", "007702": "03/11/2026", "007780": "21/09/2025",
            "008801": "10/10/2025", "009102": "01/11/2026", "006290": "12/03/2025", "004401": "15/01/2026"}
INATIVOS = {"006290"}


def _sit(cod, qt, mn):
    if cod in INATIVOS:
        return ("Inativo", "muted")
    return ("Repor", "warn") if qt < mn else ("Normal", "ok")


def _colx(w, cols):
    fixed = sum(c[1] for c in cols if c[1])
    flex = [c for c in cols if not c[1]]
    rest = max(40, (w - 32 - fixed) / max(1, len(flex)))
    xs, cx = [], 16
    for c in cols:
        cw = c[1] or rest
        xs.append((cx, cw))
        cx += cw
    return xs


def _table2(d, p, x, y, w, cols, rows, two, selected=None, row_h=56, dim_rows=(), sub_mono=False):
    """ui.table com células de duas linhas. two = {coluna: [(título, sub), ...]}."""
    rr = [list(r) for r in rows]
    for ci in two:
        for r in rr:
            r[ci] = ""
    t, th = ui.table(d, p, x, y, w, cols, rr, selected=selected, row_h=row_h, app=APP, dim_rows=dim_rows)
    xs = _colx(w, cols)
    for ci, vals in two.items():
        cx, cw = xs[ci]
        g = 0 if ci == 0 else 8
        for i, (a, b) in enumerate(vals):
            yy = 36 + i * row_h + (row_h - 36) / 2
            T(d, t, a, cx + g, yy, size=13, color=C["muted"] if i in dim_rows else C["ink"], lh=18)
            if b:
                T(d, t, b, cx + g, yy + 19, size=12, color=C["muted"], lh=16, mono=sub_mono)
    return t, th


def _stats(d, p, x, y, w, items, dev):
    """Linha de quadros (ui.stat). items: (rótulo, valor, nota, tom, rótulo curto do celular)."""
    items = [tuple(list(it) + [None] * (5 - len(it))) for it in items]
    if dev == "mobile":
        cw = (w - 8) / 2
        h = 96
        for i, (lab, val, note, tone, short) in enumerate(items):
            cx, cy = x + (i % 2) * (cw + 8), y + (i // 2) * (h + 8)
            c = ui.box(d, p, cx, cy, cw, h, fill=C["card"], name=f"Quadro {lab}")
            T(d, c, short or lab, 16, 14, size=12, color=C["text2"], lh=16)
            T(d, c, val, 16, 36, size=22, weight=500, lh=28, color=C["neg"] if tone == "neg" else C["ink"])
            if note:
                T(d, c, note, 16, 68, size=12, color=C["muted"], lh=16)
        rows = (len(items) + 1) // 2
        return rows * (h + 8) - 8
    gap = 16 if dev == "desktop" else 12
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, (lab, val, note, tone, short) in enumerate(items):
        ui.stat(d, p, x + i * (cw + gap), y, cw, lab, val, note, tone=tone)
    return 104


def _ttl(d, p, x, y, s, right=None, rx=None, size=15):
    T(d, p, s, x, y, size=size, weight=500, lh=20)
    if right:
        T(d, p, right, rx, y, size=13, color=C["muted"], lh=20, align="right")


def _shell(d, f, dev, active, h=None):
    if h:
        d.nodes[f]["height"] = float(h)
    x, y, w, _ = ui.host_shell(d, f, dev, active)
    base = (h or DEVICES[dev][1]) - (16 if dev == "mobile" else 24)
    return x, y, w, base


def _auto(d, f, dev, active, body):
    """Desenha a página com a altura que o conteúdo pede (mede antes num documento de rascunho)."""
    td = fc.Doc("medida"); pg = td.page("m")
    tf = td.frame(pg, "m", 0, 0, *DEVICES[dev])
    x, y, w, _ = ui.host_shell(td, tf, dev, active)
    end = body(td, tf, dev, x, y, w)
    H = max(DEVICES[dev][1], int(end))
    x, y, w, base = _shell(d, f, dev, active, h=H)
    body(d, f, dev, x, y, w)
    return H


def _btn_disable(d, win, label):
    for cid in d.nodes[win].get("children", []):
        if d.nodes[cid].get("name") == f"Botão {label}":
            d.nodes[cid]["opacity"] = 0.45


def _arrow(d, p, x, y, color=None):
    """Seta → desenhada (rota entre os estoques)."""
    c = color or C["muted"]
    d.polyline(p, [(x, y + 8), (x + 14, y + 8)], c, weight=1.5, name="Seta")
    d.polyline(p, [(x + 9, y + 3), (x + 14, y + 8), (x + 9, y + 13)], c, weight=1.5, name="Seta")


# =====================================================================
# H01 · Entrar no HOST
# =====================================================================
def h01(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    cw = W - 32 if mob else 400
    ch = 452
    cx = (W - cw) / 2
    cy = 72 if mob else (H - ch) / 2 - 16
    c = d.frame(f, "Cartão Entrar", cx, cy, cw, ch, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A,
                radius=ui.R_CARD if mob else ui.R_WIN)
    pad = 24 if mob else 32
    d.image(c, ui.os.path.join(ui.HERE, "marca", "logo-verde.png"), pad, pad, 55, 48, name="Logo Smoke House")
    T(d, c, "Smoke House", pad + 68, pad + 4, size=15, weight=500, lh=20)
    d.ellipse(c, pad + 68, pad + 30, 8, ACC, name="Cor HOST")
    T(d, c, "Retaguarda", pad + 82, pad + 25, size=13, color=C["text2"], lh=18)
    y = pad + 80
    T(d, c, "Entrar", pad, y, size=20 if mob else 24, weight=500, lh=32)
    y += 48
    fw = cw - 2 * pad
    _, hh = ui.field(d, c, pad, y, fw, label="Usuário", value="Lucas", chevron=True, app=APP)
    y += hh + 16
    _, hh = ui.field(d, c, pad, y, fw, label="Senha", value="••••", focused=True, app=APP, mono=True)
    y += hh + 24
    ui.button(d, c, pad, y, "Entrar", app=APP, kind="primary", w=fw, h=44, key="Enter")
    y += 44 + 24
    hair(d, c, pad, y, fw)
    T(d, c, "Loja PNZ · Petrolina-PE", pad, y + 16, size=12, color=C["muted"], lh=16)
    T(d, c, "Versão 1.2.02", pad + fw, y + 16, size=12, color=C["muted"], lh=16, mono=True, align="right")
    d.nodes[c]["height"] = float(y + 48)
    if not mob:
        T(d, f, "Servidor conectado", W / 2 + 6, H - 40, size=12, color=C["text2"], lh=16, align="center")
        d.ellipse(f, W / 2 - fc.text_width("Servidor conectado", 12) / 2 - 10, H - 36, 8, C["pos"], name="Situação do servidor")


# ---------- H01b · Aviso de chamados ao entrar ----------
CHAMADOS = [
    ("Etiqueta de preço errada na gôndola 2", "Preço", "Ana para Lucas", "hoje 09:12"),
    ("Impressora do Terminal 02 falhando", "Equipamento", "Carla para Lucas", "ontem 18:40"),
    ("Conferir sangria de 22/11 do Terminal 01", "Caixa", "Carla para Lucas", "22/11 21:05"),
]


def h01b(d, f, dev, app):
    h02(d, f, dev, app)
    mob = dev == "mobile"
    w = 560 if not mob else DEVICES["mobile"][0]
    win, w, h, top, bot = ui.window(d, f, dev, "Chamados pendentes", w, 64 + 24 + 3 * 72 + 16 + 72, app=APP,
                                    footer_buttons=[("Depois", "secondary", None), ("Ver chamados", "primary", "Enter")])
    y = top + 16
    for i, (tit, cat, quem, quando) in enumerate(CHAMADOS):
        r = d.frame(win, f"Chamado {i + 1}", 16, y, w - 32, 68, fill=None, radius=ui.R_CTL)
        q = d.frame(r, "Ícone", 8, 14, 32, 32, fill=C["raised"], radius=ui.R_CTL)
        ui.icon(d, q, "chat", 8, 8, 16, C["text2"])
        T(d, r, tit, 52, 12, size=14, weight=500, lh=20, w=w - 32 - 52 - 16)
        T(d, r, f"{cat} · {quem} · {quando}", 52, 36, size=12, color=C["muted"], lh=16, w=w - 32 - 52 - 16)
        if i < 2:
            hair(d, win, 68, y + 70, w - 92)
        y += 72


# =====================================================================
# H02 · Início
# =====================================================================
FORMAS = [("Pix", 1284.30), ("Dinheiro", 742.00), ("Débito", 618.40), ("Crédito", 590.80), ("PRAZO", 214.00),
          ("Crédito do cliente", 33.00)]
VENDIDO = sum(v for _, v in FORMAS)


def _repor_lista():
    out = []
    for p in ui.PRODUTOS:
        if p[0] in INATIVOS:
            continue
        if p[4] < MIN_FR[p[0]]:
            out.append(p)
    return out


def _formas_card(d, p, x, y, w, h, dev):
    c = ui.card(d, p, x, y, w, h, title="Vendas por forma de pagamento", app=APP)
    pad = 20
    if dev != "mobile":
        T(d, c, brl(VENDIDO), w - pad, 18, size=13, color=C["muted"], lh=20, align="right", mono=True)
    yy = 60
    step = 52 if dev == "mobile" else max(52, int((h - 60 - 72) // len(FORMAS)))
    mx = max(v for _, v in FORMAS)
    for nome, v in FORMAS:
        pct = v / VENDIDO * 100
        T(d, c, nome, pad, yy, size=14, lh=20)
        T(d, c, brl(v), w - pad - 64, yy, size=13, lh=20, mono=True, align="right")
        T(d, c, f"{pct:.1f}%".replace(".", ","), w - pad, yy, size=13, color=C["muted"], lh=20, mono=True, align="right")
        bw = w - 2 * pad
        d.frame(c, "Trilho", pad, yy + 26, bw, 6, fill=C["raised"], radius=3)
        d.frame(c, f"Barra {nome}", pad, yy + 26, max(6, bw * v / mx), 6, fill=C["text2"], radius=3)
        yy += step
    hair(d, c, pad, yy + 2, w - 2 * pad)
    T(d, c, "NFC-e emitidas", pad, yy + 16, size=14, color=C["text2"], lh=20)
    ui.status(d, c, w - pad, yy + 16, "Aguarda integração fiscal", "muted", align="right")
    return yy + 52


def _chamados_card(d, p, x, y, w, dev):
    n = len(CHAMADOS)
    h = 56 + n * 64 + 8
    c = ui.card(d, p, x, y, w, h, title="Chamados pendentes", app=APP)
    T(d, c, str(n), 20 + fc.text_width("Chamados pendentes", 15, 500) + 8, 19, size=12, color=C["muted"], lh=16, mono=True)
    ui.button(d, c, w - 20 - 84, 12, "Ver todos", app=APP, kind="ghost", w=84, h=32)
    yy = 56
    for i, (tit, cat, quem, quando) in enumerate(CHAMADOS):
        T(d, c, tit, 20, yy + 8, size=14, lh=20, w=w - 40)
        T(d, c, f"{cat} · {quem.split(' para ')[0]} · {quando}", 20, yy + 30, size=12, color=C["muted"], lh=16)
        if i < n - 1:
            hair(d, c, 20, yy + 60, w - 40)
        yy += 64
    return h


def _repor_card(d, p, x, y, w, dev, h=None):
    lst = _repor_lista()
    rh = 40
    h = h or 56 + len(lst) * rh + 8
    c = ui.card(d, p, x, y, w, h, title="Para repor na frente", app=APP)
    T(d, c, "14", 20 + fc.text_width("Para repor na frente", 15, 500) + 8, 19, size=12, color=C["muted"], lh=16, mono=True)
    ui.button(d, c, w - 20 - 112, 12, "Abrir estoque", app=APP, kind="ghost", w=112, h=32)
    T(d, c, "Frente / mín.", w - 20, 52, size=12, color=C["muted"], lh=16, align="right")
    yy = 72
    for i, p in enumerate(lst[: int((h - 80) // rh)]):
        T(d, c, p[2], 20, yy + 10, size=13, lh=20)
        T(d, c, f"{p[4]}/{MIN_FR[p[0]]}", w - 20, yy + 10, size=13, lh=20, mono=True, align="right",
          color=C["neg"] if p[4] == 0 else C["ink"])
        if i < len(lst) - 1:
            hair(d, c, 20, yy + rh, w - 40)
        yy += rh
    return h


def _hoje_card(d, p, x, y, w, dev):
    abertos = 2
    items = [("Vendido", brl(VENDIDO), "PRAZO líquido incluído"), ("Vendas", "47", "DAV 41 · NFC-e 6"),
             ("Caixas abertos", str(abertos), "Terminal 01 · Terminal 02"), ("Produtos para repor", "14", "na frente de loja")]
    if dev == "mobile":
        T(d, p, "Hoje", x, y, size=15, weight=500, lh=20)
        return 28 + _stats(d, p, x, y + 28, w, [(a, b, c_) for a, b, c_ in items], dev)
    h = 148
    c = ui.card(d, p, x, y, w, h, title="Hoje", app=APP)
    T(d, c, "atualizado às 17:42", w - 20, 18, size=12, color=C["muted"], lh=20, align="right")
    cw = (w - 40) / 4
    for i, (lab, val, note) in enumerate(items):
        cx = 20 + i * cw
        if i:
            d.frame(c, "Divisa", cx - 1, 60, 1, 68, fill=C["line"], fill_opacity=ui.LINE_A)
        px = cx + (20 if i else 0)
        T(d, c, lab, px, 56, size=13, color=C["text2"], lh=20)
        T(d, c, val, px, 80, size=28, weight=500, lh=32)
        T(d, c, note, px, 116, size=12, color=C["muted"], lh=16)
    return h


def h02(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Início")
    hh = ui.page_head(d, f, x, y, w, "Início", "Segunda, 24 de novembro de 2026 · Loja PNZ",
                      actions=[("Etiquetas", "secondary", None, "impressora")], device=dev)
    y += hh + (8 if dev != "mobile" else 4)
    if dev == "mobile":
        ui.button(d, f, x, y, "Etiquetas", app=APP, kind="secondary", w=w, icon_name="impressora")
        y += 56
        y += _hoje_card(d, f, x, y, w, dev) + 16
        y += _formas_card(d, f, x, y, w, 10 + 60 + 6 * 50 + 56, dev) + 16
        y += _chamados_card(d, f, x, y, w, dev) + 16
        y += _repor_card(d, f, x, y, w, dev) + 16
        return y
    y += _hoje_card(d, f, x, y, w, dev) + 16
    gap = 16
    rw = 400 if dev == "desktop" else 340
    lw = w - rw - gap
    ch = _chamados_card(d, f, x + lw + gap, y, rw, dev)
    _repor_card(d, f, x + lw + gap, y + ch + gap, rw, dev, h=base - (y + ch + gap))
    _formas_card(d, f, x, y, lw, base - y, dev)


# =====================================================================
# H03 · Caixas
# =====================================================================
CAIXAS = [  # terminal, operador, abertura, fechamento, vendido, situação
    ("Terminal 01", "Arthur", "07:58", "—", 1846.20, ("Aberto", "info")),
    ("Terminal 02", "Ana", "08:02", "13:10", 1012.30, ("Com divergência", "warn")),
    ("Terminal 02", "Carla", "13:24", "—", 624.00, ("Aberto", "info")),
]
CONF = [  # forma, sistema, informado
    ("Dinheiro", 412.00, 402.00), ("Pix", 318.40, 318.40), ("Débito", 146.90, 146.90), ("Crédito", 85.00, 85.00),
    ("PRAZO", 50.00, 50.00), ("Crédito do cliente", 0.00, 0.00),
]


def _conf_panel(d, p, x, y, w, h, dev):
    c = ui.card(d, p, x, y, w, h, app=APP)
    pad = 20
    T(d, c, "Caixa de Ana · aberto às 08:02 · 24/11/2026", pad, 18, size=15, weight=500, lh=20, w=w - 2 * pad)
    nl = 1 if fc.text_width("Caixa de Ana · aberto às 08:02 · 24/11/2026", 15, 500) < w - 2 * pad else 2
    yy = 18 + 20 * nl + 4
    T(d, c, "Terminal 02 · fechado às 13:10 pelo DAV", pad, yy, size=12, color=C["muted"], lh=16)
    yy += 32
    # conferência
    xs = [pad, w - pad - 2 * 92 - 8, w - pad - 92 - 4, w - pad]
    if dev == "mobile":
        xs = [pad, w - pad - 2 * 76 - 8, w - pad - 76 - 4, w - pad]
    T(d, c, "Forma", xs[0], yy, size=12, color=C["muted"], lh=16)
    T(d, c, "Sistema", xs[1], yy, size=12, color=C["muted"], lh=16, align="right")
    T(d, c, "Informado", xs[2], yy, size=12, color=C["muted"], lh=16, align="right")
    T(d, c, "Diferença", xs[3], yy, size=12, color=C["muted"], lh=16, align="right")
    yy += 24
    hair(d, c, pad, yy, w - 2 * pad)
    rh = 36
    for forma, s, i_ in CONF:
        df = i_ - s
        T(d, c, forma, xs[0], yy + 8, size=13, lh=20)
        T(d, c, _n(s), xs[1], yy + 8, size=13, lh=20, mono=True, align="right")
        T(d, c, _n(i_), xs[2], yy + 8, size=13, lh=20, mono=True, align="right")
        T(d, c, _n(df) if df else "0,00", xs[3], yy + 8, size=13, lh=20, mono=True, align="right",
          color=C["neg"] if df < 0 else (C["muted"] if not df else C["pos"]))
        yy += rh
        hair(d, c, pad, yy, w - 2 * pad)
    ts = sum(s for _, s, _ in CONF)
    ti = sum(i for *_, i in CONF)
    T(d, c, "Total", xs[0], yy + 10, size=13, weight=500, lh=20)
    T(d, c, _n(ts), xs[1], yy + 10, size=13, weight=500, lh=20, mono=True, align="right")
    T(d, c, _n(ti), xs[2], yy + 10, size=13, weight=500, lh=20, mono=True, align="right")
    T(d, c, _n(ti - ts), xs[3], yy + 10, size=13, weight=500, lh=20, mono=True, align="right", color=C["neg"])
    yy += 48
    # divergência lançada
    meta = "Lançada por Ana às 13:08 · desfazer até 23:59 de hoje"
    dh = 84 if fc.text_width(meta, 12) < w - 2 * pad - 32 else 100
    dv = d.frame(c, "Divergência", pad, yy, w - 2 * pad, dh, fill=C["page"], stroke=C["warn"], stroke_opacity=0.35, radius=ui.R_CTL)
    d.frame(dv, "Faixa", 0, 0, 3, dh, fill=C["warn"], radius=[ui.R_CTL, 0, 0, ui.R_CTL])
    T(d, dv, "Divergência em Dinheiro · -R$ 10,00", 16, 10, size=14, weight=500, lh=20)
    T(d, dv, "Motivo: troco dado a mais", 16, 32, size=13, color=C["text2"], lh=20)
    T(d, dv, meta, 16, 54, size=12, color=C["muted"], lh=16, w=w - 2 * pad - 32)
    yy += dh + 20
    if dev == "mobile":
        ui.button(d, c, pad, yy, "Comprovante", app=APP, kind="secondary", w=w - 2 * pad, icon_name="impressora")
        yy += 48
        ui.button(d, c, pad, yy, "Desfazer divergência", app=APP, kind="danger", w=w - 2 * pad, icon_name="voltar")
    else:
        bw = (w - 2 * pad - 8) / 2
        ui.button(d, c, pad, yy, "Comprovante", app=APP, kind="secondary", w=bw, icon_name="impressora")
        ui.button(d, c, pad + bw + 8, yy, "Desfazer divergência", app=APP, kind="danger", w=bw, icon_name="voltar")
    d.nodes[c]["height"] = float(yy + 40 + 20)
    return yy + 40 + 20


def h03(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Caixas")
    hh = ui.page_head(d, f, x, y, w, "Caixas", "Caixas do dia e os abertos · só leitura", device=dev)
    if dev != "mobile":
        fw = 168
        ui.field(d, f, x + w - fw, y + 4, fw, value=HOJE, mono=True, app=APP, prefix_icon="calendario")
    y += hh + 8
    if dev == "mobile":
        ui.field(d, f, x, y, w, value=HOJE, mono=True, app=APP, prefix_icon="calendario")
        y += 56
        rows = [(f"{t} · {o}", f"{a} às {fe}" if fe != "—" else f"aberto às {a}", brl(v), s[0], s[1]) for t, o, a, fe, v, s in CAIXAS]
        _, lh = ui.mobile_rows(d, f, x, y, w, rows, selected=1)
        y += lh + 8
        T(d, f, "Total do dia", x, y, size=13, color=C["text2"], lh=20)
        T(d, f, brl(sum(c[4] for c in CAIXAS)), x + w, y, size=13, weight=500, lh=20, mono=True, align="right")
        y += 40
        y += _conf_panel(d, f, x, y, w, 10, dev)
        return y + 16
    lw = 640 if dev == "desktop" else 468
    if dev == "desktop":
        cols = [("Terminal", 100, "l"), ("Operador", None, "l"), ("Abertura", 76, "r", True), ("Fechamento", 92, "r", True),
                ("Vendido", 100, "r", True), ("Situação", 148, "l")]
        rows = [[t, o, a, fe, _n(v), s] for t, o, a, fe, v, s in CAIXAS]
    else:
        cols = [("Terminal", 100, "l"), ("Operador", None, "l"), ("Vendido", 100, "r", True), ("Situação", 144, "l")]
        rows = [[t, o, _n(v), s] for t, o, a, fe, v, s in CAIXAS]
    t, th = ui.table(d, f, x, y, lw, cols, rows, selected=1, app=APP)
    tot = sum(c[4] for c in CAIXAS)
    T(d, f, "Total do dia", x + 16, y + th + 14, size=13, color=C["text2"], lh=20)
    xs = _colx(lw, cols)
    vi = [c[0] for c in cols].index("Vendido")
    T(d, f, _n(tot), x + xs[vi][0] + xs[vi][1] - 8, y + th + 14, size=13, weight=500, lh=20, mono=True, align="right")
    T(d, f, "Soma igual ao relatório Vendas por período", x + 16, y + th + 38, size=12, color=C["muted"], lh=16)
    px = x + lw + 16
    pw = w - lw - 16
    _conf_panel(d, f, px, y, pw, 10, dev)


# =====================================================================
# H04 · Clientes
# =====================================================================
CLI = [  # nome, cidade, telefone, última compra, compras, total, situação
    ("Mariana Albuquerque", "Petrolina-PE", "(87) 98841-2207", "24/11/2026", 38, 2418.60, ("VIP", "ok")),
    ("Rafael Coelho Nunes", "Juazeiro-BA", "(87) 99102-7754", "22/11/2026", 21, 1104.50, ("Recorrente", "info")),
    ("Tabacaria do Porto Ltda", "Petrolina-PE", "(87) 3861-4410", "20/11/2026", 64, 8932.00, ("VIP", "ok")),
    ("João Victor Sampaio", "Petrolina-PE", "(87) 98122-0451", "19/10/2026", 7, 312.40, ("Sumido", "warn")),
    ("Larissa Menezes", "Juazeiro-BA", "(87) 99643-1180", "02/09/2026", 4, 158.00, ("Inativo", "muted")),
    ("Pedro Henrique Brandão", "Petrolina-PE", "(87) 98810-3369", "23/11/2026", 2, 96.00, ("Novo", "info")),
    ("Camila Torres Ribeiro", "Lagoa Grande-PE", "(87) 99877-1402", "21/11/2026", 15, 688.20, ("Recorrente", "info")),
    ("Diego Araújo Lins", "Petrolina-PE", "(87) 98455-9031", "18/11/2026", 9, 402.00, ("Bloqueado", "neg")),
]
COMPRAS_MARI = [("24/11/2026", "DAV 004871", 76.00), ("17/11/2026", "DAV 004702", 54.00), ("10/11/2026", "NFC-e 000.331", 118.90),
                ("03/11/2026", "DAV 004433", 41.00), ("27/10/2026", "DAV 004290", 95.00)]


def _ficha(d, p, x, y, w, h, dev):
    c = ui.card(d, p, x, y, w, h, app=APP)
    pad = 20
    iw = w - 2 * pad
    ui.avatar(d, c, pad, pad, 40, "Mariana Albuquerque")
    T(d, c, "Mariana Albuquerque", pad + 52, pad, size=15, weight=500, lh=20)
    T(d, c, "Petrolina-PE · cliente desde 03/2024", pad + 52, pad + 22, size=12, color=C["muted"], lh=16)
    yy = pad + 56
    sx = pad
    for lab, tone in (("VIP", "ok"), ("Recorrente", "info"), ("Aniversário em 3 dias" if dev == "desktop" else "Aniversário", "warn")):
        sx += ui.status(d, c, sx, yy, lab, tone) + 14
    yy += 32
    hair(d, c, pad, yy, iw)
    yy += 12
    if dev == "desktop":
        kvr = [("CPF", "123.456.789-09"), ("E-mail", "mariana.alb@gmail.com"), ("Nascimento", "27/11/1994 · 31 anos")]
    else:
        kvr = [("CPF", "123.456.789-09"), ("Nascimento", "27/11/1994"), ("Compras", "38"), ("Total gasto", brl(2418.60))]
    yy += ui.kv(d, c, pad, yy, iw, kvr, gap=22, mono_values=False) + 6
    hair(d, c, pad, yy, iw)
    yy += 12
    if dev == "desktop":
        cw3 = iw / 3
        for i, (lab, val) in enumerate((("Compras", "38"), ("Total gasto", brl(2418.60)), ("Ticket médio", brl(63.65)))):
            T(d, c, lab, pad + i * cw3, yy, size=12, color=C["muted"], lh=16)
            T(d, c, val, pad + i * cw3, yy + 18, size=13, weight=500, lh=20, mono=True)
        yy += 48
    ui.tabs(d, c, pad, yy, ["Últimas 5 compras", "Top 5 produtos"] if dev == "desktop" else ["Últimas compras", "Top 5"], 0, app=APP, h=36)
    yy += 44
    obs_h = 64 if dev == "desktop" else 0
    free = h - yy - obs_h - 88 - pad
    nrows = max(2, min(5, int(free // 24)))
    for dt, doc, v in COMPRAS_MARI[:nrows]:
        T(d, c, dt if dev == "desktop" else dt[:5], pad, yy, size=13, color=C["text2"], lh=20, mono=True)
        T(d, c, doc, pad + (96 if dev == "desktop" else 56), yy, size=13, color=C["text2"], lh=20)
        T(d, c, brl(v), w - pad, yy, size=13, lh=20, mono=True, align="right")
        yy += 24
    if dev == "desktop":
        yy += 4
        T(d, c, "Observação", pad, yy, size=12, color=C["muted"], lh=16)
        T(d, c, "Prefere seda brown. Avisar quando chegar Zomo Love 66", pad, yy + 18, size=13, lh=20, w=iw)
    by = h - pad - 88
    ui.button(d, c, pad, by, "Ver histórico completo", app=APP, kind="secondary", w=iw, key="F4")
    bw = (iw - 8) / 2
    ui.button(d, c, pad, by + 48, "WhatsApp", app=APP, kind="secondary", w=bw, icon_name="whats")
    ui.button(d, c, pad + bw + 8, by + 48, "Editar", app=APP, kind="secondary", w=bw, icon_name="lapis")
    return c


def h04(d, f, dev, app):
    x, y, w, base = _shell(d, f, dev, "Clientes")
    hh = ui.page_head(d, f, x, y, w, "Clientes", "1.284 cadastrados · Loja PNZ",
                      actions=[("Regras das etiquetas", "secondary", None, None), ("Novo cliente", "primary", None, "mais")], device=dev)
    y += hh + (8 if dev != "mobile" else 4)
    stats = [("Clientes ativos", "412", "compraram nos últimos 30 dias", None, "Ativos"),
             ("Novos no mês", "38", "desde 01/11/2026"),
             ("Recorrentes", "57", "1 compra por semana, 4 semanas", None, "Recorrentes"),
             ("Vendas identificadas hoje", "29 de 47", "62% das vendas", None, "Identificadas hoje")]
    if dev == "mobile":
        stats = [(s[0], s[1], None, None, s[4] if len(s) > 4 else None) for s in stats]
    y += _stats(d, f, x, y, w, stats, dev) + 16
    chips = [("Todos", "1.284"), ("VIP", "46"), ("Recorrentes", "57"), ("Sumidos 30+ dias", "318"),
             ("Inativos 60+ dias", "402"), ("Aniversariantes", "9")]
    y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
    if dev == "mobile":
        ui.field(d, f, x, y, w, placeholder="Nome, CPF, CNPJ ou telefone", prefix_icon="busca", app=APP)
        y += 52
        rows = [(n, f"{cid} · {tel}", brl(tg), s[0], s[1]) for n, cid, tel, uc, nc, tg, s in CLI]
        _, lh = ui.mobile_rows(d, f, x, y, w, rows, selected=0)
        return y + lh + 16
    fw = 340 if dev == "desktop" else 300
    lw = w - fw - 16
    ui.field(d, f, x, y, lw, placeholder="Buscar por nome, CPF, CNPJ ou telefone", prefix_icon="busca", app=APP)
    _ficha(d, f, x + lw + 16, y, fw, base - y, dev)
    y += 52
    if dev == "desktop":
        cols = [("Cliente", None, "l"), ("Telefone", 144, "l", True), ("Última compra", 108, "l", True),
                ("Compras", 72, "r", True), ("Total gasto", 100, "r", True), ("Situação", 108, "l")]
        rows = [["", tel, uc, str(nc), _n(tg), s] for n, cid, tel, uc, nc, tg, s in CLI]
    else:
        cols = [("Cliente", None, "l"), ("Total gasto", 100, "r", True), ("Situação", 116, "l")]
        rows = [["", _n(tg), s] for n, cid, tel, uc, nc, tg, s in CLI]
    two = {0: [(n, cid) for n, cid, *_ in CLI]}
    nmax = int((base - y - 40) // 56)
    _table2(d, f, x, y, lw, cols, rows[:nmax], {0: two[0][:nmax]}, selected=0)


# =====================================================================
# H05 · Editar cliente
# =====================================================================
CRED_MOV = [("24/11/2026", 12.00, "Sobra de troca", "TRC-000031", "Ana"),
            ("17/11/2026", -20.00, "Uso no pagamento", "DAV 004702", "Arthur"),
            ("08/11/2026", 50.00, "Ajuste no HOST", "AJ-000014", "Lucas")]
PARCELAS = [("DAV 004433", "1 de 2", "03/12/2026", 107.00, ("Em aberto", "info")),
            ("DAV 004433", "2 de 2", "03/01/2027", 107.00, ("Em aberto", "info")),
            ("DAV 004102", "3 de 3", "28/10/2026", 0.00, ("Paga", "ok"))]


def _sec(d, p, x, y, w, h, title, action=None):
    c = ui.card(d, p, x, y, w, h, title=title, app=APP)
    if action:
        lab, ic = action
        bw = int(fc.text_width(lab, 14, 500) + 24 + 32 + 3) // 4 * 4
        ui.button(d, c, w - 20 - bw, 12, lab, app=APP, kind="secondary", w=bw, h=36, icon_name=ic)
    return c


def _cli_ident(d, p, x, y, w, dev):
    one = dev == "mobile"
    h = 56 + 64 + 64 + (64 if one else 0) + 12
    c = _sec(d, p, x, y, w, h, "Identificação")
    iw = w - 40
    yy = 52
    ui.field(d, c, 20, yy, iw, label="Nome", value="Mariana Albuquerque", app=APP); yy += 64 + 4
    if one:
        ui.field(d, c, 20, yy, iw, label="CPF ou CNPJ", value="123.456.789-09", mono=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="Nascimento", value="27/11/1994", mono=True, app=APP)
    else:
        hw = (iw - 16) / 2
        ui.field(d, c, 20, yy, hw, label="CPF ou CNPJ", value="123.456.789-09", mono=True, app=APP)
        ui.field(d, c, 20 + hw + 16, yy, hw, label="Nascimento", value="27/11/1994", mono=True, app=APP)
    return h


def _cli_contato(d, p, x, y, w, dev):
    one = dev == "mobile" or w < 460
    h = 52 + 68 * (4 if one else 2) + 44
    c = _sec(d, p, x, y, w, h, "Contato")
    iw = w - 40
    yy = 52
    hw = (iw - 16) / 2
    if one:
        ui.field(d, c, 20, yy, iw, label="Telefone ou WhatsApp", value="(87) 98841-2207", mono=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="E-mail", value="mariana.alb@gmail.com", focused=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw - 96, label="Cidade", value="Petrolina", app=APP)
        ui.field(d, c, 20 + iw - 80, yy, 80, label="Estado", value="PE", chevron=True, app=APP); yy += 68
    else:
        ui.field(d, c, 20, yy, hw, label="Telefone ou WhatsApp", value="(87) 98841-2207", mono=True, app=APP)
        ui.field(d, c, 20 + hw + 16, yy, hw, label="E-mail", value="mariana.alb@gmail.com", focused=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw - 96, label="Cidade", value="Petrolina", app=APP)
        ui.field(d, c, 20 + iw - 80, yy, 80, label="Estado", value="PE", chevron=True, app=APP); yy += 68
    ui.checkbox(d, c, 20, yy + 6, True, "Aceita ofertas pelo WhatsApp", app=APP)
    d.nodes[c]["height"] = float(yy + 44)
    return yy + 44


def _cli_rel(d, p, x, y, w, dev):
    h = 56 + 36 + 40 + 20 + 64 + 20
    c = _sec(d, p, x, y, w, h, "Relacionamento")
    yy = 56
    ui.toggle(d, c, 20, yy, True, "Sempre VIP", app=APP)
    yy += 36
    ui.toggle(d, c, 20, yy, False, "Bloquear vendas", app=APP)
    yy += 40
    T(d, c, "Observação que aparece no F1", 20, yy, size=13, color=C["text2"], lh=16)
    fb = d.frame(c, "Campo Observação", 20, yy + 20, w - 40, 56, fill=C["card"], stroke=C["line"], stroke_opacity=0.16, radius=ui.R_CTL)
    T(d, fb, "Prefere seda brown. Avisar quando chegar Zomo Love 66", 12, 10, size=14, lh=20, w=w - 64)
    return h


def _cli_credito(d, p, x, y, w, dev):
    mob = dev == "mobile"
    rows_h = 36 + 3 * (56 if mob else 40)
    h = 52 + 60 + rows_h + 20
    c = _sec(d, p, x, y, w, h, "Crédito do cliente", ("Ajustar crédito", "lapis"))
    T(d, c, "Saldo", 20, 52, size=12, color=C["muted"], lh=16)
    T(d, c, brl(42.00), 20, 70, size=24, weight=500, lh=32)
    yy = 112
    if mob:
        rows = [(f"{brl(v, sign=True)} · {o}", f"{dt} · {doc} · {u}", "", None, None) for dt, v, o, doc, u in CRED_MOV]
        _, lh = ui.mobile_rows(d, c, 12, yy, w - 24, [(a, b) for a, b, *_ in rows], row_h=56)
        d.nodes[c]["height"] = float(yy + lh + 12)
        return yy + lh + 12
    cols = [("Data", 100, "l", True), ("Valor", 80, "r", True), ("Origem", None, "l"), ("Documento", 112, "l", True), ("Quem fez", 72, "l")]
    if w < 560:
        cols = [("Data", 100, "l", True), ("Valor", 80, "r", True), ("Origem", None, "l"), ("Quem fez", 64, "l")]
        rows = [[dt, (_n(v) if v < 0 else "+" + _n(v), "neg" if v < 0 else "ok"), o, u] for dt, v, o, doc, u in CRED_MOV]
    else:
        rows = [[dt, (_n(v) if v < 0 else "+" + _n(v), "neg" if v < 0 else "ok"), o, doc, u] for dt, v, o, doc, u in CRED_MOV]
    t, th = ui.table(d, c, 12, yy, w - 24, cols, rows, app=APP)
    d.nodes[t]["stroke"]["weight"] = 0.0
    return h


def _cli_prazo(d, p, x, y, w, dev):
    mob = dev == "mobile"
    h = 52 + 64 + 36 + 3 * (56 if mob else 40) + 24
    c = _sec(d, p, x, y, w, h, "Venda a prazo", ("Alterar limite e bloqueio", "cadeado") if not mob else None)
    cw = (w - 40) / 3
    for i, (lab, val) in enumerate((("Limite", brl(500.00)), ("Em aberto", brl(214.00)), ("Disponível", brl(286.00)))):
        T(d, c, lab, 20 + i * cw, 52, size=12, color=C["muted"], lh=16)
        T(d, c, val, 20 + i * cw, 70, size=17 if not mob else 15, weight=500, lh=24, mono=True)
    yy = 112
    if mob:
        _, lh = ui.mobile_rows(d, c, 12, yy, w - 24, [(f"{dv} · parcela {pc}", f"vence {vc}", brl(v) if v else "—", s[0], s[1])
                                                       for dv, pc, vc, v, s in PARCELAS], row_h=56)
        d.nodes[c]["height"] = float(yy + lh + 12)
        return yy + lh + 12
    cols = [("Venda", None, "l"), ("Parcela", 72, "l"), ("Vencimento", 100, "l", True), ("Valor", 84, "r", True), ("Situação", 104, "l")]
    if w < 560:
        cols = [("Venda", None, "l"), ("Parcela", 56, "l"), ("Vencimento", 96, "l", True), ("Valor", 76, "r", True), ("Situação", 100, "l")]
    rows = [[dv, pc, vc, _n(v) if v else "—", s] for dv, pc, vc, v, s in PARCELAS]
    t, th = ui.table(d, c, 12, yy, w - 24, cols, rows, app=APP)
    d.nodes[t]["stroke"]["weight"] = 0.0
    return h


def _h05_body(d, f, dev, x, y, w):
    mob = dev == "mobile"
    if not mob:
        ui.icon(d, f, "seta-esq", x, y + 2, 16, C["text2"])
        T(d, f, "Clientes", x + 20, y, size=13, color=C["text2"], lh=20)
        y += 28
    T(d, f, "Editar cliente", x, y, size=24 if not mob else 20, weight=500, lh=32 if not mob else 28)
    if not mob:
        bx = x + w
        b, bw = ui.button(d, f, 0, y - 4, "Salvar alterações", app=APP, kind="primary", key="Enter")
        bx -= bw; d.nodes[b]["transform"][4] = float(bx); bx -= 8
        b, bw = ui.button(d, f, 0, y - 4, "Cancelar", app=APP, kind="secondary", key="Esc")
        bx -= bw; d.nodes[b]["transform"][4] = float(bx)
        T(d, f, "Alterações não salvas", bx - 16, y + 6, size=13, color=C["warn"], lh=20, align="right")
        y += 48
        gap = 12
        lw = (w - 16) * (0.44 if dev == "desktop" else 0.46)
        rw = w - lw - 16
        ly = y
        ly += _cli_ident(d, f, x, ly, lw, dev) + gap
        ly += _cli_contato(d, f, x, ly, lw, dev) + gap
        ly += _cli_rel(d, f, x, ly, lw, dev)
        ry = y
        ry += _cli_credito(d, f, x + lw + 16, ry, rw, dev) + gap
        ry += _cli_prazo(d, f, x + lw + 16, ry, rw, dev) + gap
        ui.button(d, f, x + lw + 16, ry, "Excluir cliente", app=APP, kind="danger", icon_name="lixo")
        return max(ly, ry + 40) + 24
    T(d, f, "Alterações não salvas", x, y + 30, size=13, color=C["warn"], lh=20)
    y += 64
    y += _cli_ident(d, f, x, y, w, dev) + 12
    y += _cli_contato(d, f, x, y, w, dev) + 12
    y += _cli_rel(d, f, x, y, w, dev) + 12
    y += _cli_credito(d, f, x, y, w, dev) + 12
    y += _cli_prazo(d, f, x, y, w, dev) + 12
    ui.button(d, f, x, y, "Alterar limite e bloqueio", app=APP, kind="secondary", w=w, icon_name="cadeado"); y += 48
    ui.button(d, f, x, y, "Excluir cliente", app=APP, kind="danger", w=w, icon_name="lixo"); y += 56
    W = DEVICES["mobile"][0]
    bar = d.frame(f, "Barra fixa", 0, y, W, 80, fill=C["card"])
    hair(d, bar, 0, 0, W)
    bw = (W - 32 - 8) / 2
    ui.button(d, bar, 16, 16, "Cancelar", app=APP, kind="secondary", w=bw, h=44)
    ui.button(d, bar, 16 + bw + 8, 16, "Salvar", app=APP, kind="primary", w=bw, h=44)
    return y + 80


def h05(d, f, dev, app):
    return _auto(d, f, dev, "Clientes", _h05_body)


# =====================================================================
# H06 · Estoque
# =====================================================================
LOCAIS = ["Frente de loja", "Fundo de loja"]
CONTAGEM = {0: (412, 14, 6), 1: (398, 9, 6)}  # produtos, para repor, inativos


def _estoque_top(d, f, dev, local=0, tab=None, right="acoes"):
    """Cabeçalho do Estoque com as abas dos dois locais (sem 'Todos') e as ações do local aberto."""
    x, y, w, base = _shell(d, f, dev, "Estoque")
    tab = local if tab is None else tab
    nome = LOCAIS[local] if tab < 2 else "Transferências"
    sub = f"{LOCAIS[local]} · {CONTAGEM[local][0]} produtos · {CONTAGEM[local][1]} abaixo do mínimo" if tab < 2 else "Consultar e desfazer transferências entre Fundo e Frente"
    if dev == "mobile":
        sub = f"{LOCAIS[local]} · {CONTAGEM[local][0]} produtos" if tab < 2 else "Consultar e desfazer"
    hh = ui.page_head(d, f, x, y, w, "Estoque", sub,
                      actions=[("Importar XML", "secondary", None, "upload"), ("Novo produto", "primary", None, "mais")], device=dev)
    y += hh + (4 if dev != "mobile" else 0)
    if dev == "mobile":
        ui.tabs(d, f, x, y, ["Frente de loja", "Fundo de loja", "Transferências"], tab, app=APP)
        y += 52
        if right == "acoes" and tab < 2:
            bw = (w - 16) / 3
            for i, (lab, ic) in enumerate((("Entrada", "mais"), ("Saída", "menos"), ("Transferir", "transferir"))):
                ui.button(d, f, x + i * (bw + 8), y, lab, app=APP, kind="secondary", w=bw, icon_name=ic)
            y += 52
        return x, y, w, base
    counts = [CONTAGEM[0][0], CONTAGEM[1][0], 6]
    ui.tabs(d, f, x, y, ["Frente de loja", "Fundo de loja", "Transferências"], tab, app=APP, counts=counts)
    if right == "acoes" and tab < 2:
        bx = x + w
        for lab, ic in reversed((("Entrada", "mais"), ("Saída", "menos"), ("Transferir", "transferir"))):
            b, bw = ui.button(d, f, 0, y - 2, lab, app=APP, kind="secondary", h=36, icon_name=ic)
            bx -= bw
            d.nodes[b]["transform"][4] = float(bx)
            bx -= 8
        if dev == "desktop":
            T(d, f, f"Estoque aberto: {LOCAIS[local]}", bx - 8, y + 8, size=12, color=C["muted"], lh=20, align="right")
    return x, y + 56, w, base


def _estoque_rows(local):
    out = []
    ordem = ui.PRODUTOS[:9] + [ui.produto("006290")] + [p for p in ui.PRODUTOS[9:] if p[0] != "006290"]
    for p in ordem:
        cod, gtin, nome, preco, fr, fu = p[:6]
        qt, mn = (fr, MIN_FR[cod]) if local == 0 else (fu, MIN_FU[cod])
        cu = CUSTO[cod]
        mg = (preco - cu) / preco * 100
        out.append(dict(cod=cod, gtin=gtin, nome=nome, cat=CATEG[cod], custo=cu, venda=preco, mg=mg, qt=qt, mn=mn,
                        cad=CADASTRO[cod], sit=_sit(cod, qt, mn)))
    return out


def h06(d, f, dev, app, local=0, sel=6):
    x, y, w, base = _estoque_top(d, f, dev, local)
    cnt = CONTAGEM[local]
    rows = _estoque_rows(local)
    chips = [("Todos", str(cnt[0])), ("Para repor", str(cnt[1])), ("Inativos", str(cnt[2]))]
    if dev == "mobile":
        y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
        ui.field(d, f, x, y, w, placeholder="Código, EAN, referência ou nome", prefix_icon="busca", app=APP)
        y += 52
        lc = "frente" if local == 0 else "fundo"
        mr = [(r["nome"], f"{r['cod']} · {lc} {r['qt']} · mín. {r['mn']}", brl(r["venda"]), r["sit"][0], r["sit"][1]) for r in rows[:10]]
        _, lh = ui.mobile_rows(d, f, x, y, w, mr, selected=sel if sel is not None and sel < 9 else None)
        return y + lh + 16
    cw = ui.chips(d, f, x, y + 4, chips, 0, app=APP)
    sw = 360 if dev == "desktop" else 300
    ui.field(d, f, x + w - sw, y, sw, placeholder="Código, EAN, referência ou nome", prefix_icon="busca", app=APP)
    y += 56
    est = "Frente/mín." if local == 0 else "Fundo/mín."
    if dev == "desktop":
        cols = [("Código", 80, "l", True), ("Produto", None, "l"), ("Custo", 84, "r", True), ("Venda", 84, "r", True),
                ("Margem", 72, "r", True), (est, 104, "r", True), ("Cadastro", 100, "l", True), ("Situação", 104, "l")]
        tr = [[r["cod"], "", _n(r["custo"]), _n(r["venda"]), f"{r['mg']:.0f}%", (f"{r['qt']}/{r['mn']}", "neg" if r["qt"] == 0 else None),
               r["cad"], r["sit"]] for r in rows]
        two = [(r["nome"], f"{r['cat']} · {r['gtin']}") for r in rows]
    else:
        cols = [("Código", 76, "l", True), ("Produto", None, "l"), ("Venda", 84, "r", True), ("Margem", 72, "r", True),
                (est, 96, "r", True), ("Situação", 104, "l")]
        tr = [[r["cod"], "", _n(r["venda"]), f"{r['mg']:.0f}%", (f"{r['qt']}/{r['mn']}", "neg" if r["qt"] == 0 else None), r["sit"]] for r in rows]
        two = [(r["nome"], r["cat"]) for r in rows]
    n = int((base - y - 40) // 56)
    dim = [i for i, r in enumerate(rows[:n]) if r["cod"] in INATIVOS]
    _table2(d, f, x, y, w, cols, tr[:n], {1: two[:n]}, selected=sel if sel is not None and sel < n else None, dim_rows=dim)


# =====================================================================
# H07 · Transferir (Fundo de loja → Frente de loja)
# =====================================================================
TRANSF = [("003302", 11), ("005510", 10), ("004120", 6), ("006265", 20)]  # cadastro, quantidade


def _p(cod):
    return ui.produto(cod)


def h07(d, f, dev, app):
    h06(d, f, dev, app, local=1, sel=None)
    mob = dev == "mobile"
    W, H = DEVICES[dev]
    ww = {"desktop": 1080, "tablet": 1040, "mobile": W}[dev]
    wh = {"desktop": 720, "tablet": 700, "mobile": 796}[dev]
    win, w, h, top, bot = ui.window(d, f, dev, "Transferir produtos", ww, wh, app=APP,
                                    footer_buttons=[("Transferir", "primary", "Enter")])
    pad = 24 if not mob else 16
    # rota
    y = top + 20
    rw = 200 if not mob else (w - 2 * pad - 32) / 2
    ui.field(d, win, pad, y, rw, label="De", value="Fundo de loja", readonly=True, app=APP)
    _arrow(d, win, pad + rw + 9, y + 32)
    ui.field(d, win, pad + rw + 32, y, rw, label="Para", value="Frente de loja", readonly=True, app=APP)
    sel = [(_p(c), q) for c, q in TRANSF]
    tot_q = sum(q for _, q in sel)
    tot_v = sum(CUSTO[p[0]] * q for p, q in sel)
    y += 60 + 20
    hair(d, win, 0, y, w)
    if mob:
        y += 16
        ui.field(d, win, pad, y, w - 2 * pad, placeholder="Código, EAN ou nome", prefix_icon="busca", app=APP)
        y += 52
        ui.chips(d, win, pad, y, [("O destino precisa", "6"), ("Todos", None)], 0, app=APP)
        y += 56
        T(d, win, "Para transferir", pad, y, size=15, weight=500, lh=20)
        T(d, win, f"{len(sel)} produtos · {tot_q} un.", w - pad, y, size=13, color=C["muted"], lh=20, align="right")
        y += 32
        for p, q in sel:
            T(d, win, p[2], pad, y, size=14, weight=500, lh=20, w=w - 2 * pad - 100)
            T(d, win, f"Fundo {p[5]} → {p[5] - q} · Frente {p[4]} → {p[4] + q}", pad, y + 22, size=12, color=C["muted"], lh=16, mono=True)
            ui.field(d, win, w - pad - 80, y + 2, 80, value=str(q), mono=True, app=APP, focused=(p[0] == "005510"))
            y += 60
        hair(d, win, pad, y, w - 2 * pad)
        ui.kv(d, win, pad, y + 12, w - 2 * pad, [("Valor a custo", brl(tot_v))])
        return
    # duas colunas: o que o destino precisa | lista para transferir
    lw = int((w - 2 * pad - 24) * (0.46 if dev == "desktop" else 0.41))
    rx = pad + lw + 24
    rwid = w - rx - pad
    y += 20
    ui.field(d, win, pad, y, lw, placeholder="Buscar por código, EAN ou nome", prefix_icon="busca", app=APP)
    y2 = y + 52
    ui.chips(d, win, pad, y2, [("O destino precisa", "6"), ("Todos", None)], 0, app=APP)
    y2 += 44
    need = [_p(c) for c in ("003302", "005510", "004120", "006265", "002251", "004401")]
    rh = 56
    lst = d.frame(win, "Lista O destino precisa", pad, y2, lw, bot - 16 - y2, fill=C["card"], stroke=C["line"],
                  stroke_opacity=ui.LINE_A, radius=ui.R_CARD, clip=True)
    yy = 4
    na = {c for c, _ in TRANSF}
    for i, p in enumerate(need):
        if i == 4:
            d.frame(lst, "Linha selecionada", 4, yy, lw - 8, rh - 4, fill=C["sel"], stroke=C["ink"], radius=6)
        T(d, lst, p[2], 16, yy + 8, size=14, lh=20, w=lw - 16 - (120 if dev == "desktop" else 60))
        T(d, lst, f"Frente {p[4]}/{MIN_FR[p[0]]} · Fundo {p[5]}", 16, yy + 30, size=12, color=C["muted"], lh=16, mono=True)
        if p[0] in na and dev != "desktop":
            ui.icon(d, lst, "ok", lw - 16 - 28, yy + 18, 16, C["pos"])
        elif p[0] in na:
            ui.icon(d, lst, "ok", lw - 16 - 16 - 64, yy + 18, 16, C["pos"])
            T(d, lst, "Na lista", lw - 16, yy + 16, size=13, color=C["text2"], lh=20, align="right")
        else:
            if dev == "desktop":
                ui.button(d, lst, lw - 16 - 104, yy + 10, "Adicionar", app=APP, kind="secondary", w=104, h=32, icon_name="mais")
            else:
                ui.button(d, lst, lw - 16 - 40, yy + 10, "", app=APP, kind="secondary", w=40, h=32, icon_name="mais")
        yy += rh
        if i < len(need) - 1 and i != 4 and i + 1 != 4:
            hair(d, lst, 16, yy - 2, lw - 32)
    # lista para transferir
    T(d, win, "Para transferir", rx, y + 10, size=15, weight=500, lh=20)
    T(d, win, f"{len(sel)} produtos · {tot_q} unidades", rx + rwid, y + 10, size=13, color=C["muted"], lh=20, align="right")
    ty = y + 52
    cols = [("Produto", None, "l"), ("Qtde", 84, "r", True), ("Fundo", 84, "r", True), ("Frente", 84, "r", True), ("", 36, "c")]
    rows = [["", "", f"{p[5]} → {p[5] - q}", f"{p[4]} → {p[4] + q}", ""] for p, q in sel]
    two = {0: [(p[2], p[0]) for p, q in sel]}
    t, th = _table2(d, win, rx, ty, rwid, cols, rows, two, row_h=56, sub_mono=True)
    xs = _colx(rwid, cols)
    for i, (p, q) in enumerate(sel):
        cx, cw = xs[1]
        ui.field(d, t, cx + cw - 8 - 64, 36 + i * 56 + 10, 64, value=str(q), mono=True, app=APP, h=36, focused=(i == 1))
        cx, cw = xs[4]
        ui.icon(d, t, "fechar", cx + (cw - 16) / 2, 36 + i * 56 + 20, 16, C["muted"])
    ky = ty + th + 16
    ui.kv(d, win, rx + rwid - 280, ky, 280, [("Unidades", str(tot_q)), ("Valor a custo", brl(tot_v))], bold_last=True)


# =====================================================================
# H08 · Cadastro de produto (Isqueiro Clipper)
# =====================================================================
PROD = ui.produto("002210")
CUSTO_HIST = [("12/03/2025", 6.40), ("10/07/2025", 6.40), ("02/12/2025", 6.90), ("15/04/2026", 6.90),
              ("02/08/2026", 7.20), ("18/11/2026", 7.70)]


def _card_ident(d, p, x, y, w, dev):
    one = w < 420
    c = _sec(d, p, x, y, w, 10, "Identificação")
    iw = w - 40
    yy = 52
    ui.field(d, c, 20, yy, iw, label="Descrição", value="Isqueiro Clipper Largo Estampado", app=APP); yy += 68
    gw = 88
    bw_ = iw - gw - 8
    if not one:
        bw_ = (iw - 16) * 0.62 - gw - 8
    ui.field(d, c, 20, yy, bw_, label="Código de barras", value="7891234100017", mono=True, app=APP,
             error="Dígito verificador não confere")
    ui.button(d, c, 20 + bw_ + 8, yy + 20, "Gerar", app=APP, kind="secondary", w=gw)
    if not one:
        rx = 20 + bw_ + 8 + gw + 16
        ui.field(d, c, rx, yy, iw - (rx - 20), label="Referência", value="CP11-EST", mono=True, app=APP)
        yy += 88
    else:
        yy += 88
        ui.field(d, c, 20, yy, iw, label="Referência", value="CP11-EST", mono=True, app=APP); yy += 68
    if one:
        ui.field(d, c, 20, yy, iw, label="Categoria", value="Isqueiros", chevron=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="Marca", value="Clipper", chevron=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="Unidade", value="UN", chevron=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="Fornecedor principal", value="Dist. Sertão Tabacaria", chevron=True, app=APP); yy += 68
    else:
        c3 = (iw - 32) / 3
        ui.field(d, c, 20, yy, c3, label="Categoria", value="Isqueiros", chevron=True, app=APP)
        ui.field(d, c, 20 + c3 + 16, yy, c3, label="Marca", value="Clipper", chevron=True, app=APP)
        ui.field(d, c, 20 + 2 * (c3 + 16), yy, c3, label="Unidade", value="UN", chevron=True, app=APP); yy += 68
        ui.field(d, c, 20, yy, iw, label="Fornecedor principal", value="Distribuidora Sertão Tabacaria Ltda", chevron=True, app=APP)
        yy += 68
    d.nodes[c]["height"] = float(yy + 4)
    return yy + 4


def _card_preco(d, p, x, y, w, dev):
    one = w < 420
    c = _sec(d, p, x, y, w, 10, "Preço e margem")
    iw = w - 40
    yy = 52
    n = 2 if one else 3
    cw = (iw - 16 * (n - 1)) / n
    fl = [("Custo", "7,70", "R$"), ("Margem", "45,0", "%"), ("Preço de venda", "14,00", "R$")]
    for i, (lab, v, suf) in enumerate(fl):
        cx = 20 + (i % n) * (cw + 16)
        cy = yy + (i // n) * 68
        ui.field(d, c, cx, cy, cw, label=lab, value=v, mono=True, suffix=suf, app=APP, focused=(lab == "Margem"))
    yy += 68 * ((len(fl) + n - 1) // n)
    box = d.frame(c, "Resultado", 20, yy, iw, 52, fill=C["page"], radius=ui.R_CTL)
    T(d, box, "Lucro por unidade", 12, 8, size=12, color=C["muted"], lh=16)
    T(d, box, brl(6.30), 12, 26, size=14, weight=500, lh=20, mono=True)
    T(d, box, "Markup", iw / 2, 8, size=12, color=C["muted"], lh=16)
    T(d, box, "81,8%", iw / 2, 26, size=14, weight=500, lh=20, mono=True)
    yy += 52 + 16
    fl2 = [("Preço de atacado", "12,50", "R$"), ("Qtde mínima atacado", "10", "UN"), ("Desconto máximo", "10", "%")]
    for i, (lab, v, suf) in enumerate(fl2):
        cx = 20 + (i % n) * (cw + 16)
        cy = yy + (i // n) * 68
        ui.field(d, c, cx, cy, cw, label=lab, value=v, mono=True, suffix=suf, app=APP)
    yy += 68 * ((len(fl2) + n - 1) // n)
    d.nodes[c]["height"] = float(yy + 4)
    return yy + 4


def _card_fiscal(d, p, x, y, w, dev):
    one = w < 420
    c = _sec(d, p, x, y, w, 10, "Fiscal")
    iw = w - 40
    yy = 52
    n = 2 if one else 3
    cw = (iw - 16 * (n - 1)) / n
    fl = [("NCM", "9613.20.00", True, False), ("CEST", "", True, False), ("CFOP", "5102", True, True),
          ("CSOSN", "102", True, True)]
    for i, (lab, v, mono, chev) in enumerate(fl):
        cx = 20 + (i % n) * (cw + 16)
        cy = yy + (i // n) * 68
        ui.field(d, c, cx, cy, cw, label=lab, value=v, placeholder="Não se aplica" if not v else "", mono=mono, chevron=chev, app=APP)
    # origem ocupa o resto da linha (texto longo)
    if one:
        yy += 2 * 68
        ui.field(d, c, 20, yy, iw, label="Origem", value="2 · Estrangeira, mercado interno", chevron=True, app=APP)
    else:
        yy += 68
        ui.field(d, c, 20 + cw + 16, yy, iw - cw - 16, label="Origem", value="2 · Estrangeira, mercado interno", chevron=True, app=APP)
    yy += 68
    hair(d, c, 20, yy + 4, iw)
    T(d, c, "Reforma tributária · IBS e CBS", 20, yy + 16, size=13, color=C["text2"], lh=20)
    yy += 44
    hw = (iw - 16) / 2
    ui.field(d, c, 20, yy, hw, label="CST do IBS/CBS", value="000", mono=True, chevron=True, app=APP)
    ui.field(d, c, 20 + hw + 16, yy, hw, label="cClassTrib", value="000001", mono=True, chevron=True, app=APP)
    yy += 68
    T(d, c, "Tributação integral", 20, yy - 4, size=12, color=C["muted"], lh=16)
    yy += 16
    d.nodes[c]["height"] = float(yy + 4)
    return yy + 4


def _card_foto(d, p, x, y, w, dev):
    h = 152
    c = _sec(d, p, x, y, w, h, "Foto")
    ui.product_tile(d, c, 20, 52, 80, PROD[7], PROD[8])
    bx = 116
    ui.button(d, c, bx, 52, "Trocar foto", app=APP, kind="secondary", h=36, icon_name="upload")
    ui.button(d, c, bx, 96, "Remover", app=APP, kind="ghost", h=36, icon_name="lixo")
    return h


def _card_estoque(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Estoque")
    iw = w - 40
    yy = 52
    hw = (iw - 16) / 2
    for i, (lab, q) in enumerate((("Frente de loja", PROD[4]), ("Fundo de loja", PROD[5]))):
        b = d.frame(c, f"Saldo {lab}", 20 + i * (hw + 16), yy, hw, 64, fill=C["page"], radius=ui.R_CTL)
        T(d, b, lab, 12, 10, size=12, color=C["muted"], lh=16)
        T(d, b, str(q), 12, 28, size=22, weight=500, lh=28, mono=True)
    yy += 80
    ui.field(d, c, 20, yy, hw, label="Mínimo da frente", value="10", mono=True, suffix="UN", app=APP)
    ui.field(d, c, 20 + hw + 16, yy, hw, label="Mínimo do fundo", value="24", mono=True, suffix="UN", app=APP)
    yy += 68
    ui.field(d, c, 20, yy, iw, label="Localização", value="Gôndola 2 · prateleira B", app=APP)
    yy += 68
    bw = (iw - 8) / 2
    ui.button(d, c, 20, yy, "Entrada", app=APP, kind="secondary", w=bw, h=36, icon_name="mais")
    ui.button(d, c, 20 + bw + 8, yy, "Saída", app=APP, kind="secondary", w=bw, h=36, icon_name="menos")
    yy += 52
    d.nodes[c]["height"] = float(yy)
    return yy


def _spark(d, p, x, y, w, h, vals):
    lo, hi = min(vals) - 0.3, max(vals) + 0.3
    pts = [(x + i * w / (len(vals) - 1), y + h - (v - lo) / (hi - lo) * h) for i, v in enumerate(vals)]
    hair(d, p, x, y + h, w)
    d.polyline(p, pts, C["text2"], weight=1.5, name="Linha do custo")
    for i, (px, py) in enumerate(pts):
        d.ellipse(p, px - 3, py - 3, 6, C["card"] if i < len(pts) - 1 else C["ink"], name="Ponto do custo", stroke=C["text2"])


def _tri(d, p, x, y, up=True, color=None):
    col = color or C["text2"]
    if up:
        d.polyline(p, [(x, y + 8), (x + 4, y + 2), (x + 8, y + 8), (x, y + 8)], col, weight=1.5, name="Subiu")
    else:
        d.polyline(p, [(x, y + 2), (x + 4, y + 8), (x + 8, y + 2), (x, y + 2)], col, weight=1.5, name="Caiu")


def _card_custo(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Histórico de custo", ("Relatório", "doc"))
    iw = w - 40
    yy = 56
    _spark(d, c, 28, yy + 8, iw - 16, 64, [v for _, v in CUSTO_HIST])
    T(d, c, "mar/25", 20, yy + 80, size=11, color=C["muted"], lh=16, mono=True)
    T(d, c, "nov/26", 20 + iw, yy + 80, size=11, color=C["muted"], lh=16, mono=True, align="right")
    yy += 108
    regs = [("18/11/2026", 7.70, 6.9, True, "Nota 001.245", "Lucas"), ("02/08/2026", 7.20, 4.3, True, "Entrada manual", "Carla"),
            ("02/12/2025", 6.90, 7.8, True, "Alteração manual", "Lucas")]
    for i, (dt, v, pc, up, orig, u) in enumerate(regs):
        T(d, c, brl(v), 20, yy, size=13, weight=500, lh=20, mono=True)
        _tri(d, c, 20 + 84, yy + 5, up)
        T(d, c, f"{pc:.1f}%".replace(".", ","), 20 + 98, yy, size=13, color=C["text2"], lh=20, mono=True)
        T(d, c, dt, 20 + iw, yy, size=12, color=C["text2"], lh=20, mono=True, align="right")
        T(d, c, f"{orig} · {u}", 20, yy + 20, size=12, color=C["muted"], lh=16)
        if i < len(regs) - 1:
            hair(d, c, 20, yy + 42, iw)
        yy += 50
    d.nodes[c]["height"] = float(yy + 12)
    return yy + 12


def _card_mov(d, p, x, y, w, dev):
    c = _sec(d, p, x, y, w, 10, "Últimas movimentações", ("Relatório", "doc"))
    iw = w - 40
    yy = 56
    movs = [("24/11 10:12", "Venda · Frente", "DAV 004871", -1), ("22/11 09:40", "Transferência Fundo → Frente", "TR-000182", 12),
            ("18/11 14:08", "Entrada por nota · Fundo", "NF-e 001.245", 48)]
    for dt, tipo, doc, q in movs:
        T(d, c, tipo, 20, yy, size=13, lh=20, w=iw - 56)
        T(d, c, f"{dt} · {doc}", 20, yy + 20, size=12, color=C["muted"], lh=16, mono=True)
        T(d, c, _q(q), 20 + iw, yy + 8, size=13, lh=20, mono=True, align="right", color=C["neg"] if q < 0 else C["pos"])
        yy += 48
    ui.button(d, c, 20, yy, "Ver tudo o que movimentou o estoque", app=APP, kind="secondary", w=iw, h=36, icon_name="relogio")
    yy += 52
    d.nodes[c]["height"] = float(yy)
    return yy


def _h08_body(d, f, dev, x, y, w):
    mob = dev == "mobile"
    W = DEVICES[dev][0]
    # cabeçalho fixo: volta, título, código, cadastrado por, produto ativo, Cancelar e Salvar
    top = y - (28 if not mob else 44)
    meta = "Código 002210 · cadastrado em 12/03/2025 por Lucas · última alteração 18/11/2026 por Lucas"
    mw = w if mob else w - 280
    ml = 1 if fc.text_width(meta, 12) < mw else 2
    hdr_h = (28 + 40 + 16 * ml + 12 + 20 + 20) if not mob else (44 + 34 + 16 * ml + 12 + 20 + 16)
    x0 = 0 if mob else x - 32
    hdr = d.frame(f, "Cabeçalho fixo", x0, top, W - x0, hdr_h, fill=C["page"])
    hair(d, hdr, 0, hdr_h - 1, W - x0)
    lx = x - x0
    oy = 0 if not mob else 12
    ui.icon(d, hdr, "seta-esq", lx, oy + 2, 16, C["text2"])
    T(d, hdr, "Estoque · Frente de loja", lx + 20, oy, size=13, color=C["text2"], lh=20)
    oy += 28 if not mob else 32
    T(d, hdr, "Isqueiro Clipper Largo Estampado", lx, oy, size=24 if not mob else 20, weight=500, lh=32 if not mob else 28)
    if not mob:
        bx = lx + w
        b, bw = ui.button(d, hdr, 0, oy, "Salvar", app=APP, kind="primary", key="Enter")
        bx -= bw; d.nodes[b]["transform"][4] = float(bx); bx -= 8
        b, bw = ui.button(d, hdr, 0, oy, "Cancelar", app=APP, kind="secondary", key="Esc")
        bx -= bw; d.nodes[b]["transform"][4] = float(bx)
    oy += 40 if not mob else 34
    T(d, hdr, meta, lx, oy, size=12, color=C["muted"], lh=16, w=mw)
    oy += 16 * ml + 12
    ui.toggle(d, hdr, lx, oy, True, "Produto ativo", app=APP)
    y = top + hdr_h + (20 if not mob else 16)
    if mob:
        for fn in (_card_ident, _card_preco, _card_estoque, _card_fiscal, _card_foto, _card_custo, _card_mov):
            y += fn(d, f, x, y, w, dev) + 12
        bar = d.frame(f, "Barra fixa", 0, y, W, 80, fill=C["card"])
        hair(d, bar, 0, 0, W)
        bw = (W - 40) / 2
        ui.button(d, bar, 16, 16, "Cancelar", app=APP, kind="secondary", w=bw, h=44)
        ui.button(d, bar, 16 + bw + 8, 16, "Salvar", app=APP, kind="primary", w=bw, h=44)
        return y + 80
    gap = 16
    c1 = (w - gap) * (0.58 if dev == "desktop" else 0.5)
    c2 = w - gap - c1
    y1 = y
    for fn in (_card_ident, _card_preco, _card_fiscal):
        y1 += fn(d, f, x, y1, c1, dev) + gap
    y2 = y
    for fn in (_card_foto, _card_estoque, _card_custo, _card_mov):
        y2 += fn(d, f, x + c1 + gap, y2, c2, dev) + gap
    return max(y1, y2) + 8


def h08(d, f, dev, app):
    return _auto(d, f, dev, "Estoque", _h08_body)


# =====================================================================
# H09 · Entrada e saída manual
# =====================================================================
MOT_ENT = ["Compra sem nota fiscal", "Devolução de cliente", "Bonificação do fornecedor", "Ajuste de inventário",
           "Transferência de outra loja", "Outro"]
MOT_SAI = ["Perda ou avaria", "Produto vencido", "Uso interno", "Brinde ou amostra", "Ajuste de inventário",
           "Furto ou extravio", "Outro"]


def _mov_window(d, f, dev, tipo="Entrada"):
    mob = dev == "mobile"
    ent = tipo == "Entrada"
    pr = ui.produto("002210" if ent else "002251")
    antes = pr[4]
    q = 12 if ent else 1
    dep = antes + q if ent else antes - q
    mot = MOT_ENT if ent else MOT_SAI
    msel = 0
    W = DEVICES[dev][0]
    ww = 640 if not mob else W
    nrows = (len(mot) + 1) // 2 if not mob else len(mot)
    wh = 64 + 20 + 84 + 84 + 24 + nrows * 32 + 8 + 68 + (56 if mob else 0) + 20 + 72
    win, w, h, top, bot = ui.window(d, f, dev, f"{tipo} no estoque · Frente de loja" if not mob else f"{tipo} · Frente de loja",
                                    ww, wh, app=APP, footer_buttons=[(f"Lançar {tipo.lower()}", "primary", "Enter")])
    pad = 24 if not mob else 16
    iw = w - 2 * pad
    y = top + 20
    # produto
    T(d, win, "Produto", pad, y, size=13, color=C["text2"], lh=16)
    pb = d.frame(win, "Produto escolhido", pad, y + 20, iw, 48, fill=C["card"], stroke=C["line"], stroke_opacity=0.16, radius=ui.R_CTL)
    ui.product_tile(d, pb, 6, 6, 36, pr[7], pr[8])
    T(d, pb, pr[2], 52, 5, size=14, weight=500, lh=20, w=iw - 52 - 40)
    T(d, pb, f"{pr[0]} · {CATEG[pr[0]]}", 52, 25, size=12, color=C["muted"], lh=16, mono=True)
    ui.icon(d, pb, "fechar", iw - 28, 16, 16)
    y += 68 + 16
    # quantidade, custo
    qw = 120 if not mob else (iw - 16) / 2
    ui.field(d, win, pad, y, qw, label="Quantidade", value=str(q), mono=True, focused=True, suffix="UN", app=APP)
    if ent:
        ui.field(d, win, pad + qw + 16, y, 200 if not mob else qw, label="Custo unitário (opcional)", value="7,90", mono=True,
                 suffix="R$", app=APP)
    # antes → depois
    bx = pad + iw - 220 if not mob else pad
    if not mob:
        bb = d.frame(win, "Antes e depois", bx, y + 20, 220, 40, fill=C["page"], radius=ui.R_CTL)
        T(d, bb, "Frente", 12, 10, size=13, color=C["text2"], lh=20)
        T(d, bb, str(antes), 120, 10, size=15, lh=20, mono=True, align="right")
        _arrow(d, bb, 132, 12)
        T(d, bb, str(dep), 208, 10, size=15, weight=500, lh=20, mono=True, align="right")
    y += 68 + 16
    T(d, win, "Motivo", pad, y, size=13, color=C["text2"], lh=16)
    y += 24
    cw = iw / 2 if not mob else iw
    for i, m in enumerate(mot):
        cx = pad + ((i // nrows) * cw if not mob else 0)
        cy = y + (i % nrows) * 32
        ui.radio(d, win, cx, cy + 2, i == msel, m, app=APP)
    y += nrows * 32 + 8
    ui.field(d, win, pad, y, iw, label="Observação", placeholder="Obrigatória quando o motivo é Outro" if False else "Opcional", app=APP,
             value="" if ent else "Caiu do balcão, tampa amassada")
    y += 68
    if mob:
        bb = d.frame(win, "Antes e depois", pad, y + 8, iw, 40, fill=C["page"], radius=ui.R_CTL)
        T(d, bb, "Frente de loja", 12, 10, size=13, color=C["text2"], lh=20)
        T(d, bb, str(antes), iw - 64, 10, size=15, lh=20, mono=True, align="right")
        _arrow(d, bb, iw - 56, 12)
        T(d, bb, str(dep), iw - 12, 10, size=15, weight=500, lh=20, mono=True, align="right")
    return win, pr, q, antes, dep


def h09(d, f, dev, app):
    h06(d, f, dev, app, local=0, sel=6)
    _mov_window(d, f, dev, "Entrada")


def h09b(d, f, dev, app):
    h06(d, f, dev, app, local=0, sel=7)
    win, pr, q, antes, dep = _mov_window(d, f, dev, "Saída")
    ui.confirm(d, f, dev, "Lançar saída na Frente de loja?",
               lines=[pr[2], f"{q} UN · Perda ou avaria", f"Frente de loja: {antes} → {dep}"], app=APP,
               yes="Lançar saída", no="Voltar")


# =====================================================================
# H10 · Transferências
# =====================================================================
TRS = [  # nº, hora, rota (0 = Fundo→Frente), produtos, unidades, valor, usuário, situação
    ("TR-000186", "16:05", 0, 2, 18, 104.40, "Carla", ("Feita", "ok")),
    ("TR-000185", "14:22", 1, 1, 6, 58.80, "Carla", ("Feita", "ok")),
    ("TR-000184", "11:40", 0, 3, 22, 129.20, "Lucas", ("Desfeita em parte", "warn")),
    ("TR-000183", "10:12", 0, 4, 47, 262.00, "Lucas", ("Feita", "ok")),
    ("TR-000182", "09:40", 0, 2, 24, 402.40, "Carla", ("Feita", "ok")),
    ("TR-000181", "08:15", 0, 3, 0, 0.00, "Carla", ("Desfeita", "neg")),
]
TR_ITENS = [("005514", 10, "ok", None), ("006264", 12, "ok", None), ("007702", 4, "undo", "Desfeito · quantidade errada")]
ROTA = ["Fundo → Frente", "Frente → Fundo"]


def _tr_row(d, p, w, yy, r, cols_x, expanded, dev):
    no, hora, rota, np_, un, val, usr, sit = r
    vals = {"Nº": no, "Hora": hora, "Rota": ROTA[rota], "Produtos": str(np_), "Unidades": str(un),
            "Valor a custo": _n(val), "Usuário": usr}
    for k, (cx, al, mono) in cols_x.items():
        if k == "Situação":
            ui.status(d, p, cx, yy + 14, sit[0], sit[1])
            continue
        if k == "":
            ui.icon(d, p, "seta-baixo" if expanded else "seta-dir", cx, yy + 16, 16, C["text2"] if expanded else C["muted"])
            continue
        T(d, p, vals[k], cx, yy + 14, size=13, lh=20, mono=mono, align="right" if al == "r" else "left",
          color=C["ink"] if k in ("Nº", "Unidades", "Valor a custo", "Produtos") else C["text2"])


def h10(d, f, dev, app):
    x, y, w, base = _estoque_top(d, f, dev, 0, tab=2)
    mob = dev == "mobile"
    # período no topo (calendário não desenhado)
    if mob:
        hw = (w - 8) / 2
        ui.field(d, f, x, y, hw, label="De", value=HOJE, mono=True, prefix_icon="calendario", app=APP)
        ui.field(d, f, x + hw + 8, y, hw, label="Até", value=HOJE, mono=True, prefix_icon="calendario", app=APP)
        y += 72
    else:
        bx = x + w
        b, bw = ui.button(d, f, 0, y - 56 - 2, "Relatório de transferências" if dev == "desktop" else "Relatório", app=APP,
                          kind="secondary", h=36, icon_name="doc")
        bx -= bw; d.nodes[b]["transform"][4] = float(bx); bx -= 12
        for lab in ("Até", "De"):
            fw = 152 if dev == "desktop" else 136
            bx -= fw
            ui.field(d, f, bx, y - 56 - 2, fw, value=HOJE, mono=True, prefix_icon="calendario", app=APP, h=36)
            T(d, f, lab, bx - 8, y - 56 + 6, size=13, color=C["text2"], lh=20, align="right")
            bx -= 8 + fc.text_width(lab, 13) + 12
    feitas = [t for t in TRS]
    un = sum(t[4] for t in TRS)
    val = sum(t[5] for t in TRS)
    stats = [("Transferências", "6", "hoje, 24/11/2026"), ("Unidades movidas", str(un), "desfeitas à parte: 25", None, "Unidades"),
             ("Valor a custo", brl(val), "desfeito à parte: R$ 212,60"), ("Itens desfeitos", "4", "25 unidades")]
    if mob:
        stats[1] = ("Unidades movidas", str(un), "desfeitas: 25", None, "Unidades")
        stats[2] = ("Valor a custo", brl(val), "desfeito: R$ 212,60")
    y += _stats(d, f, x, y, w, stats, dev) + 16
    chips = [("Todas as rotas", "6"), ("Fundo → Frente", "5"), ("Frente → Fundo", "1")]
    if mob:
        y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
        ui.field(d, f, x, y, w, placeholder="Nº, produto ou usuário", prefix_icon="busca", app=APP)
        y += 52
        rows = [(f"{r[0]} · {r[1]}", f"{ROTA[r[2]]} · {r[4]} un.", brl(r[5]), r[7][0], r[7][1]) for r in TRS]
        _, lh = ui.mobile_rows(d, f, x, y, w, rows, selected=2)
        y += lh + 16
        # produtos da selecionada
        ch = 56 + 3 * 60 + 8 + 104
        c = ui.card(d, f, x, y, w, ch, title="TR-000184 · produtos", app=APP)
        yy = 56
        for i, (cod, q, st, note) in enumerate(TR_ITENS):
            pr = ui.produto(cod)
            ui.checkbox(d, c, 16, yy + 4, i == 0, app=APP)
            T(d, c, pr[2], 44, yy, size=14, lh=20, w=w - 44 - 64, color=C["muted"] if st == "undo" else C["ink"])
            T(d, c, note or f"{pr[0]} · {brl(CUSTO[cod] * q)} a custo", 44, yy + 22, size=12, color=C["muted"], lh=16)
            T(d, c, f"{q} un.", w - 16, yy, size=14, lh=20, mono=True, align="right", color=C["muted"] if st == "undo" else C["ink"])
            yy += 60
        bw = (w - 32 - 8) / 2
        ui.button(d, c, 16, yy + 4, "Desfazer", app=APP, kind="danger", w=bw, icon_name="voltar")
        ui.button(d, c, 16 + bw + 8, yy + 4, "Romaneio", app=APP, kind="secondary", w=bw, icon_name="impressora")
        ui.button(d, c, 16, yy + 52, "Desfazer o restante", app=APP, kind="secondary", w=w - 32)
        return y + ch + 16
    ui.field(d, f, x, y, 320 if dev == "desktop" else 260, placeholder="Nº, produto ou usuário", prefix_icon="busca", app=APP)
    ui.chips(d, f, x + (336 if dev == "desktop" else 276), y + 4, chips, 0, app=APP)
    y += 56
    # lista que abre os produtos
    L = d.frame(f, "Lista de transferências", x, y, w, base - y, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A,
                radius=ui.R_CARD, clip=True)
    if dev == "desktop":
        spec = [("", 32, "l", False), ("Nº", 108, "l", True), ("Hora", 64, "l", True), ("Rota", 150, "l", False),
                ("Produtos", 80, "r", True), ("Unidades", 84, "r", True), ("Valor a custo", 120, "r", True),
                ("Usuário", 100, "l", False), ("Situação", None, "l", False)]
    else:
        spec = [("", 32, "l", False), ("Nº", 104, "l", True), ("Hora", 60, "l", True), ("Rota", 136, "l", False),
                ("Unidades", 80, "r", True), ("Valor a custo", 112, "r", True), ("Situação", None, "l", False)]
    fixed = sum(s[1] for s in spec if s[1])
    cx = 12
    cols_x = {}
    for name, cw, al, mono in spec:
        cw = cw or (w - 24 - fixed)
        ax = cx + (cw - 12 if al == "r" else 0)
        cols_x[name] = (ax, al, mono)
        if name:
            T(d, L, name, ax, 10, size=12, color=C["muted"], lh=16, align="right" if al == "r" else "left")
        cx += cw
    hair(d, L, 0, 35, w)
    yy = 36
    rh = 48
    for i, r in enumerate(TRS):
        exp = i == 2
        if exp:
            d.frame(L, "Linha selecionada", 4, yy + 2, w - 8, rh - 4, fill=C["sel"], stroke=C["ink"], radius=6)
        _tr_row(d, L, w, yy, r, cols_x, exp, dev)
        yy += rh
        if exp:
            # produtos da transferência
            ex = d.frame(L, "Produtos da transferência", 12, yy + 4, w - 24, 3 * 40 + 36 + 56, fill=C["page"], radius=ui.R_CTL)
            ew = w - 24
            T(d, ex, "Produto", 48, 10, size=12, color=C["muted"], lh=16)
            T(d, ex, "Quantidade", ew - 220, 10, size=12, color=C["muted"], lh=16, align="right")
            T(d, ex, "Valor a custo", ew - 100, 10, size=12, color=C["muted"], lh=16, align="right")
            ey = 36
            for j, (cod, q, st, note) in enumerate(TR_ITENS):
                pr = ui.produto(cod)
                undo = st == "undo"
                ui.checkbox(d, ex, 16, ey + 11, j == 0, app=APP)
                if undo:
                    d.nodes[d.nodes[ex]["children"][-1]]["opacity"] = 0.4
                T(d, ex, pr[2], 48, ey + 10, size=13, lh=20, color=C["muted"] if undo else C["ink"])
                if note:
                    T(d, ex, note, 48 + fc.text_width(pr[2], 13) + 12, ey + 10, size=12, color=C["warn"], lh=20)
                T(d, ex, str(q), ew - 220, ey + 10, size=13, lh=20, mono=True, align="right", color=C["muted"] if undo else C["ink"])
                T(d, ex, _n(CUSTO[cod] * q), ew - 100, ey + 10, size=13, lh=20, mono=True, align="right",
                  color=C["muted"] if undo else C["ink"])
                ey += 40
            hair(d, ex, 12, ey + 4, ew - 24)
            bx = 16
            for lab, kind, ic in (("Desfazer selecionados", "danger", "voltar"), ("Desfazer o restante", "secondary", None)):
                b, bw = ui.button(d, ex, bx, ey + 12, lab, app=APP, kind=kind, h=36, icon_name=ic)
                bx += bw + 8
            ui.button(d, ex, ew - 16 - 128, ey + 12, "Romaneio", app=APP, kind="secondary", w=128, h=36, icon_name="impressora")
            yy += 3 * 40 + 36 + 56 + 8
        if i < len(TRS) - 1 and not exp and i + 1 != 2:
            hair(d, L, 16, yy, w - 32)
    d.nodes[L]["height"] = float(min(base - y, yy + 4))


def h10b(d, f, dev, app):
    h10(d, f, dev, app)
    mob = dev == "mobile"
    W = DEVICES[dev][0]
    ww = 560 if not mob else W
    win, w, h, top, bot = ui.window(d, f, dev, "Desfazer transferência TR-000184", ww, 64 + 20 + 76 + 16 + 68 + 16 + 68 + 16 + 68 + 16 + 72,
                                    app=APP, footer_buttons=[("Desfazer", "danger", "Enter")])
    pad = 24 if not mob else 16
    iw = w - 2 * pad
    y = top + 20
    pr = ui.produto("005514")
    b = d.frame(win, "Produto a desfazer", pad, y, iw, 64, fill=C["page"], radius=ui.R_CTL)
    T(d, b, pr[2], 12, 10, size=14, weight=500, lh=20, w=iw - 24 - 60)
    T(d, b, "Frente 12 → 2 · Fundo 30 → 40", 12, 34, size=12, color=C["muted"], lh=16, mono=True)
    T(d, b, "10 un.", iw - 12, 10, size=14, lh=20, mono=True, align="right")
    y += 76 + 16
    ui.field(d, win, pad, y, iw, label="Motivo", value="Quantidade errada", chevron=True, app=APP)
    y += 68 + 16
    ui.field(d, win, pad, y, iw, label="Observação", value="Contagem refeita na frente", app=APP)
    y += 68 + 16
    hw = (iw - 16) / 2
    ui.field(d, win, pad, y, hw, label="Administrador", value="Lucas", chevron=True, app=APP)
    ui.field(d, win, pad + hw + 16, y, hw, label="Senha do administrador", value="••••", mono=True, focused=True, app=APP)


# =====================================================================
# H11 · Rastrear produto
# =====================================================================
def _rastro():
    """Movimentos do produto 007702, do mais antigo ao mais novo, com saldo depois em cada local."""
    ev = [  # data hora, tipo, local (F, U, FU = Fundo→Frente, UF = Frente→Fundo), qtde, documento, usuário
        ("03/11 09:20", "Estoque inicial", "U", 40, "Cadastro 007702", "Lucas"),
        ("03/11 09:41", "Transferência", "FU", 12, "TR-000171", "Lucas"),
        ("05/11 15:12", "Venda", "F", -2, "DAV 004402", "Arthur"),
        ("07/11 11:03", "Venda", "F", -1, "NFC-e 000.318", "Ana"),
        ("07/11 11:20", "Devolução", "F", 1, "DEV-000042", "Carla"),
        ("10/11 14:08", "Entrada por nota (XML)", "U", 24, "NF-e 001.198", "Lucas"),
        ("12/11 16:44", "Saída manual · perda ou avaria", "F", -1, "SM-000019", "Carla"),
        ("14/11 10:30", "Transferência", "FU", 10, "TR-000178", "Carla"),
        ("15/11 18:02", "Venda", "F", -2, "DAV 004611", "Arthur"),
        ("15/11 18:20", "Venda cancelada", "F", 2, "DAV 004611", "Carla"),
        ("18/11 13:15", "Troca", "F", -1, "TRC-000027", "Ana"),
        ("20/11 09:50", "Transferência", "FU", 8, "TR-000181", "Carla"),
        ("21/11 10:12", "Transferência desfeita", "UF", 8, "TR-000181", "Lucas"),
        ("22/11 11:05", "Entrada manual · bonificação", "U", 2, "EM-000052", "Lucas"),
        ("23/11 17:31", "Venda", "F", -2, "DAV 004833", "Arthur"),
        ("24/11 10:12", "Venda", "F", -1, "DAV 004871", "Arthur"),
    ]
    fr, fu = 0, 0
    out = []
    for dt, tipo, loc, q, doc, u in ev:
        if loc == "F":
            fr += q; lab = "Frente de loja"; saldo = f"Frente {fr}"; qq = q
        elif loc == "U":
            fu += q; lab = "Fundo de loja"; saldo = f"Fundo {fu}"; qq = q
        elif loc == "FU":
            fu -= q; fr += q; lab = "Fundo → Frente"; saldo = f"Frente {fr} · Fundo {fu}"; qq = q
        else:
            fr -= q; fu += q; lab = "Frente → Fundo"; saldo = f"Frente {fr} · Fundo {fu}"; qq = q
        out.append((dt, tipo, lab, qq, saldo, doc, u, loc))
    return list(reversed(out)), fr, fu


def h11(d, f, dev, app):
    return _auto(d, f, dev, "Estoque", _h11_body)


def _timeline_mobile(d, p, x, y, w, ev):
    c = d.frame(p, "Linha do tempo", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CARD, clip=True)
    rh = 80
    d.frame(c, "Traço", 19, 12 + 14, 2, rh * (len(ev) - 1), fill=C["ink"], fill_opacity=0.14)
    yy = 12
    for i, (dt, tipo, lab, q, saldo, doc, u, loc) in enumerate(ev):
        d.ellipse(c, 16, yy + 10, 8, C["ink"] if loc in ("FU", "UF") else C["card"], name="Ponto do movimento", stroke=C["text2"])
        T(d, c, tipo, 36, yy, size=14, weight=500, lh=20, w=w - 36 - 64)
        qs = _q(q) if loc in ("F", "U") else str(q)
        T(d, c, qs, w - 16, yy, size=14, weight=500, lh=20, mono=True, align="right",
          color=C["pos"] if (q > 0 and loc in ("F", "U")) else (C["neg"] if q < 0 else C["ink"]))
        T(d, c, f"{dt} · {lab}", 36, yy + 22, size=12, color=C["text2"], lh=16)
        T(d, c, f"{doc} · {u}", 36, yy + 40, size=12, color=C["muted"], lh=16)
        T(d, c, saldo, w - 16, yy + 40, size=12, color=C["text2"], lh=16, align="right", mono=True)
        yy += rh
        if i < len(ev) - 1:
            hair(d, c, 36, yy - 14, w - 52)
    d.nodes[c]["height"] = float(yy - 4)
    return yy - 4


def _h11_body(d, f, dev, x, y, w):
    mob = dev == "mobile"
    ev, fr, fu = _rastro()
    pr = ui.produto("007702")
    if not mob:
        ui.icon(d, f, "seta-esq", x, y + 2, 16, C["text2"])
        T(d, f, "Cadastro do produto", x + 20, y, size=13, color=C["text2"], lh=20)
        y += 28
    hh = ui.page_head(d, f, x, y, w, "Rastrear produto", "Tudo o que movimentou o estoque entre Frente e Fundo",
                      actions=[("Relatório", "secondary", None, "doc")], device=dev)
    y += hh + 8
    # produto
    ph = 80 if not mob else 120
    c = ui.card(d, f, x, y, w, ph, app=APP)
    ui.product_tile(d, c, 16, 16, 48, pr[7], pr[8])
    T(d, c, pr[2], 80, 18, size=15, weight=500, lh=20, w=w - 96 if mob else w - 480)
    T(d, c, f"{pr[0]} · {pr[1]} · {CATEG[pr[0]]}", 80, 42, size=12, color=C["muted"], lh=16, mono=True)
    if mob:
        sx = 16
        sy = 76
    else:
        sx = w - 16 - 2 * 152 - 8
        sy = 16
    for i, (lab, q, mn) in enumerate((("Frente de loja", fr, MIN_FR["007702"]), ("Fundo de loja", fu, MIN_FU["007702"]))):
        bw_ = 152 if not mob else (w - 40) / 2
        bx = sx + i * (bw_ + 8)
        b = d.frame(c, f"Saldo {lab}", bx, sy, bw_, 48 if not mob else 32, fill=C["page"], radius=ui.R_CTL)
        if mob:
            T(d, b, f"{lab.split()[0]} {q}", 10, 6, size=13, lh=20, mono=False)
            T(d, b, f"mín. {mn}", bw_ - 10, 6, size=12, color=C["muted"], lh=20, align="right")
        else:
            T(d, b, lab, 12, 6, size=12, color=C["muted"], lh=16)
            T(d, b, str(q), 12, 22, size=16, weight=500, lh=20, mono=True)
            T(d, b, f"mín. {mn}", bw_ - 12, 24, size=12, color=C["muted"], lh=16, align="right")
    y += ph + 16
    chips = [("Frente e Fundo", str(len(ev))), ("Frente de loja", str(sum(1 for e in ev if e[7] != "U"))),
             ("Fundo de loja", str(sum(1 for e in ev if e[7] != "F")))]
    if mob:
        hw = (w - 8) / 2
        ui.field(d, f, x, y, hw, value="01/11/2026", mono=True, prefix_icon="calendario", app=APP)
        ui.field(d, f, x + hw + 8, y, hw, value=HOJE, mono=True, prefix_icon="calendario", app=APP)
        y += 52
        y += ui.chips(d, f, x, y, chips, 0, app=APP, wrap_w=w) + 12
        return y + _timeline_mobile(d, f, x, y, w, ev) + 16
    ui.field(d, f, x, y, 152, value="01/11/2026", mono=True, prefix_icon="calendario", app=APP)
    T(d, f, "até", x + 160, y + 10, size=13, color=C["text2"], lh=20)
    ui.field(d, f, x + 160 + 28, y, 152, value=HOJE, mono=True, prefix_icon="calendario", app=APP)
    ui.chips(d, f, x + 360, y + 4, chips, 0, app=APP)
    y += 56
    if dev == "desktop":
        cols = [("", 36, "l"), ("Data e hora", 108, "l", True), ("Tipo", None, "l"), ("Local", 150, "l"), ("Qtde", 64, "r", True),
                ("Saldo depois", 176, "r", True), ("Documento", 136, "l", True), ("Usuário", 84, "l")]
        rows = [["", dt, tipo, lab, (_q(q) if loc in ("F", "U") else str(q), "ok" if (q > 0 and loc in ("F", "U")) else ("neg" if q < 0 else None)),
                 saldo, doc, u] for dt, tipo, lab, q, saldo, doc, u, loc in ev]
    else:
        cols = [("", 32, "l"), ("Data e hora", 104, "l", True), ("Tipo", None, "l"), ("Local", 128, "l"), ("Qtde", 56, "r", True),
                ("Saldo depois", 168, "r", True), ("Documento", 120, "l", True)]
        rows = [["", dt, tipo, lab, (_q(q) if loc in ("F", "U") else str(q), "ok" if (q > 0 and loc in ("F", "U")) else ("neg" if q < 0 else None)),
                 saldo, doc] for dt, tipo, lab, q, saldo, doc, u, loc in ev]
    rh = 44
    t, th = ui.table(d, f, x, y, w, cols, rows, row_h=rh, app=APP)
    # linha do tempo: traço vertical com um ponto por movimento
    lx = 16 + 10
    d.frame(t, "Linha do tempo", lx + 3, 36 + rh / 2, 2, rh * (len(rows) - 1), fill=C["ink"], fill_opacity=0.14)
    for i, e in enumerate(ev):
        loc = e[7]
        col = C["ink"] if loc in ("FU", "UF") else C["card"]
        d.ellipse(t, lx, 36 + i * rh + rh / 2 - 4, 8, col, name="Ponto do movimento", stroke=C["text2"])
    return y + th + 24


# =====================================================================
# H12 · Importar XML de compra
# =====================================================================
NF_ITENS = [  # item, cód. fornecedor, descrição na nota, qtde, un, custo unit, produto ligado, ligação
    (1, "ZOM001", "SEDA ZOMO KING SIZE BROWN", "120", "UN", 2.60, "006264", "Código de barras"),
    (2, "ZOM002", "SEDA ZOMO KING SIZE ROSA", "60", "UN", 2.60, "006265", "Código de barras"),
    (3, "ZOM510", "ESSENCIA ZOMO STRONG MINT 50G", "24", "UN", 9.80, "005510", "Código do fornecedor"),
    (4, "ZOM514", "ESSENCIA ZOMO LOVE 66 50G", "24", "UN", 9.80, "005514", "Código de barras"),
    (5, "ZOMCV1", "CARVAO COCO ZOMO 1KG", "20", "PCT", 18.50, "004401", "Código do fornecedor"),
    (6, "ZOMSLK", "SEDA ZOMO SLIM KS PRETA", "50", "UN", 2.90, None, "sem"),
    (7, "ZOMFT5", "FITA PAPEL ZOMO ROLO 5M", "2,5", "UN", 8.00, None, "frac"),
]
NF_TOTAL = sum(float(q.replace(",", ".")) * c for _, _, _, q, _, c, _, _ in NF_ITENS)


def _nf_head(d, p, x, y, w, dev):
    mob = dev == "mobile"
    fb = d.frame(p, "Arquivo", x, y, w, 40, fill=C["page"], radius=ui.R_CTL)
    ui.icon(d, fb, "doc", 12, 12, 16, C["text2"])
    nm = "NFe2611…12458.xml" if mob else "NFe26111123456789000110550010000012451000012458.xml"
    T(d, fb, nm, 36, 10, size=12, lh=20, mono=True)
    ui.button(d, fb, w - 4 - 132, 4, "Trocar arquivo", app=APP, kind="ghost", w=132, h=32)
    y += 56
    kv = [("Fornecedor", "Distribuidora Sertão Tabacaria Ltda", "CNPJ 23.456.789/0001-10"),
          ("Número", "001.245", "série 1"), ("Emissão", "18/11/2026", "Petrolina-PE"), ("Valor da nota", brl(NF_TOTAL), "7 itens")]
    if mob:
        for lab, v, s in kv:
            T(d, p, lab, x, y, size=12, color=C["muted"], lh=16)
            T(d, p, v, x + w, y, size=13, lh=16, align="right", mono=lab != "Fornecedor" if False else lab in ("Número", "Emissão", "Valor da nota"))
            y += 24
        return y + 8
    cws = [0.40, 0.18, 0.18, 0.24]
    cx = x
    for (lab, v, s), k in zip(kv, cws):
        cw = w * k
        T(d, p, lab, cx, y, size=12, color=C["muted"], lh=16)
        T(d, p, v, cx, y + 18, size=15, weight=500, lh=22, mono=lab in ("Número", "Emissão", "Valor da nota"))
        T(d, p, s, cx, y + 42, size=12, color=C["muted"], lh=16)
        cx += cw
    return y + 72


def _nf_items(d, p, x, y, w, dev):
    tab = dev == "tablet"
    L = d.frame(p, "Itens da nota", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CARD, clip=True)
    if tab:
        spec = [("Item", 44, "l", True), ("Descrição na nota", None, "l", False), ("Qtde", 56, "r", True),
                ("Custo", 72, "r", True), ("Produto no sistema", 240, "l", False), ("Ligação", 132, "l", False)]
    else:
        spec = [("Item", 44, "l", True), ("Cód. forn.", 88, "l", True), ("Descrição na nota", None, "l", False), ("Qtde", 56, "r", True),
                ("Un.", 48, "l", False), ("Custo", 72, "r", True), ("Produto no sistema", 270, "l", False), ("Ligação", 152, "l", False)]
    fixed = sum(s[1] for s in spec if s[1])
    cx = 16
    pos = {}
    for name, cw, al, mono in spec:
        cw = cw or (w - 32 - fixed)
        ax = cx + (cw - 12 if al == "r" else 0)
        pos[name] = (ax, al, mono, cw)
        T(d, L, name, ax, 10, size=12, color=C["muted"], lh=16, align="right" if al == "r" else "left")
        cx += cw
    hair(d, L, 0, 35, w)
    yy = 36
    rh = 40 if not tab else 36
    for i, (it, cf, desc, q, un, cu, cod, lig) in enumerate(NF_ITENS):
        extra = 48 if lig in ("sem", "frac") else 0
        sel = lig == "sem"
        if sel:
            d.frame(L, "Linha selecionada", 4, yy + 2, w - 8, rh + extra - 4, fill=C["sel"], stroke=C["ink"], radius=6)
        if lig == "frac":
            d.frame(L, "Linha bloqueada", 4, yy + 2, w - 8, rh + extra - 4, fill=C["neg"], fill_opacity=0.05,
                    stroke=C["neg"], stroke_opacity=0.35, radius=6)
        vals = {"Item": f"{it:02d}", "Cód. forn.": cf, "Descrição na nota": desc, "Qtde": q, "Un.": un, "Custo": _n(cu)}
        for k, v in vals.items():
            if k not in pos:
                continue
            ax, al, mono, cw = pos[k]
            T(d, L, v, ax, yy + (rh - 20) / 2, size=13 if not mono else 12, lh=20, mono=mono, align="right" if al == "r" else "left",
              color=C["neg"] if (k == "Qtde" and lig == "frac") else (C["ink"] if k in ("Descrição na nota", "Qtde", "Custo") else C["text2"]))
        ax = pos["Produto no sistema"][0]
        lx = pos["Ligação"][0]
        if cod:
            pr = ui.produto(cod)
            T(d, L, pr[2], ax, yy + (rh - 20) / 2, size=13, lh=20, w=pos["Produto no sistema"][3] - 8)
            ui.status(d, L, lx, yy + (rh - 20) / 2, lig if not tab else lig.replace("Código do fornecedor", "Cód. fornecedor"), "ok")
        elif lig == "sem":
            T(d, L, "Sem ligação", ax, yy + (rh - 20) / 2, size=13, color=C["text2"], lh=20)
            ui.status(d, L, lx, yy + (rh - 20) / 2, "Escolher", "warn")
            bx = pos["Descrição na nota"][0]
            for lab, kind, ic in (("Escolher produto", "secondary", "busca"), ("Cadastrar novo", "secondary", "mais"),
                                  ("Não dar entrada", "ghost", None)):
                b, bw = ui.button(d, L, bx, yy + rh + 2, lab, app=APP, kind=kind, h=36, icon_name=ic)
                bx += bw + 8
        else:
            T(d, L, "Não entra", ax, yy + (rh - 20) / 2, size=13, color=C["text2"], lh=20)
            ui.status(d, L, lx, yy + (rh - 20) / 2, "Bloqueia", "neg")
            bx = pos["Descrição na nota"][0]
            T(d, L, "Quantidade fracionada bloqueia a entrada", bx, yy + rh + 10, size=13, color=C["neg"], lh=20)
            ui.button(d, L, bx + fc.text_width("Quantidade fracionada bloqueia a entrada", 13) + 16, yy + rh + 2, "Deixar de fora",
                      app=APP, kind="secondary", h=36)
        yy += rh + extra
        if i < len(NF_ITENS) - 1 and lig not in ("sem",) and NF_ITENS[i + 1][7] not in ("sem", "frac") and lig != "frac":
            hair(d, L, 16, yy, w - 32)
    d.nodes[L]["height"] = float(yy + 4)
    return yy + 4


def _nf_bottom(d, p, x, y, w, dev, h=None):
    mob = dev == "mobile"
    if mob:
        c = ui.card(d, p, x, y, w, 124, title="Estoque de destino", app=APP)
        ui.radio(d, c, 20, 56, True, "Fundo de loja", app=APP)
        ui.radio(d, c, 20, 88, False, "Frente de loja", app=APP)
        y += 124 + 12
        c2 = ui.card(d, p, x, y, w, 200, title="Conta a pagar", app=APP)
        ui.kv(d, c2, 20, 52, w - 40, [("Fornecedor", "Dist. Sertão Tabacaria"), ("Valor", brl(NF_TOTAL))], gap=24, mono_values=False)
        ui.field(d, c2, 20, 108, w - 40, label="Vencimento", value="18/12/2026", mono=True, prefix_icon="calendario", focused=True,
                 suffix="30 dias", app=APP)
        return y + 200
    # uma faixa só: destino | conta a pagar (fornecedor, valor) | vencimento
    hair(d, p, x, y, w)
    y += 16
    T(d, p, "Estoque de destino", x, y, size=13, color=C["text2"], lh=16)
    ui.radio(d, p, x, y + 32, True, "Fundo de loja", app=APP)
    ui.radio(d, p, x + 148, y + 32, False, "Frente de loja", app=APP)
    cx = x + (340 if dev == "desktop" else 316)
    d.frame(p, "Divisa", cx - 24, y, 1, 60, fill=C["line"], fill_opacity=ui.LINE_A)
    T(d, p, "Conta a pagar", cx, y, size=13, color=C["text2"], lh=16)
    T(d, p, "Distribuidora Sertão Tabacaria Ltda", cx, y + 30, size=14, lh=20)
    vx = cx + fc.text_width("Distribuidora Sertão Tabacaria Ltda", 14) + 32
    T(d, p, "Valor", vx, y, size=13, color=C["text2"], lh=16)
    T(d, p, brl(NF_TOTAL), vx, y + 30, size=14, weight=500, lh=20, mono=True)
    fw = 232
    ui.field(d, p, x + w - fw, y - 4, fw, label="Vencimento", value="18/12/2026", mono=True, prefix_icon="calendario",
             focused=True, suffix="30 dias", app=APP)
    return y + 64


def h12(d, f, dev, app):
    mob = dev == "mobile"
    if mob:
        # no celular vira página inteira (folha alta demais para caber)
        W = DEVICES["mobile"][0]
        top = ui.topbar(d, f, dev, "host", user="Lucas")
        x, w = 16, W - 32
        y = top + 12
        T(d, f, "Importar XML de compra", x, y, size=20, weight=500, lh=28)
        cb = d.frame(f, "Fechar", W - 16 - 52, y, 52, 28, fill=None)
        ui.icon(d, cb, "fechar", 0, 6, 16, C["muted"])
        ui.keycap(d, cb, 22, 4, "Esc")
        y += 44
        y = _nf_head(d, f, x, y, w, dev)
        T(d, f, "Itens da nota", x, y, size=15, weight=500, lh=20)
        y += 28
        rows = []
        for it, cf, desc, q, un, cu, cod, lig in NF_ITENS:
            if cod:
                rows.append((ui.produto(cod)[2], f"{it:02d} · {q} {un} · {lig.lower()}", _n(cu), "Ligado", "ok"))
            elif lig == "sem":
                rows.append((desc.capitalize(), f"{it:02d} · {q} {un} · sem ligação", _n(cu), "Escolher", "warn"))
            else:
                rows.append((desc.capitalize(), f"{it:02d} · {q} {un} · fracionada", _n(cu), "Bloqueia", "neg"))
        _, lh = ui.mobile_rows(d, f, x, y, w, rows, selected=5)
        y += lh + 8
        bw = (w - 8) / 2
        ui.button(d, f, x, y, "Escolher produto", app=APP, kind="secondary", w=bw, h=40)
        ui.button(d, f, x + bw + 8, y, "Cadastrar novo", app=APP, kind="secondary", w=bw, h=40)
        y += 48
        ui.button(d, f, x, y, "Deixar o item 07 de fora", app=APP, kind="danger", w=w, h=40)
        y += 56
        y = _nf_bottom(d, f, x, y, w, dev) + 16
        bar = d.frame(f, "Barra fixa", 0, y, W, 80, fill=C["card"])
        hair(d, bar, 0, 0, W)
        b, _ = ui.button(d, bar, 16, 16, "Dar entrada", app=APP, kind="primary", w=W - 32, h=44, disabled=True)
        return y + 80
    h06(d, f, dev, app, local=0, sel=None)
    W, H = DEVICES[dev]
    ww = 1240 if dev == "desktop" else 1120
    wh = 780 if dev == "desktop" else 760
    win, w, h, top, bot = ui.window(d, f, dev, "Importar XML de compra", ww, wh, app=APP,
                                    footer_buttons=[("Dar entrada", "primary", "Enter")])
    _btn_disable(d, win, "Dar entrada")
    pad = 24
    y = top + 16
    y = _nf_head(d, win, pad, y, w - 2 * pad, dev)
    y += _nf_items(d, win, pad, y, w - 2 * pad, dev) + 16
    _nf_bottom(d, win, pad, y, w - 2 * pad, dev)


SCREENS = [
    ("H01", "Entrar no HOST", h01),
    ("H01b", "Aviso de chamados ao entrar", h01b),
    ("H02", "Início", h02),
    ("H03", "Caixas", h03),
    ("H04", "Clientes", h04),
    ("H05", "Editar cliente", h05),
    ("H06", "Estoque · Frente de loja", h06),
    ("H07", "Transferir", h07),
    ("H08", "Cadastro de produto", h08),
    ("H09", "Entrada manual", h09),
    ("H09b", "Saída manual · confirmação", h09b),
    ("H10", "Transferências", h10),
    ("H10b", "Desfazer transferência", h10b),
    ("H11", "Rastrear produto", h11),
    ("H12", "Importar XML de compra", h12),
]
