# Inventário de telas

Fonte: Especificação do PDV Smoke House v1.2.02, com uma mudança: **o estoque tem só dois locais, Frente de loja e Fundo de loja** (ver [00-escopo-e-decisoes.md](00-escopo-e-decisoes.md)). Onde a especificação fala em Matriz, vale Fundo de loja.

Cada tela é desenhada em três tamanhos: **computador 1440 × 900**, **tablet 1180 × 820** (deitado) e **celular 390 × 844**. O arquivo FigCraft fica em `pdv/design/figcraft/Smoke House · PDV.figcraft`, com uma página por aplicativo e uma linha por tela (computador, tablet e celular lado a lado).

## Regras de adaptação

| | Computador | Tablet | Celular |
|---|---|---|---|
| Barra superior | Logo, terminal, os três aplicativos e "Usuário: nome" | Igual | Logo, terminal e "Usuário: nome". Os aplicativos vão para o menu ☰ |
| Rodapé | Teclas (F1, F3…) e situação do servidor | As teclas viram botões de toque com a tecla ao lado | Sem rodapé. Barra fixa embaixo com total e botão principal |
| Janelas | Centralizadas, com título, Esc e botões no rodapé | Igual | Folha que sobe de baixo, largura total |
| Lista + detalhe | Lado a lado | Lado a lado, colunas menos importantes saem | Lista. Tocar abre o detalhe |
| Tabelas | Todas as colunas, sem rolagem lateral | Tira GTIN e colunas de apoio | Linhas viram cartões de duas linhas |
| HOST | Menu lateral de 248 | Menu lateral de 216 | Menu no ☰ |

## Frente de caixa (DAV), cor verde

| Código | Tela | O que precisa mostrar |
|---|---|---|
| D01 | Abrir caixa | Terminal 01, usuário fixo do terminal já preenchido e só leitura, senha, fundo de troco sugerido (de HOST › Regras do caixa). Estado "Senha incorreta". |
| D02 | Caixa livre | "CAIXA LIVRE" grande, relógio com segundos, "Operador nome · data" acima. Dois botões pequenos à direita com ícone em quadradinho: Dicas e Fechar caixa. Barra de busca sem texto de exemplo. |
| D03 | Busca de produto | Lista em ordem alfabética com foto, nome, preço, estoque, ID, GTIN e unidade. Detalhes do produto escolhido ao lado. Seleção: fundo cinza claro e borda fina preta. |
| D04 | Venda em andamento | Cupom à esquerda (item, cadastro, descrição, sem código de barras), último item destacado. Barra de vendas (Venda 1, Venda 2…) acima do cupom. À direita: Último item com foto, Qtde itens e TOTAL bem grande. Botões Formas de pagamento (F3, "Finalizar a venda") e Cancelar cupom (F6, discreto). |
| D04b | Alerta de estoque baixo (P14) | A venda continua; faixa discreta acima do total: "Seda Zomo King Size Rosa ficou com 2 na frente · mínimo 6". Some na próxima leitura. |
| D05 | Produto sem estoque na frente | Aviso sobre a venda: "Sem estoque na frente de loja. Há 14 no fundo de loja: peça a reposição" (ou "Em falta na frente e no fundo"). Alerta de estoque baixo. Esc volta à busca com o texto selecionado. |
| D06 | Cancelar item | Busca com "-2". Janela Sim/Não "Cancelar o item" mostrando só o item: número, nome, quantidade × preço = total. |
| D07 | Formas de pagamento (F3) | Cliente (F1), total, forma + valor + Ok, pagamentos lançados (removíveis), desconto (F8), acréscimo, restante, troco e Finalizar. |
| D07b | Pagamento com crédito de troca (P11) | O Crédito de troca da venda aparece como primeiro pagamento lançado (ticket e itens devolvidos), o resto em outra forma; "Sobra da troca → crédito" no resumo. |
| D08 | Venda a prazo | PRAZO dentro do pagamento: limite e disponível do cliente, vencimento único / 2x / 3x, data do primeiro vencimento, parcelas com datas e valores. Aviso de parcela vencida (pede supervisor). |
| D09 | Senha do supervisor | Quem autoriza (só Administrador, Gerente, Supervisor de caixa) e a senha. Motivo do pedido no topo ("Desconto de 8% acima do limite de 5%"). |
| D10 | Pré-visualização do cupom DAV | Bobina com cabeçalho da loja, itens, cancelamentos, totais, forma de pagamento, quantidade de itens, observação e "PARABÉNS POR SUA COMPRA!". Imprimir ou Esc para Caixa livre. |
| D11 | Menu principal (F11) | Suprimento, Sangria, Troca, Devolução, Identifica cliente, Crédito do cliente, Observação no cupom, Nova venda, Trocar de venda, Alterar valor do item, Cancelar cupom, Configurações (supervisor). Setas e Enter. |
| D12 | Alterar valor do item (F10) | Pede o número do item e depois o novo preço unitário. Mostra o desconto que resulta e avisa quando passa do limite. |
| D13 | Identificar cliente (F1) | Busca por CPF, CNPJ, telefone ou nome, com etiqueta do que foi digitado. Lista com só nome e telefone ("documento confere"). Ficha ao lado: etiquetas, cliente desde, compras, total gasto, ticket médio, últimas 5 compras, top 5, observação, crédito, "A prazo: limite · disponível". Bolinho de aniversário. Botão Vender sem cliente. |
| D14 | Cadastro rápido (F2) | CPF ou CNPJ, telefone/WhatsApp, nome, nascimento, e-mail, cidade, estado (BA), aceita ofertas. Erros de validação nos campos. |
| D15 | Histórico completo do cliente | Topo com compras, total, ticket médio, itens, "compra a cada X dias", última compra. Filtros 30 dias / 90 dias / 12 meses / Tudo. Compras por mês. Lateral com cadastro, 10 mais comprados, gasto por mês (gráfico) e "Como paga". |
| D16 | DAVs emitidos | Filtros Todos / Finalizados / Cancelados / Importados / Devolvidos, busca, período (começa hoje). Tabela: número, hora, cliente, pagamento, vendedor, desconto, total e situação. Detalhe ao lado. Menu ⋯: Reimpressão, WhatsApp, Ticket para troca, Alterar forma de pagamento, Cancelar cupom. |
| D17 | Cancelar venda finalizada | Motivo (cliente desistiu, erro de lançamento, produto com defeito, outro + observação), depois senha do supervisor. Antes de confirmar: produtos voltam à frente, sai do histórico do cliente, dinheiro a devolver, crédito que volta, estorno na maquininha ou PIX. |
| D18 | Troca (P11) | Número do ticket (quando exigido) e itens devolvidos pelo valor pago com desconto. Gera o **Crédito de troca**, que entra na venda aberta e aparece no F3; os produtos novos são lançados na própria venda. A sobra vira crédito do cliente ao finalizar (exige cliente). |
| D19 | Devolução | Venda de origem, itens a devolver pelo valor pago com desconto, forma de reembolso (crédito pede cliente), autorização. Venda a prazo abate parcelas. |
| D20 | Sangria e suprimento | Valor + justificativa + Confirmar, com o caixa e o operador. |
| D20b | Sangria para pagar fornecedor (P9) | Destino "Pagamento a fornecedor", escolha da conta a pagar em aberto (fornecedor, nota, vencimento, valor), valor, gaveta depois e justificativa. A sangria dá baixa na conta. |
| D21 | Crédito do cliente no caixa | Cliente (CPF, CNPJ ou telefone), valor, forma em que recebeu, observação. Senha do administrador. |
| D22 | Fechamento de caixa | "Caixa de Arthur · aberto às 07:58 · 24/11/2026". Recebido por forma, vendido no DAV, vendido no NFC-e, recebido de clientes, devoluções, total, dinheiro na gaveta. Divergência (forma, valor contado, motivo). Comprovante ao lado. Bloqueio "Há venda em andamento". Aviso das 23:30. |
| D23 | Caixa fechado | "CAIXA FECHADO", nada pode ser lançado, botão Abrir caixa. |
| D24 | Dicas | O uso do caixa com as mesmas regras: teclas, "2*produto", "-1", vendas simultâneas. |

