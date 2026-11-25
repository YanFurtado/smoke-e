# Arquitetura

Proposta para o orquestrador validar na Fase 0. Sempre que der, aproveita o que já funciona no `erp-system` (ver [06-reaproveitamento-erp.md](06-reaproveitamento-erp.md)).

## Visão geral

```
 Terminal 01 / 02 (navegador ou app instalado)         Servidor
 ┌──────────────────────────────┐                ┌──────────────────────────────────┐
 │ DAV · NFC-e · HOST (React)   │── HTTPS/WS ───▶│ Supabase: Postgres, Auth,        │
 │ fila offline (IndexedDB)     │                │ Realtime, Storage, Edge Functions│
 │ impressão térmica / gaveta   │                │ pg_cron (meia-noite, retries)    │
 └──────────────┬───────────────┘                └──────────┬───────────────────────┘
                │ local                                     │ rede interna
        impressora ESC/POS, gaveta,               ┌─────────▼──────────┐  ┌────────────────────────┐
        leitor de código, TEF                     │ nfe-service (PHP,  │  │ calculadora RTC (Java, │
                                                  │ sped-nfe): XML,    │  │ Receita) a partir de   │
                                                  │ assinatura, SEFAZ  │  │ 2027, só no servidor   │
                                                  └────────────────────┘  └────────────────────────┘
```

| Camada | Escolha | Por quê |
|---|---|---|
| Interface | React 18 + TypeScript + Vite + Tailwind, componentes próprios seguindo [02-direcao-visual.md](02-direcao-visual.md) | Mesmo stack do `erp-system`, que já tem PDV, leitor de código e fila offline |
| App instalado | Tauri (Windows) empacotando a mesma interface | A especificação diferencia "navegador" e "sistema instalado" (F11). O app instalado dá impressão ESC/POS direta, gaveta e tela cheia |
| Dados | Supabase (Postgres 15+, RLS, RPCs em PL/pgSQL) | Regras de dinheiro e estoque ficam no banco, em transação |
| Tempo real | Supabase Realtime (Postgres changes + Presence) | Vendas abertas entre terminais, estoque reservado, caixa aberto |
| Hora | `now()` do Postgres em toda regra de prazo | Especificação: nunca a hora do computador do caixa |
| Agendamento | `pg_cron` | Fechamento automático à meia-noite (23:59), retransmissão de NFC-e, etiquetas de cliente |
| Fiscal | `nfe-service` do `erp-system` (PHP 8 + nfephp-org/sped-nfe), atrás de uma Edge Function | Já monta, assina e transmite NFC-e modelo 65 |
| Tributos da reforma | Calculadoras RTC da Receita (Java) como serviço interno a partir de 2027; tabelas sincronizadas no banco | Ver [04-fiscal.md](04-fiscal.md) |
| Arquivos | Storage privado: certificado A1, XML e DANFE, fotos de produto, backups | |

## Princípios

1. **Toda regra de negócio que mexe em dinheiro, estoque ou numeração roda numa RPC do banco, numa transação.** A interface nunca grava em várias tabelas em sequência.
2. **Quem fez e quem autorizou** ficam gravados em toda ação que pede senha (tabela `autorizacoes`, ligada ao registro afetado).
3. **Nada é apagado.** Cancelar, desfazer e excluir marcam o registro e guardam motivo, usuário e data. A exceção é a exclusão de cliente, que guarda só quem excluiu, quando e o motivo (regra da especificação).
4. **Cada movimento carrega o caixa em que foi feito.** O fechamento soma só o que é daquele caixa.
5. **Datas do servidor.** O cliente nunca manda `data_abertura`, `criado_em` ou "hoje".

## Modelo de dados (resumo)

