# ref.interna.dr-matheus-cavalcanti

**Fonte:** https://drmatheuscavalcantidf.com.br/
**Title:** Dr. Matheus Cavalcanti | Ortopedia em Brasília

Rascunho MECANICO gerado por `ferramentas/extrair-identidade.py` a partir da pagina no ar. As secoes de julgamento abaixo estao vazias de proposito — preencher a mao seguindo `visual-repertorio/_templates/cartao-referencia.md`.

## Identidade extraida

### Tokens `:root` declarados (20)

| Token | Valor |
| --- | --- |
| `--fa-style-family-brands` | `"Font Awesome 6 Brands"` |
| `--fa-font-brands` | `normal 400 1em/1 "Font Awesome 6 Brands"` |
| `--fa-font-regular` | `normal 400 1em/1 "Font Awesome 6 Free"` |
| `--fa-style-family-classic` | `"Font Awesome 6 Free"` |
| `--fa-font-solid` | `normal 900 1em/1 "Font Awesome 6 Free"` |
| `--olive` | `#393b23` |
| `--olive-dark` | `#26261c` |
| `--olive-soft` | `#6f7352` |
| `--sand` | `#c6b5a3` |
| `--paper` | `#f6f4ef` |
| `--white` | `#fffefa` |
| `--mist` | `#e5e4df` |
| `--ink` | `#24251f` |
| `--muted` | `#66685f` |
| `--line` | `rgba(38, 38, 28, .18)` |
| `--sans` | `"General Sans", Arial, sans-serif` |
| `--display` | `"Cabinet Grotesk", Arial, sans-serif` |
| `--mono` | `"IBM Plex Mono", Consolas, monospace` |
| `--gutter` | `clamp(24px, 6vw, 92px)` |
| `--max` | `1360px` |

### Cores mais frequentes

| Hex | Ocorrencias |
| --- | --- |
| `#393B23` | 2 |
| `#26261C` | 1 |
| `#6F7352` | 1 |
| `#C6B5A3` | 1 |
| `#F6F4EF` | 1 |
| `#FFFEFA` | 1 |
| `#E5E4DF` | 1 |
| `#24251F` | 1 |
| `#66685F` | 1 |
| `#4D4F46` | 1 |
| `#55574F` | 1 |
| `#4C4E46` | 1 |

### Tipografia

- `FontAwesome` (4 usos)
- `Font Awesome 6 Free` (3 usos)
- `Font Awesome 6 Brands` (2 usos)
- `Font Awesome 5 Free` (2 usos)
- `Font Awesome 5 Brands` (1 usos)

### Forma e ritmo

- `<section>`: 12
- border-radius mais usados: `50%` (6), `8px` (2), `var(--fa-border-radius,.1em)` (1), `72% 44% 58% 48%` (1), `45% 45% 55% 55%` (1)
- 9 h2:
  - Informações essenciais do atendimento
  - Em quais regiões a dor aparece?
  - Comorbidades e histórico também importam.
  - Do sintoma ao próximo passo, em quatro etapas.
  - Opções discutidas após avaliação.
  - Dr. Matheus Cavalcanti
  - Atende seu convênio?
  - Tudo para chegar à sua consulta.
  - Não deixe a dor limitar sua rotina.

### Meio do icone

- healthicons (CDN pinado)
- icon font (Font Awesome)

## Leitura

**Tom:** editorial contemporaneo, quase de revista. Display grotesk pesado + mono para credenciais.

**Metafora condutora:** nao ha declarada. A unidade vem da tipografia (Cabinet Grotesk + IBM Plex Mono) e do verde-oliva.

**O que esta LP ensina:** que stack tipografico fora do Google Fonts (Fontshare) ja diferencia bastante — e o unico caso nosso com tres familias e com mono. Ensina tambem a estrutura de variacao por regiao do corpo: 6 paginas com conteudo clinico proprio, mais paginas hero-only por bairro e por convenio, tres tipos distintos que nao devem ser fundidos.

**Nota tecnica:** a home ainda usa Font Awesome + healthicons por CDN. As 6 paginas de regiao foram migradas para `svg-local` em `public/topic-icons/`, sem dependencia de terceiro em runtime. Vale alinhar a home no proximo toque.

**Ja gasto — nao repetir na proxima LP:**
- fundo creme (`#f6f4ef`)
- verde-oliva + areia (`#393b23` / `#c6b5a3`)
- General Sans / Cabinet Grotesk / IBM Plex Mono
- meio `flat-mono` via `mask-image`
- render 3D de osso como imagem de hero
