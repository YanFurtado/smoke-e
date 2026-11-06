# Smoke House · E-commerce (protótipo navegável)

Protótipo completo do e-commerce da **Tabacaria Smoke House**, com as lojas de **Luís Eduardo Magalhães (LEM, BA)** e **Petrolina (PNZ, PE)**. Projeto da Conexão Assessoria.

O sistema todo roda num único arquivo, `index.html`, sem servidor e sem instalação. Ele tem quatro partes ligadas entre si:

| Parte | Como acessar | O que faz |
|---|---|---|
| **Vitrine** | `index.html` | Confirmação de 18+, escolha da loja, busca, filtros, carrinho, checkout em 3 passos e pedido pelo WhatsApp |
| **Link do colaborador** | `index.html#pnz-vendedor-carla` | Mesma vitrine, com o pedido registrado no nome do colaborador |
| **Área do colaborador** | `index.html#colaborador` | Pedidos, estoque, link com QR code, comissões, venda no balcão e tarefas |
| **Painel dos donos** | `index.html#donos` | Visão geral, financeiro, pedidos, equipe, agenda e ajustes |

## Como rodar

**Local:** abra o `index.html` no navegador.

**GitHub Pages:**
1. Suba o repositório.
2. Vá em *Settings → Pages → Deploy from a branch → main / (root)*.
3. O site fica em `https://<usuario>.github.io/<repositorio>/`.

Os links de venda dos colaboradores passam a usar automaticamente esse endereço.

## Acessos de demonstração

| Quem | PIN |
|---|---|
| Carla (PNZ), João (PNZ), Bia (LEM) | `1234` |
| Painel dos donos | `2026` |

> Os PINs e os dados de exemplo são só para demonstração. Antes de abrir o link para clientes, troque o acesso por login real (ver "Próximos passos").

## Rotas

- `#pnz` e `#lem`: loja escolhida.
- `#pnz-vendedor-<nome>` e `#lem-vendedor-<nome>`: link de venda do colaborador.
- `#colaborador`: área do colaborador.
- `#donos`: painel dos donos.

## Estrutura

```
smokehouse-ecommerce/
├── index.html            ← site pronto (gerado pelo build.py; é o que vai para o ar)
├── build.py              ← monta o index.html a partir de src/ + assets/web/
├── src/
│   ├── template.html     ← HTML e CSS (vitrine, colaborador e painel)
│   └── app.js            ← toda a lógica (vitrine, busca, checkout, colaborador, donos)
├── assets/
│   ├── web/              ← imagens .webp e fonte .woff2 usadas no site (embutidas no build)
│   └── marca/            ← arquivos originais da marca vindos do Drive (logo, elementos)
├── tests/                ← auditoria automatizada (Playwright)
│   ├── audit.py          ← vitrine, busca, filtros, carrinho, checkout, páginas, colaborador
│   ├── owner_test.py     ← painel dos donos e integração com o colaborador
│   └── pay_test.py       ← formas de pagamento em todo o sistema
└── docs/
    └── PENDENCIAS.md     ← o que falta confirmar com o cliente
```

## Editar e gerar o site

1. Edite `src/template.html` (estrutura e estilos) ou `src/app.js` (dados e lógica).
2. Rode `python3 build.py`, que gera o `index.html` com imagens e fonte embutidas.
3. Faça o commit do `index.html` junto com os arquivos de `src/`.

Onde ficam os dados principais em `src/app.js`:

- `STORES`: endereço, WhatsApp, horário, bairros e taxas de cada loja.
- `P`: catálogo de produtos. Sedas e atacado têm preços reais do cardápio PNZ; o resto é exemplo.
- `PAYMENTS`: as 6 formas de pagamento, usadas no site inteiro.
- `TEAM`: colaboradores, loja, PIN e meta.
- `REVIEWS`, `GUIDES` e `PAGES`: avaliações do Google, guias e páginas institucionais.

## Testes

```bash
pip install playwright && python3 -m playwright install chromium
python3 tests/audit.py        # 265 verificações (computador e celular)
python3 tests/owner_test.py   # 114 verificações
python3 tests/pay_test.py     # 34 verificações
```

Para usar o Chrome instalado em vez do Chromium do Playwright: `CHROME_PATH=/caminho/do/chrome python3 tests/audit.py`.

Os prints dos testes ficam em `tests/saida/`, que é ignorada pelo git.

## Limites do protótipo

- **Dados por navegador:** pedidos, estoque, despesas, agenda e tarefas ficam no `localStorage` de quem está usando. Um pedido feito no celular não aparece no computador.
- **Pagamento:** não há gateway. O pedido é confirmado pelo WhatsApp da loja, com Pix, link ou maquininha.
- **Imagens dos produtos:** são blocos com a marca do produto, porque ainda não há fotos reais.
- **CNPJ:** não foi encontrado em bases públicas e aparece como "a informar".

## Próximos passos para o sistema real

1. Banco de dados compartilhado e login individual para donos e colaboradores. Sugestão: Supabase ou Firebase.
2. Cadastro de produtos com fotos, custo real e estoque por loja.
3. Integração de pagamento (Pix e cartão), após validação jurídica para a categoria tabacaria.
4. Pixel da Meta e GA4 com eventos de e-commerce, e recuperação de carrinho pelo n8n.
5. Domínio próprio e política de privacidade revisada pelo jurídico.

## Direitos

Logo, elementos gráficos, fonte e fotos em `assets/` pertencem à Smoke House ou aos respectivos autores e foram usados só para este projeto. Confirme a licença da fonte BrushUpToo antes de publicar em produção.
