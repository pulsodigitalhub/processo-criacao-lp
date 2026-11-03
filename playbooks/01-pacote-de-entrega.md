# Pacote de entrega para cliente de saúde

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

Cada cliente de saúde recebe este pacote, nesta ordem.

1. Criar o repositório privado `pulsodigitalhub/lp-<cliente>` antes do primeiro HTML. Configurar o autor Git como `pulsodigitalhub <313041462+pulsodigitalhub@users.noreply.github.com>`. Sem isso, a Vercel recusa o deploy por Git.
2. Publicar a página principal na raiz do domínio. Ela serve como perfil do Google Meu Negócio e como LP geral das campanhas.
3. Criar variações de campanha em `variacoes/<slug>/`, conforme o playbook 04.
4. Criar o site institucional em `/institucional/`, conforme o playbook 05.
5. Publicar a política de privacidade.
6. Configurar o sitemap padrão a partir dos templates deste repositório.
7. Apontar o domínio da Cloudflare da Pulso para a Vercel do time Pulso.
8. Executar o fechamento, conforme o playbook 07.

| entrega | onde fica | quem consome |
| --- | --- | --- |
| Página principal | Raiz do domínio | Google Ads, Google Meu Negócio, Link HUB, Google orgânico |
| Variações de campanha | `variacoes/<slug>/` | Google Ads, Google orgânico |
| Site institucional | `/institucional/` | Google Meu Negócio, Link HUB, Google orgânico |
| Política de privacidade | Rota pública | Google Ads, Google orgânico |
| Sitemap | Raiz do domínio | Google orgânico |

## Checado pelo gate

- LP fora de repositório git com origin: FALHA.
- Faltar sitemap.xml, sitemap.xsl, scripts/generate-sitemap.mjs ou .github/workflows/sitemap.yml: FALHA.
- Página publicável fora do sitemap.xml: FALHA.
- Sem política de privacidade: FALHA.
