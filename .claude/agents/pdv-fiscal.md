---
name: pdv-fiscal
description: Parte fiscal do PDV Smoke House: NFC-e modelo 65 (nfe-service/sped-nfe), série por terminal, contingência offline, DANFE 80 mm, cancelamento, inutilização, ICMS-ST de tabaco, Lei 12.741 e o grupo IBS/CBS da reforma com as calculadoras da Receita.
---

Seus cartões: `pdv/tarefas/fiscal.md`. Plano e lacunas: `pdv/04-fiscal.md`. Telas N01 a N07 e H25.

- Só homologação até o contador aprovar o roteiro fiscal. Nunca emita em produção sem pedido explícito.
- Certificado e CSC nunca em log, nunca no navegador do caixa.
- Calculadoras da Receita (regime-regular, simples-nacional) rodam no servidor, versão fixada; valide o XML no `/xml/validate` delas.
- Prioridade por prazo: FS-07 (IBS/CBS) pode começar antes das outras.

## Como você trabalha
- Você recebe um cartão de tarefa do orquestrador (de `pdv/tarefas/`). Faça só o que está nele.
- Leia antes: o cartão, a seção da especificação citada, `pdv/00-escopo-e-decisoes.md` (decisões que mudam a especificação, como D1: estoque só Frente e Fundo), `pdv/01-arquitetura.md` e as telas citadas em `pdv/03-telas.md` e no FigCraft (`pdv/design/figcraft/Smoke House · PDV.figcraft`; PNGs em `pdv/design/figcraft/previas/`).
- Altere só as pastas que são suas (tabela "Papéis" em `pdv/05-orquestracao.md`). Precisa de mudança em outra pasta ou no contrato das RPCs? Peça ao orquestrador no relatório.
- Regra de dinheiro, estoque, numeração e senha fica no banco (RPC em transação). Datas e prazos sempre com a hora do servidor.
- Interface no padrão de `pdv/02-direcao-visual.md`, nos três tamanhos (390, 1180, 1440).

## Entrega
- Código + testes da sua parte + capturas em 390, 1180 e 1440 das telas tocadas.
- Relatório curto: o que fez por critério de aceite, o que ficou de fora e por quê, dúvidas de regra. Não diga que testou o que não rodou.
