"""Captura o protótipo atual (index.html) em computador 1440, tablet 1180 e celular 390.
Uso: PYLIB=<pasta com playwright> python3 capturar.py [filtro]
Saída: capturas/<código>_<aparelho>.jpg (página inteira)."""
import asyncio, os, sys, io
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
from playwright.async_api import async_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = "file://" + os.path.abspath(os.path.join(HERE, "..", "..", "..", "index.html"))
OUT = os.path.join(HERE, "capturas"); os.makedirs(OUT, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VP = {"desktop": (1440, 900), "tablet": (1180, 820), "mobile": (390, 844)}
BASE = "localStorage.setItem('sh_age','ok');localStorage.setItem('sh_cookie','essential');"

async def reveal(pg):
    await pg.evaluate("document.querySelectorAll('.rv,.rv-pop').forEach(e=>e.classList.add('in'))")
    await pg.wait_for_timeout(500)

async def cart(pg):
    await pg.evaluate("S.cart={1:2,4:1,10:1};renderCart&&renderCart()")
    await pg.wait_for_timeout(200)

async def visible(pg, sel):
    try: return await pg.is_visible(sel)
    except Exception: return False

# cada estado: (código, título, init localStorage, hash, passos async, página inteira?)
async def s_none(pg, dev): pass
async def s_age_yes(pg, dev): await pg.click("#age-yes"); await pg.wait_for_timeout(500)
async def s_home(pg, dev): await reveal(pg)
async def s_cat(pg, dev):
    await pg.click("#circles .circle >> nth=0"); await pg.wait_for_timeout(500); await reveal(pg)
async def s_filters(pg, dev):
    await s_cat(pg, dev)
    if await visible(pg, "#f-open"): await pg.click("#f-open"); await pg.wait_for_timeout(500)
async def s_search(pg, dev):
    if dev == "mobile" and await visible(pg, "[data-bn=search]"):
        await pg.click("[data-bn=search]"); await pg.wait_for_timeout(400)
    await pg.click("#q"); await pg.keyboard.type("seda"); await pg.wait_for_timeout(500)
async def s_menu(pg, dev):
    if dev == "mobile" and await visible(pg, "[data-bn=cats]"): await pg.click("[data-bn=cats]")
    elif await visible(pg, "#all-cats"): await pg.click("#all-cats")
    await pg.wait_for_timeout(500)
async def s_cart(pg, dev):
    await cart(pg); await pg.click("#open-cart") if await visible(pg, "#open-cart") else await pg.click("[data-bn=cart]")
    await pg.wait_for_timeout(600)
async def s_co(step):
    async def f(pg, dev):
        await s_cart(pg, dev); await pg.click("#go-co"); await pg.wait_for_timeout(400)
        await pg.fill("#co-nome", "Mariana Albuquerque"); await pg.fill("#co-whats", "87988412207"); await pg.fill("#co-nasc", "27111994")
        if step >= 2:
            await pg.click("[data-conext='1']"); await pg.wait_for_timeout(300)
            await pg.click("label:has([data-cot=entrega])"); await pg.wait_for_timeout(200)
            await pg.fill("#co-rua", "Rua Joaquim Nabuco"); await pg.fill("#co-num", "120")
            await pg.select_option("#co-bairro", index=1); await pg.wait_for_timeout(200)
        if step >= 3:
            await pg.click("[data-conext='2']"); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('[data-cop=pix]')?.click()"); await pg.wait_for_timeout(300)
        if step >= 4:
            await pg.evaluate("document.querySelector('[data-co18]')?.click()"); await pg.wait_for_timeout(100)
            await pg.evaluate("document.querySelector('[data-coconfirm]')?.click()"); await pg.wait_for_timeout(800)
    return f
async def s_page(name):
    async def f(pg, dev): await pg.evaluate(f"goPage('{name}')"); await pg.wait_for_timeout(400)
    return f
async def s_sv(tab, extra=None):
    async def f(pg, dev):
        if tab != "inicio": await pg.click(f"[data-svtab={tab}]"); await pg.wait_for_timeout(600)
        if extra == "pos": await pg.click("[data-svpos]"); await pg.wait_for_timeout(300); await pg.click("[data-posadd] >> nth=0"); await pg.click("[data-posadd] >> nth=1"); await pg.wait_for_timeout(300)
    return f
async def s_sv_login(pg, dev): await pg.click("[data-svwho=carla]"); await pg.wait_for_timeout(300)
async def s_ow(tab, extra=None):
    async def f(pg, dev):
        if tab: await pg.click(f"[data-owtab={tab}]"); await pg.wait_for_timeout(500)
        if extra == "modal": await pg.click("[data-owo] >> nth=0"); await pg.wait_for_timeout(400)
    return f

async def estados():
    sv = BASE + "localStorage.setItem('sh_sv_me','carla');"
    ow = BASE + "localStorage.setItem('sh_ow','1');"
    return [
        ("E01", "Confirmação de idade", "", "", s_none, False),
        ("E02", "Escolha da loja", "", "", s_age_yes, False),
        ("E03", "Início da loja", BASE, "#pnz", s_home, True),
        ("E04", "Categoria", BASE, "#pnz", s_cat, True),
        ("E05", "Filtros", BASE, "#pnz", s_filters, False),
        ("E06", "Busca com sugestões", BASE, "#pnz", s_search, False),
        ("E07", "Menu de categorias", BASE, "#pnz", s_menu, False),
        ("E08", "Carrinho", BASE, "#pnz", s_cart, False),
        ("E09", "Checkout · dados", BASE, "#pnz", await s_co(1), False),
        ("E10", "Checkout · entrega", BASE, "#pnz", await s_co(2), False),
        ("E11", "Checkout · pagamento", BASE, "#pnz", await s_co(3), False),
        ("E12", "Pedido enviado", BASE, "#pnz", await s_co(4), False),
        ("E13", "Página de trocas", BASE, "#pnz", await s_page("trocas"), True),
        ("E14", "Guias", BASE, "#pnz", await s_page("guias"), True),
        ("E15", "Link do colaborador", BASE, "#pnz-vendedor-carla", s_home, False),
        ("C01", "Colaborador · entrar", BASE, "#colaborador", s_sv_login, False),
        ("C02", "Colaborador · início", sv, "#colaborador", await s_sv("inicio"), True),
        ("C03", "Colaborador · pedidos", sv, "#colaborador", await s_sv("pedidos"), True),
        ("C04", "Colaborador · venda no balcão", sv, "#colaborador", await s_sv("pedidos", "pos"), False),
        ("C05", "Colaborador · estoque", sv, "#colaborador", await s_sv("estoque"), True),
        ("C06", "Colaborador · link e QR", sv, "#colaborador", await s_sv("link"), True),
        ("C07", "Colaborador · comissões", sv, "#colaborador", await s_sv("comissoes"), True),
        ("O01", "Donos · entrar", BASE, "#donos", s_none, False),
        ("O02", "Donos · visão geral", ow, "#donos", await s_ow(None), True),
        ("O03", "Donos · financeiro", ow, "#donos", await s_ow("fin"), True),
        ("O04", "Donos · pedidos", ow, "#donos", await s_ow("ped"), True),
        ("O05", "Donos · pedido aberto", ow, "#donos", await s_ow("ped", "modal"), False),
        ("O06", "Donos · equipe", ow, "#donos", await s_ow("eq"), True),
        ("O07", "Donos · agenda", ow, "#donos", await s_ow("ag"), True),
        ("O08", "Donos · ajustes", ow, "#donos", await s_ow("cfg"), True),
    ]

async def main(filt=""):
    lst = await estados()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        for dev, (w, h) in VP.items():
            for code, title, init, hsh, step, full in lst:
                if filt and not code.startswith(filt): continue
                ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
                pg = await ctx.new_page()
                await pg.goto(INDEX); await pg.evaluate("localStorage.clear()")
                if init: await pg.evaluate(init)
                await pg.goto(INDEX + hsh); await pg.wait_for_timeout(700)
                try:
                    await step(pg, dev)
                except Exception as e:
                    print("AVISO", code, dev, str(e).splitlines()[0][:120])
                await pg.wait_for_timeout(300)
                png = await pg.screenshot(full_page=full)
                im = Image.open(io.BytesIO(png)).convert("RGB")
                if im.height > 7000: im = im.crop((0, 0, im.width, 7000))
                im.save(os.path.join(OUT, f"{code}_{dev}.jpg"), quality=82, optimize=True)
                print(code, dev, im.size)
                await ctx.close()
        await b.close()

asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else ""))
