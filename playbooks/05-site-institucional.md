# Site institucional

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

## Definição da casa

Decisão do Sérgio em 29/10/2026: o site institucional é uma subpágina em `/institucional/`, dentro do mesmo repositório e do mesmo domínio da LP.

É uma cópia exata da LP geral de campanhas. Todas as seções ficam, na mesma ordem, inclusive a faixa de números. Não se tira seção nenhuma. Mudam só duas coisas.

1. O título e o H1, que passam a ser o nome do médico, como no institucional do Dr. Pedro.
2. O endereçamento. Não há formulário nem webhook, e todo CTA vira link direto para o WhatsApp do médico ou da clínica, com mensagem pronta e a unidade quando o botão for de unidade.

Este é o único local em que `wa.me` direto é permitido, pois o institucional não é destino de anúncio.

Ele entra no Link HUB como botão "Institucional", do tipo site. É gerado pelo mesmo script das variações, a partir da página principal, para nunca ficar diferente da LP. Referência: pulsodigitalhub/lp-dr-breno-lima, scripts/gerar_variacoes.py, função render_institucional.

## O que não é institucional

Os sites do Rodrigo e do Matheus, `site-dr-*`, são migrações de WordPress em repositórios e domínios próprios. Não são o padrão para cliente novo.

Em 29/10/2026 a primeira versão do institucional do Breno foi feita como página nova, com conteúdo expandido e sem a faixa de números. Estava errada e foi refeita como cópia da LP.

## Checado pelo gate

- Entra no sitemap.xml e passa pelas mesmas checagens de página publicável.
- O wa.me direto precisa estar na allowlist do .checker-lp.json do projeto.
