# Orquestração: agente principal e subagentes

O trabalho é dividido entre **um orquestrador** e **subagentes especializados**. As definições ficam em `.claude/agents/` na raiz do repositório.

## Como rodar

- O orquestrador é a **sessão principal** do Claude Code, aberta na raiz do `smoke-e`. Comece com: *"Você é o orquestrador do PDV Smoke House. Siga `.claude/agents/pdv-orquestrador.md`."* Subagente não chama subagente, por isso o orquestrador não pode ser ele próprio um subagente.
- O orquestrador chama cada subagente pelo nome (`pdv-banco`, `pdv-venda`…) com o cartão da tarefa de `pdv/tarefas/`.
- Tarefas sem dependência entre si rodam em paralelo, cada uma num worktree próprio.

## Papéis

| Agente | Responde por | Pastas que pode alterar |
|---|---|---|
| **pdv-orquestrador** | Planeja, distribui, revisa, **valida o produto funcionando** contra a especificação, integra e decide. Única ponte com o usuário | `pdv/` (documentos e registro de decisões) |
| **pdv-design** | Direção visual, telas no FigCraft nos três tamanhos, revisão visual do que foi construído em **celular 390, tablet 1180 e computador 1440** | `pdv/02-direcao-visual.md`, `pdv/03-telas.md`, `~/Documents/figcraft/` |
| **pdv-banco** | Esquema, RLS, RPCs, numeração, hora do servidor, tempo real, `pg_cron`, migrações e dados de teste | `supabase/` |
| **pdv-venda** | Tela de venda do DAV e da NFC-e: busca, cupom, teclas, vendas simultâneas, pagamento, prazo no F3, pré-visualização do cupom | `src/apps/caixa/venda/` |
| **pdv-caixa** | Abrir e fechar caixa, sangria, suprimento, crédito lançado, cancelamentos, DAVs emitidos, troca, devolução, fechamento automático | `src/apps/caixa/movimentos/` |
| **pdv-clientes** | CRM: F1, cadastro rápido, histórico, etiquetas, crédito do cliente, HOST › Clientes, exclusão | `src/apps/*/clientes/` |
| **pdv-estoque** | Produtos, Frente e Fundo, entrada e saída, transferências, rastreio, importação de XML | `src/apps/host/estoque/` |
| **pdv-financeiro** | Venda a prazo, contas a receber, baixa, recibos, extrato, cobrança, contas a pagar, caixa geral | `src/apps/host/financeiro/` |
| **pdv-retaguarda** | HOST: início, caixas, configurações, formas de pagamento, usuários e permissões, autorização por senha, chamados, fornecedores, integrações, backup | `src/apps/host/` (exceto as pastas acima) |
| **pdv-relatorios** | Pré-visualização A4, PDF, Excel e todos os relatórios | `src/apps/host/relatorios/` |
| **pdv-fiscal** | NFC-e, contingência, DANFE, cancelamento, inutilização, IBS/CBS, calculadoras da Receita | `services/nfe-service/`, `supabase/functions/fiscal-*` |
| **pdv-dispositivos** | App instalado (Tauri), impressora térmica, gaveta, leitor, TEF, offline | `desktop/`, `src/lib/dispositivos/` |
| **pdv-qa** | Testes automáticos a partir das regras da especificação (unitários, RPC e ponta a ponta com Playwright nos três tamanhos) | `tests/` |

**Uma pasta, um dono.** Quem precisa mudar o que é de outro agente pede ao orquestrador, que encaminha. O contrato entre interface e banco (assinatura das RPCs e tipos gerados) é do `pdv-banco`. Mudança nele passa pelo orquestrador antes.

## Fluxo de uma tarefa

```
 cartão da tarefa ─▶ subagente constrói ─▶ pdv-qa escreve/atualiza testes ─▶ pdv-design revisa nas 3 larguras
        ▲                                                                              │
        └──────────── devolvido com achados ◀── orquestrador valida funcionando ◀──────┘
                                                        │ aprovado
                                                        ▼
                                                 integra e registra
```

