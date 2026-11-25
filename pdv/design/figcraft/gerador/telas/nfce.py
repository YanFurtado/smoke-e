"""NFC-e (Cupom fiscal): o que é próprio da nota. As telas de venda são as do DAV.

N01 venda (reaproveita dav_a com app="nfce"), N02 emissão, N03 DANFE, N04 notas emitidas,
N05 contingência, N06 cancelamento, N07 rejeição.
"""
import fc, ui
from ui import C, T, brl, PAD, DEVICES, hair
from telas import dav_a
from telas.dav_a import ITENS, TOTAL, NITENS, busca, vendas_bar, ultimo_item

PAGE = "02 · Cupom fiscal (NFC-e)"
APP = "nfce"

# ---------- dados da nota (simulados, como no protótipo) ----------
DESCONTO = 5.00
PAGAR = TOTAL - DESCONTO
PAGOS = [("Pix", 45.00), ("Dinheiro", 60.00)]
TROCO = sum(v for _, v in PAGOS) - PAGAR
TRIB_FED, TRIB_EST = 12.73, 17.10
CBS, IBS = 0.009, 0.001  # 2026: alíquotas de teste, só informativas
CLIENTE, CPF = "Mariana Albuquerque", "123.456.789-09"
SERIE, NUM = 1, 4823
PROTOCOLO = "126260019482317"
EMISSAO, AUTORIZ = "24/11/2026 17:42:51", "24/11/2026 17:42:53"
URL_SEFAZ = "nfce.sefaz.pe.gov.br/nfce/consulta"

def chave(serie=SERIE, num=NUM, tpemis=1, cnf="38472915"):
    """Chave de acesso de 44 dígitos (cUF 26 = PE, AAMM, CNPJ, modelo 65, série, número, tpEmis, cNF, DV)."""
    base = "26" + "2611" + "0" * 14 + "65" + f"{serie:03d}" + f"{num:09d}" + str(tpemis) + cnf
    s, w = 0, 2
    for ch in reversed(base):
        s += int(ch) * w; w = 2 if w == 9 else w + 1
    dv = 11 - s % 11
    return base + str(0 if dv >= 10 else dv)

def grupos(k): return " ".join(k[i:i + 4] for i in range(0, 44, 4))
def chave_linhas(k, n=2):
    g = grupos(k).split(" ")
    return [" ".join(g[:6]), " ".join(g[6:])] if n == 2 else [" ".join(g)]
def num_fmt(n): return f"{n:,}".replace(",", ".")
def v(x): return brl(x)[3:]

CHAVE = chave()
CHAVE_CONT = chave(tpemis=9, cnf="51907364")

# ---------- componentes locais ----------
def _retext(d, frame, prefix, new):
    """Troca o texto de um filho que começa com prefix (ajusta a largura estimada)."""
    for cid in d.nodes[frame]["children"]:
        n = d.nodes[cid]
        if n["type"] == "text" and n["characters"].startswith(prefix):
            st = n["style"]
            n["characters"] = new; n["name"] = new[:48]
            n["width"] = fc.text_width(new, st["font_size"], 400, st["font_family"] != "Inter") + 2
            return cid

def _textarea(d, p, x, y, w, h, label, value, counter=None, focused=True, app=APP, ok=True):
    T(d, p, label, x, y, size=13, color=C["text2"], lh=16)
    b = d.frame(p, f"Campo {label}", x, y + 20, w, h, fill=C["card"], stroke=ui.acc(app) if focused else C["line"],
                stroke_opacity=1.0 if focused else 0.16, stroke_w=2 if focused else 1, radius=ui.R_CTL)
    T(d, b, value, 12, 10, size=14, lh=20, w=w - 24)
    if counter:
        T(d, p, counter, x + w, y + 20 + h + 4, size=12, color=C["pos"] if ok else C["neg"], lh=16, align="right", mono=True)
    return 20 + h + (20 if counter else 0)

def _step(d, p, x, y, state, title, sub=None, right=None, last=False, gap=56):
    """Etapa da emissão: feita (ponto positivo com visto), em andamento (anel) ou pendente."""
    if state == "ok":
        c = d.frame(p, f"Etapa {title}", x, y, 24, 24, fill=C["pos"], radius=12)
        ui.icon(d, c, "ok", 4, 4, 16, "#ffffff")
    elif state == "doing":
        d.ellipse(p, x, y, 24, C["card"], name=f"Etapa {title}", stroke=C["ink"])
        d.ellipse(p, x + 8, y + 8, 8, C["ink"], name="Em andamento")
    else:
        d.ellipse(p, x, y, 24, C["card"], name=f"Etapa {title}", stroke=C["muted"])
    if not last:
        d.frame(p, "Ligação", x + 11.5, y + 28, 1, gap - 32, fill=C["ink"], fill_opacity=0.14)
    T(d, p, title, x + 40, y + 2, size=14, weight=500, lh=20, color=C["ink"] if state != "todo" else C["muted"])
    if sub: T(d, p, sub, x + 40, y + 24, size=12, color=C["muted"], lh=16)
    if right: T(d, p, right, d.nodes[p]["width"] - 24, y + 2, size=12, color=C["muted"], lh=20, align="right", mono=True)