| Grupo | Tabelas |
|---|---|
| Empresa | `lojas` (PNZ, LEM: CNPJ, IE, UF, IBGE), `terminais` (número, loja, usuário fixo, série NFC-e), `configuracoes` (por loja: regras do caixa, troca e devolução, prazo, etiquetas) |
| Acesso | `usuarios`, `perfis` (Administrador, Gerente, Supervisor de caixa, Operador de caixa, Faturista), `perfil_permissoes`, `usuario_permissoes`, `autorizacoes`, `acessos` (log do HOST) |
| Produtos | `produtos` (fiscal: NCM, CEST, CFOP, origem, CSOSN, cClassTrib, CST IBS/CBS; foto; atacado; desconto máximo), `categorias`, `marcas`, `historico_preco`, `historico_custo`, `fornecedores`, `produto_fornecedor_codigo` |
| Estoque | `estoque_saldos` (produto, loja, **local: frente \| fundo**, quantidade, mínimo), `estoque_movimentos` (tipo, local, quantidade, saldo depois, origem, documento, caixa, usuário), `transferencias` e `transferencia_itens` (com desfeito), `reservas` (venda aberta × produto) |
| Caixa | `caixas` (terminal, usuário, abertura, fechamento, fundo de troco, fechado_automaticamente), `movimentos_caixa` (sangria, suprimento, crédito lançado), `divergencias` (com desfeita_em) |
| Vendas | `vendas` (tipo dav \| nfce, número da loja, situação aberta \| finalizada \| cancelada, caixa, cliente, observação, desconto, acréscimo), `venda_itens` (com cancelados), `venda_pagamentos`, `cancelamentos`, `trocas`, `devolucoes`, `tickets_troca` |
| Clientes | `clientes` (bloqueado, sempre VIP, limite a prazo, bloqueado a prazo), `cliente_etiquetas` (calculadas), `credito_movimentos`, `clientes_excluidos` (só quem, quando, motivo) |
| Prazo | `titulos` (parcela, venda, vencimento, valor, pago, multa paga), `baixas` e `baixa_parcelas` (com desfeita), `recibos` (substitui / substituído por) |
| Financeiro | `formas_pagamento` (tipo, conta, taxa, recebe em, troco, parcela, ativa), `contas` (Caixa da loja, PIX, banco), `lancamentos` (caixa geral, fluxo), `contas_pagar` |
| Fiscal | `nfce` (série, número, chave, protocolo, situação, tpEmis, XML e DANFE no Storage), `eventos_fiscais` (cancelamento, inutilização), `tabelas_rtc` (cClassTrib, CST, versão) |
| Outros | `chamados`, `integracoes`, `backups` |

## Numeração

- **DAV:** uma sequência por loja (`seq_dav_pnz`, `seq_dav_lem`), tirada na finalização dentro da RPC. Nunca repete.
- **NFC-e:** por série; **uma série por terminal**, para a contingência offline de um terminal não colidir com o outro (confirmar com P8 em [00-escopo-e-decisoes.md](00-escopo-e-decisoes.md)).
- **Ticket de troca:** "T" + número da venda.

## Tempo real entre terminais

- Canal por loja. Cada venda aberta é uma linha em `vendas` com situação "aberta", gravada a cada item lançado.
- `reservas` = soma das quantidades em vendas abertas de todos os terminais. O estoque disponível para vender é `frente − reservado`.
- Presence mostra quem está em qual terminal; o fechamento verifica "Há venda em andamento" no servidor, não na tela.

## Offline

- Reaproveitar a fila do `erp-system` (`src/lib/offline/fila-vendas.ts`): venda com `uuid_local`, idempotente, cifrada.
- Offline, o caixa continua vendendo só o que estava na frente no último sincronismo e **não** permite: abrir ou fechar caixa, cancelar venda finalizada, troca, devolução, prazo e crédito do cliente. Essas regras precisam do servidor.
- No NFC-e, offline = contingência (tpEmis 9) com XML assinado e DANFE impresso na hora. Ver [04-fiscal.md](04-fiscal.md).

## Segurança e LGPD

- RLS por loja e por permissão em todas as tabelas. Funções `SECURITY DEFINER` só nas RPCs, com `search_path` fixo.
- A senha do certificado é cifrada com chave guardada fora do banco (no `erp-system` há uma chave padrão gravada no código; aqui ela é obrigatória na instalação).
- CPF e telefone aparecem só onde a especificação manda (no F1, só nome e telefone).
- Backup diário automático, mais o "Fazer backup" do HOST (sem senhas).
- Rodar a skill `varredura-seguranca` antes de cada publicação.
