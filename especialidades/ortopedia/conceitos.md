# Ortopedia — conceitos e ícones já validados

Índice para a próxima LP de ortopedia não recomeçar do zero. Todos foram escolhidos por revisão visual e estão em uso em LPs publicadas.

**Como usar:** este arquivo é consultado por `ferramentas/mapear-conceitos.py` **antes** de qualquer busca na Iconify. A coluna `Aliases` é o que o script casa contra o campo `conceito` do `cards.json` — quanto mais alias, mais cards são resolvidos por reaproveitamento em vez de busca nova. `Procedência` registra qual LP validou aquele par.

Formato das colunas é contrato do parser (`ferramentas/conceitos.py`). Mudar nome ou ordem de coluna quebra a leitura com erro explícito — não em silêncio.

## Situação / sintoma (o que o paciente vive)

| Conceito | Ícone | Aliases | Procedência |
| --- | --- | --- | --- |
| Dor lombar / curvado com dor | `healthicons:back-pain-outline` | dor lombar; lombalgia; dor nas costas; curvado de dor | dr-thiago-cerqueira |
| Dor de cabeça e pescoço | `healthicons:headache-outline` | dor cervical; dor no pescoço; cefaleia | dr-thiago-cerqueira |
| Andar com apoio / limitação | `healthicons:walk-supported-outline` | limitação no dia a dia; dificuldade para andar; apoio para caminhar | dr-thiago-cerqueira |
| Caminhar | `healthicons:walking-outline` | dor ao caminhar; marcha; caminhada | dr-thiago-cerqueira |
| Mancar / bengala | `healthicons:cane-outline` | claudicação; mancar; bengala | dr-thiago-cerqueira |
| Muleta | `healthicons:crutches-outline` | muleta; apoio para locomoção | dr-thiago-cerqueira |
| Queda / cair | `game-icons:falling` | instabilidade; sensação de falseio; joelho falseando; medo de cair; perna cedendo | dr-thiago-cerqueira |
| Trauma / após queda | `healthicons:traumatism-outline` | trauma; após queda; pancada | dr-thiago-cerqueira |
| Lesão com tipoia | `material-symbols:personal-injury-outline` | lesão ligamentar; entorse; lesão aguda | dr-thiago-cerqueira |
| Subir escadas | `material-symbols:stairs-outline` | dor ao subir escadas; descer degraus; escada | dr-thiago-cerqueira |
| Dormir / dor noturna | `material-symbols:bed-outline` | dor ao dormir; dor noturna; dor ao deitar de lado; piora à noite | dr-thiago-cerqueira |
| Correr / esporte | `healthicons:running` | dor após atividade física; corrida; treino; esporte | dr-thiago-cerqueira |
| Treino / carga | `healthicons:weights-outline` | sobrecarga; levantar peso; carga; esforço repetitivo | dr-thiago-cerqueira |
| Exercício / retorno | `healthicons:exercise-outline` | retorno ao esporte; volta à atividade; reabilitação | dr-thiago-cerqueira |
| Recorrência / ciclo | `solar:repeat-outline` | recorrente; repetido; crises repetidas; entorses de repetição | dr-thiago-cerqueira |
| Sinal de alerta | `healthicons:alert-triangle-outline` | sinal de alerta; quando procurar; atenção | dr-thiago-cerqueira |
| Calçado | `tabler:shoe` | calçado; sapato; palmilha | dr-thiago-cerqueira |
| Estalos / ruído articular | `solar:bone-crack-outline` | estalos; estalo; crepitação; ruído articular; estalos / travamento articular; estalos ou travamento; estalos no movimento; estalos ao mover os dedos | dr-matheus-cavalcanti |
| Rigidez matinal ao acordar | `solar:stretching-outline` | rigidez ao acordar; rigidez matinal; travado de manhã | dr-matheus-cavalcanti |
| Dificuldade para vestir roupa | `tabler:shirt` | vestir roupa; pentear o cabelo; gesto acima da cabeça | dr-matheus-cavalcanti |
| Rigidez e perda de mobilidade | `mingcute:flexibility-line` | perda de mobilidade; amplitude de movimento; rigidez articular progressiva | dr-matheus-cavalcanti |
| Dor irradiada para o membro | `healthicons:leg-outline` | dor irradiada; irradia para a perna; irradia para o braço; dor que desce | dr-matheus-cavalcanti |
| Crise de dor com travamento | `game-icons:back-pain` | crise de dor; crises de travamento; crise de dor com travamento; travamento agudo; episódio de dor intensa | dr-matheus-cavalcanti |
| Dor ao sentar ou levantar | `material-symbols:chair-outline` | sentar; levantar da cadeira; trocar de posição | dr-matheus-cavalcanti |
| Instabilidade crônica do tornozelo | `game-icons:foot-trip` | instabilidade crônica; tropeçar; torcer o pé de novo | dr-matheus-cavalcanti |