def _menu(d, p, x, y, w, items, hi=0):
    """Menu de contexto (⋯ ou clique direito): setas movem, Enter escolhe."""
    h = 8 + 36 * len(items) + 8
    m = d.frame(p, "Menu da nota", x, y, w, h, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A,
                radius=ui.R_CARD, shadow=ui.shadow(0.10, 12, 32))
    yy = 8
    for i, (lab, ic, tone, dis) in enumerate(items):
        if i == hi:
            d.frame(m, "Opção selecionada", 4, yy, w - 8, 36, fill=C["sel"], stroke=C["ink"], radius=6)
        col = C["neg"] if tone == "neg" else C["ink"]
        ui.icon(d, m, ic, 16, yy + 10, 16, col if tone == "neg" else C["text2"])
        T(d, m, lab, 44, yy + 8, size=14, color=col, lh=20, opacity=0.45 if dis else 1.0)
        yy += 36
    return m, h

def _receipt_danfe(cols, contingencia=False):
    """Linhas do DANFE NFC-e em bobina de 80 mm (48 colunas no computador, 45 no celular)."""
    L = [("SMOKE HOUSE TABACARIA", "cb"), ("CNPJ a informar · IE a informar", "c"),
         ("R. Joaquim Nabuco, 78, Centro", "c"), ("Petrolina-PE", "c"), ("", "hr"),
         ("Documento Auxiliar da Nota Fiscal", "c"), ("de Consumidor Eletrônica", "c"), ("", "hr")]
    if contingencia:
        L += [("EMITIDA EM CONTINGÊNCIA", "cb"), ("Pendente de autorização", "c"), ("", "hr")]
    L += [(("Item Descrição", ""), "lr"), (("     Código Qtde UN x Vl.unit", "Vl.total"), "lr")]
    for i, (cod, nome, q, u) in enumerate(ITENS):
        L += [f"{i + 1:03d}  {nome}", ((f"     {cod} {q} UN x {v(u)}", v(q * u)), "lr")]
    L += [("", "hr"), (("Qtde total de itens", str(NITENS)), "lr"), (("Valor total R$", v(TOTAL)), "lr"),
          (("Desconto R$", v(DESCONTO)), "lr"), (("Valor a pagar R$", v(PAGAR)), "lrb"),
          (("Forma de pagamento", "Valor pago R$"), "lr")]
    L += [((n, v(x)), "lr") for n, x in PAGOS]
    L += [(("Troco R$", v(TROCO)), "lr"), ("", "hr"),
          f"Tributos aproximados: R$ {v(TRIB_FED)} (Federal)", f"R$ {v(TRIB_EST)} (Estadual) Fonte: IBPT", ("", "hr")]
    k = CHAVE_CONT if contingencia else CHAVE
    L += [("Consulte pela chave de acesso em", "c"), (URL_SEFAZ, "c")] + [(ln, "c") for ln in chave_linhas(k)]
    L += [("", "hr"), (f"Consumidor CPF {CPF}", "c"), (CLIENTE, "c"), ("", "hr"),
          (f"NFC-e nº {NUM:09d}  Série {SERIE:03d}", "cb"), (f"Emissão {EMISSAO}", "c"), ("Via consumidor", "c")]
    if contingencia:
        L += [("EMITIDA EM CONTINGÊNCIA", "cb"), ("Pendente de autorização", "c")]
    L += ["", ("", "qr")]
    if not contingencia:
        L += [(f"Protocolo de autorização {PROTOCOLO}", "c"), (f"Data de autorização {AUTORIZ}", "c")]
    return L

# ---------- N01 · Venda no cupom fiscal ----------
def _cupom(d, f, x, y, w, h, app):
    c = ui.cupom_tela(d, f, x, y, w, h, ITENS, cliente=CLIENTE, doc=CPF, app=app, titulo="Cupom fiscal")
    _retext(d, c, "CPF/CNPJ do consumidor", f"CPF na nota  {CPF}")
    T(d, c, f"Próxima NFC-e  série {SERIE} · nº {num_fmt(NUM)}", w - 20, 16, size=12, color=C["text2"], lh=20, align="right", mono=True)
    return c

