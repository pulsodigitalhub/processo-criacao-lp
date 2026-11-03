"""Extrai a identidade visual de uma LP NO AR, para o prontuario de referencias.

Existe para responder mecanicamente "o que ja usamos?", que hoje ninguem
consegue responder sem abrir uma por uma. O checklist manda comparar cada LP
nova com as ultimas publicadas para evitar "LP irma" -- mas so um projeto tem
artefato registrado, entao nao ha com o que comparar.

LE A PAGINA PUBLICADA, NAO O MARKDOWN DO PROJETO. Isso e deliberado: em
`projetos/dr-rodrigo-pires/mapa-icones.md` estao documentados SVGs flat de
material-symbols/healthicons recoloridos em #d4b589, e a pagina no ar usa 15
icones 3D em WebP -- nenhum deles. O artefato envelheceu em silencio. Sobre a
pagina viva isso nao acontece.

Este script produz o rascunho MECANICO do cartao. O que exige julgamento (tom,
o que a referencia ensina, riscos de repetir) continua sendo escrito a mao,
seguindo `visual-repertorio/_templates/cartao-referencia.md`.

Uso:
    python3 extrair-identidade.py https://exemplo.com.br -o cartao.md
    python3 extrair-identidade.py pagina.html --nome "Dr. Fulano"

Precisa de um HTML que traga o CSS junto ou linkado no mesmo host. Para SPA que
so monta no cliente, extraia com o navegador e salve o HTML renderizado.
"""

import argparse
import collections
import os
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")}

# Como o icone e desenhado. E uma alavanca de diferenciacao entre clientes:
# tres LPs nossas usam tres meios distintos, e a ferramenta de icone precisa
# saber qual para nao bloquear o set certo.
ASSINATURAS_ICONE = [
    (r"api\.iconify\.design", "iconify-api (hotlink em runtime)"),
    (r"cdn\.jsdelivr\.net/npm/openmoji", "openmoji color (CDN)"),
    (r"cdn\.jsdelivr\.net/gh/resolvetosavelives/healthicons", "healthicons (CDN pinado)"),
    (r"3d-icons?/|/3d/", "3D/clay raster"),
    (r"topic-icons/", "svg local (assets do repo)"),
    (r"font-awesome|fa-solid|fontawesome", "icon font (Font Awesome)"),
    (r"material-symbols-outlined", "icon font (Material Symbols)"),
    (r"lucide-react|react-icons", "componente React"),
]


def baixar(url):
    if os.path.exists(url):
        with open(url, encoding="utf-8", errors="ignore") as fh:
            return fh.read(), None
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore"), url