## Anatomia (o que o médico explica)

| Conceito | Ícone | Aliases | Procedência |
| --- | --- | --- | --- |
| Coluna / vértebras | `healthicons:spine-outline` | coluna; vértebra; espinha; rigidez da coluna | dr-thiago-cerqueira |
| Vértebra isolada | `icon-park-outline:rectangular-vertebra` | vértebra isolada; corpo vertebral; estenose | dr-thiago-cerqueira |
| Musculatura das costas | `hugeicons:back-muscle-body` | sobrecarga muscular; musculatura das costas; muscular | dr-thiago-cerqueira |
| Nervo | `healthicons:nerve-outline` | formigamento; dormência; compressão nervosa; nervo; ciática; túnel do carpo | dr-thiago-cerqueira |
| Articulação genérica | `healthicons:joints-outline` | articulação; artrose; desgaste articular; artrite | dr-thiago-cerqueira |
| Joelho (anatomia) | `game-icons:knee-cap` | joelho; menisco; cartilagem do joelho | dr-thiago-cerqueira; dr-rodrigo-pires |
| Joelho (anatomia, alternativa) | `streamline-ultimate:medical-specialty-knee-1` | joelho; lesão de menisco | dr-matheus-cavalcanti |
| Joelheira / suporte | `game-icons:knee-pad` | joelheira; suporte de joelho; órtese de joelho | dr-thiago-cerqueira |
| Joelho enfaixado | `game-icons:knee-bandage` | joelho enfaixado; pós-operatório de joelho | dr-thiago-cerqueira |
| Ombro | `hugeicons:shoulder` | ombro; manguito rotador; tendinite do ombro | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Tipoia | `healthicons:sling-outline` | tipoia; imobilização de braço | dr-thiago-cerqueira |
| Tipoia (alternativa) | `game-icons:arm-sling` | tipoia; braço imobilizado | dr-thiago-cerqueira |
| Braço | `healthicons:arm-outline` | braço; elevar o braço; dor no braço | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Músculo / força | `hugeicons:body-part-muscle` | força; perda de força; músculo | dr-thiago-cerqueira |
| Perna | `hugeicons:body-part-leg` | perna; dor na perna; membro inferior | dr-thiago-cerqueira |
| Fêmur / quadril | `material-symbols:femur-outline` | quadril; fêmur; dor no quadril; osteoartrose de quadril; impacto femoroacetabular | dr-thiago-cerqueira |
| Fêmur / quadril (alternativa) | `material-symbols:femur-alt-outline` | quadril; bacia; labrum | dr-thiago-cerqueira |
| Punho | `material-symbols:wrist-outline` | punho; dor no punho; movimentar o punho | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Mão (palma) | `material-symbols:front-hand-outline` | mão; palma; preensão | dr-thiago-cerqueira |
| Mão (dorso) | `material-symbols:back-hand-outline` | dorso da mão; mão | dr-thiago-cerqueira |
| Ossos da mão | `material-symbols:hand-bones-outline` | ossos da mão; artrose da mão; artrose da base do polegar | dr-thiago-cerqueira |
| Ossos do antebraço | `material-symbols:ulna-radius-outline` | antebraço; rádio; ulna; fratura de antebraço | dr-thiago-cerqueira |
| Dedo | `tabler:hand-finger` | dedo; dedo em gatilho; travamento do dedo | dr-thiago-cerqueira |
| Dedo (alternativa) | `mingcute:finger-tap-line` | dedo; digitar; esforço repetitivo da mão | dr-thiago-cerqueira |
| Pé | `healthicons:foot-outline` | pé; dor no pé | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Ossos do pé | `material-symbols:foot-bones-outline` | tornozelo; ossos do pé; instabilidade do tornozelo; entorse de tornozelo | dr-thiago-cerqueira |
| Planta do pé / pegadas | `streamline-ultimate:medical-specialty-feet` | planta do pé; fascite plantar; dor no calcanhar; esporão | dr-thiago-cerqueira |
| Órtese / palmilha | `healthicons:orthotics-outline` | palmilha; órtese; suporte plantar | dr-thiago-cerqueira |
| Fratura | `lucide:bone-fracture` | fratura; osso quebrado | dr-thiago-cerqueira |
| Curativo / inflamação | `tabler:bandage` | inflamação; bursite; tendinite; inchaço; edema | dr-thiago-cerqueira |
| Dor localizada | `healthicons:pain-outline` | dor localizada; dor pontual; dor persistente; bursite | dr-thiago-cerqueira; dr-rodrigo-pires; dr-matheus-cavalcanti |
| Coluna (variante sólida) | `healthicons:spine` | hérnia de disco; disco intervertebral | dr-matheus-cavalcanti |
| Canal vertebral estreitado | `game-icons:spinal-coil` | estenose; estreitamento do canal; canal vertebral | dr-matheus-cavalcanti |
| Vértebra deslocada | `game-icons:spine-arrow` | espondilolistese; deslizamento de vértebra; escorregamento vertebral | dr-matheus-cavalcanti |
| Bacia / pelve | `game-icons:pelvis-bone` | pelve; bacia; impacto femoroacetabular | dr-matheus-cavalcanti |
| Músculo em contração | `icon-park-outline:muscle` | tendinopatia; glúteo; músculo contraído | dr-matheus-cavalcanti |
| Antebraço | `game-icons:forearm` | antebraço; tendinite de flexores; tendinite de extensores | dr-matheus-cavalcanti |
| Calcanhar / tendão de Aquiles | `game-icons:achilles-heel` | tendão de Aquiles; tendinite do calcanhar | dr-matheus-cavalcanti |
| Osso longo isolado | `streamline:bone` | esporão; esporão de calcâneo; formação óssea | dr-matheus-cavalcanti |
| Joelho enfaixado (tendinite) | `game-icons:knee-bandage` | tendinite patelar; joelho enfaixado | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Braço imobilizado | `game-icons:arm-sling` | ombro congelado; capsulite adesiva; braço imobilizado | dr-thiago-cerqueira; dr-matheus-cavalcanti |
| Palmilha ortopédica | `healthicons:orthotics-outline` | fascite plantar; palmilha; suporte plantar | dr-thiago-cerqueira; dr-matheus-cavalcanti |

