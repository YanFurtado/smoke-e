# Tarefas · pdv-dispositivos

## DV-01 · App instalado
Fase: F3 · Especificação: Teclas de atalho ("No sistema instalado o F11 abre o menu")
Aceite:
- [ ] Tauri para Windows com a mesma interface; F11 chega ao app (não vira tela cheia); abre direto no terminal configurado

## DV-02 · Impressora térmica e gaveta
Especificação: HOST › Equipamentos, Cupom impresso
Aceite:
- [ ] Cupom DAV, comprovante de fechamento, recibo e DANFE NFC-e em ESC/POS 80 mm; o DAV impresso sai com o terminal certo
- [ ] Gaveta abre só no pagamento em dinheiro (não existe botão "abrir gaveta")

## DV-03 · Leitor e TEF
Aceite:
- [ ] Leitor USB lança pelo código; após erro, a leitura seguinte substitui o texto selecionado
- [ ] TEF/POS integrado devolve bandeira, autorização e CNPJ da credenciadora para a nota (exigido em PE)

## DV-04 · Offline
Especificação: Fora do escopo (o protótipo só simula)
Aceite:
- [ ] Sem servidor: rodapé "Sem conexão com o servidor"; vende da frente sincronizada; bloqueia o que exige servidor (ver 01-arquitetura.md); fila sobe sozinha ao voltar
