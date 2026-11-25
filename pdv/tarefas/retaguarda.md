# Tarefas · pdv-retaguarda

## RT-01 · Login do HOST, Início e Caixas
Fase: F1/F3 · Telas: H01, H02, H03
Aceite:
- [ ] Login por usuário; telas sem permissão não aparecem; acessos registrados; aviso de chamados pendentes
- [ ] Início: cartão Hoje com dados reais; itens que dependem do fiscal com "Aguarda integração fiscal"; Etiquetas de preço
- [ ] Caixas só leitura: dias anteriores nunca aparecem abertos; conferência por forma; comprovante abre direto a impressão; desfazer divergência no mesmo dia com permissão; soma do Vendido bate com Vendas por período

## RT-02 · Configurações
Telas: H18 · Especificação: Configurações do caixa, HOST › Empresa, Regras do caixa, Equipamentos, Cópia de segurança
Aceite:
- [ ] Empresa com CNPJ conferido; Regras do caixa com todos os campos; Equipamentos; Fazer backup baixa arquivo sem senhas
- [ ] Um só Salvar alterações; erro dentro da seção; Configurações do caixa (DAV) continuam existindo com senha do supervisor
- [ ] P1: Regras do caixa com "Importar o DAV no NFC-e ao finalizar" (desligado por padrão)

## RT-03 · Formas de pagamento
Telas: H17
Aceite:
- [ ] Tipo ajusta o resto (Crédito liga parcelamento e 30 dias); validações da especificação; aparece na hora no F3 e na baixa; Ativa mostra/esconde; PRAZO e Crédito do cliente fixas; sem boleto e carnê

## RT-04 · Usuários e permissões
Telas: H19
Aceite:
- [ ] Nome sem repetir, perfil, terminal fixo, senha mínimo 4 dígitos (em branco mantém), ativo; renomear atualiza caixas, vendas e relatórios
- [ ] Permissões por perfil e por usuário; função sem permissão pede senha de quem tem; quem tem passa direto

## RT-05 · Chamados, fornecedores, integrações
Telas: H20, H21, H22
Aceite:
- [ ] Chamados: quem abre para quem, categoria, data; cada um vê os seus; Abertos em quadro ou lista; Concluídos paginado com gráfico e relatório; F11 do DAV abre chamado
- [ ] Fornecedores com CNPJ conferido e sem repetir; excluir tira dos produtos
- [ ] Integrações com Configurar que muda a situação do cartão

## ECO-01 · E-commerce lendo o PDV
Fase: F7 · Depende de: P6, P7
Aceite:
- [ ] A vitrine lê catálogo, preço, foto e estoque do local definido em P6; pedido do site reserva e baixa estoque pelo mesmo RPC do PDV
- [ ] P6: o site vende da Frente de loja; o pedido entra como venda aberta e reserva o estoque
- [ ] P7: boleto sai do site
