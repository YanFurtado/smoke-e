# Tarefas · pdv-qa

## QA-01 · Base de testes
Fase: F1
Aceite:
- [ ] Unitários (Vitest), RPC (pgTAP ou testes SQL) e ponta a ponta (Playwright) em 390, 1180 e 1440
- [ ] Banco de teste recriado a cada rodada a partir de BD-08; relógio do servidor controlável nos testes (meia-noite, mesmo dia, vencimentos)

## QA-02 · Um teste por critério de aceite
Contínua
Aceite:
- [ ] Cada linha "Aceite" dos cartões tem um teste com o ID do cartão no nome
- [ ] Roteiros com dois terminais (reserva de estoque, numeração, venda aberta bloqueando fechamento)

## QA-03 · Regressão fiscal
Fase: F6
Aceite:
- [ ] XMLs de exemplo validados no XSD e no `/xml/validate` da calculadora da Receita a cada atualização da tabela ou da biblioteca
