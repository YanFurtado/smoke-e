# Tarefas · pdv-fiscal

Plano completo e lacunas em [../04-fiscal.md](../04-fiscal.md). Depende de P1, P2, P3 e P5 em [../00-escopo-e-decisoes.md](../00-escopo-e-decisoes.md).

## FS-01 · Serviço de emissão próprio e homologação PE (F6.1)
Telas: N01, N02, N03, H25
Aceite:
- [ ] `nfe-service` em instância própria, só na rede interna, com token; chave de cripto do certificado definida na instalação (nunca a padrão)
- [ ] NFC-e autorizada em homologação da SEFAZ-PE; DANFE 80 mm impresso sozinho após autorizar

## FS-02 · Série por terminal e inutilização (F6.2)
Telas: N07, H25
Aceite:
- [ ] Série por terminal, numeração atômica; número rejeitado entra em fila de inutilização assistida
- [ ] P15: rejeição por cadastro deixa a venda aberta; corrigido o produto no HOST (gerente ou administrador), reemite com o mesmo número; venda abandonada manda o número para a inutilização

## FS-03 · Pagamentos completos (F6.3)
Aceite:
- [ ] Um `detPag` por forma, `vTroco`, dados de cartão; venda Pix + dinheiro + troco autorizada

## FS-04 · Tabaco e ST (F6.4)
Aceite:
- [ ] CSOSN 500 com grupo de ST retida, CFOP 5405, CEST obrigatório para cigarro e fumo; nota conferida pelo contador

## FS-05 · Lei 12.741 (F6.5)
Aceite:
- [ ] `vTotTrib` pela tabela IBPT (versão e data no HOST › Fiscal)

## FS-06 · Contingência offline (F6.6)
Telas: N05
Aceite:
- [ ] Sem resposta da SEFAZ: XML assinado na hora com tpEmis 9 e `dhCont`, DANFE "EMITIDA EM CONTINGÊNCIA"; transmissão automática por `pg_cron`; alerta antes de 24 h

## FS-07 · IBS/CBS (F6.7) · prioridade por prazo
Aceite:
- [ ] Grupo `IBSCBS` em cada item e `IBSCBSTot` nos totais, com cClassTrib e CST do produto
- [ ] XML aprovado pelo `/api/calculadora/xml/validate?tipo=nfce&subtipo=nota` da calculadora da Receita e autorizado em homologação
- [ ] Job que sincroniza cClassTrib, CST e NCM pelos `/dados-abertos` e grava a versão

## FS-08 · Cancelamento (F6.8)
Telas: N06, N04
Aceite:
- [ ] Justificativa ≥ 15 caracteres, prazo restante, senha do supervisor; evento 110111 e 110112; XML do evento guardado

## FS-09 · Loja LEM, SEFAZ-BA (F6.9)
Aceite:
- [ ] FS-01 a FS-08 repetidos com IE, CSC e certificado da LEM
