"""Responde objetivamente: as bibliotecas de icone dao conta desta especialidade?

Motivacao concreta: a sensacao de "usamos sempre os mesmos icones" tem duas
causas mensuraveis, e este script separa as duas.

1. Cobertura real -- ha conceitos da especialidade que simplesmente nao existem
   como desenho em lugar nenhum. Isso ja e parcialmente conhecido (a secao
   "Sem icone literal" do conceitos.md), mas nunca foi medido periodicamente.
2. Cegueira da ferramenta -- o `harvest-candidatos.py` ordena por uma lista
   PRIORIDADE fixa. Um set otimo que esteja fora dela cai para o fim e nunca
   entra no corte de candidatos por card. Foi o caso de `icon-park-outline` e
   `mingcute`, que o proprio conceitos.md ja usava e a PRIORIDADE ignorava.

O relatorio e datado e append-only por arquivo, para dar pra comparar cobertura
entre entregas em vez de reabrir a discussao do zero a cada LP.

Uso:
    python3 auditar-cobertura.py especialidades/ortopedia/conceitos.md \\
            -o docs/relatorios/cobertura-ortopedia-2026-08.md
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conceitos import carregar, ErroDeEsquema  # noqa: E402

API = "https://api.iconify.design"
UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")}

# Espelha harvest-candidatos.py. Duplicado de proposito: este script precisa
# comparar contra a lista COMO ELA ESTA, e importa-la criaria acoplamento que
# esconderia divergencia entre os dois.
PRIORIDADE = [
    "healthicons", "medical-icon", "streamline-ultimate", "streamline",
    "game-icons", "material-symbols", "material-symbols-light", "hugeicons",
    "solar", "tabler",
    "icon-park-outline", "mingcute", "iconoir", "ph", "mdi", "lucide",
    "carbon", "fluent",
]

# Meios que nao vivem na Iconify -- a auditoria nao consegue medir e diz isso
# em vez de fingir cobertura.
MEIOS_EXTERNOS = {
    "3d-clay": "conjuntos 3D/clay (ex.: o usado na LP do Dr. Rodrigo Pires)",
    "ilustracao": "ilustracao sob medida ou banco de ilustracao",
}


def existe(nome):
    """Confirma que o icone da base ainda resolve. Pega link rot silencioso."""
    pref, slug = nome.split(":", 1)
    try:
        req = urllib.request.Request(f"{API}/{pref}/{slug}.svg", headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            return b"<svg" in r.read(400)
    except Exception:
        return False


def buscar(termo, limit=32):
    url = f"{API}/search?query={urllib.parse.quote(termo)}&limit={limit}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r).get("icons", [])
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="Audita cobertura de icones da especialidade.")
    ap.add_argument("conceitos")
    ap.add_argument("-o", "--saida")
    ap.add_argument("--limite", type=int, help="auditar so os N primeiros conceitos")
    args = ap.parse_args()

    try:
        base = carregar(args.conceitos)
    except ErroDeEsquema as e:
        print(f"ERRO DE ESQUEMA: {e}", file=sys.stderr)
        return 2

    conceitos = base.conceitos[: args.limite] if args.limite else base.conceitos
    esp = os.path.basename(os.path.dirname(os.path.abspath(args.conceitos)))
    hoje = datetime.date.today().isoformat()

    sets_uteis = {}      # prefixo -> quantas vezes apareceu num resultado util
    quebrados = []       # icone da base que nao resolve mais
    fora_prioridade = {}

    # A busca da Iconify so entende INGLES. Os aliases da base sao em portugues
    # de proposito (e o vocabulario com que o card e escrito), entao usa-los como
    # termo de busca devolve zero para tudo -- a primeira versao deste script fez
    # isso e reportou "sem resultado" para conceitos que tinham icone validado na
    # propria base. O termo de sondagem correto e o SLUG do icone ja escolhido,
    # que e o vocabulario ingles que aquele conceito realmente ocupa.
    print(f"auditando {len(conceitos)} conceitos de '{esp}'...", file=sys.stderr)
    for i, c in enumerate(conceitos, 1):
        if ":" not in c.icone:
            continue
        pref_atual, slug = c.icone.split(":", 1)
        if not existe(c.icone):
            quebrados.append((c.conceito, c.icone))

        termo = slug.replace("-outline", "").replace("-24px", "").replace("-", " ").strip()
        for nome in buscar(termo, limit=24):
            pref = nome.split(":")[0]
            sets_uteis[pref] = sets_uteis.get(pref, 0) + 1
            if pref not in PRIORIDADE:
                fora_prioridade.setdefault(pref, []).append(f"{c.conceito} <- '{termo}'")
        time.sleep(0.05)
        if i % 10 == 0:
            print(f"  {i}/{len(conceitos)}", file=sys.stderr)

    sem_resultado = list(base.sem_literal)

    meios_usados = {}
    for ic in base.icones:
        meios_usados[ic.meio] = meios_usados.get(ic.meio, 0) + 1

    L = []
    L.append(f"# Cobertura de icones — {esp} — {hoje}")
    L.append("")
    L.append(f"{len(conceitos)} conceitos auditados a partir de "
             f"`{os.path.basename(args.conceitos)}`. Cada icone ja escolhido foi "
             f"verificado (ainda resolve?) e seu slug usado como termo de sondagem "
             f"para descobrir que outros sets servem a especialidade.")
    L.append("")
    L.append("## Icones da base que nao resolvem mais")
    L.append("")
    if quebrados:
        L.append("Link rot: o set renomeou ou removeu o icone. Reescolher antes da "
                 "proxima LP que reaproveitar este conceito.")
        L.append("")
        for c, ic in quebrados:
            L.append(f"- {c} — `{ic}`")
    else:
        L.append(f"Nenhum — os {len(conceitos)} icones da base ainda resolvem.")
    L.append("")
    L.append("## Conceitos sem icone literal em lugar nenhum")
    L.append("")
    if sem_resultado:
        L.append("Registrado na propria base. A saida é o anatomico da mesma regiao, "
                 "ou remover o card — nunca forma abstrata.")
        L.append("")
        for c in sem_resultado:
            L.append(f"- {c}")
    else:
        L.append("Nenhum registrado.")
    L.append("")
    L.append("## Sets fora do PRIORIDADE que apareceram como candidato")
    L.append("")
    if fora_prioridade:
        L.append("Estes sets tem vocabulario util para a especialidade mas nao estao na "
                 "lista de prioridade do `harvest-candidatos.py` — na pratica caem para "
                 "o fim da ordenacao e raramente entram no corte por card. Avaliar "
                 "promocao.")
        L.append("")
        L.append("| Set | Ocorrencias | Exemplo de conceito |")
        L.append("| --- | --- | --- |")
        for pref, exemplos in sorted(fora_prioridade.items(),
                                     key=lambda kv: -len(kv[1]))[:15]:
            L.append(f"| `{pref}` | {len(exemplos)} | {exemplos[0]} |")
    else:
        L.append("Nenhum — a lista PRIORIDADE cobre os sets que a especialidade usa.")
    L.append("")
    L.append("## Sets mais produtivos (ja em PRIORIDADE)")
    L.append("")
    L.append("| Set | Ocorrencias |")
    L.append("| --- | --- |")
    for pref, n in sorted(((p, n) for p, n in sets_uteis.items() if p in PRIORIDADE),
                          key=lambda kv: -kv[1])[:12]:
        L.append(f"| `{pref}` | {n} |")
    L.append("")
    L.append("## Meios em uso na base")
    L.append("")
    for m, n in sorted(meios_usados.items(), key=lambda kv: -kv[1]):
        L.append(f"- `{m}`: {n} icone(s) descrito(s)")
    L.append("")
    L.append("Meios que esta auditoria **nao consegue medir**, por nao viverem na Iconify:")
    for m, desc in MEIOS_EXTERNOS.items():
        L.append(f"- `{m}` — {desc}. Cobertura precisa ser avaliada na fonte licenciada.")
    L.append("")
    L.append("## Vies conhecido deste relatorio")
    L.append("")
    L.append("A auditoria so pergunta o que ja esta escrito na coluna Aliases. Conceito "
             "que ninguem pensou em registrar nao aparece como lacuna aqui — o relatorio "
             "mede a cobertura do vocabulario existente, nao do vocabulario possivel.")
    L.append("")

    texto = "\n".join(L)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"relatorio -> {args.saida}", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
