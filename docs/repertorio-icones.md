# Repertório de Ícones

Escolher ícone de card é uma decisão **visual**. Este documento existe porque tratá-la como decisão textual já produziu, numa LP de ortopedia real, um ícone de pulso cardíaco num card de coluna, um ícone de joelho num card de coluna, e um cadeado de segurança num card de sintoma.

## A regra

**Nenhum ícone é aprovado sem ter sido renderizado e olhado, no tamanho real de uso.**

Escolher pelo nome não funciona, e não é questão de procurar melhor. Dois casos reais, ambos invisíveis numa lista de texto:

- `healthicons:joints-outline` se chama "joints" e **desenha um joelho**. Foi parar em "Articulações da coluna".
- Buscar `cervical` retorna **colo do útero** e **gravata**. Em inglês médico, "cervical" não é pescoço.

Nenhuma revisão de nomes, por mais caprichada, pega isso.

## Método, por card

### 1. Descrever o que o card significa, em português

Uma frase curta, antes de buscar. "Crises recorrentes" numa página de coluna = *piora recorrente de dor na coluna*, não "algo que pareça um alerta".

Essa frase vai no campo `conceito` do `cards.json`, **em português**. É ela que casa contra a base do passo 2. Escrever o conceito direto em inglês é onde nascem os erros: a busca da Iconify é em inglês e devolve homônimos com cara de acerto (`disc` → CD, `thumb` → joinha, `click` → cursor de mouse, `lock` → cadeado de UI, `tear` → rosto chorando).

### 2. Consultar o que já foi validado — antes de buscar qualquer coisa

```
ferramentas/mapear-conceitos.py cards.json especialidades/<esp>/conceitos.md -o mapeamento.json
```

`especialidades/<esp>/conceitos.md` acumula os pares conceito→ícone que LPs anteriores já validaram olhando. Numa LP de ortopedia com 72 cards, **60 (83%) foram resolvidos aqui**, sem busca nova.

Este passo não é opcional nem uma otimização: pular direto para a busca foi a causa de uma entrega com balança de tribunal para "instabilidade", balão de festa para "inchaço" e raio elétrico para "formigamento" — todos com resposta já validada neste arquivo, que ninguém abriu. Por isso o `harvest-candidatos.py` recusa `cards.json` cru.

O script também avisa quando o conceito está na lista **"sem ícone literal"**, e quando o mesmo ícone casou com dois cards da mesma página.

### 3. Colher vários candidatos, de toda a base

```
ferramentas/harvest-candidatos.py mapeamento.json -o candidatos/ --meio flat-mono
```

Busca em **toda a Iconify (215 sets, ~308 mil ícones)** apenas para os cards que a base não resolveu, e baixa ~10 candidatos cada.

Use vários termos por card, incluindo o termo clínico e o termo leigo. Limitar a busca a poucos sets conhecidos foi justamente o que escondeu, numa LP de ortopedia, que existiam `game-icons:knee-cap`, `streamline-ultimate:medical-specialty-knee-1` e `hugeicons:back-muscle-body`.

**`--meio` define o que é aceitável**, porque o meio do ícone é uma alavanca de diferenciação entre clientes, não uma constante: `flat-mono` (Dr. Matheus), `3d-clay` (Dr. Rodrigo Pires), `color-emoji` (Dra. Genésia Regina, com openmoji colorido). A lista de sets bloqueados depende do meio — sets de emoji são bloqueados em `flat-mono` e liberados em `color-emoji`.

### 4. Renderizar e olhar

```
ferramentas/contact-sheet.py candidatos/ --ja-usados mapeamento.json
```

Monta um grid com cada candidato a **32px (tamanho real) e 96px**, ao lado do título do card, e **tarja os ícones já gastos naquela mesma página** — atacando a repetição no momento da escolha, não só na validação final.

Critério, por ícone: *olhando só o desenho, sem ler o título, dá pra dizer que parte do corpo/órgão é e qual é o problema?*

