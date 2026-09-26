# Spec: LP de Saude

Contrato minimo para Landing Pages de medicos, dentistas, psicologos, fisioterapeutas e demais profissionais regulados por conselho. A base regulatoria e a publicidade medica do CFM (Resolucoes 1974/2011, 2126/2015 e 2336/2023). Conselhos correlatos (CFO, CFP, COFFITO) tem regras analogas — consulte antes de publicar.

## Identificacao profissional

- Nome completo do profissional visivel no primeiro viewport.
- Numero de registro no conselho (CRM, CRO, CRP, CREFITO) com UF.
- RQE informado quando a pagina mencionar especialidade medica.
- Se a pagina e institucional (clinica), a razao social e o responsavel tecnico com registro tambem sao visiveis.

## Copy proibida

- Promessa de resultado ou cura ("voce vai emagrecer 10kg", "resolvo sua enxaqueca").
- Superlativos e autopromoção ("melhor da cidade", "unico com essa tecnica", "referencia nacional").
- Descontos, cortesias, brindes ou qualquer condicao comercial promocional.
- Comparacao direta com colegas de profissao.
- Especialidade que o profissional nao tem RQE ou registro correspondente.
- Termos tecnicos apresentados de forma que sugiram garantia ("procedimento definitivo", "sem risco").

## Imagens e provas

- Antes/depois em desacordo com a resolucao vigente do conselho — em geral proibido para procedimentos esteticos e cirurgicos. Verificar caso a caso.
- Fotos do profissional, do consultorio, do procedimento sem identificacao do paciente sao permitidas.
- Imagem de banco (stock) nao pode ser apresentada como caso real.
- Depoimento de paciente e restrito: pode contar experiencia com o atendimento, nao pode sugerir resultado garantido. Consentimento por escrito registrado.
- Numeros e claims tecnicos precisam de fonte verificavel citada.

## Icones de card

Icone em card de sintoma/causa/cuidado comunica dominio clinico. Icone errado (pulso cardiaco em pagina de ortopedia, cadeado generico em card de sintoma) nao e apenas falha estetica — desinforma o visitante sobre a especialidade da pagina.

- Seguir `docs/repertorio-icones.md` sem excecao. Card so usa arquivo de `assets/topic-icons/<regiao-do-corpo-ou-tema>/`.
- Nenhum icone e aprovado por nome. Contact sheet renderizado a 32px e a evidencia — se um leigo, olhando so o desenho, nao sabe dizer que parte do corpo/orgao e e qual e o problema, o icone esta errado.
- Quando um conceito nao tem icone literal (menisco, bursite, entorse, tunel do carpo etc.), usar o icone anatomico mais proximo da **mesma regiao**. Nunca emprestar de outra especialidade.
- Consultar `especialidades/<especialidade>/conceitos.md` antes de comecar — economiza tempo e evita repetir armadilhas ja documentadas (`cervical` retorna colo do utero, `joints` desenha um joelho).

## Conversao

- CTA primario e uma acao de contato ou agendamento, nao venda direta.
- Formulario de contato coleta somente dados necessarios para o agendamento. LGPD: politica de privacidade e consentimento antes de submit. Telefone limitado a 10 ou 11 digitos (ver `specs/google-ads.md`, "Campo de telefone").
- Canal direto (WhatsApp, telefone) pode aparecer em LP organica. Em LP de Ads, seguir `specs/google-ads.md`.

## Gates

- [ ] Identificacao profissional com CRM/RQE (ou equivalente) esta visivel no primeiro viewport.
- [ ] Nenhum trecho da copy contem promessa absoluta, superlativo ou termo promocional.
- [ ] Imagens revisadas contra a resolucao do conselho aplicavel.
- [ ] Depoimentos, quando presentes, tem consentimento registrado e nao sugerem resultado garantido.
- [ ] Numeros e claims tecnicos citam fonte.
- [ ] Politica de privacidade linkada e consentimento LGPD explicito antes do submit.
- [ ] Icones de card seguem `docs/repertorio-icones.md`: contact sheet gerado, revisado a 32px, arquivos organizados por regiao em `assets/topic-icons/<regiao>/`. Nenhum icone escolhido apenas por nome.
