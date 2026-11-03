# Mapa de Ícones — {cliente}

Mecanismo de renderização: {svg-local | css-mask-cdn | react-component | icon-font}

Preenchido na fase de Copy, antes do build. Método completo em `docs/repertorio-icones.md`.

Registrar o mecanismo importa porque LPs de clientes diferentes renderizam ícone de formas diferentes de propósito, e o mapa é o único lugar onde isso fica rastreável. Preferir `svg-local`: hotlink de CDN faz a LP do cliente depender de terceiro em runtime.

## Processo executado

1. `mapear-conceitos.py` — {N} de {total} cards resolvidos pela base já validada.
2. `harvest-candidatos.py` — candidatos colhidos para os {M} restantes, meio `{meio}`.
3. `contact-sheet.py --ja-usados` — revisão visual a 32px, com os ícones já gastos na página tarjados.
4. `validar-mapa-icones.py` — {resultado}.

## Escolha por card

| Seção | Card | O que o desenho mostra | Arquivo | Ícone de origem | Conferido a 32px | Fonte |
| --- | --- | --- | --- | --- | --- | --- |
| {seção} | {card} | {o que se vê, não o que significa} | `{pasta}/{slug}.svg` | `{prefixo:slug}` | sim | {conceitos.md \| harvest-novo \| externo} |

`Fonte` alimenta o loop de aprendizado: `promover-conceitos.py` só propõe promover o que veio como `harvest-novo`. Sem essa coluna, descoberta nova e reaproveitamento ficam indistinguíveis e a base nunca cresce.

## Regras de bloqueio

- Sem a coluna "Conferido a 32px" marcada, o card não passa no checklist.
- Nenhum ícone repetido na mesma página — verificado por `validar-mapa-icones.py`, não por releitura.
- Card da página X só usa arquivo de `{pasta-do-tópico}/X/`. Regra estrutural: ícone de outro tópico fica geograficamente impossível.
- Preencher este mapa a partir dos ícones já colocados na página é justificativa retroativa, não auditoria. Auditar exige rever candidatos e reescolher.

## Conceitos sem ícone literal

Listar aqui os cards cujo conceito está na seção "Sem ícone literal" de `especialidades/{esp}/conceitos.md`, com a decisão tomada: qual anatômico da mesma região foi usado, ou por que o card foi removido. Nunca forma abstrata escolhida por "transmitir a ideia".
