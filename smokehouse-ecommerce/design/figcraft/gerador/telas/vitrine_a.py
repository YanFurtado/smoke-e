"""Responsivo · Vitrine, parte A. E03 é a tela de referência do projeto (escrita pelo orquestrador)."""
import os
import fc, ui
from ui import C, T, DEVICES, PAD, brl, hair
from telas import _dados as D

PAGE = "Responsivo · Vitrine (início, catálogo e carrinho)"
APP = "loja"

def produtos(ids):
    return [p for i in ids for p in D.PRODUTOS if p[0] == i]

MAIS_VENDIDOS = [p for p in D.PRODUTOS if p[6]][:8] or D.PRODUTOS[:8]
OFERTAS = [p for p in D.PRODUTOS if p[5]][:8] or D.PRODUTOS[8:16]

def wrap(device):
    """Largura útil e margem: conteúdo até 1200 no computador, centralizado."""
    W = DEVICES[device][0]
    if device == "desktop": cw = 1200
    elif device == "tablet": cw = W - 64
    else: cw = W - 32
    return (W - cw) / 2, cw

def prateleira(d, f, device, y, titulo, prods, link="Ver mais"):
    x, cw = wrap(device)
    size = 40 if device != "mobile" else 30
    ui.brush(d, f, x, y, titulo, size=size)
    T(d, f, link, x + cw, y + size * 0.35, size=13, weight=600, align="right", lh=20)
    d.frame(f, "Sublinhado", x + cw - fc.text_width(link, 13, 600), y + size * 0.35 + 22, fc.text_width(link, 13, 600), 2, fill=C["yellow"])
    y += size + 24
    n = {"desktop": 4, "tablet": 4, "mobile": 2}[device]
    gap = 20 if device != "mobile" else 12
    w = (cw - gap * (n - 1)) / n
    hmax = 0
    for i, p in enumerate(prods[:n]):
        hmax = max(hmax, ui.card_produto(d, f, x + i * (w + gap), y, w, p, compact=device == "mobile"))
    return y + hmax