O 32px é o que decide. Ícone que só funciona grande não serve.

**A base propõe o melhor match, não a escolha final.** `mapear-conceitos.py` devolve o ícone semanticamente mais próximo de cada conceito — e é normal que dois cards da mesma página recebam o mesmo. Quando isso acontece o script avisa (`REPETIDO em 'X'`), e aí a escolha é sua: manter o ícone no card mais central e trocar os outros por alternativas (a própria base costuma ter variantes registradas para a mesma região).

Exemplo real: numa LP de ortopedia a base devolveu `tabler:bandage` para "inchaço", "tendinite patelar" e "bursite" na mesma página. A entrega ficou com bandage no inchaço, `game-icons:knee-bandage` na tendinite e `healthicons:pain-outline` na bursite. Rodar o mapeamento de novo depois mostra "divergência" nesses cards — não é erro, é a regra de página funcionando.

### 5. Escolher, e checar a página inteira

Sem repetir o mesmo ícone em dois cards da mesma página — nem dentro de uma seção, nem entre seções. Entre páginas diferentes, reuso é permitido.

Quando o conceito não tem ícone literal em lugar nenhum — confirmado por busca, não por suposição — use o ícone anatômico mais próximo **da mesma região do corpo**, nunca um de outra especialidade nem uma forma abstrata "que transmite a ideia". Registre a busca vazia como evidência. Remover o card é uma saída legítima e já foi usada (ver `projetos/dr-rodrigo-pires/mapa-icones.md`); forçar um ícone ambíguo, não.

### 6. Validar por comando

```
ferramentas/validar-mapa-icones.py projetos/<cliente>/mapa-icones.md
```

Sai com 1 se houver ícone repetido na página, "conferido a 32px" diferente de sim, ou arquivo fora da pasta do tópico. As três regras existiam só como texto neste documento e mesmo assim foram violadas ao vivo — agora falham o checklist.

### 7. Devolver o aprendizado, depois da LP aprovada

```
ferramentas/promover-conceitos.py projetos/<cliente>/mapa-icones.md especialidades/<esp>/conceitos.md
```

Propõe os pares novos para a base — **imprime o diff, não escreve**. Só rode depois da LP publicada e aprovada: ícone escolhido mas não publicado ainda não virou conhecimento.

Sem esse passo a base não cresce. Já aconteceu de o único ícone novo de uma entrega ficar registrado como "vale registrar numa próxima PR" e nunca ser registrado.

### Saúde da base

`ferramentas/auditar-cobertura.py` verifica se os ícones da base ainda resolvem (link rot) e quais sets úteis estão fora da lista `PRIORIDADE` do harvest. Foi assim que `icon-park-outline`, `mingcute` e `material-symbols-light` foram promovidos — os três já apareciam como bons candidatos e a ordenação os jogava para o fim.

## Organização por região

Uma pasta por região/agrupamento, um arquivo por card, nomeado pelo slug do título do card:

```
assets/topic-icons/
  coluna/dor-lombar-persistente.svg
  joelho/lesoes-de-menisco.svg
  ...
```

Isso transforma "o ícone tem que ser da região certa" em regra mecânica: **card da página `X` só pode usar ícone de `X/`**. Um ícone de joelho numa página de coluna passa a ser estruturalmente impossível, em vez de depender de alguém notar.

O agrupamento varia por especialidade — em ortopedia é região do corpo; em ginecologia pode ser fase da vida ou procedimento; em cardiologia, estrutura ou exame. O que não varia é a regra de pasta.

## Não desenhar à mão

Já foi tentado, com spec de traço, e o resultado foi pior que a biblioteca: desenho amador não sustenta uma LP de cliente. Ícone de card vem de biblioteca validada. O esforço vai para a **escolha**, não para o traço.

## Onde isso entra no processo

Fase de Copy (`docs/processo-de-criacao.md`), registrado em `templates/mapa-icones.md`, com o gate em `docs/checklists.md`.
