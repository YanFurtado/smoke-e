# Parte fiscal (NFC-e e reforma tributária)

A especificação deixa a parte fiscal "parada, a definir com o sistema que vai fazer a integração". Este documento é o plano para quando ela for liberada. Tudo aqui passa pelo contador antes de ir para produção.

## Bases

| Fonte | Uso |
|---|---|
| `erp-system/services/nfe-service` (PHP, nfephp-org/sped-nfe 5.2.8, sped-da 1.1.6) | Já monta, assina e transmite NFC-e modelo 65 com QR Code e CSC; DANFE NFC-e em PDF; cancelamento (110111); inutilização |
| [calculadora-rtc-regime-regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) v1.7.2 | CBS, IBS e Imposto Seletivo do regime regular; gera e valida o grupo XML `IBSCBS` da NFC-e; tabelas oficiais (cClassTrib, CST, NCM) pelos endpoints `/dados-abertos` |
| [calculadora-rtc-simples-nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional) v1.0.2 | CBS e IBS do Simples Nacional "por fora do DAS", a partir de 2027; atividade `cAtivSN` 01 (revenda de mercadorias) |
| [calculadora-rtc-gerador-danfse](https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse) | Não se aplica: gera o DANFSe da NFS-e (serviço). A loja só vende mercadoria |

## O que o `nfe-service` ainda não faz (lacunas encontradas)

1. **Grupo IBS/CBS** (NT 2025.002-RTC): nenhum campo no código. Segundo a documentação interna do `erp-system`, a partir de **04/01/2027** a nota de emitente do Simples sem o grupo `IBSCBS` em cada item é rejeitada (cStat 1115). **Confirmar a data na NT vigente.**
2. **ICMS-ST de tabaco:** recusa CSOSN 201/202/203 e não envia os campos de ST retida (vBCSTRet, pST, vICMSSTRet) do CSOSN 500. Sem FCP.
3. **Contingência offline:** a nota só é gerada depois, à mão, com `dhEmi` da transmissão. Precisa gerar e assinar o XML **na hora da venda**, imprimir o DANFE com "EMITIDA EM CONTINGÊNCIA" e transmitir sozinho em até 24 h.
4. **Retransmissão e consulta:** sem job para notas "pendente de transmissão" e sem consulta da situação por chave.
5. **Impressão:** o PDV não imprime o DANFE após autorizar.
6. **Pagamentos na nota:** só a forma principal com o total; falta uma linha `detPag` por forma, `vTroco` e os dados do cartão (TEF/POS integrado, exigido em PE).
7. **Lei 12.741:** sem `vTotTrib` (tabela IBPT).
8. **Cancelamento:** sem controle de prazo da UF e sem cancelamento por substituição (110112).
9. **Série:** por loja, não por terminal.
10. **Chave do certificado:** chave de criptografia padrão gravada no código. Obrigatório trocar na instalação.

## Plano por etapa

| Etapa | Entrega | Critério de pronto |
|---|---|---|
| F6.1 | Instância própria do `nfe-service`, certificado A1 e CSC de homologação de PNZ (PE) | NFC-e autorizada em homologação, DANFE impresso na térmica |
| F6.2 | Uma série por terminal; numeração atômica; inutilização assistida de número rejeitado | Dois terminais emitindo juntos sem repetir número |
| F6.3 | Pagamentos completos (`detPag` por forma, `vTroco`, cartão) | Venda com Pix + dinheiro + troco autorizada |
| F6.4 | Tabaco: CSOSN 500 com ST retida, CFOP 5405, CEST obrigatório no cadastro de cigarro e fumo | Nota de cigarro autorizada em homologação, conferida pelo contador |
| F6.5 | `vTotTrib` com a tabela IBPT, atualizada pelo HOST | Valor no DANFE igual ao da tabela |
| F6.6 | Contingência offline real (tpEmis 9) e retransmissão automática por `pg_cron` | Com a internet cortada, a venda sai com DANFE; ao voltar, autoriza sozinha |
| F6.7 | **Grupo IBS/CBS** em cada item e totais (`IBSCBSTot`), com cClassTrib e CST no produto. Em 2026: CBS 0,9% e IBS 0,1% informativos; em 2027, conforme a opção do Simples (P2) | XML validado pelo `/xml/validate?tipo=nfce` da calculadora da Receita e autorizado em homologação |
| F6.8 | Cancelamento com prazo da UF, evento 110112, XML de eventos guardado | Cancelamento dentro e fora do prazo com a mensagem certa |
| F6.9 | Loja LEM (BA): IE, CSC e SEFAZ-BA | Mesmos testes de F6.1 a F6.8 na BA |

## Como usar as calculadoras da Receita

- **Não rodar no caixa.** São serviços Java 25 com banco SQLite somente leitura; ficam no servidor, um por ambiente.
- **2026:** o cálculo é CBS 0,9% e IBS 0,1% sobre a base. Fica no código da RPC; a calculadora serve de gabarito nos testes.
- **2027 em diante:** se a loja ficar no Simples "dentro" do DAS, usar a `simples-nacional` (`cAtivSN` 01, alíquotas vindas do PGDAS-D). Se optar pelo regime regular do IBS/CBS, usar a `regime-regular`. Chamar sempre o endpoint de observabilidade, para um item ruim não derrubar a nota.
- **Imposto Seletivo:** a base da calculadora liga os NCM 2401 a 2404 ao IS a partir de 2027. Pela LC 214/2025 o IS incide uma vez, no fabricante ou importador; o varejo provavelmente não destaca. **Confirmar com o contador.**
- **Tabelas:** job diário que lê `/dados-abertos` (cClassTrib, CST, `ncm/vigentes`) e grava em `tabelas_rtc` com a versão. O HOST › Fiscal mostra a versão em uso.
- **Versão fixa:** foram dez versões entre setembro e novembro de 2026. Fixar a versão, gerar o banco na CI e rodar a regressão a cada atualização.

## O que o produto guarda

- **Por produto:** NCM (8 dígitos), CEST, CFOP, origem, CSOSN, CST e cClassTrib do IBS/CBS, unidade tributável.
- **Por venda NFC-e:** série, número, chave, protocolo, tpEmis, `dhEmi`, `dhCont`, XML autorizado, DANFE, e por item os valores de CBS e IBS calculados com a versão da tabela usada.
