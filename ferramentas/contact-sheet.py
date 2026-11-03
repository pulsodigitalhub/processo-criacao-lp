"""Gera um contact sheet HTML para revisao VISUAL obrigatoria de icones.

Esta ferramenta existe por causa de uma falha real: icones foram escolhidos
lendo o NOME numa lista de texto, sem nunca renderizar o desenho. Resultado,
entre outros: um icone chamado "joints-outline" (que desenha um JOELHO) foi
parar num card "Articulacoes da coluna". Nenhuma revisao textual pega isso.

Regra do processo: nenhum icone e aprovado sem ter passado por este contact
sheet. Criterio, por icone -- olhando SO o desenho, sem ler o titulo, da pra
dizer que parte do corpo/orgao e e qual e o problema?

Uso:
    python3 contact-sheet.py <pasta-de-icones> [-o saida.html] [--titulos t.json]

    <pasta-de-icones>  pasta com .svg (varre subpastas; cada subpasta vira secao)
    --titulos          json opcional {"nome-do-arquivo": "Titulo do card"}
                       para revisar o icone ao lado do texto que ele acompanha
    --ja-usados        mapeamento.json ou mapa-icones.md da MESMA LP; os icones
                       ja gastos aparecem tarjados. Ataca a repeticao na hora da
                       escolha, e nao so na validacao final -- ja saiu ao vivo LP
                       com o mesmo icone em 5 cards da mesma pagina.
"""

import argparse
import base64
import json
import os
import re
import sys

TEMPLATE_HEAD = """<!doctype html>
<meta charset="utf-8">
<title>Contact sheet de icones</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; background: #f5f4f0;
         color: #303235; margin: 0; padding: 32px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: #6b7280; font-size: 13px; margin-bottom: 28px; max-width: 60ch;
         line-height: 1.5; }
  h2 { font-size: 15px; text-transform: uppercase; letter-spacing: .08em;
       color: #53686a; margin: 32px 0 12px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
          gap: 14px; }
  .card { background: #fff; border: 1px solid rgba(83,104,106,.14);
          border-radius: 12px; padding: 16px; }
  .row { display: flex; align-items: center; gap: 16px; }
  .big { width: 96px; height: 96px; flex: none; }
  .real { width: 32px; height: 32px; flex: none; }
  .real-wrap { display:flex; flex-direction:column; align-items:center; gap:4px; }
  .tag { font-size: 9px; color: #9aa3a5; }
  .title { font-weight: 700; font-size: 14px; margin-top: 12px; }
  .file { font-size: 11px; color: #9aa3a5; margin-top: 2px;
          font-family: ui-monospace, monospace; word-break: break-all; }
  .card.usado { background: #f0ecea; border-color: rgba(158,86,66,.35); }
  .card.usado .row { opacity: .38; }
  .selo { display:inline-block; margin-top:10px; padding:3px 8px; border-radius:999px;
          background:#9e5642; color:#fff; font-size:10px; font-weight:700;
          letter-spacing:.06em; text-transform:uppercase; }
</style>
<h1>Contact sheet de icones</h1>
<div class="sub">Criterio: olhando <b>so o desenho</b>, sem ler o titulo, da pra dizer
que parte do corpo/orgao e e qual e o problema? Se nao, redesenhar.
O quadrado pequeno e o tamanho real de uso (32px) &mdash; e nele que a legibilidade
precisa funcionar.</div>
"""


def collect(root):
    """Retorna {secao: [(caminho, nome)]} varrendo subpastas."""
    sections = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        svgs = sorted(f for f in filenames if f.endswith(".svg"))
        if not svgs:
            continue
        rel = os.path.relpath(dirpath, root)
        section = "." if rel == "." else rel
        sections[section] = [(os.path.join(dirpath, f), f) for f in svgs]
    return dict(sorted(sections.items()))


def nome_iconify(arquivo):
    """`03_healthicons__spine-outline.svg` -> `healthicons:spine-outline`."""
    stem = os.path.splitext(arquivo)[0]
    stem = re.sub(r"^\d+_", "", stem)
    return stem.replace("__", ":")


