# Tarefas · pdv-clientes

## CL-01 · Identificar cliente (F1) e cadastro rápido (F2)
Fase: F4 · Depende de: BD-01 · Telas: D13, D14 · Especificação: F1, F2
Aceite:
- [ ] Busca por CPF, CNPJ, telefone ou nome com ou sem pontuação; etiqueta do tipo digitado; sem nada, os últimos atendidos
- [ ] Só nome e telefone na lista; documento → "documento confere"; bolinho e aviso de aniversário em até 7 dias
- [ ] Ficha: etiquetas, cliente desde, compras, total, ticket médio, últimas 5, top 5, observação; "A prazo: limite · disponível"; bloqueado → "Vendas bloqueadas, fale com o gerente"
- [ ] F2: validações da especificação; Enter salva e usa na venda

## CL-02 · Histórico completo
Telas: D15
Aceite:
- [ ] Topo com indicadores e "compra a cada X dias"; filtros 30/90 dias, 12 meses, Tudo; compras por mês com itens, desconto, pagamento e operador; lateral com cadastro, 10 mais comprados, gasto por mês, "Como paga"

## CL-03 · Etiquetas automáticas
Especificação: Etiquetas automáticas
Aceite:
- [ ] VIP (R$ 1.000 em 30 dias ou Sempre VIP), Recorrente (1x por semana nas últimas 4), Sumido (>30 dias), Inativo (>60), Novo (mês atual), Aniversário (7 dias); regras editáveis no HOST; Inativo > Sumido; quem volta a comprar sai na hora

## CL-04 · HOST › Clientes, editar e excluir
Telas: H04, H05
Aceite:
- [ ] Quadros, filtros com contagem, busca em linha própria, tabela, ficha
- [ ] Editar com validações (e-mail, nome sem repetir, dígitos de CPF/CNPJ, nascimento no passado); "Descartar alterações?"
- [ ] Excluir: motivo + senha do administrador; "Não, manter cadastro" já selecionado; some do CRM e do F1 e sai da venda em andamento; vendas continuam; registro só de quem, quando e motivo

## CL-05 · Crédito do cliente
Especificação: Crédito do cliente
Aceite:
- [ ] Entradas: sobra de troca, devolução em crédito, estorno de venda paga com crédito, lançamento no caixa, ajuste no HOST; saídas: uso no pagamento e ajuste
- [ ] Ajustar crédito: senha do administrador, motivo obrigatório, não mexe no caixa, não retira mais que o saldo; todo movimento registrado
