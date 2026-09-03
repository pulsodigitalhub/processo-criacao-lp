# Checklists e Auditoria

Checklists tornam a revisao repetivel. Eles nao substituem julgamento, mas impedem que a qualidade dependa apenas da memoria de quem entregou.

## Estrategia

- Publico, problema e momento de decisao estao definidos.
- Promessa central cabe em uma frase.
- Provas disponiveis sao reais e suficientes para a promessa.
- Objecoes foram mapeadas.
- CTA primario tem verbo, beneficio e destino definidos.
- Tipo de pagina e fonte de trafego estao claros.

## Copy

- Primeiro viewport explica o que e, para quem e e qual acao tomar.
- Titulos contam a historia em sequencia.
- Beneficios sao concretos e nao dependem de adjetivos vazios.
- Provas aparecem antes dos CTAs de maior compromisso.
- FAQ responde duvidas ou riscos reais.
- Nao ha promessas absolutas, inventadas ou vedadas pelo setor.

## Design

- Cada secao relevante possui funcao e decisao visual registrada.
- Referencias do repertorio foram citadas por ID no mapa visual.
- Layout simples foi escolha estrategica, nao preenchimento automatico.
- Imagens e icones possuem funcao.
- Nenhuma foto se repete na pagina. Duas fotos diferentes do medico e ok; a mesma foto duas vezes nao — ver `docs/uso-de-fotos.md`.
- Cada icone de card foi renderizado e OLHADO a 32px antes de ser aprovado (contact sheet), nao escolhido pelo nome.
- Cada icone tem linha no `mapa-icones.md`, com o que o desenho mostra e a marcacao de conferido.
- Nenhum icone repetido em dois cards da mesma pagina; card da pagina X so usa arquivo de `topic-icons/X/`.
- Hierarquia, contraste e leitura estao claros.
- Mobile foi revisado sem textos estourando ou controles inacessiveis.
- A pagina nao e apenas uma mudanca de cor de outro projeto.
- A LP nao parece irma das ultimas tres entregas — comparar screenshot com as ultimas LPs publicadas em `previews/` antes de fechar o build. Se paleta, tipografia, tratamento de botoes e cards batem em bloco, redesenhar puxando identidade do cliente (ver `docs/processo-de-criacao.md` §4.1).
- O visual-map do projeto tem a secao "Puxado do site do cliente" preenchida — paleta, tipografia e tratamento observados no site real, e o que a LP vai puxar de la.

## Desenvolvimento

- Formularios, links e CTAs foram testados.
- Eventos de conversao foram configurados e validados.
- O briefing identifica o controlador, o canal de privacidade e a politica aplicavel.
- A politica nao atribui automaticamente a Pulso o papel de controlador: a funcao de cada parte foi validada para o projeto.
- Se houver uma politica central da Pulso, a LP tambem identifica claramente o controlador do atendimento e fornece acesso ao aviso complementar do cliente quando necessario.
- O banner de cookies separa itens essenciais de medicao/publicidade e permite revisar a escolha.
- Imagens e fontes nao prejudicam o carregamento inicial.
- HTML possui estrutura semantica, idioma, viewport e alternativas de texto quando aplicavel.
- Responsividade e navegacao por teclado foram revisadas.
- Metadados, indexacao e schema seguem o objetivo da pagina.
- Se a LP mora em repo proprio do cliente: `scripts/generate-sitemap.mjs` + `.github/workflows/sitemap.yml` + `sitemap.xsl` estao configurados, com o dominio de producao real (nao o subdominio da Vercel) confirmado por canonical/og:url ao vivo — ver `AGENTS.md` §"Ao construir a LP".

## Compliance Google Ads

Verificado por `scripts/check-google-ads-compliance.mjs`, nao por leitura manual. Rodar sobre o output publicado, nao sobre a fonte que se acha que foi publicada.

**Bloqueantes** (reprovam a entrega):

- Nenhum `href` de ancora aponta para dominio de terceiro fora da allowlist (`wa.me`, `api.whatsapp.com`, mapa, redes do cliente). Redirecionador proprio ou de fornecedor no `href` e *destination mismatch*.
- Nenhum link interno aponta para arquivo que nao existe no output do build.
- Nenhuma pagina combina `noindex` com redirecionamento automatico (assinatura de *sneaky redirect*).
- `sitemap.xml` nao lista pagina de redirecionamento nem URL inexistente.
- Toda pagina linka politica de privacidade, hospedada no proprio dominio anunciado.
- `robots.txt` nao bloqueia `AdsBot-Google`.

**Avisos** (nao reprovam, mas vao registrados): Consent Mode v2 ausente ou depois do GTM, `noindex` em producao, metadados basicos faltando (`lang`, viewport, `title`, description).

## Regra de saida

Uma LP nao esta pronta porque o layout parece completo. Ela esta pronta quando o checklist foi revisado sobre a versao final e as pendencias restantes estao registradas de forma explicita.