def n01(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    top = ui.caixa_abas(d, f, dev, 0, app)
    if dev == "mobile":
        y = top + 12
        busca(d, f, pad, y, W - 2 * pad, h=44, app=app); y += 56
        vendas_bar(d, f, pad, y, W - 2 * pad, device=dev, app=app); y += 60
        ultimo_item(d, f, pad, y, W - 2 * pad, ITENS[-1], compact=True, app=app); y += 84
        c = ui.cupom_tela(d, f, pad, y, W - 2 * pad, H - y - 88 - 18, ITENS, cliente=CLIENTE, doc=CPF, app=app, titulo="Cupom fiscal")
        _retext(d, c, "CPF/CNPJ do consumidor", f"CPF na nota  {CPF}")
        T(d, c, f"Série {SERIE} · nº {num_fmt(NUM)}", W - 2 * pad - 20, 16, size=12, color=C["text2"], lh=20, align="right", mono=True)
        ui.mobile_bar(d, f, brl(TOTAL), NITENS, app=app)
        return
    foot = 40 if dev == "desktop" else 56
    lw = 560 if dev == "desktop" else 460
    y = top + 16
    vendas_bar(d, f, pad, y, lw, device=dev, app=app)
    _cupom(d, f, pad, y + 60, lw, H - foot - (y + 60) - 22, app)
    rx = pad + lw + 24; rw = W - rx - pad
    busca(d, f, rx, y, rw, app=app)
    by = H - foot - 24 - 64
    tb_h = 70 + (72 if dev == "desktop" else 52) + 8
    ty = by - 32 - tb_h
    ultimo_item(d, f, rx, y + 64, rw, ITENS[-1], h=ty - 24 - (y + 64), app=app)
    ui.total_block(d, f, rx, ty, rw, brl(TOTAL), NITENS, device=dev, app=app)
    ui.button(d, f, rx, by, "Formas de pagamento", app=app, kind="primary", w=rw - 196 - 12, h=64, key="F3", sub="Finalizar e emitir a NFC-e")
    ui.button(d, f, rx + rw - 196, by, "Cancelar cupom", app=app, kind="secondary", w=196, h=64, key="F6")
    ui.footer(d, f, dev, app)

# ---------- N02 · Emitindo e autorizada ----------
def n02(d, f, dev, app):
    n01(d, f, dev, app)
    mob = dev == "mobile"
    win, w, h, top, bot = ui.window(d, f, dev, "Emitindo NFC-e", 640, 568 if not mob else 640, app=app,
                                    footer_buttons=[("Enviar por WhatsApp", "secondary", None), ("Concluir", "primary", "Enter")])
    pad = 24 if not mob else 16
    y = top + 20
    T(d, win, f"NFC-e {num_fmt(NUM)} · série {SERIE}", pad, y, size=15, weight=500, lh=22)
    T(d, win, f"{CLIENTE} · CPF {CPF}", pad, y + 24, size=12 if mob else 13, color=C["text2"], lh=20)
    T(d, win, brl(PAGAR), w - pad, y - 2, size=24, weight=500, lh=32, align="right")
    y += 64
    hair(d, win, pad, y, w - 2 * pad); y += 24
    gap = 56
    _step(d, win, pad, y, "ok", "Assinando com o certificado A1", "Certificado da loja PNZ, válido até 12/08/2027", "0,2 s"); y += gap
    _step(d, win, pad, y, "ok", "Enviando à SEFAZ-PE", "Ambiente de produção · modelo 65", "1,1 s"); y += gap
    _step(d, win, pad, y, "ok", "Autorizada", f"Protocolo {PROTOCOLO} · {AUTORIZ[11:]}", "0,3 s", gap=148)
    # protocolo e chave
    bx, bw = pad + 40, w - pad - (pad + 40)
    b = d.frame(win, "Chave e protocolo", bx, y + 48, bw, 84, fill=C["raised"], radius=ui.R_CTL)
    T(d, b, "Chave de acesso", 12, 10, size=12, color=C["muted"], lh=16)
    ks = chave_linhas(CHAVE, 2 if (mob or bw < 470) else 1)
    for i, ln in enumerate(ks):
        T(d, b, ln, 12, 30 + i * 20, size=13 if not mob else 12, lh=20, mono=True)
    if len(ks) == 1: T(d, b, "Consulta em " + URL_SEFAZ, 12, 54, size=12, color=C["muted"], lh=16, mono=True)
    y += 148
    _step(d, win, pad, y, "doing", "Imprimindo o DANFE", "Impressora do caixa · 80 mm", "agora", last=True)
    y += 56
    if not mob:
        pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela

# ---------- N03 · DANFE NFC-e ----------
def n03(d, f, dev, app):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    mob = dev == "mobile"
    rw = 384 if not mob else W - 2 * pad
    lines = _receipt_danfe(48 if not mob else 45)
    y = top + (24 if not mob else 64)
    if mob:
        T(d, f, "DANFE NFC-e", pad, top + 12, size=20, weight=500, lh=28)
        ui.status(d, f, W - pad, top + 16, "Autorizada", "ok", align="right")
        r, rh = ui.receipt(d, f, pad, y, rw, lines, title="DANFE NFC-e")
        total = y + rh + 6 + 16 + 88
        d.nodes[f]["height"] = float(total)
        bar = d.frame(f, "Barra de ações", 0, total - 88, W, 88, fill=C["card"])
        hair(d, bar, 0, 0, W)
        ui.button(d, bar, pad, 22, "Enviar XML", app=app, kind="secondary", w=(W - 2 * pad - 8) / 2, h=44)
        ui.button(d, bar, pad + (W - 2 * pad - 8) / 2 + 8, 22, "Reimprimir", app=app, kind="primary", w=(W - 2 * pad - 8) / 2, h=44, key="Enter")
        return total
    foot = 40 if dev == "desktop" else 56
    # bobina à esquerda do centro, painel ao lado
    pw = 400 if dev == "desktop" else 380
    gx = (W - (rw + 48 + pw)) / 2
    rx = gx
    r, rh = ui.receipt(d, f, rx, y, rw, lines, title="DANFE NFC-e")
    total = max(H, y + rh + 6 + 32 + foot)
    d.nodes[f]["height"] = float(total)
    px = rx + rw + 48
    c = ui.card(d, f, px, y, pw, 468, title="DANFE NFC-e · 80 mm")
    ui.status(d, c, pw - 20, 18, "Autorizada", "ok", align="right")
    T(d, c, "Impresso às 17:42:53", 20, 44, size=13, color=C["text2"], lh=20)
    hair(d, c, 20, 80, pw - 40)
    ui.kv(d, c, 20, 96, pw - 40, [("NFC-e", f"{num_fmt(NUM)} · série {SERIE}"), ("Emissão", EMISSAO), ("Autorização", AUTORIZ),
                                  ("Protocolo", PROTOCOLO), ("Ambiente", "Produção"), ("Impressora", "Térmica do caixa"),
                                  ("Via", "Consumidor")], gap=28)
    yy = 96 + 7 * 28 + 8
    hair(d, c, 20, yy, pw - 40); yy += 16
    pass  # sem texto explicativo
    bw = (pw - 40 - 8) / 2
    ui.button(d, c, 20, yy, "Enviar XML", app=app, kind="secondary", w=bw)
    ui.button(d, c, 20 + bw + 8, yy, "Reimprimir", app=app, kind="primary", w=bw, key="Enter")
    yy += 52
    pass  # regra da spec: sem texto explicativo nem instrução de teclado na janela
    d.nodes[c]["height"] = float(yy + 36)
    ui.footer(d, f, dev, app)
    return total

# ---------- N04 · Notas emitidas ----------
NOTAS = [  # série, número, hora, cliente, total, situação, tom, pagamento
    (1, 4823, "17:42", CLIENTE, PAGAR, "Autorizada", "ok", "Pix + Dinheiro"),
    (2, 1207, "17:38", "Consumidor não identificado", 23.00, "Autorizada", "ok", "Dinheiro"),
    (1, 4822, "17:31", "Rafael Coelho Nunes", 289.00, "Autorizada", "ok", "Crédito"),
    (2, 1206, "17:20", "Consumidor não identificado", 44.00, "Em contingência", "warn", "Pix"),
    (1, 4821, "17:05", "Tabacaria do Porto Ltda", 480.00, "Autorizada", "ok", "Débito"),
    (1, 4820, "16:52", "João Victor Sampaio", 32.00, "Cancelada", "neg", "Pix"),
    (2, 1205, "16:40", "Larissa Menezes", 39.90, "Rejeitada", "neg", "Débito"),
    (1, 4819, "16:31", "Consumidor não identificado", 18.00, "Autorizada", "ok", "Dinheiro"),
    (1, 4818, "16:10", "Pedro Henrique Brandão", 79.90, "Autorizada", "ok", "Crédito"),
    (2, 1204, "15:58", "Consumidor não identificado", 25.00, "Em contingência", "warn", "Dinheiro"),
    (1, 4817, "15:41", "Mariana Albuquerque", 120.00, "Autorizada", "ok", "Pix"),
    (2, 1203, "15:22", "Rafael Coelho Nunes", 45.00, "Autorizada", "ok", "Débito"),
]
FILTROS = [("Todas", 38), ("Autorizadas", 33), ("Canceladas", 1), ("Em contingência", 2), ("Rejeitadas", 2)]

def _ch_curta(s, n):
    k = chave(s, n, cnf=f"{(n * 7919) % 10**8:08d}")
    return f"… {k[-8:-4]} {k[-4:]}"

def n04(d, f, dev, app, menu=True):
    W, H = DEVICES[dev]; pad = PAD[dev]
    top = ui.topbar(d, f, dev, app)
    top = ui.caixa_abas(d, f, dev, 1, app)
    mob = dev == "mobile"
    sub = "Hoje, 24/11/2026 · Loja PNZ · série 1 no Terminal 01, série 2 no Terminal 02"
    if mob:
        y = top + 16
        ui.page_head(d, f, pad, y, W - 2 * pad, "Notas emitidas", sub="Hoje, 24/11/2026 · séries 1 e 2", device=dev)
        y += 64
        ui.field(d, f, pad, y, W - 2 * pad, placeholder="Número, chave ou cliente", prefix_icon="busca", app=app, h=44)
        y += 56
        y += ui.chips(d, f, pad, y, FILTROS, active=0, app=app, wrap_w=W - 2 * pad) + 16
        rows = [(cl, f"{s} · {num_fmt(n)} · {hr} · {_ch_curta(s, n)}", brl(t), sit, tone)
                for s, n, hr, cl, t, sit, tone, pg in NOTAS[:9]]
        _, lh = ui.mobile_rows(d, f, pad, y, W - 2 * pad, rows, selected=0)
        return max(H, y + lh + 24)
    foot = 40 if dev == "desktop" else 56
    y = top + pad + 4
    ui.page_head(d, f, pad, y, W - 2 * pad, "Notas emitidas", sub=sub if dev == "desktop" else "Hoje, 24/11/2026 · séries 1 e 2", device=dev)
    sw, pw = (300, 264) if dev == "desktop" else (256, 264)
    ui.field(d, f, W - pad - pw - 8 - sw, y + 4, sw, placeholder="Número, chave, cliente ou produto" if dev == "desktop" else "Número, chave ou cliente", prefix_icon="busca", app=app)
    ui.field(d, f, W - pad - pw, y + 4, pw, value="24/11/2026 a 24/11/2026", prefix_icon="calendario", app=app, mono=True)
    y += 64
    ui.chips(d, f, pad, y, FILTROS, active=0, app=app)
    y += 48
    lw = int((W - 2 * pad) * (0.62 if dev == "desktop" else 0.60))
    if dev == "desktop":
        cols = [("Série · nº", 96, "l", True), ("Hora", 60, "l", True), ("Cliente", None, "l"), ("Chave", 120, "l", True),
                ("Total", 88, "r", True), ("Situação", 140, "l"), ("", 32, "c")]
        rows = [[f"{s} · {num_fmt(n)}", hr, cl, _ch_curta(s, n), v(t), (sit, tone), ""] for s, n, hr, cl, t, sit, tone, pg in NOTAS]
    else:
        cols = [("Série · nº", 92, "l", True), ("Hora", 56, "l", True), ("Cliente", None, "l"),
                ("Total", 84, "r", True), ("Situação", 136, "l"), ("", 32, "c")]
        rows = [[f"{s} · {num_fmt(n)}", hr, cl, v(t), (sit, tone), ""] for s, n, hr, cl, t, sit, tone, pg in NOTAS[:10]]
    t, th = ui.table(d, f, pad, y, lw, cols, rows, selected=0, app=app)
    for i in range(len(rows)):
        ui.icon(d, t, "pontos", lw - 16 - 24, 36 + i * 40 + 12, 16, C["ink"] if i == 0 else C["muted"])
    # detalhe ao lado
    dx = pad + lw + 16; dw = W - pad - dx
    dh = H - foot - 24 - y
    c = ui.card(d, f, dx, y, dw, dh)
    d.nodes[c]["clip"] = True  # o detalhe rola dentro do cartão; nada passa por baixo do rodapé
    _detalhe(d, c, dw, dh, dev)
    if menu:
        _menu(d, f, pad + lw - 8 - 240, y + 36 + 40 - 2, 240, [
            ("Reimprimir DANFE", "impressora", None, False), ("Enviar XML", "upload", None, False),
            ("Consultar na SEFAZ", "busca", None, False), ("Cancelar NFC-e", "fechar", "neg", False)])
    ui.footer(d, f, dev, app)

def _detalhe(d, c, dw, dh, dev):
    x = 20; iw = dw - 40
    T(d, c, f"NFC-e {num_fmt(NUM)} · série {SERIE}", x, 18, size=17, weight=500, lh=24)
    ui.status(d, c, dw - 20, 20, "Autorizada", "ok", align="right")
    T(d, c, f"{CLIENTE} · CPF {CPF}", x, 46, size=13, color=C["text2"], lh=20)
    hair(d, c, x, 78, iw)
    T(d, c, "Chave de acesso", x, 90, size=12, color=C["muted"], lh=16)
    ks = chave_linhas(CHAVE, 1 if iw >= 440 else 2)
    for i, ln in enumerate(ks):
        T(d, c, ln, x, 108 + i * 20, size=13, lh=20, mono=True)
    y = 108 + 20 * len(ks) + 12
    kv = [("Emissão", EMISSAO), ("Protocolo", f"{PROTOCOLO} · {AUTORIZ[11:]}")]
    if dev == "desktop": kv += [("Pagamento", "Pix 45,00 · Dinheiro 60,00"), ("Operador", "Arthur · Terminal 01")]
    y += ui.kv(d, c, x, y, iw, kv, gap=26) + 4
    hair(d, c, x, y, iw); y += 12
    T(d, c, "Itens", x, y, size=13, color=C["text2"], lh=20)
    T(d, c, "CBS e IBS informativos em 2026", dw - 20, y, size=12, color=C["muted"], lh=20, align="right")
    y += 28
    ih = 38 if dev == "desktop" else 36
    for i, (cod, nome, q, u) in enumerate(ITENS):
        tot = q * u
        T(d, c, f"{i + 1:03d}", x, y, size=12, color=C["muted"], lh=18, mono=True)
        T(d, c, nome, x + 36, y, size=13, lh=18, w=iw - 36 - 72)
        T(d, c, v(tot), dw - 20, y, size=13, lh=18, mono=True, align="right")
        T(d, c, f"{q} × {v(u)} · CBS 0,9% {v(tot * CBS)} · IBS 0,1% {v(tot * IBS)}", x + 36, y + 18, size=11, color=C["muted"], lh=16, mono=True)
        y += ih
    hair(d, c, x, y, iw); y += 12
    ui.kv(d, c, x, y, iw, [("Valor total", v(TOTAL)), ("Desconto", f"- {v(DESCONTO)}"),
                           ("Tributos aproximados (IBPT)", v(TRIB_FED + TRIB_EST)), ("Valor pago", v(PAGAR))], gap=24, bold_last=True)

# ---------- N05 · Contingência ----------
def n05(d, f, dev, app):
    n01(d, f, dev, app)
    mob = dev == "mobile"
    wide = dev == "desktop"
    w = 960 if wide else (880 if dev == "tablet" else 390)
    win, w, h, top, bot = ui.window(d, f, dev, "NFC-e emitida em contingência", w, 620 if not mob else 700, app=app,
                                    footer_buttons=[("Transmitir agora", "secondary", None), ("Continuar" if mob else "Continuar vendendo", "primary", "Enter")])
    pad = 24 if not mob else 16
    rcol = 0 if mob else (328 if wide else 300)
    cw = w - 2 * pad - (rcol + 24 if rcol else 0)
    y = top + 20
    b = d.frame(win, "Aviso SEFAZ", pad, y, cw, 64 if not mob else 84, fill=C["card"], stroke=C["warn"], stroke_opacity=0.35, radius=ui.R_CTL)
    bh = 64 if not mob else 84
    d.frame(b, "Faixa", 0, 0, 3, bh, fill=C["warn"], radius=[ui.R_CTL, 0, 0, ui.R_CTL])
    ui.icon(d, b, "aviso", 16, 12, 16, C["warn"])
    T(d, b, "A SEFAZ-PE não respondeu", 44, 10, size=14, weight=500, lh=20)
    T(d, b, "A venda não parou: a nota saiu em contingência offline (tpEmis 9)", 44, 32, size=13, color=C["text2"], lh=20, w=cw - 60)
    y += bh + 20
    T(d, win, f"NFC-e {num_fmt(NUM)} · série {SERIE} · {brl(PAGAR)}", pad, y, size=15, weight=500, lh=22); y += 26
    T(d, win, "DANFE impresso na hora com “EMITIDA EM CONTINGÊNCIA” e “Pendente de autorização”. "
      "Quando a SEFAZ voltar, a nota é transmitida sozinha.", pad, y, size=13, color=C["text2"], lh=20, w=cw)
    y += 20 * (3 if mob else 2) + 20
    T(d, win, "Fila de transmissão", pad, y, size=13, color=C["text2"], lh=20)
    T(d, win, "prazo de até 24 h por nota", pad + cw, y, size=12, color=C["muted"], lh=20, align="right")
    y += 28
    fila = [(f"{SERIE} · {num_fmt(NUM)}", "17:42", v(PAGAR), "23 h 59 min", "Aguardando"),
            ("2 · 1.206", "17:20", "44,00", "23 h 37 min", "Reenvio às 17:45"),
            ("2 · 1.204", "15:58", "25,00", "22 h 15 min", "Reenvio às 17:45")]
    if mob:
        rows = [(f"NFC-e {a} · {hr}", f"Prazo {pz}", t, st, "warn") for a, hr, t, pz, st in fila]
        _, lh = ui.mobile_rows(d, win, pad, y, cw, rows, row_h=60)
        y += lh
    else:
        cols = [("Série · nº", 92, "l", True), ("Hora", 64, "l", True), ("Total", 72, "r", True), ("Prazo restante", 112, "r", True),
                ("Situação", None, "l")]
        rows = [[a, hr, t, pz, (st, "warn")] for a, hr, t, pz, st in fila]
        _, th = ui.table(d, win, pad, y, cw, cols, rows, app=app)
        y += th
    y += 16
    ui.icon(d, win, "relogio", pad, y + 2, 16, C["text2"])
    T(d, win, "Nota perto do fim do prazo aparece em destaque em Notas emitidas e no HOST › Fiscal",
      pad + 24, y, size=12, color=C["text2"], lh=18, w=cw - 24)
    if rcol:
        # bobina de contingência ao lado (recortada pela janela)
        rx = w - pad - rcol
        box = d.frame(win, "DANFE em contingência", rx, top + 20, rcol, bot - top - 20, fill=C["raised"], radius=ui.R_CARD, clip=True)
        lines = [("SMOKE HOUSE TABACARIA", "cb"), ("CNPJ a informar · IE a informar", "c"),
                 ("R. Joaquim Nabuco, 78, Centro", "c"), ("Petrolina-PE", "c"), ("", "hr"),
                 ("Documento Auxiliar da NFC-e", "c"), ("", "hr"),
                 ("EMITIDA EM CONTINGÊNCIA", "cb"), ("Pendente de autorização", "c"), ("", "hr"),
                 (("Qtde total de itens", str(NITENS)), "lr"), (("Valor a pagar R$", v(PAGAR)), "lrb"),
                 (("Pix", v(45)), "lr"), (("Dinheiro", v(60)), "lr"), (("Troco R$", v(TROCO)), "lr"), ("", "hr"),
                 (f"NFC-e nº {NUM:09d} Série {SERIE:03d}", "c"), (f"Emissão {EMISSAO}", "c"), ("", "qr")]
        ui.receipt(d, box, 16, 16, rcol - 32, lines, title="Bobina em contingência")

# ---------- N06 · Cancelar NFC-e ----------
def n06(d, f, dev, app):
    n04(d, f, dev, app, menu=False)
    mob = dev == "mobile"
    win, w, h, top, bot = ui.window(d, f, dev, f"Cancelar NFC-e {num_fmt(NUM)}", 600, 604 if not mob else 760, app=app,
                                    footer_buttons=[("Voltar", "secondary", "Esc" if mob else None), ("Cancelar NFC-e", "danger", "Enter")], close=not mob)
    pad = 24 if not mob else 16
    iw = w - 2 * pad
    y = top + 20
    T(d, win, f"Série {SERIE} · {CLIENTE}", pad, y, size=15, weight=500, lh=22)
    if mob:
        T(d, win, f"Autorizada em {AUTORIZ}", pad, y + 24, size=12, color=C["muted"], lh=16)
        T(d, win, f"Protocolo {PROTOCOLO} · {brl(PAGAR)}", pad, y + 40, size=12, color=C["muted"], lh=16)
        y += 68
    else:
        T(d, win, f"Autorizada em {AUTORIZ} · protocolo {PROTOCOLO}", pad, y + 24, size=12, color=C["muted"], lh=16)
        T(d, win, brl(PAGAR), w - pad, y - 2, size=24, weight=500, lh=32, align="right")
        y += 56
    # prazo
    pz = d.frame(win, "Prazo restante", pad, y, iw, 44, fill=C["raised"], radius=ui.R_CTL)
    ui.icon(d, pz, "relogio", 12, 14, 16, C["text2"])
    T(d, pz, "Prazo restante para cancelar", 36, 12, size=13, color=C["text2"], lh=20)
    T(d, pz, "0 h 48 min", iw - 12, 12, size=13, weight=500, lh=20, mono=True, align="right")
    y += 44 + 20
    motivo = "Cliente desistiu da compra e o pagamento em Pix foi devolvido"
    y += _textarea(d, win, pad, y, iw, 64, "Motivo do cancelamento", motivo, counter=f"{len(motivo)} caracteres · mínimo 15", app=app, focused=False) + 12
    T(d, win, "Autorização do supervisor", pad, y, size=13, color=C["text2"], lh=20); y += 28
    if mob:
        ui.field(d, win, pad, y, iw, label="Quem autoriza", value="Carla · Supervisora de caixa", chevron=True, app=app); y += 68
        ui.field(d, win, pad, y, iw, label="Senha", value="••••", focused=True, app=app); y += 72
    else:
        ui.field(d, win, pad, y, iw - 200 - 12, label="Quem autoriza", value="Carla · Supervisora de caixa", chevron=True, app=app)
        ui.field(d, win, w - pad - 200, y, 200, label="Senha", value="••••", focused=True, app=app)
        y += 76
    ev = d.frame(win, "Evento", pad, y, iw, 72 if not mob else 104, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CTL)
    ui.icon(d, ev, "doc", 12, 12, 16, C["text2"])
    T(d, ev, "Evento de cancelamento (110111) enviado à SEFAZ-PE", 36, 10, size=13, weight=500, lh=20, w=iw - 48)
    T(d, ev, "Fica registrado na nota com protocolo, data, hora, Arthur e Carla. Os produtos voltam à frente de loja",
      36, 32 if not mob else 52, size=12, color=C["muted"], lh=16, w=iw - 48)

# ---------- N07 · Rejeição da SEFAZ ----------
def n07(d, f, dev, app):
    n01(d, f, dev, app)
    mob = dev == "mobile"
    win, w, h, top, bot = ui.window(d, f, dev, "A SEFAZ rejeitou a NFC-e", 640, 604 if not mob else 760, app=app,
                                    footer_buttons=[("Voltar à venda", "secondary", "Esc" if mob else None), ("Emitir de novo", "primary", "Enter")], close=not mob)
    pad = 24 if not mob else 16
    iw = w - 2 * pad
    y = top + 20
    b = d.frame(win, "Rejeição", pad, y, iw, 64, fill=C["card"], stroke=C["neg"], stroke_opacity=0.35, radius=ui.R_CTL)
    d.frame(b, "Faixa", 0, 0, 3, 64, fill=C["neg"], radius=[ui.R_CTL, 0, 0, ui.R_CTL])
    ui.icon(d, b, "aviso", 16, 12, 16, C["neg"])
    T(d, b, "778 – Informado NCM inexistente", 44, 10, size=14, weight=500, lh=20, mono=False)
    T(d, b, "Resposta da SEFAZ-PE às 17:42:52", 44, 32, size=12, color=C["muted"], lh=20)
    y += 64 + 20
    T(d, win, "O que aconteceu", pad, y, size=13, color=C["text2"], lh=20); y += 24
    T(d, win, "Um produto da venda está com o NCM (código fiscal do produto) errado no cadastro. A nota não foi autorizada e não vale como cupom fiscal.",
      pad, y, size=14, lh=20, w=iw)
    y += 20 * max(1, -(-int(fc.text_width("Um produto da venda está com o NCM (código fiscal do produto) errado no cadastro. A nota não foi autorizada e não vale como cupom fiscal.", 14)) // int(iw))) + 16
    it = d.frame(win, "Item com problema", pad, y, iw, 64, fill=C["raised"], radius=ui.R_CTL)
    cod, nome, q, u = ITENS[-1]
    T(d, it, f"005  {cod}", 12, 10, size=12, color=C["text2"], lh=20, mono=True)
    T(d, it, nome, 12 + fc.text_width(f"005  {cod}  ", 12, 400, True), 10, size=14, weight=500, lh=20, w=iw - 24 - 110)
    T(d, it, "NCM 9614.00.99", iw - 12, 10 if not mob else 34, size=12, color=C["neg"], lh=20, mono=True, align="right")
    T(d, it, "Não existe na tabela de NCM", 12, 34, size=12, color=C["muted"], lh=20)
    y += 64 + 20
    T(d, win, "O que corrigir", pad, y, size=13, color=C["text2"], lh=20); y += 24
    passos = ["Peça ao gerente para abrir HOST › Estoque › cadastro 007702, seção Fiscal",
              "Informe o NCM certo, com 8 dígitos (o da embalagem ou da nota do fornecedor)",
              "Volte aqui e emita de novo: os itens e os pagamentos continuam na venda"]
    for i, ps in enumerate(passos):
        T(d, win, f"{i + 1}", pad, y, size=13, color=C["muted"], lh=20, mono=True)
        T(d, win, ps, pad + 20, y, size=13, lh=20, w=iw - 20)
        nl = max(1, -(-int(fc.text_width(ps, 13)) // int(iw - 20)))
        y += 20 * nl + 8
    y += 8
    hair(d, win, pad, y, iw); y += 16
    ui.icon(d, win, "doc", pad, y + 2, 16, C["text2"])
    T(d, win, f"O número {num_fmt(NUM)} da série {SERIE} ficou reservado. Se a venda não for emitida com ele, entra na lista para inutilizar no HOST › Fiscal",
      pad + 24, y, size=12, color=C["text2"], lh=18, w=iw - 24)

# ---------- N08 · Importar DAV no NFC-e (decisões P1 e P12) ----------
DAVS_SEM_NOTA = [("004812", "17:42", "Mariana Albuquerque", "Pix + Dinheiro", 95.00, 7),
                 ("004809", "16:58", "Consumidor", "Dinheiro", 18.00, 1),
                 ("004805", "16:20", "Rafael Coelho Nunes", "Débito", 64.00, 3),
                 ("004798", "15:31", "Consumidor", "Pix", 25.00, 1)]

def n08(d, f, dev, app):
    n04(d, f, dev, app, menu=False)
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    win, w, h, top, bot = ui.window(d, f, dev, "Importar DAV no NFC-e", W if mob else 880, 760 if mob else 600, app=app,
                                    footer_buttons=[("Cancelar", "secondary", "Esc"), ("Emitir NFC-e", "primary", "Enter")])
    x = 24 if not mob else 16; cw = w - 2 * x; y = top + 20
    ui.field(d, win, x, y, cw, placeholder="Número do DAV ou cliente", prefix_icon="busca", app=app, focused=False)
    y += 56
    T(d, win, "DAVs de hoje sem nota · Caixa de Arthur", x, y, size=13, color=C["text2"], lh=20); y += 28
    if mob:
        _, th = ui.mobile_rows(d, win, x, y, cw, [(c, f"DAV {n} · {hr} · {pg}", v(t), None, None) for n, hr, c, pg, t, it in DAVS_SEM_NOTA],
                               selected=0, row_h=60)
        y += th + 16
        ui.kv(d, win, x, y, cw, [("Itens", "7"), ("CPF na nota", "123.456.789-09"), ("Vira", f"NFC-e série {SERIE} · nº {num_fmt(NUM + 1)}")])
        return
    lw = 520
    _, th = ui.table(d, win, x, y, lw, [("DAV", 76, "l", True), ("Hora", 56, "l", True), ("Cliente", None, "l"), ("Total", 84, "r", True)],
                     [[n, hr, c, v(t)] for n, hr, c, pg, t, it in DAVS_SEM_NOTA], selected=0, app=app)
    rx = x + lw + 24; rw = cw - lw - 24
    c = ui.card(d, win, rx, y, rw, 52 + 6 * 28 + 12, title="DAV 004812")
    ui.kv(d, c, 20, 52, rw - 40, [("Cliente", "Mariana"), ("CPF na nota", "123.456.789-09"), ("Itens", "7"),
                                   ("Pagamentos", "Pix · Dinheiro"), ("Total", "95,00"),
                                   ("Vira", f"série {SERIE} · nº {num_fmt(NUM + 1)}")], gap=28)

SCREENS = [
    ("N01", "Venda no cupom fiscal", n01),
    ("N02", "Emitindo e autorizada", n02),
    ("N03", "DANFE NFC-e", n03),
    ("N04", "Notas emitidas", n04),
    ("N05", "Contingência", n05),
    ("N06", "Cancelar NFC-e", n06),
    ("N07", "Rejeição da SEFAZ", n07),
    ("N08", "Importar DAV no NFC-e", n08),
]
