# Tarefas · pdv-caixa

## CX-01 · Abrir caixa
Fase: F3 · Depende de: BD-02, BD-05 · Telas: D01, D23 · Especificação: Terminais e caixas
Aceite:
- [ ] Usuário fixo do terminal já preenchido e só leitura; senha; fundo de troco sugerido pelas Regras do caixa
- [ ] "Senha incorreta" não entra; usuário inativo não entra; cria caixa novo para aquele usuário naquele terminal
- [ ] Caixa fechado mostra "CAIXA FECHADO" e não deixa lançar produto, pagar, sangria, suprimento, troca, devolução nem crédito

## CX-02 · Sangria, suprimento e crédito lançado
Telas: D20, D21 · Especificação: Sangria e suprimento, Crédito do cliente lançado no caixa
Aceite:
- [ ] Valor + justificativa; marcado no caixa com data e operador; entra no caixa geral e no fechamento
- [ ] Crédito lançado pede senha do administrador; vira saldo do cliente e entra no fechamento daquele caixa

## CX-03 · Cancelar cupom e venda finalizada
Telas: D17 · Especificação: Cancelar cupom (F6), Cancelar venda finalizada
Aceite:
- [ ] F6 Sim/Não "Todos os itens foram cancelados. Deseja cancelar o cupom?"; Sim registra cancelado e volta ao Caixa livre
- [ ] Venda finalizada: motivo → senha do supervisor → resumo do que acontece (estoque volta à frente, sai do histórico, dinheiro a devolver, crédito que volta, estorno de cartão/PIX)
- [ ] Prazo com parcela paga: bloqueado até desfazer as baixas; venda com devolução não cancela

## CX-04 · DAVs emitidos
Telas: D16 · Especificação: DAVs emitidos
Aceite:
- [ ] Filtros, busca por número/cliente/produto, período começando hoje; todas as colunas sem rolagem lateral
- [ ] Menu ⋯ / clique direito com setas: Reimpressão, WhatsApp (valida DDD + número), Ticket de troca (sem preços, "T" + número, data limite), Alterar forma de pagamento (mesmo total, supervisor, registrado), Cancelar cupom
- [ ] P1/P12: "Importar no NFC-e" transforma o DAV finalizado em NFC-e (mesmo cliente, itens e pagamentos); o DAV fica "Importado", com Alterar forma de pagamento e Cancelar cupom desativados; o fechamento mostra quantos DAVs ficaram sem nota

## CX-05 · Troca e devolução
Telas: D18, D19 · Especificação: Troca e devolução
Aceite:
- [ ] Regras de Configurações › Troca e devolução (prazo, senha, volta ao estoque, reembolso, sobra, exigir ticket)
- [ ] Valor pago de fato com desconto; venda a prazo abate parcelas; sobra vira crédito com cliente identificado
- [ ] Troca com crédito e sem produto novo: F6 oferece desfazer; produto volta à frente e aparece no rastreio
- [ ] P11: a janela Troca registra só os devolvidos e gera o Crédito de troca na venda aberta; os produtos novos são lançados na venda (tela D18)
- [ ] P10: devolução de venda a prazo abate a parcela em aberto mais nova

## CX-06 · Fechamento de caixa
Telas: D22 · Especificação: Fechamento de caixa e conferência
Aceite:
- [ ] Só pelo DAV; venda aberta bloqueia; valores puxados do sistema; fechamento cego opcional
- [ ] Conteúdo: por forma, DAV, NFC-e, recebido de clientes, devoluções, total, gaveta = fundo + suprimentos − sangrias − devoluções em dinheiro; PRAZO líquido
- [ ] Divergência com forma, valor contado, motivo, observação, quem e quando; sai no comprovante
- [ ] Aviso a partir das 23:30; comprovante no modelo com as seções da especificação; Relatório de fechamento em cupom ou A4
- [ ] P13: pagamento com Crédito do cliente aparece em "Recebido por forma" e não soma na gaveta; crédito lançado em dinheiro soma em Dinheiro e na gaveta