def e03(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    total = {"desktop": 2140, "tablet": 2100, "mobile": 2380}[dev]
    ui.altura(d, f, total)
    y = ui.loja_header(d, f, dev, cart_n=0)
    # herói: foto da loja com o título pincelado no espaço calmo
    hh = {"desktop": 440, "tablet": 400, "mobile": 420}[dev]
    hero = d.frame(f, "Herói", 0, y, W, hh, fill=C["black"], clip=True)
    img_h = hh if not mob else 220
    d.image(hero, os.path.join(ui.HERE, "marca", "banner-loja.png"), 0 if not mob else -180, 0, W if not mob else 660, img_h, name="Foto da loja", mode="fill")
    d.frame(hero, "Véu", 0, 0, W, img_h, fill=C["black"], fill_opacity=0.45)
    if not mob:
        T(d, hero, "TEM MUITO MAIS NA SMOKE HOUSE", W / 2, 64, size=12, weight=700, color=C["yellow"], align="center", lh=18, ls=12)
        ui.brush(d, hero, W / 2, 92, [("DO JEITO QUE VOCÊ", "white")], size=64 if dev == "desktop" else 56, align="center")
        ui.brush(d, hero, W / 2, 166, [("IMAGINA.", "green")], size=64 if dev == "desktop" else 56, align="center")
        T(d, hero, "Sedas, isqueiros, acessórios e a linha Tattoo Supply com preço de balcão, para retirar na loja ou receber em casa",
          W / 2 - 280, 252, size=15, color="#e7e7e2", align="center", lh=24, w=560)
        b, bw = ui.button(d, hero, W / 2 - 110, 320, "Ver ofertas da semana", app=app, kind="primary", w=220, h=48)
        d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
        for c in d.nodes[b]["children"]:
            if d.nodes[c]["type"] == "text": d.nodes[c]["fills"] = [fc.paint(C["ink"])]
    else:
        ui.brush(d, hero, 16, 236, [("DO JEITO QUE", "white")], size=40)
        ui.brush(d, hero, 16, 282, [("VOCÊ", "white"), ("IMAGINA.", "green")], size=40)
        T(d, hero, "Sedas, isqueiros e Tattoo Supply com preço de balcão", 16, 334, size=13, color="#e7e7e2", lh=20, w=W - 32)
        b, _ = ui.button(d, hero, 16, 364, "Ver ofertas da semana", app=app, kind="primary", w=W - 32, h=44)
        d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
        for c in d.nodes[b]["children"]:
            if d.nodes[c]["type"] == "text": d.nodes[c]["fills"] = [fc.paint(C["ink"])]
    y += hh
    # faixa de confiança: 4 itens numa linha (2×2 no celular, antes quebrava torto)
    itens = [("4,6 ★ no Google", "88 avaliações"), ("Aberto até 23h", "todos os dias"), ("Retire na loja", "sem frete"), ("Embalagem discreta", "em todo pedido")]
    th = 64 if not mob else 112
    tb = d.frame(f, "Confiança", 0, y, W, th, fill=C["card"])
    hair(d, tb, 0, th - 1, W)
    x, cw = wrap(dev)
    cols = 4 if not mob else 2
    iw = cw / cols
    for i, (a, b2) in enumerate(itens):
        cx = x + (i % cols) * iw; cy = 12 + (i // cols) * 48
        ui.icon(d, tb, "ok", cx, cy + 10, 18, C["pos"])
        T(d, tb, a, cx + 28, cy + 2, size=13, weight=600, lh=18)
        T(d, tb, b2, cx + 28, cy + 20, size=11, color=C["muted"], lh=16)
    y += th + (56 if not mob else 32)
    # categorias
    ui.brush(d, f, x, y, [("ENCONTRE O PRODUTO", "ink"), ("CERTO", "green")], size=40 if not mob else 28)
    y += (40 if not mob else 28) + 28
    n = len(D.CATEGORIAS)
    if mob:
        s = 92; gx = (cw - 3 * s) / 2
        for i, (lab, img) in enumerate(D.CATEGORIAS):
            ui.circulo_cat(d, f, x + (i % 3) * (s + gx), y + (i // 3) * (s + 40), s, lab, img)
        y += 2 * (s + 40) + 24
    else:
        s = 120 if dev == "desktop" else 112
        gx = (cw - n * s) / (n - 1)
        for i, (lab, img) in enumerate(D.CATEGORIAS):
            ui.circulo_cat(d, f, x + i * (s + gx), y, s, lab, img)
        y += s + 64
    y = prateleira(d, f, dev, y, [("MAIS", "ink"), ("VENDIDOS", "green")], MAIS_VENDIDOS) + 56
    y = prateleira(d, f, dev, y, [("OFERTAS DA", "ink"), ("SEMANA", "green")], OFERTAS, "Confira todas") + 56
    if mob:
        total = y + 64
        ui.altura(d, f, total)
        ui.bottom_nav(d, f, "Início")
        ui.whats_fab(d, f, dev)
    else:
        total = y + 24
        ui.altura(d, f, total)
        ui.whats_fab(d, f, dev)
    return total

# =====================================================================
# E01, E02, E04 a E08 (subagente de design, mesmo jeito da E03)
# =====================================================================
DISPLAY = ui.DISPLAY
DIM = "#b9bbb4"          # texto secundário sobre preto
DIM2 = "#8d8f87"

def _p(pid):
    return next(p for p in D.PRODUTOS if p[0] == pid)

def _img(d, p, nome, x, y, w, opacity=1.0):
    """Sticker da marca com a proporção real do PNG."""
    path = os.path.join(ui.HERE, "marca", nome + ".png")
    pw, ph = fc._img_size(open(path, "rb").read(32 * 1024))
    n = d.image(p, path, x, y, w, w * ph / pw, name=nome)
    if opacity != 1.0: d.nodes[n]["opacity"] = opacity
    return w * ph / pw

def _logo(d, p, x, y, w):
    return _img(d, p, "logo-branco", x, y, w)

def _veu(d, f, x, y, w, h, a=0.45):
    return d.frame(f, "Fundo escurecido", x, y, w, h, fill=C["overlay"], fill_opacity=a)

def _selo(d, p, x, y, txt):
    w = fc.text_width(txt, 11, 700) + 16
    b = d.frame(p, "Selo " + txt, x, y, w, 20, fill=C["yellow"], radius=10)
    T(d, b, txt, w / 2, 2, size=11, weight=700, align="center", lh=16)
    return w

def _mini(d, p, x, y, s, marca, radius=8):
    """Miniatura do produto (carrinho e sugestões): bloco na cor da marca com o nome em pincel."""
    c1, c2 = ui.marca_cor(marca)
    t = d.frame(p, f"Miniatura {marca}", x, y, s, s, fill=c2, radius=radius, clip=True)
    d.frame(t, "Sombra da marca", 0, s * 0.55, s, s * 0.45, fill=c1, fill_opacity=0.55)
    nome = {"TATTOO": "TATTOO", "GIFT": "KIT", "VINHO": "VINHO", "BEM BOLADO": "BEM BOLADO"}.get(marca, marca)
    fs = int(s * 0.3)
    while fc.text_width(nome, fs, family=DISPLAY) > s - 6 and fs > 8: fs -= 1
    d.text(t, nome, s / 2, (s - fs * 1.1) / 2, size=fs, family=DISPLAY, color="#ffffff", align="center", lh=int(fs * 1.1))
    return t

def _estrelas(d, p, x, y, nota, txt, size=13, color=None):
    """Cinco estrelas (a última apagada quando a nota não é cheia) e o texto da nota."""
    color = color or C["yellow"]
    cheias = 5 if nota >= 4.95 else 4
    for i in range(5):
        T(d, p, "★", x + i * (size + 1), y, size=size, color=color, lh=size + 6, opacity=1.0 if i < cheias else 0.35)
    tx = x + 5 * (size + 1) + 6
    T(d, p, txt, tx, y, size=size, weight=600, color=color, lh=size + 6)
    return tx + fc.text_width(txt, size, 600) - x

def _botao_linha_escuro(d, p, x, y, w, h, label):
    b = d.frame(p, f"Botão {label}", x, y, w, h, stroke="#ffffff", stroke_opacity=0.35, radius=ui.R_CTL)
    T(d, b, label, w / 2, (h - 20) / 2, size=15, weight=600, color="#ffffff", align="center", lh=20)
    return b

def _botao_amarelo(d, p, x, y, label, w, h=44):
    b, bw = ui.button(d, p, x, y, label, app="loja", kind="primary", w=w, h=h)
    d.nodes[b]["fills"] = [fc.paint(C["yellow"])]
    for c in d.nodes[b]["children"]:
        if d.nodes[c]["type"] == "text": d.nodes[c]["fills"] = [fc.paint(C["ink"])]
    return b

# ---------------------------------------------------------------- E01
def e01(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    d.frame(f, "Fundo", 0, 0, W, H, fill=C["black"])
    if dev == "desktop":
        for nome, x, y, w in (("fumaca", 90, 140, 120), ("narguile", -10, 330, 125), ("folha", 200, 560, 100), ("smiley", 135, 690, 95),
                              ("nuvem", 1190, 30, 200), ("asterisco", 1250, 210, 80), ("cinzeiro", 1110, 540, 125), ("charuto", 1300, 440, 140), ("bloco", 1150, 720, 145)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty = 260, 190, 56, 470
    elif dev == "tablet":
        for nome, x, y, w in (("fumaca", 60, 120, 110), ("narguile", -10, 320, 110), ("smiley", 110, 620, 90),
                              ("nuvem", 960, 30, 170), ("cinzeiro", 940, 500, 115), ("charuto", 1050, 330, 120)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty = 240, 150, 52, 410
    else:
        for nome, x, y, w in (("fumaca", 12, 40, 92), ("asterisco", 318, 60, 52), ("narguile", 4, 700, 72), ("cinzeiro", 290, 724, 84)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty = 200, 130, 40, 330
    lh = _logo(d, f, (W - lw) / 2, ly, lw)
    if not mob:
        ui.brush(d, f, W / 2, ty, [("VOCÊ TEM", "white"), ("18 ANOS", "green"), ("OU MAIS?", "white")], size=ts, align="center")
        y = ty + ts + 24
        T(d, f, "Este site vende produtos destinados exclusivamente a maiores de idade", W / 2, y, size=16, color="#d6d7d2", align="center", lh=24)
        y += 48
        bw, gap = 200, 12
        x0 = (W - (bw * 2 + gap)) / 2
        ui.button(d, f, x0, y, "Sim, tenho 18+", app=app, kind="primary", w=bw, h=52)
        _botao_linha_escuro(d, f, x0 + bw + gap, y, bw, 52, "Não")
        y += 52 + 28
        T(d, f, "A venda de produtos fumígenos e bebidas alcoólicas a menores é proibida por lei", W / 2, y, size=13, color=DIM2, align="center", lh=20)
    else:
        ui.brush(d, f, W / 2, ty, [("VOCÊ TEM", "white"), ("18 ANOS", "green")], size=ts, align="center")
        ui.brush(d, f, W / 2, ty + ts + 2, [("OU MAIS?", "white")], size=ts, align="center")
        y = ty + 2 * ts + 20
        T(d, f, "Este site vende produtos destinados exclusivamente a maiores de idade", 32, y, size=15, color="#d6d7d2", align="center", lh=22, w=W - 64)
        y += 44 + 28
        ui.button(d, f, 16, y, "Sim, tenho 18+", app=app, kind="primary", w=W - 32, h=52)
        y += 52 + 12
        _botao_linha_escuro(d, f, 16, y, W - 32, 52, "Não")
        y += 52 + 24
        T(d, f, "A venda de produtos fumígenos e bebidas alcoólicas a menores é proibida por lei", 32, y, size=12, color=DIM2, align="center", lh=18, w=W - 64)
    return H

# ---------------------------------------------------------------- E02
LOJAS_GATE = [
    ("lem", 5.0, "5,0 · 58 avaliações", "Tabacaria, vinhos e Tattoo Supply · retirada na loja", "Aberto até 00h"),
    ("pnz", 4.6, "4,6 · 88 avaliações", "13 anos no Centro · entrega em 20 a 60 min", "Aberto até 23h"),
]

def _cartao_loja(d, p, x, y, w, loja, destaque=False, mob=False):
    key, nota, aval, meta, hora = loja
    code, cidade, end = D.LOJAS[key]
    c = d.frame(p, f"Loja {code}", x, y, w, 10, fill="#1b1d1a", stroke=C["green"] if destaque else "#ffffff",
                stroke_opacity=1.0 if destaque else 0.12, radius=16, clip=True)
    cx = w / 2
    yy = 20 if mob else 24
    cs = 44 if mob else 52
    ui.brush(d, c, cx, yy, [(code, "green")], size=cs, align="center")
    yy += cs + 6
    T(d, c, cidade, cx, yy, size=17, weight=600, color="#ffffff", align="center", lh=24); yy += 30
    sw = 5 * 14 + 6 + fc.text_width(aval, 13, 600)
    _estrelas(d, c, cx - sw / 2, yy, nota, aval); yy += 28
    T(d, c, meta, 20, yy, size=13, color=DIM, align="center", lh=20, w=w - 40)
    nl = max(1, -(-int(fc.text_width(meta, 13)) // int(w - 40)))
    yy += 20 * nl + 6
    ew = fc.text_width(end, 12) + 22
    ui.icon(d, c, "pin", cx - ew / 2, yy + 1, 14, DIM2)
    T(d, c, end, cx - ew / 2 + 22, yy, size=12, color=DIM2, lh=18); yy += 26
    hair_y = yy + 2
    d.frame(c, "Linha", 0, hair_y, w, 1, fill="#ffffff", fill_opacity=0.10)
    lab = f"Comprar na {code}"
    T(d, c, hora, 20, hair_y + 15, size=12, color=DIM, lh=18)
    tw = fc.text_width(lab, 14, 600)
    T(d, c, lab, w - 44, hair_y + 14, size=14, weight=600, color="#ffffff" if not destaque else C["yellow"], align="right", lh=20)
    ui.icon(d, c, "seta-dir", w - 36, hair_y + 16, 16, "#ffffff" if not destaque else C["yellow"])
    h = hair_y + 48
    d.nodes[c]["height"] = float(h)
    return h

def e02(d, f, dev, app):
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    d.frame(f, "Fundo", 0, 0, W, H, fill=C["black"])
    if dev == "desktop":
        for nome, x, y, w in (("trevo", 190, 80, 110), ("cinzeiro", 90, 260, 130), ("bolsa", 150, 480, 120), ("narguile", -10, 590, 120),
                              ("asterisco", 1090, 80, 72), ("charuto", 1330, 160, 120), ("folha", 1190, 380, 100), ("zippo", 1250, 520, 130), ("pinca", 1190, 730, 140)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty, cw, cy = 170, 110, 52, 294, 400, 434
    elif dev == "tablet":
        for nome, x, y, w in (("trevo", 70, 70, 100), ("narguile", -10, 560, 110), ("charuto", 1050, 120, 110), ("zippo", 1020, 560, 120)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty, cw, cy = 160, 48, 50, 220, 380, 360
    else:
        for nome, x, y, w in (("trevo", 12, 24, 56), ("charuto", 318, 18, 64)):
            _img(d, f, nome, x, y, w)
        lw, ly, ts, ty, cw, cy = 130, 28, 34, 152, W - 32, 252
    _logo(d, f, (W - lw) / 2, ly, lw)
    ui.brush(d, f, W / 2, ty, [("ESCOLHA A SUA", "white"), ("LOJA", "green")], size=ts, align="center")
    sub = "O estoque, os preços e a entrega mudam conforme a cidade"
    if not mob:
        T(d, f, sub, W / 2, ty + ts + 16, size=16, color="#d6d7d2", align="center", lh=24)
        gap = 24
        x0 = (W - (2 * cw + gap)) / 2
        for i, lj in enumerate(LOJAS_GATE):
            _cartao_loja(d, f, x0 + i * (cw + gap), cy, cw, lj, destaque=i == 0)
        T(d, f, "Dá para trocar de loja depois, no topo do site", W / 2, cy + 290, size=13, color=DIM2, align="center", lh=20)
    else:
        T(d, f, sub, 32, ty + ts + 10, size=14, color="#d6d7d2", align="center", lh=20, w=W - 64)
        y = cy
        for i, lj in enumerate(LOJAS_GATE):
            y += _cartao_loja(d, f, 16, y, cw, lj, destaque=i == 0, mob=True) + 12
        T(d, f, "Dá para trocar de loja depois, no topo do site", W / 2, y + 4, size=12, color=DIM2, align="center", lh=18)
    return H

# ---------------------------------------------------------------- listagem e filtros (E04, E05)
TAM = {1: ("King Size", "Brown"), 2: ("King Size", "Rosa"), 3: ("King Size", "Branca"), 4: ("King Size", "Brown"),
       5: ("King Size", "Brown"), 6: ("King Size", "Hemp"), 7: ("KS Slim", "Branca"), 8: ("KS Slim", "Branca"),
       9: ("King Size", "Branca"), 10: ("King Size", "Alfafa"), 11: ("KS Slim", "Brown"), 12: ("KS Slim", "Hemp"),
       13: ("King Size", "Hemp")}  # sz e pp de src/app.js
PRICES = [("Até R$ 10", 0, 10), ("R$ 10 a R$ 30", 10, 30), ("R$ 30 a R$ 100", 30, 100), ("Acima de R$ 100", 100, 1e9)]
OUT_PNZ = {41, 70, 71}
SEDAS = [p for p in D.PRODUTOS if p[1] == "Sedas"]

def _filtro(**kw):
    f = dict(brands=set(), sz=set(), pp=set(), price=None, avail=False, promo=False)
    f.update(kw)
    return f

FILTRO_E05 = _filtro(avail=True, brands={"OCB", "RAW"}, price=1)

def _passa(p, f, skip=None):
    sz, pp = TAM.get(p[0], (None, None))
    if skip != "brands" and f["brands"] and p[2] not in f["brands"]: return False
    if skip != "sz" and f["sz"] and sz not in f["sz"]: return False
    if skip != "pp" and f["pp"] and pp not in f["pp"]: return False
    if skip != "price" and f["price"] is not None:
        _, a, b = PRICES[f["price"]]
        if not (a <= p[4] < b): return False
    if skip != "avail" and f["avail"] and p[0] in OUT_PNZ: return False
    if skip != "promo" and f["promo"] and not p[6]: return False
    return True

def _n_filtros(f):
    return len(f["brands"]) + len(f["sz"]) + len(f["pp"]) + (f["price"] is not None) + f["avail"] + f["promo"]

def _facetas(base, f):
    """Mesma conta do renderFilters do app.js: cada grupo conta ignorando o próprio filtro."""
    def fac(key, get, label=lambda v: v):
        allv = {}
        for p in base:
            v = get(p)
            if v: allv.setdefault(v, 0)
        for p in base:
            if _passa(p, f, key):
                v = get(p)
                if v: allv[v] += 1
        return sorted(((label(v), v, n, v in f[key]) for v, n in allv.items()), key=lambda t: t[0])
    grupos = [("Marca", "brands", fac("brands", lambda p: p[2], lambda v: D.NOME_MARCA.get(v, v)))]
    pr = [(lab, i, sum(1 for p in base if _passa(p, f, "price") and a <= p[4] < b), f["price"] == i) for i, (lab, a, b) in enumerate(PRICES)]
    grupos.append(("Preço", "price", pr))
    grupos.append(("Tamanho", "sz", fac("sz", lambda p: TAM.get(p[0], (None, None))[0])))
    grupos.append(("Tipo de papel", "pp", fac("pp", lambda p: TAM.get(p[0], (None, None))[1])))
    n_av = sum(1 for p in base if _passa(p, f, "avail") and p[0] not in OUT_PNZ)
    n_pr = sum(1 for p in base if _passa(p, f, "promo") and p[6])
    return grupos, n_av, n_pr

def _chips_do_filtro(f):
    out = []
    if f["avail"]: out.append("Disponível na PNZ")
    if f["promo"]: out.append("Em promoção")
    out += sorted(D.NOME_MARCA.get(b, b) for b in f["brands"])
    if f["price"] is not None: out.append(PRICES[f["price"]][0])
    out += sorted(f["sz"]) + ["Papel " + v for v in sorted(f["pp"])]
    return out

def _filtros_lista(d, p, x, y, w, f, base, app):
    """Computador: filtros na lateral, em lista com marcação e contagem."""
    c = d.frame(p, "Filtros", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=ui.R_CARD)
    grupos, n_av, n_pr = _facetas(base, f)
    ui.brush(d, c, 20, 20, [("FILTROS", "ink")], size=26)
    if _n_filtros(f):
        T(d, c, "Limpar tudo", w - 20, 24, size=13, weight=600, color=ui.acc(app), align="right", lh=20)
    yy = 68
    for lab, n, on in ((f"Disponível na loja PNZ", n_av, f["avail"]), ("Em promoção", n_pr, f["promo"])):
        T(d, c, lab, 20, yy, size=13, lh=20)
        T(d, c, f"({n})", 20 + fc.text_width(lab, 13) + 4, yy, size=12, color=C["muted"], lh=20)
        ui.toggle(d, c, w - 20 - 36, yy, on=on, app=app)
        yy += 36
    for titulo, key, ops in grupos:
        hair(d, c, 20, yy + 4, w - 40); yy += 20
        T(d, c, titulo, 20, yy, size=14, weight=600, lh=20); yy += 30
        for lab, v, n, on in ops:
            dis = n == 0 and not on
            if key == "price": ui.radio(d, c, 20, yy + 1, on=on, app=app)
            else: ui.checkbox(d, c, 20, yy + 1, on=on, app=app)
            T(d, c, lab, 48, yy, size=13, weight=500 if on else 400, color=C["muted"] if dis else C["ink"], lh=20, opacity=0.6 if dis else 1.0)
            T(d, c, str(n), w - 20, yy, size=12, color=C["muted"], align="right", lh=20)
            yy += 30
        yy += 2
    d.nodes[c]["height"] = float(yy + 12)
    return yy + 12

def _opcao(d, p, x, y, label, n, on, dis, app, h=40):
    """Opção de filtro para toque (tablet e celular): pílula de 40 com a contagem."""
    lw = fc.text_width(label, 13, 600 if on else 500)
    nw = fc.text_width(str(n), 12, 500)
    iw = 20 if on else 0
    w = int(16 + iw + lw + 8 + nw + 16)
    b = d.frame(p, f"Opção {label}", x, y, w, h, fill=C["ink"] if on else C["card"], stroke=None if on else C["line"],
                stroke_opacity=0.16, radius=h / 2, opacity=0.4 if dis else 1.0)
    cx = 16
    if on:
        ui.icon(d, b, "ok", cx - 2, (h - 16) / 2, 16, C["yellow"]); cx += iw
    T(d, b, label, cx, (h - 20) / 2, size=13, weight=600 if on else 500, color="#ffffff" if on else C["ink"], lh=20)
    T(d, b, str(n), cx + lw + 8, (h - 20) / 2, size=12, weight=500, color=DIM if on else C["muted"], lh=20)
    return w

def _filtros_toque(d, p, x, y, w, f, base, app, sep=20, tit=30):
    """Tablet e celular: grupos com opções em pílula (alvo de 40), dentro da gaveta."""
    grupos, n_av, n_pr = _facetas(base, f)
    yy = y
    for lab, n, on in (("Disponível na loja PNZ", n_av, f["avail"]), ("Em promoção", n_pr, f["promo"])):
        T(d, p, lab, x, yy + 12, size=14, lh=20)
        T(d, p, f"({n})", x + fc.text_width(lab, 14) + 4, yy + 12, size=13, color=C["muted"], lh=20)
        ui.toggle(d, p, x + w - 36, yy + 12, on=on, app=app)
        yy += 44
    for titulo, key, ops in grupos:
        hair(d, p, x, yy + 6, w); yy += sep
        T(d, p, titulo, x, yy, size=14, weight=600, lh=20); yy += tit
        cx, cy = x, yy
        for lab, v, n, on in ops:
            lw = 16 + (20 if on else 0) + fc.text_width(lab, 13, 600 if on else 500) + 8 + fc.text_width(str(n), 12, 500) + 16
            if cx + lw > x + w:
                cx, cy = x, cy + 48
            cx += _opcao(d, p, cx, cy, lab, n, on, n == 0 and not on, app) + 8
        yy = cy + 40 + 6
    return yy - y

def _cabecalho_lista(d, f, dev, y, titulo, n, fl, app):
    x, cw = wrap(dev)
    mob = dev == "mobile"
    y += 20 if mob else 24
    T(d, f, "Início", x, y, size=12, color=C["text2"], lh=18)
    hair(d, f, x, y + 17, fc.text_width("Início", 12))
    T(d, f, "/  " + titulo, x + fc.text_width("Início", 12) + 6, y, size=12, color=C["muted"], lh=18)
    y += 26
    ts = 44 if not mob else 36
    ui.brush(d, f, x, y, [(titulo.upper(), "ink")], size=ts)
    y += ts + 6
    T(d, f, f"{n} produto{'s' if n != 1 else ''} na loja PNZ", x, y, size=13, color=C["muted"], lh=20)
    nf = _n_filtros(fl)
    if dev == "desktop":
        ui.field(d, f, x + cw - 220, y - 36, 220, value="Mais relevantes", chevron=True, h=44, app=app)
        return y + 20 + 24
    y += 20 + 16
    bw = 132 if not mob else (cw - 8) / 2
    b, _ = ui.button(d, f, x, y, "Filtrar", app=app, kind="secondary", w=bw, h=44, icon_name="filtro")
    if nf:
        bd = d.frame(b, "Contador", bw - 30, 12, 20, 20, fill=ui.acc(app), radius=10)
        T(d, bd, str(nf), 10, 2, size=11, weight=700, color="#ffffff", align="center", lh=16)
    sw = 220 if not mob else (cw - 8) / 2
    ui.field(d, f, x + cw - sw, y, sw, value="Mais relevantes", chevron=True, h=44, app=app)
    return y + 44 + 20

def _chips_ativos(d, f, x, y, w, itens, app):
    if not itens: return 0
    cx, cy = x, y
    for lab in itens:
        cw = fc.text_width(lab, 13, 500) + 16 + 8 + 14 + 12
        if cx + cw > x + w: cx, cy = x, cy + 44
        c = d.frame(f, f"Filtro ativo {lab}", cx, cy, cw, 36, fill=C["card"], stroke=C["ink"], stroke_opacity=0.22, radius=18)
        T(d, c, lab, 16, 8, size=13, weight=500, lh=20)
        ui.icon(d, c, "fechar", cw - 12 - 14, 11, 14, C["text2"])
        cx += cw + 8
    if len(itens) > 1:
        lab = "Limpar filtros"
        lw = fc.text_width(lab, 13, 600)
        if cx + lw + 8 > x + w: cx, cy = x, cy + 44
        T(d, f, lab, cx + 8, cy + 8, size=13, weight=600, color=ui.acc(app), lh=20)
        d.frame(f, "Sublinhado", cx + 8, cy + 28, lw, 2, fill=C["yellow"])
    return cy - y + 36

def _grade(d, f, x, y, w, n, prods, mob=False):
    gap = 20 if not mob else 12
    cwid = (w - gap * (n - 1)) / n
    for r in range(0, len(prods), n):
        hmax, cards = 0, []
        for i, p in enumerate(prods[r:r + n]):
            cx = x + i * (cwid + gap)
            k = len(d.nodes[f]["children"])
            h = ui.card_produto(d, f, cx, y, cwid, p, compact=mob)
            cards.append((d.nodes[f]["children"][k], h))
            hmax = max(hmax, h)
            if p[1] == "Sedas" and p[6]:
                pad = 10 if mob else 12
                _selo(d, f, cx + pad + 8, y + pad + 8, "3 por 2")
        ih = int(cwid * (0.9 if not mob else 0.86))
        for cid, h in cards:
            if h < hmax:
                d.nodes[cid]["height"] = float(hmax)
                for ch in d.nodes[cid]["children"]:
                    t = d.nodes[ch]["transform"]
                    if t[5] > ih + 12: t[5] += hmax - h
        y += hmax + gap
    return y - gap

def _listagem(d, f, dev, app, fl, fundo=False):
    """Categoria Sedas. fundo=True: só a parte de cima (base da gaveta de filtros), sem barra de baixo."""
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    ui.altura(d, f, H)
    y = ui.loja_header(d, f, dev, cart_n=0)
    prods = [p for p in SEDAS if _passa(p, fl)]
    y = _cabecalho_lista(d, f, dev, y, "Sedas", len(prods), fl, app)
    x, cw = wrap(dev)
    if dev == "desktop":
        sw = 264
        sh = _filtros_lista(d, f, x, y, sw, fl, SEDAS, app)
        gx, gw = x + sw + 32, cw - sw - 32
        top = y
        ah = _chips_ativos(d, f, gx, y, gw, _chips_do_filtro(fl), app)
        if ah: y += ah + 20
        yb = _grade(d, f, gx, y, gw, 4, prods)
        total = max(yb, top + sh) + 64
    else:
        ah = _chips_ativos(d, f, x, y, cw, _chips_do_filtro(fl), app)
        if ah: y += ah + 20
        yb = _grade(d, f, x, y, cw, 4 if dev == "tablet" else 2, prods, mob=mob)
        total = yb + (32 if not mob else 24)
    if fundo:
        return H
    if mob:
        total += 64
        ui.altura(d, f, total)
        ui.bottom_nav(d, f, "Categorias")
    else:
        ui.altura(d, f, total)
    ui.whats_fab(d, f, dev)
    return total

def e04(d, f, dev, app):
    return _listagem(d, f, dev, app, _filtro())

def e05(d, f, dev, app):
    fl = FILTRO_E05
    if dev == "desktop":
        return _listagem(d, f, dev, app, fl)
    W, H = DEVICES[dev]
    mob = dev == "mobile"
    _listagem(d, f, dev, app, fl, fundo=True)
    _veu(d, f, 0, 0, W, H, 0.5)
    n = sum(1 for p in SEDAS if _passa(p, fl))
    if mob:
        gw, gh = W, H
        g = d.frame(f, "Gaveta de filtros", 0, 0, gw, gh, fill=C["card"], clip=True)
        pad, top = 16, 0
    else:
        gw, gh = 440, H
        g = d.frame(f, "Gaveta de filtros", W - gw, 0, gw, gh, fill=C["card"], clip=True, shadow=ui.shadow(0.16, 0, 32))
        pad, top = 24, 12
    ui.brush(d, g, pad, top + 12, [("FILTROS", "ink")], size=28)
    T(d, g, "Limpar tudo", gw - pad - 52, top + 18, size=13, weight=600, color=ui.acc(app), align="right", lh=20)
    cb = d.frame(g, "Fechar", gw - pad - 40, top + 8, 40, 40, fill=C["raised"], radius=20)
    ui.icon(d, cb, "fechar", 12, 12, 16, C["ink"])
    hair(d, g, 0, top + 60, gw)
    fh = 80
    area = d.frame(g, "Opções", 0, top + 61, gw, gh - fh - top - 61, clip=True)
    _filtros_toque(d, area, pad, 2, gw - 2 * pad, fl, SEDAS, app, sep=14 if mob else 20, tit=28 if mob else 30)
    fb = d.frame(g, "Barra da gaveta", 0, gh - fh, gw, fh, fill=C["card"])
    hair(d, fb, 0, 0, gw)
    ui.button(d, fb, pad, 16, f"Ver {n} produtos", app=app, kind="primary", w=gw - 2 * pad, h=48)
    return H

# ---------------------------------------------------------------- E06 busca com sugestões
def _resultados(q):
    """Ordem do search() do app.js para "seda": todos com a palavra valem 4, destaque +0,3."""
    hits = [p for p in D.PRODUTOS if p[1] in ("Sedas", "Atacado") or p[0] == 31]
    return sorted(hits, key=lambda p: -(4 + (0.3 if p[7] else 0)))

def _marca_texto(d, p, nome, q, x, y, size, weight, maxw):
    """Desenha o nome com o trecho buscado marcado em amarelo (como o <mark> do app)."""
    i = nome.lower().find(q.lower())
    if i >= 0:
        a = fc.text_width(nome[:i], size, weight); b = fc.text_width(nome[i:i + len(q)], size, weight)
        if a + b < maxw:
            d.frame(p, "Marca da busca", x + a - 1, y + 1, b + 2, size + 6, fill=C["yellow"], fill_opacity=0.55, radius=3)
    T(d, p, nome, x, y, size=size, weight=weight, lh=size + 6, w=maxw)

def _linha_sugestao(d, p, x, y, w, prod, q, sel=False, s=40):
    pid, cat, marca, nome, preco = prod[:5]
    pr = ui.brl(preco)
    prw = fc.text_width(pr, 14, 600)
    tx = x + 12 + s + 12
    tw = w - (tx - x) - prw - 24
    nl = max(1, -(-int(fc.text_width(nome, 14, 500)) // int(tw)))
    h = max(s + 16, 12 + 20 * nl + 18 + 12)
    if sel: d.frame(p, "Sugestão em foco", x + 4, y + 2, w - 8, h - 4, fill=C["sel"], radius=8)
    _mini(d, p, x + 12, y + (h - s) / 2, s, marca)
    _marca_texto(d, p, nome, q, tx, y + 10, 14, 500, tw)
    T(d, p, f"{cat} · {D.NOME_MARCA.get(marca, marca)}", tx, y + 12 + 20 * nl, size=12, color=C["muted"], lh=16)
    T(d, p, pr, x + w - 12, y + 10, size=14, weight=600, align="right", lh=20)
    return h

def _painel_sugestoes(d, p, x, y, w, q, res, app, n_linhas=6):
    c = d.frame(p, "Sugestões da busca", x, y, w, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.10, radius=ui.R_CARD,
                shadow=ui.shadow(0.18, 12, 32), clip=True)
    yy = 16
    T(d, c, "Categorias", 16, yy, size=12, weight=600, color=C["muted"], lh=16); yy += 24
    ui.chips(d, c, 16, yy, [("Sedas", 13), ("Atacado", 4)], active=None, app=app); yy += 32 + 16
    hair(d, c, 0, yy, w); yy += 14
    T(d, c, "Produtos", 16, yy, size=12, weight=600, color=C["muted"], lh=16); yy += 22
    for i, prod in enumerate(res[:n_linhas]):
        yy += _linha_sugestao(d, c, 4, yy, w - 8, prod, q, sel=i == 0)
    yy += 4
    hair(d, c, 0, yy, w)
    lab = f"Ver todos os {len(res)} resultados para “{q}”"
    T(d, c, lab, 16, yy + 14, size=14, weight=600, color=ui.acc(app), lh=20)
    ui.icon(d, c, "seta-dir", 16 + fc.text_width(lab, 14, 600) + 8, yy + 16, 16, ui.acc(app))
    yy += 48
    d.nodes[c]["height"] = float(yy)
    return yy

def _campo_busca(d, p, x, y, w, q, h=40, app="loja"):
    ui.field(d, p, x, y, w, value=q, focused=True, prefix_icon="busca", h=h, app=app)
    ui.icon(d, p, "fechar", x + w - 30, y + (h - 14) / 2, 14, C["text2"])

def _base_inicio(d, f, dev, app, cart_n=0, cart_total=None):
    """Início da loja (E03) cortado na altura da janela, como fundo de painel aberto por cima."""
    W, H = DEVICES[dev]
    e03(d, f, dev, app)
    ui.altura(d, f, H)
    if cart_n: ui.loja_header(d, f, dev, cart_n=cart_n, cart_total=cart_total)

def _pos_busca(dev):
    pad = 32 if dev == "desktop" else ui.PAD[dev]
    sx = pad + 64 + 170
    return sx, 32 + 12, 420 if dev == "desktop" else 330

def e06(d, f, dev, app):
    W, H = DEVICES[dev]
    q = "seda"
    res = _resultados(q)
    if dev != "mobile":
        _base_inicio(d, f, dev, app)
        _veu(d, f, 0, 140, W, H - 140, 0.4)
        sx, sy, sw = _pos_busca(dev)
        _campo_busca(d, f, sx, sy, sw, q)
        pw = 560 if dev == "desktop" else 500
        _painel_sugestoes(d, f, sx, sy + 48, pw, q, res, app)
        return H
    # celular: a busca abre em tela cheia, sem o cabeçalho e a barra de categorias por baixo
    bar = d.frame(f, "Topo da busca", 0, 0, W, 72, fill=C["black"])
    ui.icon(d, bar, "seta-esq", 16, 28, 18, "#ffffff")
    _campo_busca(d, bar, 48, 14, W - 64, q, h=44)
    x, cw = wrap(dev)
    y = 72 + 20
    T(d, f, "Categorias", x, y, size=12, weight=600, color=C["muted"], lh=16); y += 24
    ui.chips(d, f, x, y, [("Sedas", 13), ("Atacado", 4)], active=None, app=app); y += 32 + 20
    T(d, f, "Produtos", x, y, size=12, weight=600, color=C["muted"], lh=16); y += 24
    lst = d.frame(f, "Lista de sugestões", x, y, cw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=ui.R_CARD)
    yy = 4
    for i, prod in enumerate(res[:5]):
        if i: hair(d, lst, 16, yy, cw - 32)
        yy += _linha_sugestao(d, lst, 0, yy, cw, prod, q, s=44)
    d.nodes[lst]["height"] = float(yy + 4)
    y += yy + 4 + 16
    ui.button(d, f, x, y, f"Ver os {len(res)} resultados", app=app, kind="primary", w=cw, h=48)
    ui.bottom_nav(d, f, "Buscar")
    return H

# ---------------------------------------------------------------- E07 menu de categorias
CONTAGEM = {c: sum(1 for p in D.PRODUTOS if p[1] == c) for c in D.MENU}
IMG_CAT = dict((a, b) for a, b in D.CATEGORIAS)
IMG_CAT.update({"Piteiras": "charuto", "Vinhos": "smiley"})  # sem sticker próprio no Drive
CATS = [c for c in D.MENU if c != "Ofertas"]

def _circ(d, p, x, y, s, img):
    o = d.frame(p, "Ícone da categoria", x, y, s, s, fill=C["black"], radius=s / 2, clip=True)
    d.image(o, os.path.join(ui.HERE, "marca", img + ".png"), s * 0.14, s * 0.14, s * 0.72, s * 0.72, name=img, mode="fit")

def _cartao_ofertas(d, p, x, y, w, h, app, compacto=False):
    c = d.frame(p, "Ofertas da semana", x, y, w, h, fill=C["black"], radius=ui.R_CARD, clip=True)
    if compacto:
        _img(d, c, "cinzeiro", w - 92, h - 84, 96, opacity=0.9)
        ui.brush(d, c, 16, 16, [("OFERTAS DA", "white"), ("SEMANA", "yellow")], size=26)
        T(d, c, "Até 24% off em piteiras, isqueiros, Tattoo Supply e presentes", 16, 50, size=13, color="#e7e7e2", lh=20, w=w - 120)
        _botao_amarelo(d, c, 16, h - 56, "Ver ofertas", 132, 40)
        return
    _img(d, c, "cinzeiro", w - 96, h - 104, 110, opacity=0.9)
    ui.brush(d, c, 20, 20, [("OFERTAS DA", "white")], size=30)
    ui.brush(d, c, 20, 52, [("SEMANA", "yellow")], size=30)
    T(d, c, "Até 24% off em piteiras, isqueiros, Tattoo Supply e presentes", 20, 96, size=13, color="#e7e7e2", lh=20, w=w - 40)
    _botao_amarelo(d, c, 20, h - 64, "Ver ofertas", 140, 44)

def e07(d, f, dev, app):
    W, H = DEVICES[dev]
    if dev != "mobile":
        _base_inicio(d, f, dev, app)
        pad = 32 if dev == "desktop" else ui.PAD[dev]
        # botão "Todas categorias" aberto
        allb = d.frame(f, "Todas categorias aberto", pad, 96, 168, 44, fill=ui.acc(app))
        ui.icon(d, allb, "fechar", 14, 14, 16, "#ffffff")
        T(d, allb, "Todas categorias", 38, 12, size=13, weight=600, color="#ffffff", lh=20)
        d.frame(allb, "Aberto", 0, 41, 168, 3, fill=C["yellow"])
        _veu(d, f, 0, 140, W, H - 140, 0.4)
        x, cw = wrap(dev)
        ph = 300 if dev == "desktop" else 312
        m = d.frame(f, "Menu de categorias", 0, 140, W, ph, fill=C["card"])
        hair(d, m, 0, ph - 1, W)
        ow = 300 if dev == "desktop" else 280
        gw = cw - ow - 32
        T(d, m, "Todas as categorias", x, 24, size=12, weight=600, color=C["muted"], lh=16)
        cols = 4
        tw = gw / cols
        rh = 76
        for i, cat in enumerate(CATS):
            tx, ty = x + (i % cols) * tw, 52 + (i // cols) * (rh + 8)
            if i == 0: d.frame(m, "Categoria em foco", tx - 8, ty, tw - 8, rh, fill=C["raised"], radius=ui.R_CARD)
            _circ(d, m, tx + 4, ty + 12, 52, IMG_CAT[cat])
            T(d, m, cat, tx + 68, ty + 16, size=15, weight=600, lh=22)
            T(d, m, f"{CONTAGEM[cat]} produtos", tx + 68, ty + 40, size=12, color=C["muted"], lh=16)
        ly = 52 + 2 * (rh + 8) + 8
        T(d, m, "Mais vendidos", x, ly, size=14, weight=600, lh=20)
        ui.icon(d, m, "seta-dir", x + fc.text_width("Mais vendidos", 14, 600) + 6, ly + 2, 16, C["ink"])
        d.frame(m, "Sublinhado", x, ly + 22, fc.text_width("Mais vendidos", 14, 600), 2, fill=C["yellow"])
        _cartao_ofertas(d, m, x + cw - ow, 24, ow, ph - 48, app)
        return H
    # celular: aba Categorias da barra de baixo
    x, cw = wrap(dev)
    rh = 68
    oh = 164
    total = 136 + 20 + 40 + 12 + oh + 12 + len(CATS) * rh + 8 + 12 + 60 + 88 + 64
    ui.altura(d, f, total)
    y = ui.loja_header(d, f, dev)
    y += 20
    ui.brush(d, f, x, y, [("CATEGORIAS", "ink")], size=36); y += 40 + 12
    _cartao_ofertas(d, f, x, y, cw, oh, app, compacto=True)
    y += oh + 12
    lst = d.frame(f, "Lista de categorias", x, y, cw, len(CATS) * rh + 8, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=ui.R_CARD)
    for i, cat in enumerate(CATS):
        ry = 4 + i * rh
        if i: hair(d, lst, 76, ry, cw - 92)
        _circ(d, lst, 12, ry + 10, 48, IMG_CAT[cat])
        T(d, lst, cat, 76, ry + 14, size=15, weight=600, lh=22)
        T(d, lst, f"{CONTAGEM[cat]} produtos", 76, ry + 36, size=12, color=C["muted"], lh=16)
        ui.icon(d, lst, "seta-dir", cw - 32, ry + 26, 16, C["muted"])
    y += len(CATS) * rh + 8 + 12
    mv = d.frame(f, "Mais vendidos", x, y, cw, 60, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=ui.R_CARD)
    T(d, mv, "Mais vendidos", 16, 12, size=15, weight=600, lh=22)
    T(d, mv, "Os preferidos das duas lojas", 16, 34, size=12, color=C["muted"], lh=16)
    ui.icon(d, mv, "seta-dir", cw - 32, 22, 16, C["muted"])
    ui.bottom_nav(d, f, "Categorias")
    ui.whats_fab(d, f, dev)
    return total

# ---------------------------------------------------------------- E08 carrinho
CARRINHO = [(1, 2), (4, 1), (10, 1)]          # (id, quantidade)
ESTOQUE_PNZ = {pid: ((pid * 7) % 17) + 2 for pid, _ in CARRINHO}   # getStock do app.js

def _totais():
    l = [(_p(pid), q) for pid, q in CARRINHO]
    sub = sum(p[4] * q for p, q in l)
    sedas = sorted(x for p, q in l if p[1] == "Sedas" and p[6] for x in [p[4]] * q)
    disc = sum(sedas[i] for i in range(len(sedas) // 3))
    faltam = 3 - len(sedas) % 3
    return l, sub, disc, sub - disc, (sub - disc) * 0.95, sum(q for _, q in l), faltam

def _qtd(d, p, x, y, q, w=112, h=40, no_max=False):
    b = d.frame(p, "Quantidade", x, y, w, h, fill=C["card"], stroke=C["line"], stroke_opacity=0.18, radius=h / 2)
    ui.icon(d, b, "menos", 12, (h - 16) / 2, 16, C["ink"])
    T(d, b, str(q), w / 2, (h - 20) / 2, size=15, weight=600, align="center", lh=20)
    ui.icon(d, b, "mais", w - 28, (h - 16) / 2, 16, C["muted"] if no_max else C["ink"])

def _linha_carrinho(d, p, x, y, w, prod, q, mob=False):
    pid, cat, marca, nome, preco, antigo, hot, hl = prod
    s = 56
    qw = 104 if mob else 112
    tx = x + s + 12
    tw = w - (s + 12) - qw - 12
    _mini(d, p, x, y, s, marca)
    T(d, p, nome, tx, y - 2, size=14, weight=600, lh=20, w=tw)
    nl = max(1, -(-int(fc.text_width(nome, 14, 600)) // int(tw)))
    yy = y - 2 + 20 * nl + 2
    T(d, p, f"{ui.brl(preco)} un.", tx, yy, size=12, color=C["muted"], lh=18)
    if cat == "Sedas" and hot:
        _selo(d, p, tx + fc.text_width(f"{ui.brl(preco)} un.", 12) + 8, yy - 1, "3 por 2")
    yy += 20
    est = ESTOQUE_PNZ[pid]
    if est < 5:
        T(d, p, f"Últimas {est} unidades na loja PNZ", tx, yy, size=12, weight=500, color=C["warn"], lh=18); yy += 20
    _qtd(d, p, x + w - qw, y + 2, q, w=qw)
    T(d, p, ui.brl(preco * q), x + w, y + 50, size=13, weight=600, align="right", lh=18)
    return max(yy - y, 72)

def _aviso_promo(d, p, x, y, w, faltam, app):
    txt = f"Promoção 3 por 2 aplicada. Leve mais {faltam} sedas com a etiqueta e ganhe outra"
    nl = max(1, -(-int(fc.text_width(txt, 13, 500)) // int(w - 52)))
    h = 24 + 20 * nl
    b = d.frame(p, "Aviso da promoção", x, y, w, h, fill=ui.APPS[app]["soft"], radius=ui.R_CTL)
    ui.icon(d, b, "ok", 14, 12 + (20 * nl - 16) / 2, 16, C["pos"])
    T(d, b, txt, 40, 12, size=13, weight=500, color=C["pos"], lh=20, w=w - 52)
    return h

def _resumo(d, p, x, y, w, total_grande=True):
    l, sub, disc, tot, pix, n, faltam = _totais()
    rows = [("Subtotal", ui.brl(sub), C["ink"]), ("Promoção 3 por 2", "-" + ui.brl(disc), C["pos"]), ("Entrega", "calculada no próximo passo", C["ink"])]
    yy = y
    for k, v, col in rows:
        T(d, p, k, x, yy, size=13, color=col if col == C["pos"] else C["text2"], weight=600 if col == C["pos"] else 400, lh=20)
        T(d, p, v, x + w, yy, size=13, color=col, weight=600 if col == C["pos"] else 400, align="right", lh=20)
        yy += 26
    yy += 6
    T(d, p, "Total", x, yy, size=20, weight=700, lh=28)
    T(d, p, ui.brl(tot), x + w, yy, size=20, weight=700, align="right", lh=28)
    yy += 34
    T(d, p, f"{ui.brl(pix)} pagando no Pix", x, yy, size=13, weight=600, color=C["pos"], lh=20); yy += 22
    T(d, p, "Pix, crédito, débito, carteira digital, boleto e dinheiro", x, yy, size=12, color=C["muted"], lh=18, w=w)
    yy += 18 * max(1, -(-int(fc.text_width("Pix, crédito, débito, carteira digital, boleto e dinheiro", 12)) // int(w)))
    return yy - y

def _topo_carrinho(d, p, w, n, pad):
    top = d.frame(p, "Topo do carrinho", 0, 0, w, 72, fill=C["black"])
    bw = ui.brush(d, top, pad, 20, [("SEU CARRINHO", "white")], size=30)
    T(d, top, f"{n} itens", pad + bw + 12, 28, size=13, color=DIM, lh=20)
    cb = d.frame(top, "Fechar", w - pad - 40, 16, 40, 40, fill="#ffffff", fill_opacity=0.12, radius=20)
    ui.icon(d, cb, "fechar", 12, 12, 16, "#ffffff")

def e08(d, f, dev, app):
    W, H = DEVICES[dev]
    l, sub, disc, tot, pix, n, faltam = _totais()
    if dev != "mobile":
        _base_inicio(d, f, dev, app, cart_n=n, cart_total=tot)
        _veu(d, f, 0, 0, W, H, 0.55)
        gw = 440
        g = d.frame(f, "Gaveta do carrinho", W - gw, 0, gw, H, fill=C["card"], clip=True, shadow=ui.shadow(0.2, 0, 32))
        pad = 24
        _topo_carrinho(d, g, gw, n, pad)
        y = 72 + 20
        for i, (p, q) in enumerate(l):
            if i: hair(d, g, pad, y - 10, gw - 2 * pad)
            y += _linha_carrinho(d, g, pad, y, gw - 2 * pad, p, q) + 20
        _aviso_promo(d, g, pad, y, gw - 2 * pad, faltam, app)
        fh = 20 + 26 * 3 + 6 + 34 + 22 + 18 + 16 + 48 + 8 + 44 + 20
        fy = H - fh
        hair(d, g, 0, fy, gw)
        yy = fy + 20 + _resumo(d, g, pad, fy + 20, gw - 2 * pad) + 16
        ui.button(d, g, pad, yy, "Finalizar pedido", app=app, kind="primary", w=gw - 2 * pad, h=48)
        ui.button(d, g, pad, yy + 56, "Continuar comprando", app=app, kind="secondary", w=gw - 2 * pad, h=44)
        return H
    # celular: página própria, ação principal fixa embaixo
    x, cw = wrap(dev)
    _topo_carrinho(d, f, W, n, 16)
    y = 72 + 20
    for i, (p, q) in enumerate(l):
        if i: hair(d, f, x, y - 10, cw)
        y += _linha_carrinho(d, f, x, y, cw, p, q, mob=True) + 20
    y += _aviso_promo(d, f, x, y, cw, faltam, app) + 16
    c = d.frame(f, "Resumo", x, y, cw, 10, fill=C["card"], stroke=C["line"], stroke_opacity=0.08, radius=ui.R_CARD)
    h = _resumo(d, c, 16, 16, cw - 32) + 32
    d.nodes[c]["height"] = float(h)
    y += h + 12
    ui.button(d, f, x, y, "Continuar comprando", app=app, kind="secondary", w=cw, h=44)
    total = max(H, y + 44 + 24 + 88)
    ui.altura(d, f, total)
    ui.mobile_bar(d, f, ui.brl(tot), caption=f"Total · {ui.brl(pix)} no Pix", app=app, label="Finalizar pedido")
    return total

SCREENS = [
    ("E01", "Confirmação de idade", e01),
    ("E02", "Escolha da loja", e02),
    ("E03", "Início da loja", e03),
    ("E04", "Categoria", e04),
    ("E05", "Filtros", e05),
    ("E06", "Busca com sugestões", e06),
    ("E07", "Menu de categorias", e07),
    ("E08", "Carrinho", e08),
]