## Cupom fiscal (NFC-e), cor azul-petróleo

As telas de venda são as mesmas do DAV. Aqui só o que é próprio da nota.

| Código | Tela | O que precisa mostrar |
|---|---|---|
| N01 | Venda no cupom fiscal | Igual ao D04, com "CPF na nota" no cupom e a série/número da próxima NFC-e. |
| N02 | Emitindo e autorizada | Etapas: assinando, enviando à SEFAZ, autorizada (protocolo e chave). Imprime o DANFE sozinho. |
| N03 | DANFE NFC-e | Bobina 80 mm: emitente, itens, totais, forma de pagamento, tributos aproximados (Lei 12.741), consumidor, chave de acesso, QR Code, protocolo. |
| N04 | Notas emitidas | Filtros Autorizadas / Canceladas / Em contingência / Rejeitadas, série e número, chave, situação. Menu: reimprimir, enviar XML, cancelar, consultar na SEFAZ. |
| N05 | Contingência | Sem resposta da SEFAZ: a nota sai em contingência offline (tpEmis 9), DANFE impresso na hora, fila de transmissão com prazo de 24 h. |
| N06 | Cancelar NFC-e | Motivo com pelo menos 15 caracteres, prazo restante, senha do supervisor, evento registrado. |
| N08 | Importar DAV no NFC-e (P1, P12) | DAVs do caixa sem nota, busca por número ou cliente, detalhe do escolhido (cliente, CPF, itens, pagamentos, total) e a série e número que a NFC-e vai receber. O DAV passa a "Importado". Também aparece como "Importar no NFC-e" no menu ⋯ dos DAVs emitidos. |
| N07 | Rejeição da SEFAZ | Código e mensagem da rejeição em português claro, o que corrigir (ex.: NCM inválido no produto) e o número que fica para inutilizar. |

