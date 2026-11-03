# Publicação

Status: vigente desde 29/10/2026. Origem: LP do Dr. Breno Lima e as LPs do Pedro, Rodrigo e Matheus.

## Passo a passo

1. Rodar `python3 scripts/gate_skill.py lp --projeto <pasta>` no repositório `politicas-plataformas`.
2. Fazer commit com o autor `pulsodigitalhub`.
3. Enviar para a branch principal. O projeto ligado ao repositório publica sozinho na Vercel.
4. Depois do deploy, rodar o gate de novo com `--url`.

## Domínio

Criar a zona na Cloudflare da Pulso. Usar o cofre "Cloudflare API (DNS Pulso)".

Criar registros sem proxy com os valores retornados por `GET api.vercel.com/v6/domains/<dominio>/config`.

O titular deve trocar os nameservers no Registro.br. Se o HTTPS não subir, pedir o certificado por `POST /v8/certs`.

Usar `noindex` somente enquanto o conteúdo não estiver aprovado.

## Plano B

Se o deploy por Git falhar, fazer upload direto pela API. O script de referência é `docs/deploy_vercel.py` no repositório do Breno.

## Checado pelo gate

- O gate inteiro roda antes do push e de novo com --url. RESULTADO: FAIL impede publicar.
- noindex: só aviso, com a lista de páginas.
- sitemap apontando para *.vercel.app: aviso.
