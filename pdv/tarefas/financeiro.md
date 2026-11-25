# Tarefas · pdv-financeiro

## FI-01 · Contas a receber e ficha do cliente
Fase: F5 · Depende de: BD-06 · Telas: H13, H14
Aceite:
- [ ] Só clientes a prazo; quadros Em aberto, Vencido, Vence em 7 dias, Recebido em 30 dias; filtros; busca; ↑↓ Enter
- [ ] Ficha: limite, em aberto, vencido, disponível; abas Parcelas, Compras a prazo, Pagamentos e recibos; Cobrar no WhatsApp, Extrato, Limite e bloqueio (senha do administrador; limite abaixo do devido aceito com aviso)

## FI-02 · Dar baixa
Telas: H15
Aceite:
- [ ] Sempre na data de hoje; multa e juros calculados; desconto e "Dispensar multa e juros" pedem supervisor
- [ ] Pagamento parcial mostra como fica cada parcela; várias formas somando exatamente o pago; dinheiro no Caixa da loja, PIX na conta PIX, cartão no banco

## FI-03 · Recibo, desfazer baixa, extrato e cobrança
Telas: H16
Aceite:
- [ ] Recibo com compra, produtos, "PAGO AGORA: PARCELA X DE Y", quanto falta ou "COMPRA QUITADA", multa e juros, forma, saldo devedor; reimpressão com os valores do dia
- [ ] Desfazer só no mesmo dia, com motivo e senha do administrador; várias parcelas voltam juntas; "SUBSTITUI / SUBSTITUÍDO PELO RECIBO Nº"
- [ ] Extrato em impressão, PDF, Excel e WhatsApp; cobrança com mensagem editável

## FI-04 · Caixa geral, contas a pagar, DRE
Especificação: Relatórios (Financeiro)
Aceite:
- [ ] Cada caixa fechado lança no caixa geral e no fluxo um registro por forma; sangria vai para a conta do banco (P9 em aberto)
- [ ] Contas a pagar (inclusive as do XML); DRE por competência sem imposto duplicado
- [ ] P9: sangria com destino "Pagamento a fornecedor" pede a conta a pagar e dá baixa nela
