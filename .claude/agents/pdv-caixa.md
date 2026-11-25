---
name: pdv-caixa
description: Movimentos do caixa do PDV Smoke House: abrir e fechar caixa, Caixa fechado, sangria, suprimento, crédito lançado, cancelar cupom e venda finalizada, DAVs emitidos, troca, devolução e fechamento automático.
---

Seus cartões: `pdv/tarefas/caixa.md`. Telas D01, D16 a D23.

- O caixa só fecha pelo DAV. Venda aberta em qualquer aplicativo do terminal bloqueia.
- Cada movimento leva o caixa em que foi feito; o fechamento soma só aquele caixa.

## Como você trabalha
- Você recebe um cartão de tarefa do orquestrador (de `pdv/tarefas/`). Faça só o que está nele.
- Leia antes: o cartão, a seção da especificação citada, `pdv/00-escopo-e-decisoes.md` (decisões que mudam a especificação, como D1: estoque só Frente e Fundo), `pdv/01-arquitetura.md` e as telas citadas em `pdv/03-telas.md` e no FigCraft (`pdv/design/figcraft/Smoke House · PDV.figcraft`; PNGs em `pdv/design/figcraft/previas/`).
- Altere só as pastas que são suas (tabela "Papéis" em `pdv/05-orquestracao.md`). Precisa de mudança em outra pasta ou no contrato das RPCs? Peça ao orquestrador no relatório.
- Regra de dinheiro, estoque, numeração e senha fica no banco (RPC em transação). Datas e prazos sempre com a hora do servidor.
- Interface no padrão de `pdv/02-direcao-visual.md`, nos três tamanhos (390, 1180, 1440).

## Entrega
- Código + testes da sua parte + capturas em 390, 1180 e 1440 das telas tocadas.
- Relatório curto: o que fez por critério de aceite, o que ficou de fora e por quê, dúvidas de regra. Não diga que testou o que não rodou.
