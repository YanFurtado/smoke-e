# Direção visual

Definida com o método do [unslop](https://github.com/heydamir/unslop), de Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), licença CC BY 4.0. A especificação manda o visual ser "profissional e humano, sem cara de IA, com espaçamento para o design respirar". O unslop dá as regras concretas para isso.

## As cinco linhas

- **Produto.** Frente de caixa e retaguarda das duas lojas da Smoke House Tabacaria (Petrolina-PE e Luís Eduardo Magalhães-BA). O operador vende pelo teclado e pelo leitor no balcão; o gerente confere caixa, estoque e contas a prazo.
- **Caráter.** Ligeiro, exato, de balcão.
- **Mundo.** O balcão da tabacaria: a bobina térmica do cupom, papel de seda, madeira escura, o verde da marca. Daí vêm os neutros levemente quentes e a cor do papel do cupom.
- **Momentos.** (1) O cupom na tela, desenhado como bobina térmica (papel creme, Menlo, itens 001, 002…, serrilha embaixo), com o TOTAL grande ao lado. (2) No HOST, o comprovante de fechamento e os números do dia. Fora isso, tudo fica quieto.
- **Assinatura.** As teclas: F3, F7, Esc e as outras aparecem como teclas desenhadas (keycaps), no rodapé, nos botões e nas janelas. Em nenhum outro lugar.

## Cor

Uma rampa de neutros levemente quente. As superfícies não ganham cor.

| Papel | Valor |
|---|---|
| Fundo da tela | `#f4f3ef` |
| Faixa (rodapé, menu lateral, abas inativas) | `#ebe9e3` |
| Cartão, janela | `#ffffff` |
| Campo, linha ativa | `#eeece6` |
| Linha selecionada | `#e6e4de` com borda de 1 px `#1c1b18` (regra da especificação) |
| Papel do cupom | `#fffdf8` |
| Texto principal | `#1c1b18` |
| Texto secundário | `#55534d` |
| Texto apagado, ícones | `#77746c` |
| Linha fina (hairline) | texto principal a 10% |

**Cor de cada aplicativo** (da especificação). Aparece só no botão principal, no foco do campo, na aba ativa e no ponto ao lado do nome do aplicativo no topo.

| Aplicativo | Cor | Fundo suave (último item do cupom) |
|---|---|---|
| Frente de caixa (DAV) | Verde `#256d45` | `#e3efe7` |
| Cupom fiscal (NFC-e) | Azul-petróleo `#1b6670` | `#e1eef0` |
| Retaguarda (HOST) | Azul-petróleo escuro `#134a52` | `#e0eaec` |

O verde `#34925e` da marca não serve para texto branco por cima (contraste 3,9:1). Por isso o botão usa `#256d45` (6,4:1).

**Cores de sentido:** positivo `#256d45`, erro e cancelado `#b4332f`, aviso `#9a6400`, interrogação das janelas Sim/Não `#1b6670`. Situação é sempre um ponto de 8 px mais texto, nunca uma pílula colorida.

Proibido: gradiente entre cores, texto em gradiente, brilho, sombra colorida, manchas de cor atrás do conteúdo, borda neon.

## Tipo

- **Inter** em toda a interface. Pesos 400 e 500; 600 só no cupom impresso.
- **Menlo** para o cupom, códigos (cadastro, GTIN, chave de acesso), teclas e números de tabela.
- Hierarquia por tamanho e cor, não por peso. Sem caixa alta espaçada, sem itálico, sem ponto final em rótulo e botão, sem exclamação.
- Exceção pedida pela especificação: "CAIXA LIVRE" e "CAIXA FECHADO" em caixa alta, grandes.

| Uso | Tamanho / linha |
|---|---|
| Meta, contagem, tecla | 11 a 12 / 16 |
| Texto secundário, célula de tabela | 13 / 20 |
| Texto, item de menu | 14 / 20 |
| Título de janela | 17 / 24 |
| Título de página | 24 / 32 (celular 20 / 28) |
| Número de quadro | 28 / 32 |
| TOTAL da venda | 72 no computador, 52 no tablet, 28 na barra do celular |
| CAIXA LIVRE | 88 / 72 / 44 |

## Espaço e forma

- Grade de 4 px. Bordas da página: 24 (computador), 20 (tablet), 16 (celular).
- Linhas de tabela de 40; resultados de busca de 56; menu lateral de 34 com 2 entre linhas.
- Raio: tecla 4, campo e botão 8, cartão 12, janela 16. Raio interno = externo − espaçamento.
- Botão principal 40 de altura (64 na tela de venda). Alvo de toque mínimo 40 no tablet e no celular.
- Profundidade por degraus de superfície e linha fina. Sombra só em janela (preta a 10%, 12 de deslocamento, 32 de raio) e na bobina impressa.

## Ícones

Um só conjunto de linha (Lucide no código), 16 px, traço 1,5, na cor do texto secundário ou apagado. Sem emoji em lugar nenhum.

## Componentes que se repetem

Barra superior, rodapé de teclas, barra de busca com ☰, cupom na tela, bloco do total, janela (título + Esc + botões), janela Sim/Não, senha do supervisor, tabela com seleção, filtros arredondados com contagem, quadro de número, aviso com faixa lateral, folha de baixo no celular, menu lateral do HOST, bobina impressa. Estão desenhados na página "00 · Direção visual" do arquivo FigCraft e no gerador `pdv/design/figcraft/gerador/ui.py`.

## Movimento

Uma curva para tudo, `cubic-bezier(0.22, 1, 0.36, 1)`. Hover e toque 120 a 180 ms; janelas e menus 160 a 220 ms. Nada pisca nem fica em loop. O relógio do Caixa livre muda o número sem animação. Só se animam cor, fundo, borda, opacidade e transform.

## Verificação antes de entregar uma tela

- [ ] Grade de 4 e coisas iguais com o mesmo tamanho
- [ ] Uma cor de aplicativo, usada só no principal, no foco e na aba
- [ ] Seleção em lista com fundo cinza claro e borda preta, igual com mouse e teclado
- [ ] Esc visível em toda janela
- [ ] Nenhum emoji, gradiente, brilho ou pílula colorida
- [ ] Números em Menlo e no mesmo formato (R$ 1.234,50)
- [ ] Celular de 390 sem rolagem lateral e nenhum texto abaixo de 11
- [ ] Teste do modelo: trocando o nome Smoke House por outro, a tela ainda serviria? Se sim, faltou o cupom, a tecla ou o produto real