## Retaguarda (HOST), cor azul-petróleo escuro

| Código | Tela | O que precisa mostrar |
|---|---|---|
| H01 | Entrar no HOST | Usuário e senha. Aviso de chamados pendentes depois de entrar. |
| H02 | Início | Cartão Hoje (vendido, número de vendas, caixas abertos, produtos para repor), vendas por forma de pagamento, chamados pendentes, botão Etiquetas. |
| H03 | Caixas | Caixas do dia e os abertos: terminal, operador, abertura, fechamento, vendido, situação. Conferência por forma (sistema × informado × diferença). Reimprimir comprovante. Desfazer divergência (mesmo dia). |
| H04 | Clientes | Quadros (ativos, novos no mês, recorrentes, vendas identificadas hoje), filtros arredondados com contagem, busca em linha própria, tabela e ficha ao lado. |
| H05 | Editar cliente | Identificação, contato, relacionamento (Sempre VIP, Bloquear vendas, observação). Crédito do cliente com movimentos e Ajustar crédito. Venda a prazo com limite, em aberto, disponível, parcelas. |
| H06 | Estoque · Frente de loja | Abas Frente de loja e Fundo de loja (sem "Todos"). Lista: código, produto com categoria e código de barras, custo, venda, margem, estoque/mínimo, cadastro, situação. Filtros Todos / Para repor / Inativos. Botões Entrada, Saída, Transferir, Importar XML. |
| H07 | Transferir | Do estoque aberto para o outro (Fundo → Frente ou Frente → Fundo). Filtro "O destino precisa", lista com quantidades, Transferir. |
| H08 | Cadastro de produto | Código, cadastrado por, produto ativo. Identificação, preço e margem (custo, margem, venda, lucro, markup, atacado, desconto máximo), estoque (mínimos de frente e fundo), fiscal (NCM, CEST, CFOP, origem, CSOSN, cClassTrib e CST do IBS/CBS), foto, histórico de custo com gráfico. |
| H09 | Entrada e saída manual | Produto, quantidade, motivo, estoque antes → depois, confirmação com o nome do estoque. |
| H10 | Transferências | Período, quadros (transferências, unidades, valor a custo, itens desfeitos), busca e rota, lista que abre os produtos, Desfazer, Romaneio. |
| H11 | Rastrear produto | Linha do tempo entre Frente e Fundo: vendas, cancelamentos, trocas, devoluções, transferências, entradas e saídas, XML, estoque inicial. |
| H12 | Importar XML de compra | Fornecedor, número, data, valor, itens ligados por código de barras ou código do fornecedor, itens sem ligação, destino (Fundo já marcado), conta a pagar com vencimento. |
| H13 | Contas a receber | Quadros (em aberto, vencido, vence em 7 dias, recebido em 30 dias), filtros, tabela de clientes a prazo. |
| H14 | Ficha do cliente a prazo | Limite, em aberto, vencido, disponível. Abas Parcelas, Compras a prazo, Pagamentos e recibos. Cobrar no WhatsApp, Extrato, Limite e bloqueio. |
| H15 | Dar baixa | Parcelas marcadas, valores de hoje (multa 2%, juros 1% a.m. por dia, desconto, dispensar), valor pago parcial e como fica cada parcela, várias formas. |
| H16 | Recibo | Por parcela: compra, produtos, "PAGO AGORA: PARCELA 1 DE 3", quanto falta, multa e juros, forma, saldo devedor. "SUBSTITUI O RECIBO Nº". |
| H17 | Formas de pagamento | Lista com tipo, nome no caixa, maquininha ou conta, taxa, recebe em, troco, parcelamento, ativa. Janela Nova forma de pagamento. PRAZO e Crédito do cliente como formas fixas. |
| H18 | Configurações | Empresa (razão social, fantasia, CNPJ, IE, regime, tabela IBPT), Regras do caixa, Equipamentos, Cópia de segurança. Um botão Salvar alterações. |
| H19 | Usuários e permissões | Usuários com perfil, terminal fixo e situação. Perfis e funções liberadas por perfil e por usuário. |
| H20 | Chamados | Abertos (quadro ou lista, busca, categoria) e Concluídos. |
| H21 | Fornecedores | Lista com busca, Novo e Editar (razão social, CNPJ, contato, telefone, e-mail, cidade, UF). |
| H22 | Integrações | Cartões: Central do fornecedor, Central do cliente, PIX, Envio para a contabilidade, Backup na nuvem, Notas fiscais (MD-e). |
| H23 | Relatórios | Categorias e relatórios com período e operador. |
| H24 | Pré-visualizar relatório | Folha A4 paginada, zoom, "1 de 3", Imprimir, PDF, Excel. |
| H25 | Fiscal | Certificado A1 (validade), CSC por loja, série da NFC-e por terminal, ambiente (homologação/produção), regime e opção IBS/CBS, situação da tabela de cClassTrib, contingência e inutilização. |
