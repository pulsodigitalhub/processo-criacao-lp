# Prontuário das LPs — o que já usamos

Índice do que cada LP nossa já ocupou. Existe porque `docs/checklists.md` manda comparar cada LP nova com as últimas publicadas para evitar "LP irmã", e até agora não havia com o que comparar: só um projeto tinha artefato registrado, e `visual-repertorio/03-cartoes-referencia/` só guarda referências externas (Stripe, Linear, Notion...).

Os cartões são gerados por `ferramentas/extrair-identidade.py` **a partir da página no ar**, nunca do markdown do projeto. Isso não é preciosismo: o `mapa-icones.md` do Dr. Rodrigo Pires documenta SVGs flat recoloridos em `#d4b589`, e a página publicada usa 15 ícones 3D em WebP — nenhum deles. Artefato envelhece em silêncio; página no ar, não.

A parte mecânica (tokens, paleta, tipografia, seções, meio do ícone) sai do script. Tom, metáfora condutora e "o que não repetir" são escritos à mão.

## O que está ocupado

| | Fundo | Acento | Tipografia | Meio do ícone | Metáfora |
| --- | --- | --- | --- | --- | --- |
| [Dr. Gustavo Pimpão](dr-gustavo-pimpao.md) | off-white `#f8f4ee` | **vinho `#a01a2a`** | IBM Plex Sans | a inspecionar | — |
| [Dr. Luiz Sarmanho](dr-luiz-sarmanho.md) | off-white `#f7f4ef` | petróleo `#2f4652` | Manrope | a inspecionar | — |
| [Dr. Matheus Cavalcanti](dr-matheus-cavalcanti.md) | off-white `#f6f4ef` | oliva `#393b23` + areia `#c6b5a3` | Cabinet Grotesk + IBM Plex Mono | `flat-mono` | — |
| [Dr. Rodrigo Pires](dr-rodrigo-pires.md) | creme `#f3ebde` | navy `#212e51` + gold `#d4b589` | Montserrat | `3d-clay` raster | — |
| [Dr. Thiago Cerqueira](dr-thiago-cerqueira.md) | off-white `#f6f7f5` | verde `#6e8f71` + dourado `#b4863f` | Inter | a inspecionar | — |
| [Dra. Genésia Regina](dra-genesia-regina.md) | creme `#fffdf5` | marrom `#7e552f` + sálvia `#90a570` | Playfair Display + Poppins | `color-emoji` | **árvore da vida** |
| [Dra. Lara Andrade](dra-lara-andrade.md) | off-white `#f7f4f1` | marrom `#6f5547` + `#a68a7a` | Montserrat | a inspecionar | — |
| [Rafael Rocha](rafael-rocha.md) | — | azul `#1d4e6b` + ciano `#5bb4d0` | Inter | a inspecionar | — |

## O que isso diz para a próxima LP

**O fundo é o problema, não o acento.** Sete das oito têm fundo off-white quente, entre `#f3ebde` e `#fffdf5` — uma faixa estreitíssima. Já os acentos são bem variados (vinho, petróleo, oliva, navy, verde, marrom, azul) e a tipografia também (Montserrat ×2, Inter ×2, IBM Plex Sans, Manrope, Playfair+Poppins, Cabinet Grotesk).

Ou seja: a sensação de "LP irmã" não vem de repetirmos cor de marca — vem de **todas partilharem a mesma tela de fundo**. É o elemento que ocupa mais área da página e o único que quase não varia. A próxima LP sair do off-white quente resolve mais que qualquer troca de acento.

**Só uma das oito tem metáfora condutora declarada — e é a que a agência mais gostou.** A da Genésia (árvore da vida) organiza logo, paleta, ilustração e ritmo de seção ao mesmo tempo. As outras têm unidade só por paleta e tipografia, e foi entre duas delas que apareceu a crítica "está praticamente idêntico ao Dr. Matheus Cavalcanti". A hipótese que este prontuário sustenta: **a metáfora carrega mais diferenciação que a paleta.** Vale tratar como requisito da próxima LP, não como enfeite.

**Meios de ícone:** três identificados (`flat-mono`, `3d-clay`, `color-emoji`), cinco ainda por inspecionar — a detecção automática cobre só assinaturas conhecidas e falha silenciosamente em stacks novas. Confirmar à mão antes de usar a coluna como veto.

## Como usar

1. Antes de decidir direção visual, ler a tabela acima e a seção "Já gasto" de cada cartão.
2. Levar para o mood board o que está **vetado**, não só o que se quer usar.
3. Depois de publicar a LP nova, gerar o cartão dela e acrescentar aqui.

Reaproveitar elemento de LP nossa é permitido — desde que reinterpretado e registrado no `visual-map`, nunca copiado como bloco. É o mesmo limite que `docs/repertorio-visual.md` já impõe para referência externa.
