# Tarefas · pdv-banco

## BD-01 · Esquema base, lojas, terminais e configurações
Fase: F1 · Depende de: F0 · Especificação: Visão geral, Terminais e caixas, Configurações
Aceite:
- [ ] Lojas PNZ e LEM com CNPJ, IE, UF e código IBGE; terminais 01 e 02 por loja com usuário fixo e série de NFC-e
- [ ] `configuracoes` por loja com os valores padrão da especificação (desconto máximo sem senha 5%, fechamento cego desligado, prazo ligado, vencimento 30 dias, até 3x, multa 2%, juros 1% a.m.)
- [ ] Toda tabela com RLS ligada; usuário de uma loja não lê a outra sem permissão

## BD-02 · Usuários, perfis, permissões e autorizações
Fase: F1 · Especificação: Usuários e permissões, Senha
Aceite:
- [ ] Perfis Administrador, Gerente, Supervisor de caixa, Operador de caixa e Faturista com permissões padrão; ajuste por usuário
- [ ] RPC `autorizar(acao, usuario_autorizador, senha)` devolve um token de uso único válido por 2 minutos; senha errada → erro "Senha incorreta"; perfil sem direito → recusa
- [ ] Toda RPC sensível exige o token quando o usuário não tem a permissão e grava `autorizacoes` (quem fez, quem autorizou, ação, registro, data do servidor)
- [ ] Administrador principal não pode ser desativado nem mudar de perfil; usuário com caixa aberto não pode ser desativado

## BD-03 · Estoque em dois locais
Fase: F2 · Especificação: Estoques por local (com D1: só Frente e Fundo)
Aceite:
- [ ] `estoque_saldos` com local `frente|fundo`; mínimo por local; saldo nunca negativo
- [ ] RPCs `entrada`, `saida`, `transferir`, `desfazer_transferencia` com motivo, usuário e caixa; cada uma grava `estoque_movimentos` com saldo depois
- [ ] `disponivel_frente(produto)` = frente − reservado por vendas abertas de qualquer terminal

## BD-04 · Vendas, numeração e reserva
Fase: F3 · Especificação: Numeração, Vendas em andamento, Estoque no caixa, Vendas simultâneas
Aceite:
- [ ] Venda aberta gravada no servidor a cada item; até 4 abertas por caixa; DAV e NFC-e separadas
- [ ] `finalizar_venda` em uma transação: valida caixa aberto, estoque da frente, formas, limite de desconto (exige autorização acima de 5%), tira número da sequência da loja, baixa estoque, lança pagamentos, títulos a prazo e crédito
- [ ] Dois terminais finalizando ao mesmo tempo nunca repetem número (teste com 200 finalizações concorrentes)
- [ ] P8: sequência de DAV por loja; NFC-e com série por terminal (1 = Terminal 01, 2 = Terminal 02) e numeração própria

## BD-05 · Caixa, fechamento e meia-noite
Fase: F3 · Especificação: Fechamento de caixa e conferência
Aceite:
- [ ] `fechar_caixa` recusa com "Há venda em andamento" se houver venda aberta no terminal (DAV ou NFC-e)
- [ ] `pg_cron` às 00:00 fecha caixas abertos com hora 23:59 do dia anterior e marca "fechado automaticamente"
- [ ] Divergência e desfazer divergência só no mesmo dia (data do servidor)

## BD-06 · Prazo e baixas
Fase: F5 · Especificação: Venda a prazo e contas a receber
Aceite:
- [ ] Multa 2% uma vez, juros 1% a.m. pro rata por dia; baixa parcial quita multa → juros → principal, da parcela mais antiga para a mais nova; juros recomeçam do dia do pagamento
- [ ] Exemplo da especificação: devido R$ 318,76, pago R$ 300,00 → parcela com R$ 18,76 em aberto
- [ ] Desfazer baixa só no mesmo dia; devolve saldo, multa e juros de antes; recibo marcado "Baixa desfeita"; novo recibo "SUBSTITUI O RECIBO Nº X"

## BD-07 · Tempo real e presença
Fase: F1 · Especificação: Comunicação entre os terminais
Aceite:
- [ ] Canal por loja com vendas abertas, reservas e caixas abertos; um terminal vê o item reservado pelo outro em menos de 1 s na rede local

## BD-08 · Dados de teste
Fase: F1 · Especificação: Padrões de tela (Dados de teste)
Aceite:
- [ ] Vendas de 01/08/2026 até hoje nos dois terminais, DAV em ordem de data, clientes com etiquetas variadas, títulos a prazo vencidos e em dia
