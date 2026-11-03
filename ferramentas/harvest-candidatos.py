"""Baixa CANDIDATOS de icone por card, de toda a base do Iconify, para escolha visual.

Existe por causa de uma falha real: icones foram escolhidos lendo o NOME numa
lista de texto, sem nunca renderizar. Ex.: "joints-outline" (que desenha um
JOELHO) foi parar num card "Articulacoes da coluna".

O conserto nao e "procurar melhor por nome" -- e ver varios candidatos
renderizados lado a lado e escolher olhando. Este script produz os candidatos;
o contact-sheet.py renderiza; a escolha e feita olhando.

NAO E MAIS A PORTA DE ENTRADA. Este script recebe `mapeamento.json`, produzido
por `mapear-conceitos.py`, e trabalha SO no que nao foi resolvido pela base de
`especialidades/<esp>/conceitos.md`. A inversao existe porque o entrypoint
antigo pedia ao agente para inventar `termos` em ingles -- exatamente onde moram
as armadilhas de homonimo (`cervical` devolve colo do utero, `tear` devolve
rosto chorando). Numa entrega de 2026-08 isso produziu balanca de tribunal para
"instabilidade" e balao de festa para "inchaco", ambos com resposta ja validada
na base que nunca foi aberta.

Uso:
    python3 mapear-conceitos.py cards.json especialidades/ortopedia/conceitos.md -o mapeamento.json
    python3 harvest-candidatos.py mapeamento.json -o candidatos/ --meio flat-mono
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.iconify.design"

# A API rejeita o User-Agent padrao do urllib com 403.
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
}


def _abrir(url, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)

# Marca / produto / tema de editor: nunca servem como icone de card, em nenhum
# meio. Bloqueio incondicional.
SETS_MARCA = {
    "skill-icons", "logos", "simple-icons", "devicon", "vscode-icons",
    "flagpack", "circle-flags", "cif", "flag", "cryptocurrency-color",
    "token-branded", "arcticons", "material-icon-theme", "catppuccin", "unjs",
}

# Multicoloridos / emoji: bloqueados em LP de icone monocromatico, mas LIBERADOS
# quando o meio escolhido para aquela LP e colorido. A LP da Dra. Genesia Regina
# usa openmoji colorido (footprints, olhos, bussola) como icone de card, com
# resultado aprovado -- com a blocklist antiga e absoluta, essa escolha teria
# sido impedida pela propria ferramenta.
SETS_COLORIDOS = {
    "noto", "noto-v1", "twemoji", "openmoji", "emojione", "emojione-v1",
    "emojione-monotone", "fluent-emoji", "fluent-emoji-flat",
    "fluent-emoji-high-contrast", "fxemoji", "streamline-color",
    "streamline-flex-color", "streamline-sharp-color", "streamline-ultimate-color",
    "streamline-freehand-color",
}

# Estilizados demais para card clinico monocromatico.
SETS_ESTILIZADOS = {"pixel", "pinhead", "glyphs-poly"}

# Preferencia: sets com vocabulario clinico/anatomico real primeiro.
# icon-park-outline e mingcute entraram porque `conceitos.md` ja os usa
# (rectangular-vertebra, finger-tap-line) e sem estar aqui eles caiam para o fim
# da ordenacao e nunca entravam no corte de candidatos por card.
PRIORIDADE = [
    "healthicons", "medical-icon", "streamline-ultimate", "streamline",
    "game-icons", "material-symbols", "material-symbols-light", "hugeicons",
    "solar", "tabler",
    "icon-park-outline", "mingcute", "iconoir", "ph", "mdi", "lucide",
    "carbon", "fluent",
]

# Cada meio define o que e aceitavel. O meio e uma decisao de diferenciacao
# estetica por cliente -- LPs diferentes usam meios diferentes de proposito
# (flat-mono no Dr. Matheus, 3d-clay no Dr. Rodrigo, color-emoji na Dra. Genesia).
MEIOS = {
    "flat-mono":   SETS_MARCA | SETS_COLORIDOS | SETS_ESTILIZADOS,
    "line-art":    SETS_MARCA | SETS_COLORIDOS | SETS_ESTILIZADOS,
    "duotone":     SETS_MARCA | SETS_COLORIDOS | SETS_ESTILIZADOS,
    "color-emoji": SETS_MARCA | SETS_ESTILIZADOS,
}

# Meios que nao vivem na Iconify. Harvest nao resolve; a fonte e externa.
MEIOS_FORA_DA_ICONIFY = {
    "3d-clay": "conjuntos 3D/clay nao estao na Iconify (ex.: o set usado na LP do "
               "Dr. Rodrigo Pires, `img/3d-icons/*.webp`). Colher a mao da fonte "
               "licenciada e registrar procedencia no mapa de icones.",
    "ilustracao": "ilustracao sob medida ou banco de ilustracao -- fora da Iconify.",
}


def buscar(termo, limit=32):
    url = f"{API}/search?query={urllib.parse.quote(termo)}&limit={limit}"
    try:
        with _abrir(url) as r:
            return json.load(r).get("icons", [])
    except Exception as e:
        print(f"    ! busca '{termo}' falhou: {e}")
        return []


def pontuar(nome):
    """Menor = melhor. Prioriza set clinico e variante de contorno."""
    prefixo = nome.split(":")[0]
    p = PRIORIDADE.index(prefixo) if prefixo in PRIORIDADE else len(PRIORIDADE)
    slug = nome.split(":", 1)[1] if ":" in nome else nome
    # variantes de contorno primeiro; evitar duplicatas -24px/-alt
    contorno = 0 if ("outline" in slug or "line" in slug) else 1
    ruido = 1 if ("24px" in slug or slug.endswith("-alt")) else 0
    return (p, contorno, ruido, len(slug))


def baixar(nome, destino, cor="%23527d8f"):
    prefixo, slug = nome.split(":", 1)
    url = f"{API}/{prefixo}/{slug}.svg?color={cor}&width=32&height=32"
    try:
        with _abrir(url) as r:
            dados = r.read()
        if b"<svg" not in dados:
            return False
        with open(destino, "wb") as fh:
            fh.write(dados)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(
        description="Colhe candidatos de icone SO para os cards nao resolvidos pela base."
    )
    ap.add_argument("mapeamento", help="saida de mapear-conceitos.py")
    ap.add_argument("-o", "--saida", default="candidatos")
    ap.add_argument("-n", "--por-card", type=int, default=10)
    ap.add_argument("--meio", default="flat-mono", choices=sorted(set(MEIOS) | set(MEIOS_FORA_DA_ICONIFY)))
    args = ap.parse_args()

    with open(args.mapeamento, encoding="utf-8") as fh:
        dados = json.load(fh)

    # Recusa cards.json cru. Nao e purismo: e o gate que impede voltar ao fluxo
    # que causou as escolhas erradas -- entrar por aqui significa nao ter
    # consultado a base de conceitos.
    if not isinstance(dados, dict) or "sem_match" not in dados:
        print(
            "ERRO: esperado o mapeamento.json de `mapear-conceitos.py`, nao um "
            "cards.json cru.\n\n"
            "  python3 mapear-conceitos.py <cards.json> "
            "<especialidades/<esp>/conceitos.md> -o mapeamento.json\n\n"
            "Entrar direto aqui pula a consulta a base de conceitos, que e a causa "
            "documentada de icone errado (forma abstrata para conceito que ja tinha "
            "resposta validada).",
            file=sys.stderr,
        )
        return 2

    if args.meio in MEIOS_FORA_DA_ICONIFY:
        print(f"meio '{args.meio}': {MEIOS_FORA_DA_ICONIFY[args.meio]}", file=sys.stderr)
        return 3

    bloqueados = MEIOS[args.meio]
    pendentes = dados["sem_match"]
    if not pendentes:
        print("Nada pendente -- a base resolveu todos os cards. Nao ha o que colher.")
        return 0

    print(f"{len(pendentes)} cards pendentes, meio '{args.meio}'.")
    total = 0
    for ident, info in sorted(pendentes.items()):
        regiao, chave = ident.split("/", 1)
        termos = list(info.get("termos") or [])
        # o conceito em portugues tambem vira termo: as vezes casa direto
        if info.get("conceito"):
            termos.append(info["conceito"])

        vistos = []
        for termo in termos:
            for nome in buscar(termo):
                prefixo = nome.split(":")[0]
                if prefixo in bloqueados:
                    continue
                if nome not in vistos:
                    vistos.append(nome)
            time.sleep(0.05)

        vistos.sort(key=pontuar)
        escolhidos = vistos[: args.por_card]

        pasta = os.path.join(args.saida, regiao, chave)
        os.makedirs(pasta, exist_ok=True)
        ok = 0
        for i, nome in enumerate(escolhidos):
            arq = f"{i:02d}_{nome.replace(':', '__')}.svg"
            if baixar(nome, os.path.join(pasta, arq)):
                ok += 1
                total += 1
        alerta = "  [SEM ICONE LITERAL]" if info.get("sem_icone_literal") else ""
        print(f"  {ident}: {ok} candidatos ({len(vistos)} achados){alerta}")

    print(f"\n{total} candidatos em {args.saida}/")
    print("Agora rode o contact-sheet.py e ESCOLHA OLHANDO.")
    print("Use --ja-usados <mapa-icones.md> para marcar o que ja foi gasto nesta LP.")


if __name__ == "__main__":
    sys.exit(main())