def css_externo(html, base):
    """Baixa os <link rel=stylesheet> do mesmo host, onde os tokens costumam viver."""
    juntos = []
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', html):
        if href.startswith("//"):
            href = "https:" + href
        elif not href.startswith("http"):
            if not base:
                continue
            href = urllib.parse.urljoin(base, href)
        if "fonts.googleapis" in href:
            continue
        try:
            req = urllib.request.Request(href, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                juntos.append(r.read().decode("utf-8", "ignore"))
        except Exception:
            pass
    return "\n".join(juntos)


def main():
    ap = argparse.ArgumentParser(description="Extrai identidade visual de uma LP publicada.")
    ap.add_argument("alvo", help="URL ou caminho de HTML")
    ap.add_argument("-o", "--saida")
    ap.add_argument("--nome", help="nome do cliente/LP para o cartao")
    args = ap.parse_args()

    try:
        html, base = baixar(args.alvo)
    except Exception as e:
        print(f"nao consegui ler {args.alvo}: {e}", file=sys.stderr)
        return 1

    todo = html + "\n" + css_externo(html, base)

    titulo = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    titulo = re.sub(r"\s+", " ", titulo.group(1)).strip() if titulo else "(sem title)"
    nome = args.nome or titulo

    # tokens :root -- quando existem, sao a fonte mais confiavel da identidade
    tokens = []
    # `:root` costuma vir numa LISTA de seletores (`:root,:host{`, `:root,[data-theme]{`),
    # entao exigir `{` colado ao `:root` perdia o bloco inteiro em silencio -- foi o
    # que aconteceu com a LP do Dr. Gustavo Pimpao, que reportou "sem :root declarado"
    # tendo 40+ tokens.
    for bloco in re.findall(r":root[^{}]*\{(.*?)\}", todo, re.S):
        # o `;` final e opcional: em CSS minificado a ultima declaracao vem
        # colada no `}` (`--sans:Poppins,Arial,sans-serif}`) e exigir `;`
        # descartava justamente o ultimo token do bloco, em silencio.
        for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;}]+)\s*[;}]?", bloco):
            tokens.append((m.group(1), m.group(2).strip()))

    hexes = [h.upper() for h in re.findall(r"#([0-9a-fA-F]{6})\b", todo)]
    freq_hex = collections.Counter("#" + h for h in hexes).most_common(12)

    fontes = collections.Counter()
    for f in re.findall(r"font-family\s*:\s*([^;}]+)", todo):
        prim = f.split(",")[0].strip().strip("'\"")
        if prim and not prim.startswith("var("):
            fontes[prim] += 1
    # A URL do Google Fonts encadeia varias familias com `&family=`. Cortar no
    # primeiro `&` faz uma LP de duas fontes parecer ter uma so.
    google = []
    for q in re.findall(r"fonts\.googleapis\.com/css2?\?([^\"'>]+)", todo):
        for fam in re.findall(r"family=([^&:]+)", q):
            fam = urllib.parse.unquote(fam).replace("+", " ").strip()
            if fam and fam not in google:
                google.append(fam)

    radius = collections.Counter(re.findall(r"border-radius\s*:\s*([^;}]+)", todo)).most_common(5)

    meios = [rot for pat, rot in ASSINATURAS_ICONE if re.search(pat, todo, re.I)]

    secoes = len(re.findall(r"<section\b", html, re.I))
    h2 = [re.sub(r"<[^>]+>", "", h).strip()[:70]
          for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S | re.I)]

    L = []
    L.append(f"# ref.interna.{re.sub(r'[^a-z0-9]+', '-', nome.lower()).strip('-')[:40]}")
    L.append("")
    L.append(f"**Fonte:** {args.alvo}")
    L.append(f"**Title:** {titulo}")
    L.append("")
    L.append("Rascunho MECANICO gerado por `ferramentas/extrair-identidade.py` a partir "
             "da pagina no ar. As secoes de julgamento abaixo estao vazias de proposito "
             "— preencher a mao seguindo `visual-repertorio/_templates/cartao-referencia.md`.")
    L.append("")
    L.append("## Identidade extraida")
    L.append("")
    if tokens:
        L.append(f"### Tokens `:root` declarados ({len(tokens)})")
        L.append("")
        L.append("| Token | Valor |")
        L.append("| --- | --- |")
        for k, v in tokens[:40]:
            L.append(f"| `{k}` | `{v}` |")
        L.append("")
    else:
        L.append("Sem `:root` declarado — identidade inferida por frequencia.")
        L.append("")
    L.append("### Cores mais frequentes")
    L.append("")
    L.append("| Hex | Ocorrencias |")
    L.append("| --- | --- |")
    for h, n in freq_hex:
        L.append(f"| `{h}` | {n} |")
    L.append("")
    L.append("### Tipografia")
    L.append("")
    for f, n in fontes.most_common(6):
        L.append(f"- `{f}` ({n} usos)")
    if google:
        L.append(f"- carregadas do Google Fonts: `{', '.join(google)[:200]}`")
    if not fontes and not google:
        L.append("- nao detectada no CSS acessivel")
    L.append("")
    L.append("### Forma e ritmo")
    L.append("")
    L.append(f"- `<section>`: {secoes}")
    if radius:
        L.append("- border-radius mais usados: " + ", ".join(f"`{r}` ({n})" for r, n in radius))
    if h2:
        L.append(f"- {len(h2)} h2:")
        for t in h2[:12]:
            L.append(f"  - {t}")
    L.append("")
    L.append("### Meio do icone")
    L.append("")
    if meios:
        for m in meios:
            L.append(f"- {m}")
    else:
        L.append("- nao identificado automaticamente — inspecionar a mao")
    L.append("")
    L.append("## A preencher a mao")
    L.append("")
    L.append("**Tom:** ")
    L.append("")
    L.append("**Metafora condutora:** (existe? qual? — e o que mais diferencia uma LP)")
    L.append("")
    L.append("**O que esta LP ensina:** ")
    L.append("")
    L.append("**Ja gasto — nao repetir na proxima LP:** ")
    L.append("")

    texto = "\n".join(L)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
        print(f"cartao -> {args.saida}", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