## Consulta (serve a qualquer especialidade)

| Conceito | Ícone | Aliases | Procedência |
| --- | --- | --- | --- |
| Exame clínico | `healthicons:stethoscope-outline` | consulta; exame clínico; avaliação | dr-thiago-cerqueira |
| Exame clínico (alternativa) | `material-symbols:stethoscope-outline` | consulta ortopédica; exame clínico | dr-rodrigo-pires |
| Raio-x | `healthicons:xray-outline` | raio-x; radiografia | dr-thiago-cerqueira |
| Radiologia / tomografia | `healthicons:radiology-outline` | tomografia; ressonância; imagem | dr-thiago-cerqueira |
| Ultrassom | `healthicons:ultrasound-scanner-outline` | ultrassonografia; ultrassom musculoesquelético | dr-thiago-cerqueira; dr-rodrigo-pires |
| Plano / conduta | `healthicons:medical-records-outline` | conduta; plano de tratamento; prontuário | dr-thiago-cerqueira |
| Procedimento / infiltração | `healthicons:syringe-outline` | infiltração; bloqueio; injeção; viscossuplementação | dr-thiago-cerqueira; dr-rodrigo-pires |
| Medicina regenerativa | `healthicons:blood-cells-outline` | PRP; ortobiológicos; medicina regenerativa | dr-rodrigo-pires |
| Dúvida de conduta | `material-symbols:signpost-outline` | dúvida de conduta; segunda opinião; qual caminho seguir | dr-rodrigo-pires |
| Retorno ao esporte (medalha) | `mdi:medal-outline` | retorno ao esporte; volta à competição | dr-rodrigo-pires |
| Segunda opinião (profissional) | `healthicons:doctor-outline` | segunda opinião ortopédica; outro médico | dr-rodrigo-pires |
| Limitação com bengala | `mdi:human-cane` | limitação no dia a dia; dificuldade de locomoção | dr-rodrigo-pires |

