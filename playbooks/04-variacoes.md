# Variações de campanha

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

Variações são páginas estáticas geradas a partir da página principal. O gerador de referência é `pulsodigitalhub/lp-dr-breno-lima`, em `scripts/gerar_variacoes.py`.

Nunca carregar variações por JavaScript. O padrão antigo do Pedro, que troca apenas o H1 via fetch, não serve para anúncio porque o Google lê o HTML.

## Tipos e prioridade

Prioridade definida pelo custo por conversão medido nas contas Pulso de ortopedia no DF, entre julho e outubro de 2026.

1. Região do corpo
   Pé e tornozelo, R$ 16 a 32.
   Mão e punho, R$ 15 a 43.
   Quadril, R$ 17 a 50.
   Coluna, R$ 20 a 47.
   Joelho, R$ 22 a 188.
   Ombro, R$ 21 a 81.
2. Bairro da unidade, R$ 20 a 43.
3. Convênio, R$ 17 a 43.
4. Procedimento por último. Infiltração, R$ 57 a 107.

## Regras por variação

Mudar title, H1, descrição e texto do hero. Colocar o card do tema em primeiro lugar. Levar a origem ao rastreio no formato `<slug>:<secao>`. Definir canonical próprio para cada variação e remover o canonical herdado da página base.

Confirmar com o médico se ele atende cada região antes de anunciar.

## Checado pelo gate

- Variação fora do sitemap.xml: FALHA.
- Foto repetida e depoimento de exemplo valem também nas variações.
