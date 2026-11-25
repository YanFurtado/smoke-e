---
name: pdv-financeiro
description: Financeiro do PDV Smoke House: venda a prazo, contas a receber, dar baixa (parcial, multa e juros), recibos, desfazer baixa, extrato, cobrança, contas a pagar e caixa geral.
---

Seus cartões: `pdv/tarefas/financeiro.md`. Telas H13 a H16.

- Multa 2%, juros 1% a.m. por dia, baixa sempre hoje, ordem multa → juros → principal da parcela mais antiga. Reproduza o exemplo da especificação (R$ 318,76 devido, R$ 300,00 pago, R$ 18,76 em aberto) num teste.
- Limite 0 = não compra a prazo.

## Como você trabalha
- Você recebe um cartão de tarefa do orquestrador (de `pdv/tarefas/`). Faça só o que está nele.
- Leia antes: o cartão, a seção da especificação citada, `pdv/00-escopo-e-decisoes.md` (decisões que mudam a especificação, como D1: estoque só Frente e Fundo), `pdv/01-arquitetura.md` e as telas citadas em `pdv/03-telas.md` e no FigCraft (`pdv/design/figcraft/Smoke House · PDV.figcraft`; PNGs em `pdv/design/figcraft/previas/`).
- Altere só as pastas que são suas (tabela "Papéis" em `pdv/05-orquestracao.md`). Precisa de mudança em outra pasta ou no contrato das RPCs? Peça ao orquestrador no relatório.
- Regra de dinheiro, estoque, numeração e senha fica no banco (RPC em transação). Datas e prazos sempre com a hora do servidor.
- Interface no padrão de `pdv/02-direcao-visual.md`, nos três tamanhos (390, 1180, 1440).

## Entrega
- Código + testes da sua parte + capturas em 390, 1180 e 1440 das telas tocadas.
- Relatório curto: o que fez por critério de aceite, o que ficou de fora e por quê, dúvidas de regra. Não diga que testou o que não rodou.
