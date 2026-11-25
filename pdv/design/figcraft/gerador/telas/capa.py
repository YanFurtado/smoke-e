"""Página 00: capa e direção visual (tokens e componentes)."""
import os
import fc, ui
from ui import C, T, brl, APPS, hair

PAGE = "00 · Capa e direção visual"
APP = "dav"

def _sw(d, p, x, y, hexc, nome, valor, w=168):
    b = d.frame(p, f"Cor {nome}", x, y, w, 72, fill=hexc, stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CTL)
    T(d, p, nome, x, y + 84, size=13, weight=500, lh=20)
    T(d, p, valor, x, y + 104, size=12, color=C["muted"], lh=16, mono=True)

def build_page(d, page):
    # ---------- capa ----------
    f = d.frame(page, "00 · Capa", 0, 0, 1440, 900, fill=C["page"], clip=True)
    d.image(f, os.path.join(ui.HERE, "marca", "logo-verde.png"), 96, 96, 137, 120, name="Logo Smoke House")
    T(d, f, "PDV Smoke House", 96, 264, size=56, weight=500, lh=64, ls=-2)
    T(d, f, "Frente de caixa, cupom fiscal e retaguarda das lojas de Petrolina e Luís Eduardo Magalhães", 96, 340,
      size=20, color=C["text2"], lh=30, w=720)
    T(d, f, "Telas a partir da Especificação v1.2.02 · estoque em Frente e Fundo de loja · 24/11/2026", 96, 408,
      size=14, color=C["muted"], lh=20)
    y = 488
    for key, pg in (("dav", "01 · Frente de caixa (DAV)"), ("nfce", "02 · Cupom fiscal (NFC-e)"), ("host", "03 · Retaguarda (HOST)")):
        a = APPS[key]
        row = d.frame(f, f"Página {pg}", 96, y, 640, 64, fill=C["card"], stroke=C["line"], stroke_opacity=ui.LINE_A, radius=ui.R_CARD)
        d.ellipse(row, 20, 28, 8, a["acc"])
        T(d, row, a["nome"], 40, 12, size=15, weight=500, lh=20)
        T(d, row, pg, 40, 34, size=12, color=C["muted"], lh=16, mono=True)
        T(d, row, a["acc"], 640 - 20, 22, size=12, color=C["muted"], lh=16, mono=True, align="right")
        y += 76
    T(d, f, "Cada tela aparece em computador 1440, tablet 1180 e celular 390, lado a lado", 96, y + 16, size=13, color=C["text2"], lh=20)
    # momento da capa: o cupom
    lines = [("SMOKE HOUSE TABACARIA", "cb"), ("R. Joaquim Nabuco, 78 · Petrolina-PE", "c"), ("", "hr"),
             ("DAV 004812 · Terminal 01", "l"), ("24/11/2026 17:42 · Operador Arthur", "l"), ("", "hr"),
             (("001 Seda Zomo King Size Brown", "10,00"), "lr"), (("    2 × 5,00", ""), "lr"),
             (("002 Papelito Marrom c/ Piteira", "15,00"), "lr"), (("003 Isqueiro Clipper Largo", "14,00"), "lr"),
             (("004 Essência Zomo Love 66 50 g", "36,00"), "lr"), (("    2 × 18,00", ""), "lr"),
             (("005 Piteira de vidro Squadafum", "25,00"), "lr"), ("", "hr"),
             (("TOTAL", "R$ 100,00"), "lrb"), (("Pix", "45,00"), "lr"), (("Dinheiro", "60,00"), "lr"),
             (("Desconto", "-5,00"), "lr"), (("Troco", "10,00"), "lr"), ("", "hr"), ("PARABÉNS POR SUA COMPRA!", "c")]
    ui.receipt(d, f, 960, 120, 340, lines, title="Cupom DAV")
    # ---------- direção visual ----------
    g = d.frame(page, "00 · Direção visual", 1560, 0, 1440, 2280, fill=C["page"], clip=True)
    x = 96; y = 96
    T(d, g, "Direção visual", x, y, size=40, weight=500, lh=48, ls=-1); y += 72
    T(d, g, "Método unslop, de Damir Sokolovsky (@heydamir), CC BY 4.0", x, y, size=13, color=C["muted"], lh=20); y += 48
    linhas = [("Produto", "Frente de caixa e retaguarda das duas lojas da Smoke House Tabacaria: o operador vende pelo teclado e pelo leitor no balcão; o gerente confere caixa, estoque e contas a prazo"),
              ("Caráter", "Ligeiro, exato, de balcão"),
              ("Mundo", "O balcão da tabacaria: a bobina térmica do cupom, papel de seda, madeira escura e o verde da marca"),
              ("Momentos", "O cupom na tela, como bobina térmica, com o TOTAL grande ao lado. No HOST, o comprovante de fechamento e os números do dia"),
              ("Assinatura", "As teclas desenhadas (F3, F7, Esc) no rodapé, nos botões e nas janelas, e em nenhum outro lugar")]
    for k, v in linhas:
        T(d, g, k, x, y, size=14, weight=500, lh=22)
        T(d, g, v, x + 160, y, size=14, color=C["text2"], lh=22, w=860)
        y += 22 * max(1, -(-int(fc.text_width(v, 14)) // 860)) + 16
    y += 32; hair(d, g, x, y, 1248); y += 40
    T(d, g, "Neutros", x, y, size=20, weight=500, lh=28); y += 44
    cx = x
    for hexc, nome in [(C["page"], "Fundo"), (C["deep"], "Faixa"), (C["card"], "Cartão"), (C["raised"], "Campo"),
                       (C["sel"], "Seleção"), (C["paper"], "Papel do cupom"), (C["ink"], "Texto"), (C["text2"], "Secundário")]:
        _sw(d, g, cx, y, hexc, nome, hexc, w=140); cx += 156
    y += 148
    T(d, g, "Cor de cada aplicativo e cores de sentido", x, y, size=20, weight=500, lh=28); y += 44
    cx = x
    for key in ("dav", "nfce", "host"):
        a = APPS[key]; _sw(d, g, cx, y, a["acc"], a["nome"], a["acc"], w=180); cx += 196
    for hexc, nome in [(C["pos"], "Positivo"), (C["neg"], "Erro"), (C["warn"], "Aviso"), (C["info"], "Interrogação")]:
        _sw(d, g, cx, y, hexc, nome, hexc, w=140); cx += 156
    y += 148
    T(d, g, "Tipo", x, y, size=20, weight=500, lh=28); y += 44
    for txt, size, wt, mono, meta in [("CAIXA LIVRE", 88, 500, False, "Inter 88 · só Caixa livre e Caixa fechado"),
                                      ("R$ 100,00", 72, 500, False, "Inter 72 · TOTAL da venda"),
                                      ("Fechamento de caixa", 24, 500, False, "Inter 24 · título de página"),
                                      ("Formas de pagamento", 17, 500, False, "Inter 17 · título de janela"),
                                      ("Seda Zomo King Size Brown", 14, 400, False, "Inter 14 · texto"),
                                      ("006264  7898920550018  2 × 5,00", 13, 400, True, "Menlo 13 · códigos e valores")]:
        T(d, g, txt, x, y, size=size, weight=wt, lh=int(size * 1.2), mono=mono, ls=-2 if size > 40 else 0)
        T(d, g, meta, x + 1248, y + int(size * 1.2) / 2 - 10, size=12, color=C["muted"], lh=16, align="right", mono=True)
        y += int(size * 1.2) + 20
    y += 24; hair(d, g, x, y, 1248); y += 40
    T(d, g, "Componentes", x, y, size=20, weight=500, lh=28); y += 48
    bx = x
    for lab, kind, key in [("Formas de pagamento", "primary", "F3"), ("Finalizar", "dark", "Enter"), ("Cancelar cupom", "secondary", "F6"),
                           ("Cancelar venda", "danger", None), ("Voltar", "ghost", "Esc")]:
        _, w = ui.button(d, g, bx, y, lab, kind=kind, key=key); bx += w + 12
    y += 64
    ui.field(d, g, x, y, 300, label="Fundo de troco", value="150,00", mono=True)
    ui.field(d, g, x + 324, y, 300, label="Senha", value="••••", focused=True)
    ui.field(d, g, x + 648, y, 300, label="Código de barras", value="7898920550017", mono=True, error="Dígito verificador não confere")
    ui.field(d, g, x + 972, y, 276, label="Forma", value="Dinheiro", chevron=True)
    y += 96
    ui.chips(d, g, x, y, [("Todos", 412), ("Para repor", 23), ("Inativos", 9)], active=0)
    cx = x + 460
    for k in ("F1", "F3", "F6", "F7", "F8", "F10", "F11", "Esc", "Enter"):
        cx += ui.keycap(d, g, cx, y + 6, k) + 8
    sx = x + 900
    for lab, tone in (("Finalizada", "ok"), ("Cancelada", "neg"), ("Pendente", "warn")):
        sx += ui.status(d, g, sx, y + 6, lab, tone) + 24
    y += 64
    ui.toggle(d, g, x, y, True, "Venda a prazo", sub="Desligada, a forma PRAZO some do caixa")
    ui.checkbox(d, g, x + 400, y, True, "Exigir ticket na troca")
    ui.radio(d, g, x + 700, y, True, "Vencimento único")
    ui.radio(d, g, x + 900, y, False, "Até 3x")
    y += 64
    ui.banner(d, g, x, y, 620, "Sem estoque na frente de loja", "Há 14 no fundo de loja. Peça a reposição", tone="warn")
    ui.stat(d, g, x + 652, y - 20, 290, "Vendido hoje", "R$ 4.812,40", "+8% sobre a segunda passada")
    ui.stat(d, g, x + 958, y - 20, 290, "Caixas abertos", "2", "Terminal 01 e 02")
    y += 120
    rows = [["004812", "17:42", "Mariana Albuquerque", "Pix + Dinheiro", "Arthur", "5,00", "100,00", ("Finalizada", "ok")],
            ["004811", "17:31", "—", "Débito", "Arthur", "", "32,00", ("Finalizada", "ok")],
            ["004810", "17:20", "Rafael Coelho Nunes", "PRAZO", "Ana", "", "289,00", ("Finalizada", "ok")],
            ["004809", "17:02", "—", "Dinheiro", "Ana", "", "18,00", ("Cancelada", "neg")]]
    ui.table(d, g, x, y, 1248, [("Número", 96, "l", True), ("Hora", 72, "l", True), ("Cliente", None, "l"), ("Pagamento", 160, "l"),
                                 ("Vendedor", 120, "l"), ("Desconto", 96, "r", True), ("Total", 112, "r", True), ("Situação", 140, "l")],
             rows, selected=1)
    y += 36 + 4 * 40 + 48
    T(d, g, "A linha selecionada tem fundo cinza claro e borda fina preta, igual com mouse e teclado", x, y, size=13, color=C["text2"], lh=20)
    d.nodes[g]["height"] = float(y + 96)
