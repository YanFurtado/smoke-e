# Tarefas · pdv-venda

## VE-01 · Moldura do caixa e Caixa livre
Fase: F3 · Depende de: BD-01, BD-02 · Especificação: Visão geral, Regras gerais de interface, Caixa livre · Telas: D02
Aceite:
- [ ] Topo com logo verde, "Terminal 01" e só "Usuário: nome"; navegação DAV / NFC-e / HOST; rodapé só com teclas e situação do servidor
- [ ] "CAIXA LIVRE", relógio com segundos (hora do servidor sincronizada), "Operador nome · data"; botões Dicas e Fechar caixa (leva à aba Fechamento)
- [ ] Esc fecha qualquer janela e volta à anterior; confirmações Sim/Não aceitam S/Enter e N/Esc

## VE-02 · Busca de produto
Telas: D03, D05 · Especificação: Barra de busca, Estoque no caixa
Aceite:
- [ ] "essencia" encontra "Essência"; código de barras e cadastro; "6264" encontra "006264"; inativo não aparece
- [ ] Lista alfabética com foto, nome, preço, estoque, ID, GTIN e unidade; detalhes ao lado; ↑↓ Home End PgUp PgDn; clique duplo lança
- [ ] Enter lança direto quando código de barras ou cadastro bate exatamente
- [ ] Sem estoque na frente: aviso com "há N no fundo de loja, peça a reposição" ou "em falta"; produto não entra; Esc volta à busca com o texto selecionado
- [ ] P14: produto vendido que chega ao mínimo mostra a faixa "<produto> ficou com N na frente · mínimo M" acima do total, sem interromper; some na próxima leitura (tela D04b)

## VE-03 · Cupom, quantidade e cancelamento de item
Telas: D04, D06 · Especificação: Quantidade e cancelamento de item, Cupom na tela
Aceite:
- [ ] "2*produto" lança 2; "0,5*" e "0*" recusados com aviso
- [ ] "-2" + Enter abre Sim/Não "Cancelar o item" só com o item 2; sem senha (a não ser que a configuração ligue); itens renumerados 001, 002…
- [ ] Cupom sem código de barras; último item destacado; Último item com foto; Qtde itens; TOTAL grande

## VE-04 · Vendas simultâneas
Telas: D04 · Especificação: Vendas simultâneas (F7 e F8)
Aceite:
- [ ] F7 guarda a atual e abre outra; máximo 4; não abre se a atual está vazia; F8 e clique na barra trocam
- [ ] Cada venda guarda itens, cliente, desconto, observação e crédito de troca; DAV e NFC-e não se misturam; trocar de terminal não mistura

## VE-05 · Formas de pagamento e finalização
Telas: D07, D09, D10 · Especificação: Pagamento e finalização da venda
Aceite:
- [ ] F1 e F8 dentro do pagamento; forma sem troco não aceita valor acima do restante; remover pagamento
- [ ] Desconto total acima do limite pede senha do supervisor ao finalizar; Esc com pagamentos pergunta "Sair do pagamento?"
- [ ] Crédito do cliente só aparece com cliente com saldo e não passa do saldo
- [ ] Ao finalizar, pré-visualização do cupom DAV; Esc volta ao Caixa livre; próxima venda começa sem cliente; venda entra no histórico do cliente
- [ ] P11: "Crédito de troca" da venda aparece no F3 como forma; sobra exige cliente e vira crédito ao finalizar

## VE-06 · Venda a prazo no F3
Telas: D08 · Especificação: Vender a prazo
Aceite:
- [ ] Recusa sem cliente, bloqueado, sem limite ou acima do disponível (mostra quanto pode); parcela vencida pede supervisor
- [ ] Único ou 2x/3x, 1º vencimento depois de hoje até 120 dias; um só PRAZO por venda; cada parcela vira título

## VE-07 · Teclas, menu e Dicas
Telas: D11, D12, D24 · Especificação: Teclas de atalho e Menu principal
Aceite:
- [ ] F1, F3, F6, F7, F8, F9, F10, F11, Esc conforme a tabela; F2, F4, F5 sem função; no navegador o botão ☰ abre o menu
- [ ] F10 pede número do item e novo preço; abaixo do limite pede senha na hora
- [ ] Menu com os 12 itens; Configurações pede supervisor
