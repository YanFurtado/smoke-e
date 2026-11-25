# Briefing: redesenho responsivo do e-commerce Smoke House no FigCraft

Você redesenha um grupo de telas do **e-commerce que já existe** no repositório (`smokehouse-ecommerce/index.html`, gerado de `src/template.html` + `src/app.js`), em **computador 1440, tablet 1180 e celular 390**, gerando o FigCraft por código. Não é um produto novo: mantenha a marca, o conteúdo e as funções de hoje; o trabalho é deixar cada tela certa nos três tamanhos.

## Leia antes
1. A skill `~/.claude/skills/figcraft-telas/SKILL.md` e `references/componentes.md`, `references/armadilhas.md`.
2. As capturas de hoje das suas telas: `capturas/<código>_desktop.jpg`, `_tablet.jpg`, `_mobile.jpg` (abra com Read). São a referência de conteúdo e de marca.
3. `src/app.js` e `src/template.html` do e-commerce, para textos, regras e dados reais (preços, lojas, formas de pagamento, passos do checkout, abas dos painéis).
4. O gerador nesta pasta: `ui.py` (tokens da marca e componentes; no fim estão os da marca: `brush`, `foto_produto`, `card_produto`, `circulo_cat`, `ticker`, `loja_header`, `bottom_nav`, `whats_fab`, `painel_header`, `painel_nav`), `telas/_dados.py` (dados reais extraídos do app.js) e **`telas/vitrine_a.py` (E03, a tela de referência: copie o jeito)**.

## Marca (não mude)
Fundo `#f3f2ed`, preto `#0e0f0d` no topo, verde `#34925e` (texto branco por cima: use o `acc` `#2b7d50`), amarelo `#ffbe00` para destaques e chamadas, Poppins no texto (`ui.FONT`), títulos pincelados com `ui.brush` (fonte `BrushUpTooW01-Regular`, sempre em caixa alta, duas cores: preto + verde). Cartões brancos com raio 12. Foto de produto: `ui.foto_produto` (bloco na cor da marca, sem gradiente).

## O que o responsivo tem de resolver (problemas vistos nas capturas)
- **Celular:** a barra de categorias grudava por cima do checkout → no celular não há barra de categorias; use `ui.bottom_nav` (Início, Categorias, Buscar, Carrinho).
- **Celular:** abas do painel do colaborador e dos donos cortavam à direita → `ui.painel_header` + `ui.painel_nav` (barra de baixo; mais de 5 abas vira "Mais").
- **Celular:** tabelas espremidas (pedidos dos donos) → viram cartões (`ui.mobile_rows` ou cartão próprio), nada de rolagem lateral.
- **Celular:** o botão do WhatsApp cobria botões → `ui.whats_fab` acima da barra de baixo; ação principal em barra fixa embaixo quando houver (checkout, carrinho).
- **Celular:** o aviso "Protótipo navegável" ocupava 3 linhas → não desenhe esse aviso em nenhum tamanho.
- **Tablet:** hoje é o computador espremido → use 1180 de verdade: menos colunas onde aperta, painéis laterais viram coluna única quando não cabem, alvos de toque ≥ 40.
- **Computador:** conteúdo até 1200 de largura, centralizado (`wrap()` em vitrine_a.py).

## Regras de trabalho
- Escreva só no seu módulo (está no seu pedido). Não altere `ui.py`, `fc.py`, `build.py`, `_dados.py` nem módulos de outros. Componente novo: no seu módulo com prefixo `_`, e cite no relatório.
- `PAGE`, `APP` (`"loja"`, `"colab"` ou `"donos"`) e `SCREENS = [(código, título, função)]` em ordem. Use os **mesmos códigos** das capturas (E01…, C01…, O01…).
- Tela que rola: `ui.altura(d, f, total)` antes de desenhar a moldura e de novo no fim, se mudar; devolva a altura.
- Texto em português, curto, sem ponto final em rótulo e botão. Dados do `_dados.py` e do app.js.

## Conferir
```bash
cd <esta pasta>
export FC_PORT=<sua porta>
python3 -I -c "import sys; sys.path.insert(0,'.'); import fcctl; fcctl.launch()"
python3 build.py --saida out/<modulo>.figcraft --so <modulo> --sem-espelho
python3 render.py out/<modulo>.figcraft
PYLIB=/private/tmp/claude-501/-Users-jeanlsg-Documents-github-smoke-e/7b067a75-e9ea-4226-925b-f5dad33ed92c/scratchpad/pylib python3 prancha.py <códigos>
```
Compare a prancha com a captura de hoje da mesma tela. No máximo três rodadas. Nenhum `ERRO`, nenhum texto fora da caixa ou sobreposto. No fim: `pkill -f -- "--control $FC_PORT"` (só a sua).

## Relatório
Telas entregues; o que mudou em cada tamanho em relação a hoje (o responsivo); o que ficou de fora; componentes que valeriam ir para o ui.py; dúvidas.
