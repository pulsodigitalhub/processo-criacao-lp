# Site institucional

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

## Definição da casa

Decisão do Sérgio em 29/10/2026: o site institucional é uma subpágina em `/institucional/`, dentro do mesmo repositório e do mesmo domínio da LP.

É uma cópia da LP geral de campanhas com três diferenças.

1. Não tem formulário.
2. Não tem webhook.
3. Todos os CTAs levam diretamente ao WhatsApp do médico ou da clínica.

Este é o único local em que `wa.me` direto é permitido, pois o institucional não é destino de anúncio.

Ele entra no Link HUB como botão "Institucional", do tipo site. Gerar a página a partir da página principal, como as variações.

## Exceção registrada

O Dr. Breno Lima tem um institucional próprio, com conteúdo expandido e formulário. Ele é mantido como está por decisão do Sérgio.

Não confundir com os sites do Rodrigo e do Matheus, `site-dr-*`. Eles são migrações de WordPress em repositórios e domínios próprios, e não são o padrão para cliente novo.

## Checado pelo gate

- Entra no sitemap.xml e passa pelas mesmas checagens de página publicável.
- O wa.me direto precisa estar na allowlist do .checker-lp.json do projeto.
