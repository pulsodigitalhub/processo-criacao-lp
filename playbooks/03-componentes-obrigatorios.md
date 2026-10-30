# Componentes obrigatórios para LP de anúncio

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

Toda LP de anúncio deve ter os componentes abaixo.

1. Menu no topo, também no mobile, com botão de pelo menos 44px.
2. Barra fixa de CTA no rodapé do mobile, com ícone do WhatsApp antes do texto.
3. Botão flutuante redondo com ícone do WhatsApp, na cor dos botões. No mobile, ele some enquanto o banner de cookies estiver aberto.
4. Banner de cookies não modal, à esquerda no desktop, com as opções "Apenas essenciais" e "Aceitar". A política de privacidade deve permitir reabrir o banner.
5. Formulário de agendamento em etapas.

## Formulário de agendamento

1. Convênio com busca, com "Consulta particular" como primeira opção.
2. Unidades que atendem aquele convênio, com o horário de funcionamento de cada uma e botão "Agendar em <RA>". Mesmo horário dos cards de Unidades.
3. Nome, WhatsApp e aceite da política de privacidade.
4. Envio ao webhook `https://leads-clientes.sergioshouse.com.br/<cliente>`, com UTMs, gclid, gbraid e wbraid.
5. Abertura do WhatsApp com mensagem pronta somente depois do envio.

O webhook pertence ao repositório `7crispim/lead-webhook-pulso`, com a rota ligada em `config.json`.

Nunca usar link direto `wa.me` em LP de anúncio.

Código de referência, não copiar para este playbook: `pulsodigitalhub/lp-dr-breno-lima`, `assets/agendamento.js` e `assets/breno.css`.

## Checado pelo gate

- Política sem controlador ou sem canal de contato: FALHA.
- Redirecionamento por JavaScript para domínio fora da allowlist do .checker-lp.json: FALHA (checker-lp).
- Menu mobile, barra fixa e botão flutuante: nada ainda, depende de revisão.