def carregar_ja_usados(caminho):
    """Aceita mapeamento.json (chave `batidos`) ou mapa-icones.md preenchido.

    Devolve {pagina: {icone: [cards]}}. O escopo e POR PAGINA porque e assim que
    a regra existe: `docs/repertorio-icones.md` proibe repetir icone na mesma
    pagina, nao no projeto inteiro. Marcar globalmente faria a ferramenta vetar
    reuso legitimo entre LPs de regioes diferentes -- e um aviso que aparece
    demais e um aviso que se aprende a ignorar.
    """
    usados = {}
    if caminho.endswith(".json"):
        with open(caminho, encoding="utf-8") as fh:
            dados = json.load(fh)
        for ident, d in (dados.get("batidos") or {}).items():
            if not d.get("icone"):
                continue
            pagina, card = ident.split("/", 1) if "/" in ident else ("", ident)
            usados.setdefault(pagina, {}).setdefault(d["icone"], []).append(card)
        return usados
    with open(caminho, encoding="utf-8") as fh:
        for l in fh:
            if not l.strip().startswith("|"):
                continue
            cels = [c.strip() for c in l.strip().strip("|").split("|")]
            pagina = cels[0].strip().lower() if cels else ""
            for c in cels:
                c = c.strip("`").strip()
                if re.fullmatch(r"[a-z0-9-]+:[a-z0-9-]+", c):
                    usados.setdefault(pagina, {}).setdefault(c, []).append("mapa")
    return usados


def render(sections, titles, ja_usados):
    parts = [TEMPLATE_HEAD]
    if ja_usados:
        n = sum(len(v) for v in ja_usados.values())
        parts.append(
            f'<div class="sub"><b>{n} icones ja estao gastos</b> nas paginas desta LP '
            "e aparecem tarjados na secao da propria pagina. Nenhum icone pode se "
            "repetir <b>na mesma pagina</b> &mdash; escolher outro, mesmo que o "
            "tarjado pareca o melhor. Reuso entre paginas diferentes e permitido.</div>"
        )
    total = 0
    for section, files in sections.items():
        label = section if section != "." else "(raiz)"
        # a pagina e o primeiro nivel do caminho: `coluna/causa-hernia` -> `coluna`
        pagina = section.split(os.sep)[0] if section != "." else ""
        usados_aqui = ja_usados.get(pagina, {})
        parts.append(f'<h2>{label} &mdash; {len(files)} icones</h2>\n<div class="grid">')
        for path, name in files:
            with open(path, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode()
            src = f"data:image/svg+xml;base64,{b64}"
            stem = os.path.splitext(name)[0]
            title = titles.get(stem) or titles.get(name) or ""
            iconify = nome_iconify(name)
            onde = usados_aqui.get(iconify)
            classe = "card usado" if onde else "card"
            selo = (f'<div><span class="selo">ja usado nesta pagina: {onde[0]}</span></div>'
                    if onde else "")
            parts.append(
                f'<div class="{classe}"><div class="row">'
                f'<img class="big" src="{src}" alt="">'
                '<div class="real-wrap">'
                f'<img class="real" src="{src}" alt="">'
                '<span class="tag">32px</span>'
                "</div></div>"
                + (f'<div class="title">{title}</div>' if title else "")
                + f'<div class="file">{name}</div>{selo}</div>'
            )
            total += 1
        parts.append("</div>")
    parts.append(f'<div class="sub" style="margin-top:32px">Total: {total} icones.</div>')
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("-o", "--saida", default="contact-sheet.html")
    ap.add_argument("--titulos", help="json {arquivo: titulo do card}")
    ap.add_argument("--ja-usados", dest="ja_usados",
                    help="mapeamento.json ou mapa-icones.md da mesma LP")
    args = ap.parse_args()

    if not os.path.isdir(args.pasta):
        sys.exit(f"pasta nao encontrada: {args.pasta}")

    titles = {}
    if args.titulos:
        with open(args.titulos, encoding="utf-8") as fh:
            titles = json.load(fh)

    ja_usados = carregar_ja_usados(args.ja_usados) if args.ja_usados else {}

    sections = collect(args.pasta)
    if not sections:
        sys.exit(f"nenhum .svg encontrado em {args.pasta}")

    html = render(sections, titles, ja_usados)
    with open(args.saida, "w", encoding="utf-8") as fh:
        fh.write(html)

    n = sum(len(v) for v in sections.values())
    print(f"contact sheet com {n} icones -> {args.saida}")
    if ja_usados:
        print(f"{len(ja_usados)} icones marcados como ja usados nesta LP.")
    print("ABRA E OLHE antes de aprovar qualquer icone.")


if __name__ == "__main__":
    main()
