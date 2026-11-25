# Telas do PDV no FigCraft

| Item | O que é |
|---|---|
| `Smoke House · PDV.figcraft` | O arquivo de design (abre no FigCraft). 60 telas + capa e direção visual, cada tela em computador 1440, tablet 1180 e celular 390 |
| `previas/` | Um JPG por quadro, para ver sem abrir o FigCraft (e para os agentes conferirem) |
| `gerador/` | O código que gera o arquivo. A fonte da verdade é o código, não o arquivo |

## Mudar uma tela

1. Edite o módulo da tela em `gerador/telas/` (`dav_a`, `dav_b`, `nfce`, `host_a`, `host_b`, `capa`). Componentes e tokens ficam em `gerador/ui.py`.
2. `cd gerador && python3 build.py`: monta o arquivo aqui, guarda a versão anterior em `gerador/backups/` e copia para `~/Documents/figcraft/`.
3. Para conferir: `python3 -I -c "import sys; sys.path.insert(0,'.'); import fcctl; fcctl.launch()"` abre uma segunda instância do FigCraft com controle; `python3 render.py "../Smoke House · PDV.figcraft" D04` exporta os PNGs; `python3 previas.py` atualiza os JPGs (precisa do Pillow).
4. Feche só a instância de controle: `pkill -f -- "--control 47611"`.

Editar direto no FigCraft é perdido na próxima geração. Se fizer um ajuste à mão, leve-o para o módulo.

O mesmo fluxo, para qualquer projeto, está na skill global `figcraft-telas`.
