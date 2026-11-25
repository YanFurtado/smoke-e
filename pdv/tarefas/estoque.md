# Tarefas · pdv-estoque

Decisão D1: dois locais por loja, **Frente de loja** e **Fundo de loja**. O caixa vende só da Frente.

## ES-01 · Lista de produtos e abas por local
Fase: F2 · Depende de: BD-03 · Telas: H06 · Especificação: Lista de produtos, Estoques por local
Aceite:
- [ ] Uma aba por local (Frente, Fundo), sem aba "Todos"; cada aba mostra só a quantidade daquele local e os abaixo do mínimo
- [ ] Colunas: código, produto (categoria e código de barras embaixo), custo, venda, margem, estoque/mínimo, cadastro, situação (Normal, Repor, Inativo); filtros com contagem; busca por código, EAN, referência ou descrição

## ES-02 · Cadastro de produto
Telas: H08 · Especificação: Cadastro do produto, Histórico de custo
Aceite:
- [ ] Código automático; "Cadastrado em … por …"; produto ativo; descrição sem repetir
- [ ] Código de barras: botão Gerar com prefixo 2; 8, 12, 13 ou 14 dígitos; dígito verificador; sem repetir
- [ ] Custo, margem e venda se calculam entre si; lucro e markup; atacado ≤ venda; venda ≥ custo; desconto máximo 0–100%; vírgula ou ponto
- [ ] Estoque inicial só no cadastro novo (inteiro, local escolhido); mínimos de frente e fundo; depois, só leitura
- [ ] Fiscal: NCM (8 dígitos se preenchido), CEST, CFOP, origem, CSOSN, cClassTrib e CST do IBS/CBS; categoria sugere NCM
- [ ] Foto: acrescentar, trocar, remover; aparece no caixa; histórico de preço e de custo com gráfico e 3 últimos registros
- [ ] P5: NCM 2402/2403 → CSOSN 500, CFOP 5405 e CEST (segmento 04) obrigatório; acessórios → CSOSN 102, CFOP 5102; a categoria preenche o padrão

## ES-03 · Entrada e saída manual
Telas: H09
Aceite:
- [ ] Motivos da especificação; "Outro" exige observação; saída ≤ saldo do local; custo opcional na entrada vai para o histórico
- [ ] Confirmação mostra o nome do estoque; Voltar mantém o formulário

## ES-04 · Transferir e Transferências
Telas: H07, H10
Aceite:
- [ ] Fundo → Frente e Frente → Fundo; filtro "O destino precisa"; muda na hora nos dois locais; sem aprovação
- [ ] Aba Transferências: período (não aceita futuro), quadros, busca, rota; desfazer itens ou tudo com motivo e senha do administrador; não desfaz se o produto já saiu do destino; romaneio e relatório

## ES-05 · Rastrear produto
Telas: H11
Aceite:
- [ ] Linha do tempo com vendas, vendas canceladas, trocas, devoluções, transferências e desfeitas, entradas e saídas, XML e estoque inicial; a soma bate com os saldos

## ES-06 · Importar XML de compra
Telas: H12 · Especificação: Importar XML de compra
Aceite:
- [ ] Lê fornecedor, número, data, valor e itens; liga por código de barras ou código do fornecedor usado antes
- [ ] Item sem ligação: escolher, cadastrar novo ou não dar entrada; quantidade fracionada bloqueia até sair
- [ ] Destino Fundo de loja já marcado; atualiza custo com histórico; cria ou atualiza fornecedor; não aceita a mesma nota duas vezes; cria conta a pagar com vencimento editável; tudo numa transação
