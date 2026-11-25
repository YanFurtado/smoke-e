# PDV Smoke House: documentação do projeto

Plano para construir o PDV de balcão (Frente de caixa, Cupom fiscal e Retaguarda) das lojas PNZ e LEM a partir da *Especificação do PDV Smoke House v1.2.02*. Por enquanto o projeto tem só documentos e telas; nenhum código do sistema foi escrito.

| Documento | Para que serve |
|---|---|
| [00-escopo-e-decisoes.md](00-escopo-e-decisoes.md) | O que é o produto, decisões já tomadas (D1: estoque só Frente e Fundo) e pendências que bloqueiam etapas |
| [01-arquitetura.md](01-arquitetura.md) | Stack, modelo de dados, numeração, tempo real, offline e segurança |
| [02-direcao-visual.md](02-direcao-visual.md) | Direção visual pelo método unslop: cores, tipo, espaço, componentes e checklist |
| [03-telas.md](03-telas.md) | Inventário das 60 telas (DAV, NFC-e, HOST) e como cada uma se adapta a celular, tablet e computador |
| [04-fiscal.md](04-fiscal.md) | NFC-e, contingência, tabaco, IBS/CBS e uso das calculadoras da Receita Federal |
| [05-orquestracao.md](05-orquestracao.md) | Orquestrador e subagentes: papéis, fluxo de uma tarefa, validação funcional, fases e portões |
| [06-reaproveitamento-erp.md](06-reaproveitamento-erp.md) | O que copiar do `erp-system` e o que não copiar |
| [tarefas/](tarefas/) | Cartões de tarefa por subagente, com critérios de aceite |

**Agentes:** `.claude/agents/` na raiz do repositório (`pdv-orquestrador` e doze especialistas).

**Especificação:** [especificacao/](especificacao/) (PDF v1.2.02 e o texto extraído, para os agentes lerem).

**Telas:** [design/figcraft/Smoke House · PDV.figcraft](design/figcraft/) (abre no FigCraft; uma cópia fica em `~/Documents/figcraft/`). Prévia de cada tela em JPG em [design/figcraft/previas/](design/figcraft/previas/). O arquivo é gerado por código em [design/figcraft/gerador/](design/figcraft/gerador/): `python3 build.py` monta e guarda backup da versão anterior, `python3 render.py "../Smoke House · PDV.figcraft"` exporta os PNGs e `python3 previas.py` gera os JPGs.

## Para começar

1. As pendências P1 a P15 já têm decisão em [00-escopo-e-decisoes.md](00-escopo-e-decisoes.md). Falta o contador assinar P1, P2 e P5 (**P2 até 30/11/2026**) e o cliente entregar os dados das lojas (seção "O que ainda depende de fora").
2. Abrir o Claude Code na raiz do `smoke-e` e dizer: *"Você é o orquestrador do PDV Smoke House. Siga `.claude/agents/pdv-orquestrador.md`."*
3. O orquestrador começa pela fase F1 e, em paralelo, pela tarefa FS-07 (IBS/CBS), por causa do prazo de janeiro de 2027.
