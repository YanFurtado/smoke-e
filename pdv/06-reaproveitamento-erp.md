# O que reaproveitar do erp-system

O `erp-system` (em `~/Documents/github/erp-system`) é o ERP "X-Life", de outro cliente (suplementos, Petrolina-PE e Juazeiro-BA). Ele **não** é a base do PDV Smoke House, mas tem partes prontas que valem a cópia. Nada é compartilhado em produção: a Smoke House tem banco próprio.

## Aproveitar

| Parte | Onde está | Uso no PDV |
|---|---|---|
| Fila de vendas offline (IndexedDB, idempotente por `uuid_local`, cifrada) | `src/lib/offline/` e migration `052_fase5_pdv_offline.sql` | Base da contingência do caixa |
| Leitor de código de barras USB e câmera | `use-leitor-usb.ts`, `components/leitor-codigo-barras.tsx` | Busca do caixa |
| Pagamento misto | `components/pagamentos-venda.tsx`, `erp_venda_pagamentos` (085/086) | Ponto de partida do F3 (ajustar às regras da especificação) |
| Login real por CPF, limite de tentativas | migrations 121, 122, edge `erp-login` | Login do HOST e abertura de caixa |
| Permissões por papel e por usuário, auditoria por gatilho | 042, 073, 045 | Base de perfis e permissões (faltam Supervisor de caixa, Faturista e a autorização por senha de terceiro) |
| Importação de XML de compra (casa EAN e cProd, cria fornecedor, gera contas a pagar, não repete a chave) | `pages/compras.importar-nfe.tsx`, `lib/nfe-xml-parser.ts` | H12. Mover as gravações para uma RPC em transação e acrescentar local de destino e bloqueio de quantidade fracionada |
| Cancelamento de venda com travas no banco | `099_cancelar_venda.sql`, `lib/cancelar-venda.ts` | D17, acrescentando motivos fixos, senha do supervisor e "o que acontece" |
| Resumo do caixa e da gaveta | `vw_caixa_resumo` (082), `lib/fechamento-por-forma.ts` | D22 |
| Serviço de NF-e/NFC-e | `services/nfe-service`, edges `erp-emitir-nfe`, `erp-danfe`, `erp-eventos-fiscais` | Ver [04-fiscal.md](04-fiscal.md) |

## Não aproveitar (diverge da especificação)

| Parte | Por quê |
|---|---|
| Tela `pdv.tsx` (3.264 linhas) | Usa as teclas do sistema anterior (Excellent: F10 finaliza, F8 cancela item, F5 localiza), que batem de frente com a especificação. Sem "2*", "-n", F7/F8, menu F11, Caixa livre. Reescrever |
| Estoque `UNIQUE(produto_id, loja_id)` | Não tem local. O PDV precisa de Frente e Fundo |
| Crediário com juros Price (até 12x, 2,5% a.m.) | A especificação pede 1 a 3x sem juros de financiamento, multa 2% e juros de mora 1% a.m. por dia, baixa parcial. E no ERP "limite 0" é "sem limite"; na especificação é "não compra a prazo" |
| Formas de pagamento fixas no enum (com boleto, cheque, promissória) | A especificação quer formas configuráveis e sem boleto e carnê |
| Fechamento indireto pelo HOST e operador digitando sempre o contado | A especificação: fecha só pelo DAV, valores puxados do sistema, fechamento cego desligado |
| Numeração `SERIAL` global | A especificação: sequência por loja |
| Data de abertura do caixa vinda do navegador | Regra de prazo tem de usar a hora do servidor |
