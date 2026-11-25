# Escopo e decisões

## O que é

O PDV Smoke House é o sistema de balcão das duas lojas da Smoke House Tabacaria: **PNZ** (Petrolina-PE) e **LEM** (Luís Eduardo Magalhães-BA). São três aplicativos que dividem o mesmo caixa e os mesmos cadastros:

| Aplicativo | Nome na tela | Cor | Serve para |
|---|---|---|---|
| DAV | Frente de caixa | Verde | Vendas, cancelamentos, DAVs emitidos e fechamento de caixa |
| NFC-e | Cupom fiscal | Azul-petróleo | As mesmas telas do DAV; ao finalizar emite NFC-e |
| HOST | Retaguarda | Azul-petróleo escuro | Configurações, cadastros, estoque, clientes, financeiro, relatórios e fiscal |

**Fonte principal das regras:** *Especificação do PDV Smoke House*, versão 1.2.02, de 17/11/2026 (Lucas Prazeres). O que está lá foi aprovado. Este pacote de documentos organiza o trabalho em cima dela e registra as decisões tomadas depois.

O e-commerce (`smokehouse-ecommerce/`) é outro produto, por enquanto um protótipo em HTML. Ele passa a ler catálogo e estoque do mesmo banco do PDV (tarefa ECO-01), mas o redesenho dele está fora deste escopo.

## Decisões tomadas

| # | Data | Decisão | Efeito |
|---|---|---|---|
| D1 | 24/11/2026 | **O estoque tem dois locais por loja: Frente de loja e Fundo de loja.** Não existe Matriz. | A especificação fala em três locais (Matriz, Fundo, Frente). Onde ela diz Matriz, vale Fundo. Transferência só Fundo ↔ Frente. O aviso do caixa diz "há no fundo de loja" ou "em falta". A importação de XML entra no Fundo por padrão. O motivo de entrada "transferência de outra loja" continua existindo (PNZ ↔ LEM), mas transferência entre lojas é outra operação, com NF-e (ver D-pendente P4). |
| D2 | 24/11/2026 | Neste momento a entrega é **só documentação e telas**. Nenhum código do sistema. | Este pacote e o arquivo FigCraft. |
| D3 | 24/11/2026 | Visual definido pelo método **unslop** (heydamir/unslop). | [02-direcao-visual.md](02-direcao-visual.md). |
| D4 | 24/11/2026 | O trabalho é feito por **subagentes especializados e um orquestrador**, que revisa e valida o produto em funcionamento. O agente de design responde pelas versões celular, tablet e computador. | [05-orquestracao.md](05-orquestracao.md) e `.claude/agents/`. |
| D5 | 24/11/2026 | **Base técnica:** reaproveitar padrões e partes do `erp-system` (Supabase, fila offline, serviço de NF-e em PHP com sped-nfe), numa **instância própria** da Smoke House, sem dividir banco com o ERP X-Life. | [01-arquitetura.md](01-arquitetura.md). |

## Decisões sobre as pendências (24/11/2026)

As pendências P1 a P15 foram decididas pelo orquestrador para o projeto andar. As marcadas com **contador** são decisões de produto que já valem no sistema, mas o contador precisa assinar antes da Fase 6 (fiscal) ir para produção.

