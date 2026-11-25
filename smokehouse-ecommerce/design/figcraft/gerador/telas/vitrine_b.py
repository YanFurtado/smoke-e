"""Responsivo · Vitrine, parte B: checkout em 3 passos, pedido enviado, páginas (trocas e guias) e o link do colaborador.

Regras do checkout (src/app.js): passo 1 seus dados (nome, WhatsApp, nascimento para a maioridade), passo 2 retirada
ou entrega com bairro e taxa, passo 3 pagamento (6 formas, parcelamento em até 3x a partir de R$ 60, confirmação de
maioridade) e o pedido sai pelo WhatsApp da loja. Resumo com promoção 3 por 2 e desconto Pix (5%).
Celular: uma coluna, resumo recolhido no topo e o botão de continuar numa barra fixa embaixo.
Computador e tablet: resumo ao lado.
"""
import os
import fc, ui
from ui import C, T, DEVICES, brl, hair
from telas import _dados as D
from telas.vitrine_a import wrap, prateleira, MAIS_VENDIDOS

PAGE = "Responsivo · Vitrine (checkout, páginas e link do colaborador)"
APP = "loja"

LOJA = D.LOJAS["pnz"]
WHATS_LOJA = "(87) 98825-7595"
BAIRROS = {"Centro": 5, "Areia Branca": 7, "Vila Eduardo": 6, "Cidade Universitária": 8}
CARRINHO = [(1, 2), (4, 1), (10, 1), (42, 1), (30, 1)]   # id do produto, quantidade
CLIENTE = {"nome": "Mariana Albuquerque", "whats": "(87) 98841-2207", "nasc": "27/11/1994",
           "bairro": "Areia Branca", "rua": "Rua Dr. Pacífico da Luz", "num": "214"}
PEDIDO = "PNZ-1043"

# ---------- dados e contas (as mesmas do app.js) ----------
def _prod(i):
    return next(p for p in D.PRODUTOS if p[0] == i)

