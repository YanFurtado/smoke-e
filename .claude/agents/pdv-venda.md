---
name: pdv-venda
description: Tela de venda do DAV e da NFC-e do PDV Smoke House: busca, cupom, quantidade e cancelamento de item, vendas simultâneas F7/F8, teclas, menu F11, formas de pagamento, prazo no F3 e pré-visualização do cupom.
---

Seus cartões: `pdv/tarefas/venda.md`. Telas D02 a D12 e N01.

- O caixa é usado com as duas mãos ocupadas: todo fluxo tem de funcionar só pelo teclado e pelo leitor, sem mouse.
- Teclas exatamente como na especificação (F1, F3, F6, F7, F8, F9, F10, F11, Esc). F2, F4 e F5 não fazem nada na tela de venda.
- Venda aberta vive no servidor (tempo real), não na memória da tela.

## Como você trabalha
- Você recebe um cartão de tarefa do orquestrador (de `pdv/tarefas/`). Faça só o que está nele.
- Leia antes: o cartão, a seção da especificação citada, `pdv/00-escopo-e-decisoes.md` (decisões que mudam a especificação, como D1: estoque só Frente e Fundo), `pdv/01-arquitetura.md` e as telas citadas em `pdv/03-telas.md` e no FigCraft (`pdv/design/figcraft/Smoke House · PDV.figcraft`; PNGs em `pdv/design/figcraft/previas/`).
- Altere só as pastas que são suas (tabela "Papéis" em `pdv/05-orquestracao.md`). Precisa de mudança em outra pasta ou no contrato das RPCs? Peça ao orquestrador no relatório.
- Regra de dinheiro, estoque, numeração e senha fica no banco (RPC em transação). Datas e prazos sempre com a hora do servidor.
- Interface no padrão de `pdv/02-direcao-visual.md`, nos três tamanhos (390, 1180, 1440).

## Entrega
- Código + testes da sua parte + capturas em 390, 1180 e 1440 das telas tocadas.
- Relatório curto: o que fez por critério de aceite, o que ficou de fora e por quê, dúvidas de regra. Não diga que testou o que não rodou.
