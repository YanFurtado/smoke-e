import asyncio
from playwright.async_api import async_playwright
import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = "file://" + str(ROOT / "index.html")
OUT = ROOT / "tests" / "saida"; OUT.mkdir(exist_ok=True)
CHROME = os.environ.get("CHROME_PATH")  # opcional: caminho do Chrome; sem ele usa o Chromium do Playwright
LAUNCH = dict(executable_path=CHROME, args=["--no-sandbox"]) if CHROME else dict(args=["--no-sandbox"])
SP = str(OUT) + "/"
R=[]
def ok(n,c,i=""):R.append((n,bool(c),i))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**LAUNCH)
        for vp,tag in [({"width":1366,"height":900},"desk"),({"width":390,"height":844},"mob")]:
            pg=await b.new_page(viewport=vp);errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
            await pg.goto(INDEX+"#pnz");await pg.evaluate("localStorage.setItem('sh_age','ok');localStorage.setItem('sh_cookie','all')");await pg.reload();await pg.wait_for_timeout(300)
            ok(tag+" rodapé com 12 bandeiras",await pg.evaluate("document.querySelectorAll('#f-pay span').length===12"))
            await pg.evaluate("S.cart={41:0};delete S.cart[41];S.cart[50]=2;renderCart()")
            await pg.click("#open-cart");await pg.wait_for_timeout(300)
            ok(tag+" carrinho mostra parcelas e formas","3x" in await pg.inner_text("#cart-foot") and "boleto" in await pg.inner_text("#cart-foot"))
            await pg.click("#go-co");await pg.wait_for_timeout(300)
            await pg.fill("#co-nome","Ana Teste");await pg.fill("#co-whats","87999991234");await pg.fill("#co-nasc","10101990");await pg.click("[data-conext='1']");await pg.click("[data-conext='2']");await pg.wait_for_timeout(200)
            ok(tag+" checkout com 6 formas",await pg.evaluate("document.querySelectorAll('[data-cop]').length===6"))
            await pg.click("label:has([data-cop=credito])");await pg.wait_for_timeout(200)
            ok(tag+" crédito mostra 1x a 3x",await pg.evaluate("document.querySelectorAll('[data-coparc]').length===3"))
            ok(tag+" crédito sem desconto Pix","Desconto Pix" not in await pg.inner_text(".co-aside"))
            await pg.click("label:has([data-coparc='3'])")
            w=await pg.evaluate("[document.documentElement.scrollWidth,innerWidth]");ok(tag+" sem rolagem lateral no pagamento",w[0]<=w[1]+1,w)
            await pg.click("[data-co18]");await pg.click("[data-coconfirm]");await pg.wait_for_timeout(300)
            ok(tag+" pedido salvo com crédito 3x",await pg.evaluate("S.lastOrder.pag==='credito'&&S.lastOrder.parc===3"))
            ok(tag+" recibo mostra parcelas","3x" in await pg.inner_text("#checkout"))
            msg=await pg.evaluate("orderMsg(S.lastOrder)");ok(tag+" WhatsApp com forma e parcelas","Cartão de crédito em 3x sem juros" in msg,msg[-80:])
            await pg.evaluate("S.cart={2:1};goCheckout()");await pg.click("[data-conext='2']");await pg.wait_for_timeout(200)
            await pg.click("label:has([data-cop=credito])");await pg.wait_for_timeout(150)
            ok(tag+" valor baixo: só 1x e aviso",await pg.evaluate("document.querySelectorAll('[data-coparc]').length===1") and "a partir de R$ 60" in await pg.inner_text("#checkout"))
            for k in ["debito","carteira","boleto","dinheiro","pix"]:
                await pg.click(f"label:has([data-cop={k}])");await pg.wait_for_timeout(100)
            ok(tag+" Pix volta a dar desconto","Desconto Pix" in await pg.inner_text(".co-aside"))
            await pg.evaluate("goPage('pagamento')");await pg.wait_for_timeout(150)
            ok(tag+" página lista as 6 formas",await pg.evaluate("document.querySelectorAll('#page h2').length===6"))
            # colaborador
            await pg.evaluate("localStorage.setItem('sh_sv_me','carla');location.hash='colaborador'");await pg.wait_for_timeout(400)
            await pg.evaluate("SV.pos={items:[{id:2,n:'x',p:5,q:1}],pag:'pix'};svPos()")
            ok(tag+" balcão com 6 formas",await pg.evaluate("document.querySelectorAll('#pos-pag option').length===6"))
            await pg.evaluate("closePos();SV.tab='pedidos';SV.of='todos';svShell()")
            ok(tag+" pedidos antigos 'cartao' viram crédito",await pg.evaluate("payOf('cartao').k==='credito'"))
            # dono
            await pg.evaluate("localStorage.setItem('sh_ow','1');location.hash='donos'");await pg.wait_for_timeout(400)
            ok(tag+" rosca do painel com mais formas",await pg.evaluate("document.querySelectorAll('.donut')[0].querySelectorAll('circle').length>4"))
            await pg.click("[data-owtab=fin]");await pg.wait_for_timeout(200)
            ok(tag+" financeiro por forma",await pg.evaluate("[...document.querySelectorAll('.dl span')].some(s=>s.textContent==='Crédito')"))
            ok(tag+" sem erros",not errs,errs[:2])
            await pg.close()
        await b.close()
    f=[r for r in R if not r[1]];print(f"TOTAL {len(R)} OK {len(R)-len(f)} FALHAS {len(f)}")
    for r in f:print("FALHA",r)
asyncio.run(main())
