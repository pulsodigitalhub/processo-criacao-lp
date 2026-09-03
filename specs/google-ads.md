# Spec: LP de Google Ads

Contrato minimo para Landing Pages destinadas a campanhas pagas (Google Ads, Meta Ads, Kwai Ads). O objetivo e proteger o Quality Score, a atribuicao de conversao e a coerencia entre anuncio e pagina.

## Message match

- Titulo do hero repete a promessa central do anuncio (verbo + beneficio + publico).
- Se a campanha tem varios anuncios, cada grupo aponta para uma LP ou secao com match especifico. Nao mandar todo o trafego para uma pagina generica.
- A imagem ou cor dominante do hero conversa com o criativo do anuncio quando possivel.

## CTA e conversao

- Um unico CTA primario por LP. CTAs secundarios podem existir, mas nao podem competir por atencao no primeiro viewport.
- **Rodape sem telefone, WhatsApp direto, e-mail ou qualquer canal fora do CTA rastreado.** Toda conversao precisa passar por evento mensuravel. Um canal solto no rodape vaza conversao e destroi a atribuicao da campanha.
- Formulario curto: nome, telefone e no maximo um campo condicional. Cada campo extra reduz CVR.
- Politica de privacidade linkada. Consentimento LGPD explicito antes do submit.

## Tracking

- GA4 ou GTM configurado antes do deploy, nao depois.
- Evento de conversao (form_submit, whatsapp_click, phone_click quando aplicavel) testado com o proprio DevTools antes de ligar a campanha.
- Se o CTA leva a WhatsApp: usar um handler de clique que empurra o evento pro `dataLayer` e **em seguida** navega para `wa.me`/`api.whatsapp.com`. O `href` do link continua sendo o destino final real (`https://wa.me/<numero>`), para que a falha do JS leve a pessoa ao WhatsApp e nao a um erro.
- **Proibido** apontar o `href` para redirecionador de terceiro ou dominio proprio de tracking (`.../go/...`, encurtadores, bridge externa). Cross-domain redirect a partir do anuncio e classificado como *destination mismatch* e *circumventing systems*, e a penalidade e suspensao da conta sem aviso previo.
- **Proibido** criar pagina intersticial com `noindex` + redirecionamento automatico (`window.location`, `<meta http-equiv="refresh">`). Essa combinacao e a assinatura de *sneaky redirect*.
- **Proibido** listar qualquer pagina de redirecionamento no `sitemap.xml` — isso entrega o padrao diretamente ao rastreador do Google.
- Google Tag ou Meta Pixel disparando pageview e evento de conversao. Verificar em Tag Assistant ou equivalente.

## Por que estas regras existem

Em 03/09/2026 a conta de Google Ads de um cliente foi suspensa por phishing. A LP seguia a redacao anterior desta spec, que mandava "intermediar por uma bridge page". A implementacao escolhida foi um redirecionador de terceiro (`sistema.pulso.marketing/go/<cliente>`) no `href` de 100 links, mais uma pagina `/agendar/` com `noindex` e `window.location` automatico, listada no `sitemap.xml`. Os tres elementos juntos sao exatamente o padrao que o Google classifica como redirecionamento enganoso.

O redirecionador ainda estava retornando HTTP 502 quando o incidente foi investigado, ou seja: alem do padrao suspeito, o destino estava quebrado.

Licao: o evento de conversao pode e deve ser disparado por handler no proprio dominio. Nao existe motivo tecnico para tirar o usuario do dominio anunciado antes de entregar ele no destino prometido.

## Consentimento e Consent Mode v2

Toda LP em Ads que carregue GA4, Google Ads, Meta Pixel, Microsoft Clarity ou similar precisa de Consent Mode v2 nativo do GTM ativo desde o primeiro pageview. Sem isso, os pixels rodam sem consentimento LGPD e a LP fica exposta a reclamacoes na ANPD, alem de perder atribuicao quando o titular exercer direito de oposicao.

### Estado default antes do GTM

Registrar `consent 'default'` no `<head>`, ACIMA da tag do GTM. Depois nao funciona — o Consent Mode v2 exige que o default seja lido antes do primeiro pageview.

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });
  try {
    const saved = localStorage.getItem('{marca}_consent_v1');
    if (saved) gtag('consent', 'update', JSON.parse(saved));
  } catch (e) {}
