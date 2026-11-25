# E-commerce Smoke House no FigCraft

| Item | O que é |
|---|---|
| `Smoke House · E-commerce.figcraft` | O arquivo de design (abre no FigCraft) |
| `previas/` | Um JPG por quadro, para ver sem abrir o FigCraft |
| `gerador/` | O código que gera o arquivo (fonte da verdade) |
| `gerador/capturas/` | O protótipo atual (`index.html`) capturado no Chrome em computador, tablet e celular |

## Páginas do arquivo

- **Hoje · Vitrine / Área do colaborador / Painel dos donos:** como o protótipo está hoje, capturado sem alteração. É a referência.
- **Responsivo · …:** as mesmas telas redesenhadas em computador 1440, tablet 1180 e celular 390, com a marca de hoje e corrigindo o que quebra em cada tamanho:
  - celular: barra de baixo (Início, Categorias, Buscar, Carrinho) no lugar da barra de categorias que cobria o checkout; abas dos painéis na barra de baixo (antes cortavam à direita); tabelas viram cartões; WhatsApp acima da barra; ação principal fixa embaixo; sem o aviso "Protótipo navegável";
  - tablet: layout próprio de 1180, não o computador apertado;
  - computador: conteúdo até 1200 de largura, centralizado.

## Fonte da marca

Os títulos usam a fonte pincelada do site (`assets/web/brush.woff2`, família "BrushUpTooW01-Regular"). Para o FigCraft mostrá-la, ela foi convertida para TTF e copiada para `~/Library/Application Support/Craft Fonts/SHBrush.ttf`. Em outro computador, repita isso antes de abrir o arquivo. Confirme a licença da fonte (pendência já registrada no README do e-commerce).

## Gerar de novo

```bash
cd gerador
PYLIB=<pasta com playwright e pillow> python3 capturar.py   # só se o protótipo mudar
python3 build.py                                            # monta, guarda backup, copia para ~/Documents/figcraft
export FC_PORT=47611; python3 -I -c "import sys; sys.path.insert(0,'.'); import fcctl; fcctl.launch()"
python3 render.py "../Smoke House · E-commerce.figcraft" && python3 previas.py
pkill -f -- "--control $FC_PORT"
```

O fluxo é o da skill global `figcraft-telas`. `telas/_dados.py` é extraído de `src/app.js`; se o catálogo mudar, extraia de novo em vez de editar à mão.
