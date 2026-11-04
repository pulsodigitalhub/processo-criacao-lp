# Briefing de Landing Page — Visual Tintas Atacado

Fontes: `clients.documents/visual-tintas-onboarding` (02/11/2026), `visual-tintas-pesquisa/docs/respostas-rafael.md` (diagnóstico preenchido + áudios de 17/09/2026). Agência: Hound.

## Contexto

- Empresa ou profissional: Visual Atacadista Ltda (CNPJ 62.125.464/0001-81), braço de atacado da Visual Tintas (NB Comercial de Tintas, varejo em lojavisualtintas.com.br). Decisor: Rafael Alves Freitas.
- Oferta principal: fornecimento de tinta e acessórios no atacado para empresas, com cotação pelo WhatsApp. Linhas: imobiliária (Sherwin-Williams, Resicolor, Suvinil), automotiva (Farben, Lazzuril), massas/seladores/texturas/impermeabilizantes, industrial e piso (epóxi, PU) e acessórios (Condor, EPI).
- Objetivo da página: gerar conversa qualificada de empresa no WhatsApp do atacado (cotação) e levar quem quer ver produto ao catálogo `/catalogo`.
- Tipo: Ads (Meta, verba mínima R$ 1.000/mês) + apoio à prospecção ativa (o vendedor manda o link na cadência).
- Fonte de tráfego: Meta Ads no raio de 10 km da loja; link da prospecção ativa (lista de CNPJs); Google Business Profile do atacado.
- Cidade ou região: DF, só perto da loja (Núcleo Bandeirante, Guará e região). Endereço: Terceira Avenida, Núcleo Bandeirante, Brasília-DF, nos fundos da loja Visual Tintas da Av. Central (Área Especial 19, Lote G). Coordenadas: -15.866809, -47.959807.

## Público e decisão

- Quem chega: comprador ou dono de construtora/incorporadora, empreiteira e pintura predial, condomínio e administradora, funilaria e oficina automotiva, empresa de licitação de pintura. Secundário: lojas menores de tinta, serralherias, movelarias.
- Fora do público: pintor autônomo MEI e quem só compra a prazo longo.
- Momento de busca: precisa comprar volume para obra ou oficina, quer cotação rápida, várias marcas num fornecedor e entrega sem atraso.
- Nível de consciência: conhece produto e marcas; está comparando fornecedor.
- Objeções: "vocês são varejo, não atacado"; "preço não compete com distribuidor grande"; "a cotação demora"; "não tem minha marca ou cor"; "a entrega atrasa a obra"; "preciso de condição de pagamento para empresa".

## Posicionamento

- Promessa central: Cotação de tinta e acessórios para empresas no DF, com várias marcas num só pedido e atendimento técnico perto da sua obra.
- Diferenciais (declarados pelo Rafael, conferir antes de publicar):
  - Várias marcas num só lugar (confirmado no histórico de vendas 2025–2026: Sherwin-Williams, Suvinil, Coral, Resicolor, Lazzuril, Farben, Condor, 3M, Norton e outras).
  - Atendimento técnico para escolher o produto certo.
  - 30 anos de nome na região.
  - Máquina tintométrica, cores imobiliárias e automotivas (confirmado no histórico de vendas).
- Provas: mais de 3 mil itens em catálogo; loja física; fotos oficiais dos fabricantes para produtos; fotos do estoque [A VALIDAR, captação nesta semana]. Depoimentos e notas do Google não serão usados na página.
- Compliance: proibido preço de Sherwin-Williams, Suvinil e Lazzuril em site ou anúncio. Regra da página: nenhum preço de nenhuma marca. Sem promessa de menor preço (Rafael diz que perde venda por preço). Não citar pedido mínimo de R$ 10 mil da entrega direta.

## Conversão

- CTA primário: "Pedir cotação no WhatsApp".
- Destino: WhatsApp por handler rastreado (nunca `wa.me` direto no href). Mensagem padrão: "Olá! Vim pelo site do atacado da Visual Tintas. Sou da empresa ____ (CNPJ ____) e quero cotar: ____". Número: (61) 99874-8169 (`wa 5561998748169`) — provisório, número do varejo.
- CTA secundário: "Ver catálogo de produtos" → `/catalogo` (sem preço; lista de orçamento também sai pelo WhatsApp).
- Formulário: nenhum; a qualificação (empresa, CNPJ, segmento) vai na mensagem e no atendimento.
- Eventos: `whatsapp_click` (GA4 `generate_lead`, Meta `Contact`) com a seção de origem; `catalog_click`. Consent Mode v2 antes das tags.

## Ativos

- Identidade visual: logo em Drive HOUND/Clientes - HOUND/Visual Tintas/04 Material do Cliente. Paleta e tipografia: tirar do site do varejo no mapa visual.
- Fotos e vídeos: usar fotos oficiais dos fabricantes coletadas da internet para produtos. Fotos do estoque [A VALIDAR, captação nesta semana].
- Referências: Gravia (gravia.com) no catálogo; biblioteca-design no mapa visual.
- Contato: seg a sex 8h–18h, sáb 8h–12h (Francisco Magno). Endereço: Terceira Avenida, Núcleo Bandeirante, Brasília-DF, nos fundos da loja Visual Tintas da Av. Central (Área Especial 19, Lote G). WhatsApp: (61) 99874-8169 (`wa 5561998748169`) — provisório, número do varejo.
- Privacidade: controlador Visual Atacadista Ltda; canal do titular [A VALIDAR]; GTM, GA4, Meta Pixel.
- Domínio: visualtintasatacadista.com.br; zona Cloudflare criada em 03/11/2026 (NS ara/drew.ns.cloudflare.com); `noindex` até aprovação.
- Formas de pagamento: fora da página por decisão do cliente.

### Pendências `[A VALIDAR]`

1. Número próprio do WhatsApp do atacado (futuro).
2. Fotos do estoque.
3. Canal do titular de dados.