def _totais(tipo="retirada", bairro=None, pag="pix"):
    itens = [(_prod(i), q) for i, q in CARRINHO]
    sub = sum(p[4] * q for p, q in itens)
    sedas = sorted(p[4] for p, q in itens if p[1] == "Sedas" and p[6] for _ in range(q))
    disc = sum(sedas[: len(sedas) // 3])
    fee = BAIRROS.get(bairro, 0) if tipo == "entrega" else 0
    pix = (sub - disc) * 0.05 if pag == "pix" else 0
    base = sub - disc
    mp = min(3, int(base // 30)) if base >= 60 else 1
    return {"itens": itens, "sub": sub, "disc": disc, "fee": fee, "pix": pix, "total": sub - disc - pix + fee,
            "n": sum(q for _, q in itens), "tipo": tipo, "pag": pag, "mp": mp, "bairro": bairro}

PAGAMENTOS = [  # app.js PAYMENTS
    ("pix", "Pix", "5% de desconto · QR code ou chave enviados no WhatsApp"),
    ("credito", "Cartão de crédito", "Até 3x sem juros · Visa, Mastercard, Elo, Hipercard, Amex"),
    ("debito", "Cartão de débito", "Na maquininha, na entrega ou na retirada"),
    ("carteira", "Carteira digital", "Apple Pay, Google Pay, Samsung Pay, PicPay ou Mercado Pago"),
    ("boleto", "Boleto bancário", "Para atacado e revenda · separado após a compensação"),
    ("dinheiro", "Dinheiro", "Na entrega ou na retirada · informe o troco"),
]

# ---------- peças deste módulo ----------
def _nl(s, size, w, weight=400):
    """Linhas que o texto ocupa na largura w (com folga de 5% na medida)."""
    return sum(max(1, -(-int(fc.text_width(seg, size, weight) * 1.02) // int(max(1, w)))) for seg in s.split("\n"))

def _par(d, p, s, x, y, w, size=14, lh=22, color=None, weight=400):
    T(d, p, s, x, y, size=size, weight=weight, color=color or C["text2"], lh=lh, w=w)
    return _nl(s, size, w, weight) * lh

def _kicker(d, p, s, x, y, color=None, align="left"):
    T(d, p, s.upper(), x, y, size=11, weight=700, color=color or C["pos"], lh=16, ls=12, align=align)
    return 16

def _crumbs(d, p, x, y, itens):
    cx = x
    for i, s in enumerate(itens):
        last = i == len(itens) - 1
        T(d, p, s, cx, y, size=12, color=C["muted"] if last else C["text2"], lh=18)
        tw = fc.text_width(s, 12)
        if not last:
            hair(d, p, cx, y + 17, tw)
            T(d, p, "/", cx + tw + 6, y, size=12, color=C["muted"], lh=18)
            cx += tw + 18
    return 18

def _mini(d, p, x, y, s, marca):
    """Miniatura do produto no resumo: bloco na cor da marca com o nome curto pincelado."""
    c1, c2 = ui.marca_cor(marca)
    t = d.frame(p, f"Miniatura {marca}", x, y, s, s, fill=c2, radius=8, clip=True)
    d.frame(t, "Sombra da marca", 0, s * 0.55, s, s * 0.45, fill=c1, fill_opacity=0.55)
    nome = {"BEM BOLADO": "BEM", "PURE HEMP": "HEMP", "SQUADAFUM": "SQUAD"}.get(marca, marca)
    fs = 14
    while fc.text_width(nome, fs, family=ui.DISPLAY) > s - 8 and fs > 7: fs -= 1
    d.text(t, nome, s / 2, (s - fs * 1.1) / 2, size=fs, family=ui.DISPLAY, color="#ffffff", align="center", lh=int(fs * 1.1))
    return t

def _topo_checkout(d, f):
    """Celular: topo enxuto do checkout (voltar, logo e loja). Sem busca nem categorias para não disputar com o formulário."""
    W = DEVICES["mobile"][0]
    bar = d.frame(f, "Topo do checkout", 0, 0, W, 56, fill=C["black"])
    ui.icon(d, bar, "seta-esq", 12, 18, 20, "#ffffff")
    d.image(bar, os.path.join(ui.HERE, "marca", "logo-branco.png"), 40, 8, 44, 38, name="Logo")
    T(d, bar, "Finalizar pedido", 96, 17, size=15, weight=600, color="#ffffff", lh=22)
    pill = d.frame(bar, "Loja escolhida", W - 16 - 58, 14, 58, 28, fill=C["green"], radius=14)
    T(d, pill, LOJA[0], 29, 5, size=11, weight=700, color="#ffffff", align="center", lh=18)
    return 56

def _passos(d, p, x, y, ativo, mob=False):
    nomes = ["Seus dados", "Entrega", "Pagamento"]
    cx = x
    s = 24
    for i, nome in enumerate(nomes):
        n = i + 1
        feito, on = n < ativo, n == ativo
        circ = d.frame(p, f"Passo {n}", cx, y, s, s, fill=C["ink"] if feito else (ui.acc("loja") if on else C["deep"]), radius=s / 2)
        if feito: ui.icon(d, circ, "ok", 4, 4, 16, "#ffffff")
        else: T(d, circ, str(n), s / 2, 3, size=12, weight=600, color="#ffffff" if on else C["text2"], align="center", lh=18)
        size = 12 if mob else 13
        T(d, p, nome, cx + s + 6, y + 3, size=size, weight=600 if on else 500, color=C["ink"] if (on or feito) else C["muted"], lh=18)
        cx += s + 6 + fc.text_width(nome, size, 600 if on else 500)
        if n < 3:
            gap = 10 if mob else 14
            lw = 16 if mob else 28
            hair(d, p, cx + gap, y + s / 2, lw)
            cx += gap * 2 + lw
    return s

def _caixa(d, p, x, y, w, n, titulo, estado, mob, resumo=None):
    """Caixa de um passo. estado: cur (aberto, borda verde), done (resumo e Alterar) ou lock (fechado).
    Devolve (frame, y do conteúdo, padding). Quem chama fecha a altura com _fecha."""
    pad = 16 if mob else 24
    cur = estado == "cur"
    b = d.frame(p, f"Passo {n} · {titulo}", x, y, w, 10, fill=C["card"] if estado != "lock" else C["raised"],
                stroke=ui.acc("loja") if cur else C["line"], stroke_opacity=1.0 if cur else 0.10, stroke_w=2 if cur else 1, radius=12)
    ts = 16 if mob else 18
    T(d, b, f"{n}. {titulo}", pad, pad - 2, size=ts, weight=600, color=C["muted"] if estado == "lock" else C["ink"], lh=26)
    yy = pad + 26
    if estado == "done":
        T(d, b, "Alterar", w - pad, pad + 1, size=13, weight=600, color=ui.acc("loja"), align="right", lh=20)
        yy += 6
        yy += _par(d, b, resumo, pad, yy, w - 2 * pad, size=13, lh=20)
        yy += pad
        d.nodes[b]["height"] = float(yy)
    elif estado == "lock":
        ui.icon(d, b, "cadeado", w - pad - 16, pad + 3, 16, C["muted"])
        d.nodes[b]["height"] = float(yy + pad - 4)
    else:
        yy += 14
    return b, yy, pad

def _fecha(d, b, h):
    d.nodes[b]["height"] = float(h)
    return h

def _opcao_h(w, sub):
    return 16 + 20 + 2 + _nl(sub, 12, w - 44 - 16) * 18 + 14

def _opcao(d, p, x, y, w, titulo, sub, on, tag=None, h=None):
    """Escolha em cartão (retirada/entrega, forma de pagamento): rádio, título e linha de apoio. Devolve a altura."""
    tw = w - 44 - 16 - (48 if tag else 0)
    h = h or _opcao_h(w, sub)
    o = d.frame(p, f"Opção {titulo}", x, y, w, h, fill=ui.APPS["loja"]["soft"] if on else C["card"],
                stroke=ui.acc("loja") if on else C["line"], stroke_opacity=1.0 if on else 0.14, stroke_w=2 if on else 1, radius=10)
    ui.radio(d, o, 16, 17, on=on, app="loja")
    T(d, o, titulo, 44, 14, size=14, weight=600, lh=20, w=tw)
    T(d, o, sub, 44, 36, size=12, color=C["text2"], lh=18, w=w - 44 - 16)
    if tag:
        tg = d.frame(o, "Selo", w - 12 - 44, 13, 44, 22, fill=C["yellow"], radius=4)
        T(d, tg, tag, 22, 3, size=11, weight=700, align="center", lh=16)
    return h

def _resumo(d, p, x, y, w, t, seller=None):
    """Resumo do pedido ao lado do checkout (computador e tablet)."""
    pad = 20
    b = d.frame(p, "Resumo do pedido", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
    T(d, b, f"Resumo · loja {LOJA[0]}", pad, pad, size=16, weight=600, lh=24)
    T(d, b, f"{t['n']} itens", w - pad, pad + 2, size=12, color=C["muted"], align="right", lh=20)
    yy = pad + 40
    for prod, q in t["itens"]:
        pid, cat, marca, nome, preco = prod[:5]
        _mini(d, b, pad, yy, 44, marca)
        vw = fc.text_width(brl(preco * q), 13, 600)
        nw = w - 2 * pad - 56 - vw - 12
        nl = _nl(nome, 13, nw, 500)
        T(d, b, nome, pad + 56, yy, size=13, weight=500, lh=18, w=nw)
        T(d, b, f"{q} × {brl(preco)}", pad + 56, yy + nl * 18 + 2, size=12, color=C["muted"], lh=16)
        T(d, b, brl(preco * q), w - pad, yy + 1, size=13, weight=600, align="right", lh=18)
        yy += max(44, nl * 18 + 20) + 14
    hair(d, b, pad, yy, w - 2 * pad); yy += 14
    linhas = [("Subtotal", brl(t["sub"]), None)]
    if t["disc"]: linhas.append(("Promoção 3 por 2", "-" + brl(t["disc"]), "ok"))
    if t["pix"]: linhas.append(("Desconto Pix (5%)", "-" + brl(t["pix"]), "ok"))
    if t["tipo"] == "entrega":
        linhas.append((f"Entrega · {t['bairro']}" if t["bairro"] else "Entrega", brl(t["fee"]) if t["bairro"] else "Escolha o bairro", None))
    else:
        linhas.append(("Retirada na loja", "Grátis", None))
    for k, v, tone in linhas:
        col = C["pos"] if tone == "ok" else C["ink"]
        T(d, b, k, pad, yy, size=13, color=col if tone else C["text2"], weight=500 if tone else 400, lh=20)
        T(d, b, v, w - pad, yy, size=13, color=col, weight=500 if tone else 400, align="right", lh=20)
        yy += 26
    yy += 4
    hair(d, b, pad, yy, w - 2 * pad); yy += 14
    T(d, b, "Total", pad, yy + 2, size=17, weight=700, lh=24)
    T(d, b, brl(t["total"]), w - pad, yy, size=22, weight=700, align="right", lh=28)
    yy += 32
    if t["pag"] == "credito" and t["mp"] > 1:
        T(d, b, f"em {t['mp']}x de {brl(t['total'] / t['mp'])} sem juros no cartão", w - pad, yy, size=12, color=C["muted"], align="right", lh=18)
        yy += 22
    elif t["pag"] == "pix":
        T(d, b, "com 5% de desconto no Pix", w - pad, yy, size=12, color=C["pos"], weight=500, align="right", lh=18)
        yy += 22
    if seller:
        yy += 4
        at = d.frame(b, "Atendimento", pad, yy, w - 2 * pad, 40, fill=ui.APPS["loja"]["soft"], radius=8)
        ui.icon(d, at, "pessoa", 12, 12, 16, C["pos"])
        T(d, at, f"Atendimento: {seller}", 36, 10, size=13, weight=500, lh=20)
        yy += 52
    yy += 8
    ui.button(d, b, pad, yy, "Editar carrinho", app="loja", kind="secondary", w=w - 2 * pad, h=44)
    yy += 44 + pad
    d.nodes[b]["height"] = float(yy)
    return yy

def _resumo_recolhido(d, p, x, y, w, t):
    """Celular: resumo do pedido recolhido no topo (toque abre a lista de itens)."""
    b = d.frame(p, "Resumo recolhido", x, y, w, 60, fill=C["card"], stroke=C["line"], stroke_opacity=0.10, radius=12)
    ic = d.frame(b, "Ícone", 12, 12, 36, 36, fill=ui.APPS["loja"]["soft"], radius=18)
    ui.icon(d, ic, "caixa", 9, 9, 18, C["pos"])
    T(d, b, "Resumo do pedido", 58, 10, size=14, weight=600, lh=20)
    T(d, b, f"{t['n']} itens · loja {LOJA[0]}", 58, 31, size=12, color=C["muted"], lh=18)
    T(d, b, brl(t["total"]), w - 40, 19, size=15, weight=700, align="right", lh=22)
    ui.icon(d, b, "seta-baixo", w - 30, 22, 16, C["text2"])
    return 60

def _checkout(d, f, dev, app, passo):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    tipo = "retirada" if passo == 1 else "entrega"
    pag = "credito" if passo == 3 else "pix"
    t = _totais(tipo, CLIENTE["bairro"] if passo >= 2 else None, pag)
    ui.altura(d, f, 2400)
    x, cw = wrap(dev)
    if mob:
        y = _topo_checkout(d, f) + 16
        y += _passos(d, f, x, y, passo, mob=True) + 16
        y += _resumo_recolhido(d, f, x, y, cw, t) + 16
        lx, lw = x, cw
        aside_y = None
    else:
        y = ui.loja_header(d, f, dev, cart_n=t["n"], cart_total=t["sub"] - t["disc"]) + 24
        _crumbs(d, f, x, y, ["Voltar para a loja", "Finalizar pedido"])
        y += 36
        aside_y = y
        aw = 380 if dev == "desktop" else 340
        gap = 32 if dev == "desktop" else 24
        lx, lw = x, cw - aw - gap
        ui.brush(d, f, x, y, [("FINALIZAR", "ink"), ("PEDIDO", "green")], size=44)
        y += 56
        y += _passos(d, f, x, y, passo) + 24
    gap_b = 12 if mob else 16
    # passo 1
    if passo > 1:
        b, _, _ = _caixa(d, f, lx, y, lw, 1, "Seus dados", "done", mob, f"{CLIENTE['nome']} · {CLIENTE['whats']}")
        y += d.nodes[b]["height"] + gap_b
    else:
        b, yy, pad = _caixa(d, f, lx, y, lw, 1, "Seus dados", "cur", mob)
        iw = lw - 2 * pad
        fh = 48 if mob else 44
        _, h = ui.field(d, b, pad, yy, iw, label="Nome completo", value=CLIENTE["nome"], h=fh); yy += h + 16
        if mob:
            _, h = ui.field(d, b, pad, yy, iw, label="WhatsApp", value=CLIENTE["whats"], h=fh); yy += h + 16
            _, h = ui.field(d, b, pad, yy, iw, label="Data de nascimento", value=CLIENTE["nasc"], focused=True, h=fh); yy += h + 12
        else:
            hw = (iw - 16) / 2
            ui.field(d, b, pad, yy, hw, label="WhatsApp", value=CLIENTE["whats"], h=fh)
            _, h = ui.field(d, b, pad + hw + 16, yy, hw, label="Data de nascimento", value=CLIENTE["nasc"], focused=True, h=fh); yy += h + 12
        nota = d.frame(b, "Maioridade", pad, yy, iw, 10, fill=C["raised"], radius=8)
        ui.icon(d, nota, "dica", 12, 12, 16, C["pos"])
        nh = _par(d, nota, "Usamos a data de nascimento para confirmar a maioridade. O documento com foto é conferido na retirada ou na entrega",
                  36, 10, iw - 48, size=12, lh=18)
        d.nodes[nota]["height"] = float(nh + 20); yy += nh + 20 + 20
        if not mob:
            ui.button(d, b, pad, yy, "Continuar", app="loja", kind="primary", w=168, h=44); yy += 44
        y += _fecha(d, b, yy + pad) + gap_b
    # passo 2
    if passo > 2:
        b, _, _ = _caixa(d, f, lx, y, lw, 2, "Entrega ou retirada", "done", mob,
                         f"Entrega em {CLIENTE['rua']}, {CLIENTE['num']} · {CLIENTE['bairro']} · 20 a 60 min")
        y += d.nodes[b]["height"] + gap_b
    elif passo < 2:
        b, _, _ = _caixa(d, f, lx, y, lw, 2, "Entrega ou retirada", "lock", mob)
        y += d.nodes[b]["height"] + gap_b
    else:
        b, yy, pad = _caixa(d, f, lx, y, lw, 2, "Entrega ou retirada", "cur", mob)
        iw = lw - 2 * pad
        fh = 48 if mob else 44
        ops = [("Retirar na loja", f"Grátis · {LOJA[2].split(' · ')[0]}", False), ("Receber em casa", "20 a 60 min · taxa por bairro", True)]
        if mob:
            for a, s, on in ops:
                yy += _opcao(d, b, pad, yy, iw, a, s, on) + 10
            yy += 6
        else:
            hw = (iw - 12) / 2
            hh = max(_opcao_h(hw, s) for a, s, on in ops)
            for i, (a, s, on) in enumerate(ops):
                _opcao(d, b, pad + i * (hw + 12), yy, hw, a, s, on, h=hh)
            yy += hh + 20
        _, h = ui.field(d, b, pad, yy, iw, label="Bairro", value=f"{CLIENTE['bairro']} · {brl(BAIRROS[CLIENTE['bairro']])}", chevron=True, h=fh); yy += h + 16
        _, h = ui.field(d, b, pad, yy, iw, label="Rua", value=CLIENTE["rua"], h=fh); yy += h + 16
        nw = 112 if mob else (iw - 16) / 2
        ui.field(d, b, pad, yy, nw, label="Número", value=CLIENTE["num"], focused=True, h=fh)
        _, h = ui.field(d, b, pad + nw + 12, yy, iw - nw - 12, label="Complemento", placeholder="Apto, bloco", h=fh); yy += h + 16
        _, h = ui.field(d, b, pad, yy, iw, label="Ponto de referência", placeholder="Opcional", h=fh); yy += h + 12
        yy += _par(d, b, "A taxa do bairro entra no total. Fora da lista, a loja confirma a taxa pelo WhatsApp", pad, yy, iw, size=12, lh=18, color=C["muted"]) + 20
        if not mob:
            ui.button(d, b, pad, yy, "Continuar", app="loja", kind="primary", w=168, h=44); yy += 44
        y += _fecha(d, b, yy + pad) + gap_b
    # passo 3
    if passo < 3:
        b, _, _ = _caixa(d, f, lx, y, lw, 3, "Pagamento", "lock", mob)
        y += d.nodes[b]["height"]
    else:
        b, yy, pad = _caixa(d, f, lx, y, lw, 3, "Pagamento", "cur", mob)
        iw = lw - 2 * pad
        cols = 1 if mob else 2
        ow = (iw - 12 * (cols - 1)) / cols
        ry = yy
        for r in range(-(-len(PAGAMENTOS) // cols)):
            linha = list(enumerate(PAGAMENTOS))[r * cols:(r + 1) * cols]
            hmax = max(_opcao_h(ow, desc) for _, (k, lab, desc) in linha)
            for i, (k, lab, desc) in linha:
                _opcao(d, b, pad + (i % cols) * (ow + 12), ry, ow, lab, desc, k == pag, tag="-5%" if k == "pix" else None, h=hmax)
            ry += hmax + 10
        yy = ry + 10
        # parcelamento (crédito, a partir de R$ 60, até 3x sem juros)
        T(d, b, "Parcelamento", pad, yy, size=13, color=C["text2"], lh=16); yy += 22
        parc = [f"{i + 1}x de {brl(t['total'] / (i + 1))}" + (" sem juros" if i else "") for i in range(t["mp"])]
        if mob:
            for i, s in enumerate(parc):
                on = i == t["mp"] - 1
                o = d.frame(b, f"Parcela {s}", pad, yy, iw, 44, fill=ui.APPS["loja"]["soft"] if on else C["card"],
                            stroke=ui.acc("loja") if on else C["line"], stroke_opacity=1.0 if on else 0.14, stroke_w=2 if on else 1, radius=8)
                ui.radio(d, o, 14, 13, on=on)
                T(d, o, s, 42, 12, size=14, weight=600 if on else 400, lh=20)
                yy += 52
        else:
            pw = (iw - 12 * (len(parc) - 1)) / len(parc)
            for i, s in enumerate(parc):
                on = i == t["mp"] - 1
                o = d.frame(b, f"Parcela {s}", pad + i * (pw + 12), yy, pw, 44, fill=ui.APPS["loja"]["soft"] if on else C["card"],
                            stroke=ui.acc("loja") if on else C["line"], stroke_opacity=1.0 if on else 0.14, stroke_w=2 if on else 1, radius=8)
                ui.radio(d, o, 14, 13, on=on)
                T(d, o, s, 42, 12, size=13, weight=600 if on else 400, lh=20)
            yy += 52
        yy += 8
        _, h = ui.field(d, b, pad, yy, iw, label="Observações", placeholder="Opcional", h=64); yy += h + 20
        ok = d.frame(b, "Confirmação de maioridade", pad, yy, iw, 10, fill=C["raised"], radius=8)
        ui.checkbox(d, ok, 14, 15, on=True)
        mh = _par(d, ok, "Confirmo que tenho 18 anos ou mais e vou apresentar documento com foto", 44, 12, iw - 58, size=13, lh=20, color=C["ink"], weight=500)
        d.nodes[ok]["height"] = float(mh + 24); yy += mh + 24 + 20
        if not mob:
            _, bw = ui.button(d, b, pad, yy, f"Confirmar pedido · {brl(t['total'])}", app="loja", kind="primary", h=48, icon_name="whats")
            yy += 48 + 12
        wa = d.frame(b, "Sai pelo WhatsApp", pad, yy, iw, 10)
        ui.icon(d, wa, "whats", 0, 2, 16, C["pos"])
        wh = _par(d, wa, f"O pedido vai para o WhatsApp da loja {LOJA[0]}, que confirma o pagamento e a entrega", 24, 0, iw - 24, size=12, lh=18, color=C["muted"])
        d.nodes[wa]["height"] = float(wh); yy += wh
        y += _fecha(d, b, yy + pad)
    if mob:
        total = y + 24 + 88
        ui.altura(d, f, total)
        cap = {1: "Total no Pix", 2: f"Total no Pix · entrega {brl(t['fee'])}", 3: f"Total · {t['mp']}x de {brl(t['total'] / t['mp'])}"}[passo]
        ui.mobile_bar(d, f, brl(t["total"]), caption=cap, app=app, label="Confirmar pedido" if passo == 3 else "Continuar")
        return total
    ah = _resumo(d, f, x + lw + (32 if dev == "desktop" else 24), aside_y, cw - lw - (32 if dev == "desktop" else 24), t)
    total = max(H, max(y, aside_y + ah) + 64)
    ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

def e09(d, f, dev, app): return _checkout(d, f, dev, app, 1)
def e10(d, f, dev, app): return _checkout(d, f, dev, app, 2)
def e11(d, f, dev, app): return _checkout(d, f, dev, app, 3)

# ---------- E12 pedido enviado ----------
def _mensagem(t):
    """Texto que vai para o WhatsApp da loja (orderMsg do app.js), linha a linha: (texto, negrito)."""
    m = [(f"Pedido {PEDIDO} · Smoke House {LOJA[0]}", True), ("", False),
         (f"Cliente: {CLIENTE['nome']}", False), (f"WhatsApp: {CLIENTE['whats']}", False), ("", False), ("Itens", True)]
    for p, q in t["itens"]:
        m.append((f"• {q}x {p[3]} · {brl(p[4] * q)}", False))
    m += [("", False), (f"Subtotal: {brl(t['sub'])}", False), (f"Promoção 3 por 2: -{brl(t['disc'])}", False),
          (f"Entrega: {brl(t['fee'])}", False), ("", False),
          (f"Endereço: {CLIENTE['rua']}, {CLIENTE['num']} · {CLIENTE['bairro']}", False), ("", False),
          (f"Total: {brl(t['total'])}", True), (f"Pagamento: Cartão de crédito em {t['mp']}x sem juros", True)]
    return m

def _bolha(d, p, x, y, w, t):
    """Prévia da mensagem do pedido como balão do WhatsApp."""
    pad = 14
    b = d.frame(p, "Mensagem do pedido", x, y, w, 10, fill="#dcf3e3", radius=[12, 12, 2, 12])
    yy = pad
    for s, bold in _mensagem(t):
        if not s:
            yy += 8; continue
        yy += _par(d, b, s, pad, yy, w - 2 * pad, size=12, lh=18, color=C["ink"], weight=600 if bold else 400)
    T(d, b, "agora", w - pad, yy + 2, size=10, color=C["muted"], align="right", lh=14)
    yy += 18 + pad - 4
    d.nodes[b]["height"] = float(yy)
    return yy

def e12(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    t = _totais("entrega", CLIENTE["bairro"], "credito")
    ui.altura(d, f, 2600)
    x, cw = wrap(dev)
    y = ui.loja_header(d, f, dev, cart_n=0, cart_total=0) + (24 if mob else 48)
    if mob:
        lx, lw = x, cw
    else:
        rw = 440 if dev == "desktop" else 400
        gap = 48 if dev == "desktop" else 32
        lw = min(660, cw - rw - gap)
        tot_w = lw + gap + rw
        lx = x + (cw - tot_w) / 2
    y0 = y
    ok = d.frame(f, "Pedido registrado", lx, y, 64 if not mob else 56, 64 if not mob else 56, fill=C["green"], radius=32)
    s = 64 if not mob else 56
    ui.icon(d, ok, "ok", s * 0.25, s * 0.25, s * 0.5, "#ffffff")
    y += s + 20
    bs = 48 if not mob else 34
    ui.brush(d, f, lx, y, [("PEDIDO", "ink"), ("REGISTRADO!", "green")], size=bs)
    y += int(bs * 1.1) + 12
    T(d, f, "Número do pedido", lx, y, size=14, color=C["text2"], lh=22)
    nb = d.frame(f, "Número", lx + fc.text_width("Número do pedido", 14) + 10, y - 3, fc.text_width(PEDIDO, 14, 700) + 20, 28, fill=C["yellow"], radius=6)
    T(d, nb, PEDIDO, 10, 4, size=14, weight=700, lh=20)
    y += 36
    y += _par(d, f, f"Envie o pedido pelo WhatsApp da loja {LOJA[0]} para confirmar o pagamento e a entrega", lx, y, min(lw, 520), size=15 if not mob else 14, lh=24 if not mob else 22, color=C["ink"]) + 24
    # recibo
    pad = 20
    r = d.frame(f, "Recibo", lx, y, lw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
    yy = pad
    for p, q in t["itens"]:
        vw = fc.text_width(brl(p[4] * q), 13)
        nw = lw - 2 * pad - vw - 16
        T(d, r, f"{q}× {p[3]}", pad, yy, size=13, lh=20, w=nw)
        T(d, r, brl(p[4] * q), lw - pad, yy, size=13, align="right", lh=20)
        yy += _nl(f"{q}× {p[3]}", 13, nw) * 20 + 8
    hair(d, r, pad, yy + 2, lw - 2 * pad); yy += 14
    for k, v, tone in [("Promoção 3 por 2", "-" + brl(t["disc"]), "ok"), (f"Entrega · {CLIENTE['bairro']}", brl(t["fee"]), None)]:
        T(d, r, k, pad, yy, size=13, color=C["pos"] if tone else C["text2"], weight=500 if tone else 400, lh=20)
        T(d, r, v, lw - pad, yy, size=13, color=C["pos"] if tone else C["ink"], weight=500 if tone else 400, align="right", lh=20)
        yy += 28
    hair(d, r, pad, yy + 2, lw - 2 * pad); yy += 16
    T(d, r, "Total", pad, yy, size=15, weight=700, lh=22)
    T(d, r, f"Cartão de crédito em {t['mp']}x de {brl(t['total'] / t['mp'])} sem juros", pad, yy + 24, size=12, color=C["muted"], lh=18, w=lw - 2 * pad - 110)
    T(d, r, brl(t["total"]), lw - pad, yy + 4, size=20, weight=700, align="right", lh=28)
    yy += 24 + _nl(f"Cartão de crédito em {t['mp']}x de {brl(t['total'] / t['mp'])} sem juros", 12, lw - 2 * pad - 110) * 18 + pad
    d.nodes[r]["height"] = float(yy)
    y += yy + 24
    # próximos passos
    passos = [("whats", "Envie pelo WhatsApp", f"A mensagem já sai pronta para a loja {LOJA[0]}"),
              ("moeda", "A loja confirma o pagamento", "Link seguro do cartão no WhatsApp ou maquininha na entrega"),
              ("caminhao", "Entrega em 20 a 60 min", "O entregador confere um documento com foto de maior de 18 anos")]
    T(d, f, "Próximos passos", lx, y, size=16, weight=600, lh=24); y += 36
    for ic, a, s2 in passos:
        o = d.frame(f, f"Passo {a}", lx, y, 36, 36, fill=ui.APPS["loja"]["soft"], radius=18)
        ui.icon(d, o, ic, 10, 10, 16, C["pos"])
        T(d, f, a, lx + 50, y - 1, size=14, weight=600, lh=20)
        sh = _par(d, f, s2, lx + 50, y + 20, lw - 50, size=13, lh=20, color=C["muted"])
        y += max(44, 20 + sh) + 12
    y += 12
    if not mob:
        bx = lx
        b1, w1 = ui.button(d, f, bx, y, "Enviar pelo WhatsApp", app="loja", kind="primary", h=48, icon_name="whats"); bx += w1 + 12
        b2, w2 = ui.button(d, f, bx, y, "Copiar pedido", app="loja", kind="secondary", h=48); bx += w2 + 12
        ui.button(d, f, bx, y, "Voltar para a loja", app="loja", kind="dark", h=48)
        y += 48 + 16
        # prévia da mensagem ao lado
        px = lx + lw + gap
        T(d, f, "Mensagem que vai para a loja", px, y0 + 4, size=13, weight=600, color=C["text2"], lh=20)
        chat = d.frame(f, "WhatsApp da loja", px, y0 + 36, rw, 10, fill="#efeae2", radius=16, clip=True)
        hd = d.frame(chat, "Contato", 0, 0, rw, 56, fill=C["black"])
        o = d.frame(hd, "Foto da loja", 14, 10, 36, 36, fill=C["green"], radius=18)
        T(d, o, LOJA[0], 18, 9, size=10, weight=700, color="#ffffff", align="center", lh=18)
        T(d, hd, f"Smoke House {LOJA[0]}", 60, 9, size=14, weight=600, color="#ffffff", lh=20)
        T(d, hd, WHATS_LOJA, 60, 29, size=11, color="#b9bbb4", lh=16)
        bh = _bolha(d, chat, 40, 72, rw - 56, t)
        d.nodes[chat]["height"] = float(72 + bh + 20)
        y = max(y, y0 + 36 + 72 + bh + 20)
    else:
        y += 4
        b2, _ = ui.button(d, f, lx, y, "Copiar pedido", app="loja", kind="secondary", w=(lw - 12) / 2, h=44)
        ui.button(d, f, lx + (lw - 12) / 2 + 12, y, "Voltar para a loja", app="loja", kind="dark", w=(lw - 12) / 2, h=44)
        y += 44 + 16
    if mob:
        total = y + 24 + 88
        ui.altura(d, f, total)
        bar = d.frame(f, "Barra de ação", 0, total - 88, W, 88, fill=C["card"])
        hair(d, bar, 0, 0, W)
        ui.button(d, bar, 16, 22, "Enviar pelo WhatsApp", app="loja", kind="primary", w=W - 32, h=48, icon_name="whats")
        return total
    total = max(H, y + 64)
    ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

# ---------- páginas institucionais ----------
PAGINAS_AJUDA = ["Entrega e retirada", "Trocas e devoluções", "Formas de pagamento", "Regras de promoção",
                 "Privacidade e cookies", "Termos de uso", "Quem somos", "Guias"]

TROCAS = [  # app.js PAGES.trocas
    ("Arrependimento em compras pelo site", "Compras feitas pelo site ou pelo WhatsApp podem ser canceladas em até 7 dias corridos após o recebimento, como garante o Código de Defesa do Consumidor. O valor pago é devolvido integralmente."),
    ("Produto com defeito", "Avise a loja pelo WhatsApp com foto do problema. O prazo para reclamar é de 30 dias para produtos não duráveis e de 90 dias para produtos duráveis, contados do recebimento. Fazemos a troca, o conserto ou a devolução do valor."),
    ("Comprou o item errado?", "Se o produto estiver lacrado e sem uso, trocamos por outro da loja. Para materiais de tatuagem, consulte a equipe antes da compra: confirmamos a referência certa com você ou com o seu tatuador."),
    ("Itens estéreis e de higiene", "Por segurança sanitária, cartuchos, agulhas e itens de uso pessoal só voltam ao estoque com a embalagem original lacrada."),
    ("Como solicitar", "Fale com a loja onde você comprou, informe o número do pedido e o motivo. Respondemos no mesmo dia, dentro do horário de funcionamento."),
]

def _menu_ajuda(d, f, x, y, w, ativo):
    """Computador e tablet: lista lateral das páginas de ajuda (hoje são botões soltos no fim do texto)."""
    T(d, f, "Ajuda e institucional", x, y, size=13, weight=600, color=C["text2"], lh=20)
    yy = y + 32
    for s in PAGINAS_AJUDA:
        on = s == ativo
        it = d.frame(f, f"Página {s}", x, yy, w, 40, fill=C["card"] if on else None, radius=8)
        if on: d.frame(it, "Marca", 0, 8, 3, 24, fill=C["green"], radius=2)
        T(d, it, s, 14, 10, size=14, weight=600 if on else 400, color=C["ink"] if on else C["text2"], lh=20)
        yy += 44
    return yy - y

def _cabeca_pagina(d, f, dev, x, y, w, crumb, kicker, partes, lead):
    mob = dev == "mobile"
    _crumbs(d, f, x, y, ["Início", crumb]); y += 18 + (20 if not mob else 16)
    _kicker(d, f, kicker, x, y); y += 16 + 6
    size = 52 if dev == "desktop" else (46 if dev == "tablet" else 34)
    ui.brush(d, f, x, y, partes, size=size)
    y += int(size * 1.1) + 12
    y += _par(d, f, lead, x, y, w, size=16 if not mob else 15, lh=26 if not mob else 24, color=C["text2"])
    return y

def e13(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    ui.altura(d, f, 3000)
    x, cw = wrap(dev)
    y = ui.loja_header(d, f, dev) + (24 if mob else 40)
    if mob:
        ax, aw = x, cw
    else:
        nw = 248 if dev == "desktop" else 232
        gap = 72 if dev == "desktop" else 40
        _menu_ajuda(d, f, x, y + 38, nw, "Trocas e devoluções")
        ax, aw = x + nw + gap, min(760, cw - nw - gap)
    y = _cabeca_pagina(d, f, dev, ax, y, aw, "Trocas e devoluções", "Ajuda", [("TROCAS E", "ink"), ("DEVOLUÇÕES", "green")],
                       "Queremos que você saia satisfeito. Estas são as regras para trocar ou devolver um produto") + 28
    # prazos em destaque (os números do texto, para achar de relance)
    prazos = [("7 dias", "para desistir de compra feita pelo site ou WhatsApp"),
              ("30 dias", "para reclamar de defeito em produto não durável"),
              ("90 dias", "para reclamar de defeito em produto durável")]
    if mob:
        for a, s in prazos:
            c = d.frame(f, f"Prazo {a}", ax, y, aw, 64, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
            T(d, c, a.upper(), 16, 16, size=24, family=ui.DISPLAY, color=C["green"], lh=28)
            T(d, c, s, 104, 12, size=13, color=C["text2"], lh=20, w=aw - 120)
            y += 64 + 10
        y += 22
    else:
        pw = (aw - 24) / 3
        hmax = 0
        for i, (a, s) in enumerate(prazos):
            c = d.frame(f, f"Prazo {a}", ax + i * (pw + 12), y, pw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
            T(d, c, a.upper(), 18, 16, size=30, family=ui.DISPLAY, color=C["green"], lh=34)
            hh = 58 + _par(d, c, s, 18, 58, pw - 36, size=13, lh=20) + 16
            d.nodes[c]["height"] = float(hh); hmax = max(hmax, hh)
        for cid in d.nodes[f]["children"][-3:]:
            d.nodes[cid]["height"] = float(hmax)
        y += hmax + 40
    for h2, p in TROCAS:
        T(d, f, h2, ax, y, size=19 if not mob else 17, weight=600, lh=28, w=aw); y += _nl(h2, 19 if not mob else 17, aw, 600) * 28 + 10
        y += _par(d, f, p, ax, y, aw, size=15 if not mob else 14, lh=26 if not mob else 23, color=C["text2"]) + (32 if not mob else 26)
    # chamada para falar com a loja
    pad = 24 if not mob else 18
    cta = d.frame(f, "Falar com a loja", ax, y, aw, 10, fill=C["black"], radius=12)
    T(d, cta, "Precisa trocar ou devolver?", pad, pad, size=17, weight=600, color="#ffffff", lh=24)
    th = _par(d, cta, f"Fale com a loja {LOJA[0]} pelo WhatsApp {WHATS_LOJA} e tenha o número do pedido em mãos", pad, pad + 30,
              aw - 2 * pad - (200 if not mob else 0), size=13, lh=20, color="#c9cac4")
    if mob:
        yy = pad + 30 + th + 16
        ui.button(d, cta, pad, yy, "Falar com a loja", app="loja", kind="primary", w=aw - 2 * pad, h=44, icon_name="whats")
        hh = yy + 44 + pad
    else:
        hh = max(pad + 30 + th + pad, 96)
        ui.button(d, cta, aw - pad - 180, (hh - 44) / 2, "Falar com a loja", app="loja", kind="primary", w=180, h=44, icon_name="whats")
    d.nodes[cta]["height"] = float(hh)
    y += hh + 32
    if mob:
        T(d, f, "Outras páginas de ajuda", ax, y, size=15, weight=600, lh=22); y += 34
        lst = d.frame(f, "Páginas de ajuda", ax, y, aw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12)
        yy = 0
        outras = [s for s in PAGINAS_AJUDA if s != "Trocas e devoluções"]
        for i, s in enumerate(outras):
            T(d, lst, s, 16, yy + 14, size=14, lh=20)
            ui.icon(d, lst, "seta-dir", aw - 32, yy + 16, 16, C["muted"])
            if i < len(outras) - 1: hair(d, lst, 16, yy + 48, aw - 32)
            yy += 49
        d.nodes[lst]["height"] = float(yy)
        y += yy + 24
        total = y + 120
        ui.altura(d, f, total)
        ui.bottom_nav(d, f, "Início")
        ui.whats_fab(d, f, dev)
        return total
    total = max(H, y + 40)
    ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

# ---------- E14 guias ----------
GUIAS = [  # app.js GUIDES
    ("Guia de compra", "3 min", "Como escolher a sua seda", "Tamanho, tipo de papel e espessura explicados em 3 minutos.", "seda", C["yellow"]),
    ("Tattoo Supply", "4 min", "Começando na tatuagem: para que serve cada material", "Cartucho, tinta, pele de treino e pós-tattoo sem confusão.", "coroa", C["green"]),
    ("Ideias de presente", "2 min", "Três tipos de pessoa, três ideias de presente", "Do colecionador ao prático: acerte o presente sem complicar.", "trevo", C["black"]),
]

def _cartao_guia(d, f, x, y, w, g, img_h, horizontal=False):
    kick, tempo, titulo, desc, img, bg = g
    pad = 20 if not horizontal else 16
    c = d.frame(f, f"Guia {titulo}"[:40], x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=12, clip=True)
    iw = w if not horizontal else 128
    ih = img_h
    ib = d.frame(c, "Imagem", 0, 0, iw, ih, fill=bg)
    s = min(iw, ih) * 0.7
    d.image(ib, os.path.join(ui.HERE, "marca", img + ".png"), (iw - s) / 2, (ih - s) / 2, s, s, name=img, mode="fit")
    tx = pad if not horizontal else iw + pad
    tw = w - tx - pad
    yy = (ih + pad) if not horizontal else pad - 2
    _kicker(d, c, f"{kick} · {tempo}", tx, yy); yy += 24
    ts = 18 if not horizontal else 15
    T(d, c, titulo, tx, yy, size=ts, weight=600, lh=26 if not horizontal else 22, w=tw)
    yy += _nl(titulo, ts, tw, 600) * (26 if not horizontal else 22) + 8
    yy += _par(d, c, desc, tx, yy, tw, size=13, lh=20, color=C["muted"]) + 14
    T(d, c, "Ler guia", tx, yy, size=13, weight=600, lh=20)
    ui.icon(d, c, "seta-dir", tx + fc.text_width("Ler guia", 13, 600) + 4, yy + 2, 16, C["ink"])
    d.frame(c, "Sublinhado", tx, yy + 22, fc.text_width("Ler guia", 13, 600), 2, fill=C["yellow"])
    yy += 24 + pad
    h = max(yy, ih) if horizontal else yy
    if horizontal: d.nodes[ib]["height"] = float(h)
    d.nodes[c]["height"] = float(h)
    return h

def e14(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    ui.altura(d, f, 2400)
    x, cw = wrap(dev)
    y = ui.loja_header(d, f, dev) + (24 if mob else 40)
    y = _cabeca_pagina(d, f, dev, x, y, min(cw, 720), "Guias Smoke House", "Conteúdo", [("GUIAS", "ink"), ("SMOKE HOUSE", "green")],
                       "Explicações rápidas para você comprar certo, escritas por quem atende no balcão todos os dias") + 32
    if mob:
        # o primeiro guia em destaque, os outros em cartões horizontais (cabe mais na tela)
        y += _cartao_guia(d, f, x, y, cw, GUIAS[0], 176) + 12
        for g in GUIAS[1:]:
            y += _cartao_guia(d, f, x, y, cw, g, 150, horizontal=True) + 12
        y += 12
    else:
        gap = 24 if dev == "desktop" else 16
        gw = (cw - 2 * gap) / 3
        hs = [_cartao_guia(d, f, x + i * (gw + gap), y, gw, g, 220 if dev == "desktop" else 190) for i, g in enumerate(GUIAS)]
        for cid in d.nodes[f]["children"][-3:]:
            d.nodes[cid]["height"] = float(max(hs))
        y += max(hs) + 40
    # chamada: dúvida vai para o WhatsApp da loja
    pad = 20
    cl = d.frame(f, "Ainda em dúvida", x, y, cw, 10, fill=ui.APPS["loja"]["soft"], radius=12)
    o = d.frame(cl, "Ícone", pad, pad, 40, 40, fill=C["green"], radius=20)
    ui.icon(d, o, "whats", 12, 12, 16, "#ffffff")
    tw = cw - pad * 2 - 56 - (220 if not mob else 0)
    T(d, cl, "Ainda em dúvida?", pad + 56, pad, size=15, weight=600, lh=22)
    th = _par(d, cl, f"Conte para a equipe da loja {LOJA[0]} o que você procura e o seu orçamento. A gente indica pelo WhatsApp", pad + 56, pad + 24, tw, size=13, lh=20)
    if mob:
        hh = pad + 24 + th + 16
        ui.button(d, cl, pad, hh, "Falar com a loja", app="loja", kind="primary", w=cw - 2 * pad, h=44)
        hh += 44 + pad
    else:
        hh = max(pad + 24 + th + pad, 84)
        ui.button(d, cl, cw - pad - 180, (hh - 44) / 2, "Falar com a loja", app="loja", kind="primary", w=180, h=44)
    d.nodes[cl]["height"] = float(hh)
    y += hh + 32
    if mob:
        total = y + 120
        ui.altura(d, f, total)
        ui.bottom_nav(d, f, "Início")
        ui.whats_fab(d, f, dev)
        return total
    total = max(H, y + 32)
    ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

# ---------- E15 link do colaborador ----------
SELLER = "Carla"

def _faixa_colaborador(d, f, dev, y):
    """Faixa logo abaixo do topo: quem está atendendo pelo link de venda (#pnz-vendedor-carla)."""
    W = DEVICES[dev][0]
    mob = dev == "mobile"
    x, cw = wrap(dev)
    h = 64 if not mob else 72
    b = d.frame(f, "Link do colaborador", 0, y, W, h, fill=ui.APPS["loja"]["soft"])
    hair(d, b, 0, h - 1, W)
    s = 40
    av = d.frame(b, f"Foto {SELLER}", x, (h - s) / 2, s, s, fill=C["green"], radius=s / 2, stroke="#ffffff", stroke_w=2)
    T(d, av, SELLER[0], s / 2, 9, size=15, weight=700, color="#ffffff", align="center", lh=22)
    tx = x + s + 12
    if mob:
        T(d, b, f"Atendimento: {SELLER}", tx, 14, size=14, weight=600, lh=20)
        T(d, b, f"Você está comprando pelo link da {SELLER}. A venda fica registrada para ela", tx, 34, size=12, color=C["text2"], lh=17, w=cw - s - 12)
        return h
    T(d, b, f"Você está comprando pelo link da {SELLER}", tx, 12, size=14, weight=600, lh=20)
    T(d, b, f"A venda fica registrada para ela · Smoke House {LOJA[0]} · {LOJA[1]}", tx, 33, size=12, color=C["text2"], lh=18)
    tag = f"Atendimento: {SELLER}"
    tw = fc.text_width(tag, 12, 600) + 40
    t = d.frame(b, "Selo de atendimento", x + cw - tw, (h - 32) / 2, tw, 32, fill=C["card"], radius=16, stroke=C["green"], stroke_opacity=0.4)
    ui.icon(d, t, "pessoa", 12, 8, 16, C["pos"])
    T(d, t, tag, 32, 6, size=12, weight=600, lh=20)
    return h

def e15(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    ui.altura(d, f, 2400)
    y = ui.loja_header(d, f, dev, cart_n=0)
    y += _faixa_colaborador(d, f, dev, y)
    hh = {"desktop": 420, "tablet": 380, "mobile": 404}[dev]
    hero = d.frame(f, "Herói", 0, y, W, hh, fill=C["black"], clip=True)
    img_h = hh if not mob else 200
    d.image(hero, os.path.join(ui.HERE, "marca", "banner-loja.png"), 0 if not mob else -180, 0, W if not mob else 660, img_h, name="Foto da loja", mode="fill")
    d.frame(hero, "Véu", 0, 0, W, img_h, fill=C["black"], fill_opacity=0.45)
    if not mob:
        T(d, hero, "TEM MUITO MAIS NA SMOKE HOUSE", W / 2, 60, size=12, weight=700, color=C["yellow"], align="center", lh=18, ls=12)
        bs = 64 if dev == "desktop" else 56
        ui.brush(d, hero, W / 2, 88, [("DO JEITO QUE VOCÊ", "white")], size=bs, align="center")
        ui.brush(d, hero, W / 2, 88 + bs * 1.15, [("IMAGINA.", "green")], size=bs, align="center")
        T(d, hero, f"Escolha seus produtos: a {SELLER} recebe o pedido e acompanha até a retirada ou a entrega",
          W / 2 - 260, 92 + bs * 2.3, size=15, color="#e7e7e2", align="center", lh=24, w=520)
        b, _ = ui.button(d, hero, W / 2 - 110, hh - 88, "Ver ofertas da semana", app=app, kind="primary", w=220, h=48)
    else:
        ui.brush(d, hero, 16, 196, [("DO JEITO QUE", "white")], size=36)
        ui.brush(d, hero, 16, 238, [("VOCÊ", "white"), ("IMAGINA.", "green")], size=36)
        T(d, hero, f"A {SELLER} recebe o seu pedido e acompanha até a entrega", 16, 288, size=13, color="#e7e7e2", lh=20, w=W - 32)
        b, _ = ui.button(d, hero, 16, hh - 56, "Ver ofertas da semana", app=app, kind="primary", w=W - 32, h=44)
    d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
    for c in d.nodes[b]["children"]:
        if d.nodes[c]["type"] == "text": d.nodes[c]["fills"] = [fc.paint(C["ink"])]
    y += hh + (48 if not mob else 32)
    y = prateleira(d, f, dev, y, [("MAIS", "ink"), ("VENDIDOS", "green")], MAIS_VENDIDOS) + 48
    if mob:
        total = y + 120
        ui.altura(d, f, total)
        ui.bottom_nav(d, f, "Início")
        ui.whats_fab(d, f, dev)
        return total
    total = max(H, y)
    ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

SCREENS = [
    ("E09", "Checkout · dados", e09),
    ("E10", "Checkout · entrega", e10),
    ("E11", "Checkout · pagamento", e11),
    ("E12", "Pedido enviado", e12),
    ("E13", "Página de trocas", e13),
    ("E14", "Guias", e14),
    ("E15", "Link do colaborador", e15),
]