</script>
```

### Banner de consentimento

- **Nao-modal, fixed bottom.** Nao bloquear scroll nem interacao. LGPD nao exige modal e a UX de nao-modal e superior.
- **Dois botoes minimos:** aceitar tudo (primario) e usar apenas essenciais (secundario). Botao "personalizar" e opcional na primeira versao.
- **Sem X de fechar.** Fechar sem escolher = manter default (denied). Nao criar caminho de "adiar" que sugira consentimento implicito.
- **Persistir escolha** em `localStorage` com chave versionada (`{marca}_consent_v1`). Ao mudar politicas de tracking, incrementar a versao para refetch de consent.
- **Expor mecanismo de reabrir** (ex: `window.reopenConsent()`) para a Politica de Privacidade linkar.

### Ferramentas fora do consent mode nativo

Consent Mode v2 cobre tags do Google. Terceiros exigem chamada propria no handler de aceitar/rejeitar:

- **Microsoft Clarity:** `window.clarity('consent', bool)`.
- **Meta Pixel:** carregar somente se `ad_storage === 'granted'`, ou usar `fbq('consent', 'grant'|'revoke')`.
- **Hotjar, Amplitude, PostHog:** cada um tem API propria — nao esquecer.

### O que a Politica de Privacidade precisa cobrir

- Categorias de cookies (essenciais, analise, mensuracao de origem).
- Como gerenciar preferencias (com botao que chama o mecanismo de reabrir o banner).
- Nao afirmar explicitamente "legitimo interesse" como base para publicidade/remarketing — a ANPD tende a exigir consentimento para esses casos. Deixar a base legal como definicao interna do controlador.

### Efeito sobre atribuicao

UTMs e `gclid` viajam pela URL, nao dependem de cookie. Mesmo com consent negado, a atribuicao de conversao ao anuncio (via gclid + evento na bridge page) e preservada. O que se perde: remarketing (audiencia sem cookie), sessao gravada (Clarity) e cross-session. Consent Mode v2 recupera parte disso via modelagem de conversao do Google.

## Performance e mobile

- LCP < 2,5s em conexao mobile 4G. Imagens em WebP, fontes com `preconnect` e `display=swap`.
- Hero e CTA renderizados sem depender de scroll no viewport 375px.
- Nenhuma imagem decorativa carrega antes de promessa e CTA aparecerem.
- Formulario funciona com teclado virtual sem esconder o botao de submit.

## Indexacao

- **Nao** usar `noindex` em producao — historial de LP afeta Quality Score futuro.
- Meta description coerente com o anuncio.
- URL curta, legivel e sem parametros de tracking indexaveis.

## Coerencia com o setor

- Se a LP e de saude, tambem se aplica `specs/saude.md`. Regras se somam, nao se substituem.
- Se a oferta e produto, tambem se aplica `specs/ecommerce.md`.

## Gates

- [ ] Titulo do hero faz message match com o anuncio.
- [ ] CTA primario e unico e visivel no primeiro viewport.
- [ ] Rodape nao contem telefone, WhatsApp ou canal direto sem tracking.
- [ ] Evento de conversao configurado e testado.
- [ ] LCP mobile abaixo de 2,5s.
- [ ] Politica de privacidade linkada.
- [ ] Pagina indexavel (nenhum `noindex` acidental).
- [ ] `gtag('consent', 'default', ...)` registrado ANTES do GTM, com defaults negados.
- [ ] Banner de consentimento nao-modal aparece no primeiro pageview e nao reaparece apos escolha.
- [ ] Rejeitar dispara `update` com denied; DevTools confirma requests para `google.com/ccm/collect` com `_p=1` (cookieless pings), sem `cid`/`sid`.
- [ ] Politica de Privacidade tem botao "Gerenciar preferencias" que reabre o banner.
- [ ] Terceiros fora do consent mode nativo (Clarity, Meta Pixel etc.) tem chamada propria no handler.
- [ ] Nenhum `href` de ancora aponta para dominio de terceiro fora da allowlist (`wa.me`, `api.whatsapp.com`, mapa, redes do cliente).
- [ ] Nenhum link interno aponta para arquivo inexistente no output do build.
- [ ] Nenhuma pagina combina `noindex` com redirecionamento automatico.
- [ ] `sitemap.xml` nao lista pagina de redirecionamento nem URL inexistente.
- [ ] Politica de privacidade linkada e hospedada no proprio dominio anunciado.
- [ ] `robots.txt` nao bloqueia `AdsBot-Google`.
- [ ] `scripts/check-google-ads-compliance.mjs` rodou e retornou `RESULTADO: PASS`.