1. **Cartão.** O orquestrador entrega o cartão (de `pdv/tarefas/`) com: objetivo, seção da especificação, telas do FigCraft, dependências, critérios de aceite.
2. **Construção.** O subagente entrega código + testes da própria parte + capturas de tela 390/1180/1440 + relatório (o que fez, o que ficou de fora, dúvidas).
3. **Testes.** O `pdv-qa` transforma cada critério de aceite em teste automático.
4. **Revisão visual.** O `pdv-design` compara com o FigCraft e com a checklist de [02-direcao-visual.md](02-direcao-visual.md). Achados vão como lista: tela, tamanho, problema, valor esperado.
5. **Validação funcional (orquestrador).** Ver abaixo. É o portão que decide.
6. **Integração.** O orquestrador junta, roda tudo e atualiza o registro da fase.

## Validação funcional pelo orquestrador

O orquestrador não confia no relatório do subagente: **usa o produto**. Para cada tarefa:

1. Sobe o app com o banco de teste (dados de agosto até hoje, numeração de DAV em ordem de data, como pede a especificação).
2. Percorre os **roteiros** da tarefa só com o teclado no computador, depois com toque no tablet e no celular (Playwright ou navegador), com dois terminais abertos quando a regra envolve outro terminal.
3. Confere cada critério de aceite e marca: passou, falhou (com passo a passo para reproduzir) ou não testável.
4. Roda os testes automáticos e a varredura de segurança.
5. Decide: **aprovado**, **aprovado com pendência registrada** ou **devolvido**.

Regras do portão:
- Regra de dinheiro, estoque, numeração ou senha que falha devolve a tarefa, sem exceção.
- Defeito só visual em um tamanho pode ser aprovado com pendência, se não impedir o uso.
- Nada vai para a loja sem passar pelo **portão da fase** (abaixo).

## Fases e portões

| Fase | Conteúdo | Portão |
|---|---|---|
| F0 Decisões | Respostas P1 a P9, validação da arquitetura | O orquestrador registra as respostas em `00-escopo-e-decisoes.md` |
| F1 Fundação | Banco, login, perfis e permissões, autorização por senha, terminais, hora do servidor, tempo real, configurações | Dois terminais logados veem um ao outro; senha errada recusada; ação autorizada grava quem autorizou |
| F2 Cadastros e estoque | Produtos, Frente/Fundo, entrada, saída, transferência, rastreio, XML, fornecedores | Rastreio de um produto bate com o saldo nos dois locais depois de 20 movimentos variados |
| F3 Frente de caixa | Abrir caixa, Caixa livre, busca, venda, F7/F8, pagamento, cupom, cancelamentos, DAVs emitidos, sangria, suprimento, fechamento | Um dia de loja simulado em dois terminais fecha os dois caixas sem diferença, e o fechamento automático das 23:59 funciona |
| F4 Clientes e trocas | CRM, etiquetas, crédito do cliente, troca, devolução | Troca com sobra vira crédito e é usada na venda seguinte; devolução de venda a prazo abate a parcela |
| F5 Prazo e financeiro | Venda a prazo, contas a receber, baixa parcial, recibos, desfazer, caixa geral | Exemplo da especificação (devido R$ 318,76, pago R$ 300,00, resta R$ 18,76) reproduzido exatamente |
| F6 Fiscal | NFC-e em homologação, contingência, IBS/CBS ([04-fiscal.md](04-fiscal.md)) | Roteiro fiscal completo em homologação, conferido pelo contador |
| F7 Relatórios e HOST | Relatórios, chamados, integrações, backup, e-commerce lendo o estoque | Vendas por período bate com a soma dos caixas |
| F8 Piloto | PNZ primeiro, LEM depois | Uma semana na PNZ sem divergência de caixa nem nota rejeitada sem tratamento |

Paralelismo: em F2 e F3, `pdv-estoque`, `pdv-venda` e `pdv-caixa` trabalham juntos depois que o `pdv-banco` publica as RPCs da fase. `pdv-design` e `pdv-qa` acompanham todas as fases. `pdv-fiscal` pode começar F6.1 e F6.7 (IBS/CBS) em paralelo à F2, porque o prazo de janeiro de 2027 corre.

## Relatório do orquestrador ao usuário

Ao fim de cada fase: o que foi aprovado, o que ficou pendente e por quê, decisões que precisam do usuário, e o link das capturas nos três tamanhos.
