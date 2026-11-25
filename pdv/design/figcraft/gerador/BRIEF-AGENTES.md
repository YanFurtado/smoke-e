# Briefing dos subagentes de design (telas do PDV Smoke House no FigCraft)

Você desenha um grupo de telas do PDV Smoke House, em três tamanhos cada (computador 1440×900, tablet 1180×820, celular 390×844), gerando um arquivo FigCraft por código Python. O orquestrador junta tudo depois e revisa.

## Leia antes de começar
1. `/Users/jeanlsg/Documents/github/smoke-e/pdv/03-telas.md`: o que cada tela precisa mostrar e as regras de adaptação por aparelho. **Seus códigos estão no seu pedido.**
2. `/Users/jeanlsg/Documents/github/smoke-e/pdv/02-direcao-visual.md`: cores, tipo, espaço, checklist. Siga à risca.
3. A especificação completa (texto extraído do PDF, fonte principal das regras): `/Users/jeanlsg/Documents/github/smoke-e/pdv/especificacao/Especificacao-PDV-Smoke-House-v1.2.02.txt`. **Mudança aprovada:** o estoque tem só Frente de loja e Fundo de loja. Onde a especificação diz Matriz, use Fundo de loja; não desenhe Matriz.
4. O gerador, em `/Users/jeanlsg/Documents/github/smoke-e/pdv/design/figcraft/gerador/`:
   - `fc.py`: base (Doc, frame, text, ellipse, polyline, image). `text()` aceita `align="right"|"center"` (com ou sem `w`), `w=` para quebrar linha, `mono=True` para Menlo.
   - `ui.py`: tokens e componentes. **Use os componentes**: `topbar`, `footer`, `host_shell`, `sidebar`, `page_head`, `button`, `field`, `toggle`, `checkbox`, `radio`, `tabs`, `chips`, `status`, `banner`, `stat`, `table`, `mobile_rows`, `card`, `kv`, `window`, `confirm`, `keycap`, `icon`, `product_tile`, `produto`, `avatar`, `cupom_tela`, `total_block`, `receipt`, `mobile_bar`, `brl`. Dados de exemplo: `ui.PRODUTOS`, `ui.CLIENTES`.
   - `telas/dav_a.py`: **telas de referência** (D02, D03, D04, D07). Copie o jeito de montar: uma função por tela `fn(d, f, dev, app)`, ramos para `dev == "mobile"`, rodapé e topo pelos componentes.
   - `build.py` (monta), `render.py` (exporta PNG), `fcctl.py` (controle do FigCraft).

## Regras de trabalho
- Escreva **só** no seu módulo `telas/<modulo>.py`. Não altere `fc.py`, `ui.py`, `build.py`, `render.py` nem módulos de outros agentes. Se precisar de um componente novo, crie a função dentro do seu módulo (prefixo `_`) e cite no relatório como sugestão para o `ui.py`.
- O módulo expõe `PAGE` (nome da página), `APP` (`"dav"`, `"nfce"` ou `"host"`) e `SCREENS = [(codigo, titulo, funcao), ...]` em ordem de código.
- A função desenha dentro do quadro `f`, que já tem o tamanho do aparelho. Para tela que rola (comum no celular e em cadastros), devolva a altura total; o quadro cresce.
- Janelas por cima de uma tela: desenhe a tela de fundo chamando a função da tela base (como D07 chama D04) e depois `ui.window(...)` ou `ui.confirm(...)`. No celular a janela vira folha de baixo sozinha.
- Texto da interface em português do Brasil, curto, sem ponto final em rótulo e botão, sem exclamação, sem emoji. Dados plausíveis: produtos de `ui.PRODUTOS`, clientes de `ui.CLIENTES`, operadores Arthur (Terminal 01) e Ana (Terminal 02), supervisora de caixa Carla, administrador Lucas, data 24/11/2026, lojas PNZ (Petrolina-PE) e LEM (Luís Eduardo Magalhães-BA). Dinheiro sempre no formato `R$ 1.234,50` (use `brl`). CNPJ da loja: "CNPJ a informar".
- Seleção em lista: sempre o `selected=` do `table`/`mobile_rows` (fundo cinza claro e borda preta, regra da especificação).
- Nada fora da tela: nenhum texto pode passar da borda do quadro nem sobrepor outro. No celular, nada abaixo de 11 px e nada de rolagem lateral.

## Como conferir o que desenhou
Use **a sua** instância do FigCraft, na porta indicada no seu pedido (nunca a 47611 e nunca outra porta):
```bash
cd /Users/jeanlsg/Documents/github/smoke-e/pdv/design/figcraft/gerador
FC_PORT=<sua porta> python3 -I -c "import sys; sys.path.insert(0,'.'); import fcctl; fcctl.launch()"
python3 build.py out/<modulo>.figcraft --so <modulo>
FC_PORT=<sua porta> python3 render.py out/<modulo>.figcraft <filtro opcional, ex.: D05>
```
Os PNGs saem em `out/png/` (nome começa pelo código da tela). Abra-os com a ferramenta Read e confira contra a checklist da direção visual e contra a especificação. Corrija e renderize de novo. Faça no máximo três rodadas completas; depois, só a tela que ainda tem defeito.

`build.py` imprime "ERRO" quando uma função quebra. Nenhuma tela pode terminar com erro.

Ao terminar, feche **só a sua** instância: `pkill -f -- "--control <sua porta>"`. Nunca feche outro processo do FigCraft: há uma instância do usuário aberta.

## Relatório final (curto)
- Telas entregues (código, título) e o que cada uma mostra das regras da especificação.
- O que ficou de fora ou ficou diferente da especificação, e por quê.
- Componentes que você criou localmente e que valeriam ir para o `ui.py`.
- Dúvidas de regra que o orquestrador precisa decidir.