## Ícones — descrições e conexões

Uma linha por ícone (não por conceito). A coluna `Conceitos que já cobriu` cresce a cada LP aprovada, via `ferramentas/promover-conceitos.py`. `Meio` existe porque a diferenciação estética entre clientes usa meios diferentes — a mesma ideia pode ter rendition flat, 3D ou line-art, e o acúmulo precisa sobreviver a essa troca.

Meios válidos: `flat-mono`, `color-emoji`, `3d-clay`, `line-art`, `duotone`, `ilustracao`.

| Ícone | Meio | Descrição visual | Conceitos que já cobriu |
| --- | --- | --- | --- |
| `healthicons:back-pain-outline` | flat-mono | Silhueta humana curvada com marca de dor na lombar | Dor lombar; Dor articular persistente |
| `game-icons:falling` | flat-mono | Figura humana caindo para trás, desequilibrada | Queda; Instabilidade; Sensação de falseio |
| `material-symbols:bed-outline` | flat-mono | Cama vista de lado, com travesseiro | Dor noturna; Dor ao dormir de lado |
| `healthicons:weights-outline` | flat-mono | Halter / anilha de carga | Treino; Sobrecarga mecânica |
| `material-symbols:femur-outline` | flat-mono | Osso do fêmur isolado | Quadril; Fêmur; Osteoartrose de quadril |
| `material-symbols:foot-bones-outline` | flat-mono | Ossos do pé em vista superior | Tornozelo; Entorse; Instabilidade crônica |
| `tabler:bandage` | flat-mono | Curativo adesivo em diagonal | Inflamação; Bursite; Tendinite |
| `healthicons:nerve-outline` | flat-mono | Feixe nervoso ramificado | Formigamento; Dormência; Túnel do carpo |
| `healthicons:spine-outline` | flat-mono | Coluna vertebral em vista lateral, vértebras empilhadas | Coluna; Rigidez da coluna |
| `material-symbols:stairs-outline` | flat-mono | Degraus de escada em perfil | Dor ao subir escadas |
| `healthicons:joints-outline` | flat-mono | Articulação em corte — **desenha um joelho**, não usar em página de coluna | Artrose; Desgaste articular |
| `material-symbols:signpost-outline` | flat-mono | Placa de rua com setas para dois lados | Dúvida de conduta; Segunda opinião |
| `healthicons:blood-cells-outline` | flat-mono | Três glóbulos agrupados | Medicina regenerativa; PRP |
| `solar:bone-crack-outline` | flat-mono | Osso com trinca no meio | Estalos ou travamento; Estalos no movimento; Estalos ao mover os dedos |
| `solar:stretching-outline` | flat-mono | Figura humana se alongando | Rigidez ao acordar |
| `mingcute:flexibility-line` | flat-mono | Figura em alongamento de flexibilidade | Rigidez e perda de mobilidade |
| `tabler:shirt` | flat-mono | Camiseta | Dificuldade para vestir roupa |
| `healthicons:leg-outline` | flat-mono | Perna inteira em contorno | Dor irradiada para braço ou perna |
| `game-icons:back-pain` | flat-mono | Figura ajoelhada com estouro de dor nas costas | Crises de travamento |
| `healthicons:spine` | flat-mono | Coluna sólida, vértebras empilhadas | Hérnia de disco |
| `game-icons:spinal-coil` | flat-mono | Anel espinhal fechado, sugere estreitamento | Estenose do canal vertebral |
| `game-icons:spine-arrow` | flat-mono | Coluna com seta de deslocamento | Espondilolistese |
| `material-symbols:chair-outline` | flat-mono | Cadeira em perspectiva | Dor ao sentar ou levantar |
| `game-icons:pelvis-bone` | flat-mono | Bacia / pelve completa | Impacto femoroacetabular |
| `icon-park-outline:muscle` | flat-mono | Braço flexionando músculo | Tendinopatia glútea |
| `game-icons:forearm` | flat-mono | Antebraço com musculatura | Tendinite dos flexores ou extensores |
| `game-icons:achilles-heel` | flat-mono | Pé com seta apontando o calcanhar | Tendinite do tendão de Aquiles |
| `game-icons:foot-trip` | flat-mono | Pé tropeçando | Instabilidade crônica |
| `streamline:bone` | flat-mono | Osso longo isolado | Esporão de calcâneo |
| `game-icons:knee-bandage` | flat-mono | Joelho enfaixado | Tendinite patelar |
| `game-icons:arm-sling` | flat-mono | Braço imobilizado em tipoia | Ombro congelado |
| `healthicons:orthotics-outline` | flat-mono | Pé sobre palmilha ortopédica | Fascite plantar |

