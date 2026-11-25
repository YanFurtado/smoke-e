"""Páginas "Hoje": o protótipo atual (index.html) capturado em computador, tablet e celular (capturar.py)."""
import os
import ui
from ui import C, T

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITULOS = {
    "E01": "Confirmação de idade", "E02": "Escolha da loja", "E03": "Início da loja", "E04": "Categoria",
    "E05": "Filtros", "E06": "Busca com sugestões", "E07": "Menu de categorias", "E08": "Carrinho",
    "E09": "Checkout · dados", "E10": "Checkout · entrega", "E11": "Checkout · pagamento", "E12": "Pedido enviado",
    "E13": "Página de trocas", "E14": "Guias", "E15": "Link do colaborador",
    "C01": "Colaborador · entrar", "C02": "Colaborador · início", "C03": "Colaborador · pedidos",
    "C04": "Colaborador · venda no balcão", "C05": "Colaborador · estoque", "C06": "Colaborador · link e QR",
    "C07": "Colaborador · comissões",
    "O01": "Donos · entrar", "O02": "Donos · visão geral", "O03": "Donos · financeiro", "O04": "Donos · pedidos",
    "O05": "Donos · pedido aberto", "O06": "Donos · equipe", "O07": "Donos · agenda", "O08": "Donos · ajustes",
}
DEV = [("desktop", "Computador 1440"), ("tablet", "Tablet 1180"), ("mobile", "Celular 390")]

def pagina(d, page, prefixo, intro):
    T(d, page, intro, 0, -120, size=20, color=C["text2"], lh=28, w=2800, name="Introdução")
    y = 0
    for code in sorted(c for c in TITULOS if c.startswith(prefixo)):
        T(d, page, f"{code} · {TITULOS[code]} · hoje", 0, y, size=28, weight=500, lh=36, name=f"Título {code}")
        x, row_h = 0, 0
        for dev, lab in DEV:
            path = os.path.join(HERE, "capturas", f"{code}_{dev}.jpg")
            if not os.path.exists(path): continue
            w = ui.DEVICES[dev][0]
            from fc import _img_size
            iw, ih = _img_size(open(path, "rb").read())
            h = ih * w / iw
            T(d, page, lab, x, y + 52, size=14, color=C["text2"], lh=20, name=f"Rótulo {code} {dev}")
            fr = d.frame(page, f"{code} · {TITULOS[code]} · {lab} · hoje", x, y + 84, w, h, fill="#ffffff", clip=True)
            d.image(fr, path, 0, 0, w, h, name="Captura", mode="fill")
            row_h = max(row_h, h); x += w + 120
        y += 84 + row_h + 200