| # | Pendência | Decisão | Confirma |
|---|---|---|---|
| P1 | Venda só no DAV, sem NFC-e | O DAV é a venda de balcão e fecha no caixa como na especificação. Todo DAV finalizado pode ser **importado no NFC-e**: vira NFC-e com o mesmo cliente, itens e pagamentos, e passa à situação "Importado". O fechamento mostra quantos DAVs do caixa ficaram sem nota. Se o contador exigir nota em toda venda ao consumidor, liga-se em Regras do caixa a opção "Importar o DAV no NFC-e ao finalizar" e o fluxo passa a ser automático | Contador |
| P2 | Regime e IBS/CBS em 2027 | Simples Nacional, com IBS/CBS **dentro do DAS** (varejo a consumidor final, que não aproveita crédito). O sistema já nasce com o grupo IBS/CBS na nota e com a opção "por fora" no HOST › Fiscal, para trocar sem programar. Atenção: segundo a documentação do erp-system, a desistência da opção feita em setembro para o 1º semestre de 2027 vai **até 30/11/2026** | Contador, até 30/11/2026 |
| P3 | CNPJ, IE, CSC e certificado de cada loja | Não é decisão: são dados. Lista do que coletar na seção abaixo. Até lá, telas e testes usam "CNPJ a informar" e homologação | Cliente |
| P4 | Transferência de mercadoria entre PNZ e LEM | Fica **fora do PDV na versão 1**. Se acontecer, a NF-e de transferência é emitida pelo contador ou por outro sistema, e a loja de destino dá entrada pelo Importar XML. O motivo de entrada "Transferência de outra loja" continua para ajuste manual | Cliente |
| P5 | Quais produtos têm ICMS-ST | Regra de cadastro: NCM 2402 (cigarros, charutos, cigarrilhas) e 2403 (fumo) → CSOSN 500, CFOP 5405, CEST do segmento 04 obrigatório. Acessórios (sedas, isqueiros, piteiras, narguilé, essências) → CSOSN 102, CFOP 5102. A categoria preenche o padrão e o cadastro não salva NCM 2402/2403 sem CEST | Contador, produto a produto |
| P6 | O e-commerce vende de qual estoque | Da **Frente de loja**. O pedido do site entra como venda aberta, reserva o estoque igual a um terminal e baixa quando é concluído | — |
| P7 | Boleto no site | **Sai do site.** Sem gateway, o boleto era gerado à mão. Atacado paga por Pix ou cartão. A especificação do PDV já exclui boleto e carnê | Cliente |
| P8 | Numeração única | DAV: uma sequência por loja, para os dois terminais. NFC-e: **uma série por terminal** (série 1 no Terminal 01, série 2 no Terminal 02), com numeração própria. É o que a nota exige e o que deixa a contingência de um terminal independente do outro | — |
| P9 | Sangria para pagar fornecedor | A sangria ganha o destino "Pagamento a fornecedor", que pede a conta a pagar e dá baixa nela. O destino padrão continua a conta do banco | — |
| P10 | Devolução de venda a prazo: qual parcela abate | A **mais nova** em aberto. O cliente mantém as datas que já combinou, e as parcelas mais antigas continuam como estão | — |
| P11 | Troca: onde entram os produtos novos | Na **própria venda**. A janela Troca registra os itens devolvidos e gera o "Crédito de troca", que entra na venda aberta e aparece no F3 como forma de pagamento. A sobra vira crédito do cliente ao finalizar (exige cliente). F6 sem produto novo desfaz a troca. Tela D18 redesenhada | — |
| P12 | Situação "Importado" em DAVs emitidos | DAV que virou NFC-e (P1). No menu ⋯: Reimpressão, WhatsApp e Ticket de troca ficam ativos; Alterar forma de pagamento e Cancelar cupom ficam desativados (o cancelamento é feito na NFC-e) | — |
| P13 | Crédito do cliente no fechamento | Sim nos dois: o pagamento com Crédito do cliente aparece em "Recebido por forma" (não soma na gaveta), e o crédito lançado em dinheiro soma na linha Dinheiro e na gaveta | — |
| P14 | Alerta de estoque baixo na venda | Sim: uma faixa discreta acima do total ("Seda Zomo Rosa ficou com 2 na frente · mínimo 6"), que some na próxima leitura e não interrompe a venda | — |
| P15 | Quem corrige o cadastro após rejeição da SEFAZ | Gerente ou administrador, no HOST. A venda fica aberta no caixa; corrigido o cadastro, o operador emite de novo com o mesmo número. Se a venda for abandonada, o número vai para a inutilização | — |

Regras menores decididas na revisão das telas:

- A janela Sim/Não mostra Esc no título (S ou Enter confirma, N ou Esc volta).
- No PRAZO com parcela vencida, "Lançar PRAZO" fica desativado até a senha do supervisor.
- Preço de um item abaixo do limite pede a senha na hora (F10); o desconto total acima do limite pede ao finalizar.
- Contas a receber: os quadros "Em aberto" e "Vencido" mostram o principal; multa e juros aparecem em "Total hoje".
- Recibo que substitui outro: o número novo no topo e "SUBSTITUI O RECIBO Nº" logo abaixo.
- A aba Transferências fica dentro de Estoque (a especificação a chama de aba).

## O que ainda depende de fora

| Item | Quem | Para quando |
|---|---|---|
| Assinar P1, P2 e P5 | Contador | P2 até 30/11/2026; P1 e P5 antes da Fase 6 |
| Razão social, CNPJ, IE, endereço, código IBGE e regime de **cada loja** (PNZ e LEM) | Cliente | Fase 1 |
| Certificado A1 (.pfx e senha) de cada CNPJ | Cliente | Fase 6 |
| CSC e id do CSC de homologação e de produção, SEFAZ-PE e SEFAZ-BA | Contador ou cliente | Fase 6 |
| Credenciadora da maquininha (para o grupo de cartão da NFC-e e o TEF) | Cliente | Fase 6 |
| Tabela IBPT atual | Contador | Fase 6 |

## Fora do escopo por enquanto

- Comissões, ordens de serviço e "recebimentos de crediário" (a especificação diz que não existem).
- Balança, venda por peso e a unidade GR.
- Boleto e carnê como forma de pagamento no PDV.
- Envio automático de WhatsApp (o PDV abre o `wa.me` com a mensagem pronta).
- NFS-e e DANFSe: a loja só vende mercadoria. O gerador de DANFSe da Receita não se aplica.