## Sem ícone literal em lugar nenhum

Confirmado por busca em toda a Iconify (215 sets, ~308 mil ícones): **menisco, cisto/gânglio, bursite, entorse, crepitação, túnel do carpo, ombro congelado, tornozelo e quadril** não existem como desenho próprio.

Nesses cards, use o ícone anatômico mais próximo da **mesma região** (fêmur para quadril, ossos do pé para tornozelo, curativo para inflamação) e registre. Nunca um ícone de outra especialidade, nunca uma forma abstrata escolhida por "transmitir a ideia".

Custou caro aprender: numa entrega de 2026-08 foram usados balança de tribunal para "instabilidade", balão de festa para "inchaço", raio elétrico para "formigamento", floco de neve para "ombro congelado" e carinha tonta para "instabilidade crônica" — todos exatamente a forma abstrata que esta seção proíbe, e todos com resposta já disponível nas tabelas acima. Se o conceito está nesta lista, a saída é o anatômico da região ou **remover o card** (precedente: `projetos/dr-rodrigo-pires/mapa-icones.md` §"Card removido durante o processo").

## Armadilhas de busca

- `cervical` → colo do útero e gravata. Em inglês médico não é pescoço.
- `joints` → desenha um **joelho**. Não usar em página de coluna.
- `hip`, `ankle`, `neck` → nada anatômico existe.
- `pulse`, `flare` → cardiologia e efeito gráfico. Fora do domínio.
- `tear` → rosto chorando, não ruptura de ligamento.
- `inflammation` → ícones de gengiva/odontologia.
- `thumb` → gesto de joinha, não o dedo polegar.
- `heel` e `achilles` → sapato de salto alto (e `wheel` por homofonia).
- `stumble`, `unstable`, `dizzy` → logo de rede social, orbe de jogo e emoji de tontura.

Regra prática: buscar em **português no `conceito`** e deixar o alias fazer a ponte. Termo em inglês genérico é onde o homônimo mora.
