"""Casa os cards da LP contra a base de conceitos ANTES de qualquer busca nova.

Esta e a porta de entrada do fluxo de icones. Existe porque o entrypoint antigo
era o `harvest-candidatos.py`, que pedia ao agente para inventar `termos` em
INGLES -- exatamente onde moram as armadilhas de homonimo que
`especialidades/*/conceitos.md` ja documenta (`cervical` devolve colo do utero,
`joints` desenha um joelho, `tear` devolve rosto chorando).

O resultado pratico daquele desenho: 72 icones escolhidos sem nunca abrir a base,
com balanca de tribunal para "instabilidade" e balao de festa para "inchaco" --
os dois com resposta ja validada no arquivo.

Aqui o conceito e escrito em PORTUGUES (a lingua em que o card foi pensado) e o
casamento acontece contra a coluna Aliases. So o que nao casa vai para o harvest.

Uso:
    python3 mapear-conceitos.py cards.json especialidades/ortopedia/conceitos.md -o mapeamento.json

    cards.json:
    {
      "joelho": {
        "sintoma-instabilidade": {
          "titulo": "Sensacao de instabilidade",
          "conceito": "instabilidade / joelho falseando",
          "termos": ["knee instability"]          # opcional, so usado no harvest
        }
      }
    }
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conceitos import carregar, ErroDeEsquema  # noqa: E402

# Abaixo disso o match e fraco demais para ser reaproveitado sem olhar.
LIMIAR_ACEITE = 65


def main():
    ap = argparse.ArgumentParser(
        description="Casa cards contra a base de conceitos; so o que sobra vai ao harvest."
    )
    ap.add_argument("cards")
    ap.add_argument("conceitos")
    ap.add_argument("-o", "--saida", default="mapeamento.json")
    ap.add_argument("--limiar", type=int, default=LIMIAR_ACEITE)
    args = ap.parse_args()

    try:
        base = carregar(args.conceitos)
    except ErroDeEsquema as e:
        print(f"ERRO DE ESQUEMA: {e}", file=sys.stderr)
        return 2

    with open(args.cards, encoding="utf-8") as fh:
        cards = json.load(fh)

    faltando_conceito = []
    for regiao, mapa in cards.items():
        for chave, info in mapa.items():
            if not info.get("conceito"):
                faltando_conceito.append(f"{regiao}/{chave}")
    if faltando_conceito:
        print(
            "ERRO: card sem campo 'conceito' (em portugues). O conceito e o que "
            "casa contra a base; sem ele o fluxo cai direto na busca em ingles, "
            "que e a causa documentada das escolhas erradas.\n  "
            + "\n  ".join(faltando_conceito),
            file=sys.stderr,
        )
        return 2

    batidos, sem_match, avisos = {}, {}, []
    for regiao, mapa in cards.items():
        for chave, info in mapa.items():
            ident = f"{regiao}/{chave}"
            conceito = info["conceito"]

            sem_lit = base.e_sem_literal(conceito)
            achados = base.buscar(conceito)
            melhor = achados[0] if achados else None

            if sem_lit:
                avisos.append(
                    f"{ident}: '{sem_lit}' nao existe como desenho proprio em toda a "
                    f"Iconify. Usar o anatomico da MESMA regiao ou remover o card -- "
                    f"nunca forma abstrata."
                )

            if melhor and melhor.score >= args.limiar:
                batidos[ident] = {
                    "titulo": info.get("titulo", ""),
                    "conceito": conceito,
                    "icone": melhor.icone,
                    "meio": base.meio_de(melhor.icone),
                    "score": melhor.score,
                    "alias_casado": melhor.alias_casado,
                    "procedencia": melhor.procedencia,
                    "sem_icone_literal": sem_lit,
                }
            else:
                sem_match[ident] = {
                    "titulo": info.get("titulo", ""),
                    "conceito": conceito,
                    "termos": info.get("termos", []),
                    "sem_icone_literal": sem_lit,
                    "melhores_palpites": [
                        {"icone": m.icone, "score": m.score, "alias": m.alias_casado}
                        for m in achados[:3]
                    ],
                }

    # Colisao: mesmo icone reaproveitado em dois cards da mesma regiao.
    # docs/repertorio-icones.md proibe repetir icone na mesma pagina, entao isso
    # precisa aparecer aqui e nao so na validacao final.
    colisoes = {}
    for ident, d in batidos.items():
        regiao = ident.split("/", 1)[0]
        colisoes.setdefault((regiao, d["icone"]), []).append(ident)
    for (regiao, icone), idents in sorted(colisoes.items()):
        if len(idents) > 1:
            avisos.append(
                f"REPETIDO em '{regiao}': {icone} casou com {len(idents)} cards "
                f"({', '.join(i.split('/', 1)[1] for i in idents)}). "
                f"Escolher variante distinta para todos menos um."
            )

    saida = {
        "conceitos_md": os.path.abspath(args.conceitos),
        "batidos": batidos,
        "sem_match": sem_match,
        "avisos": avisos,
    }
    with open(args.saida, "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=1)

    total = len(batidos) + len(sem_match)
    print(f"{len(batidos)}/{total} ja validados na base, {len(sem_match)} vao para o harvest.")
    for ident, d in sorted(batidos.items()):
        print(f"  = {ident:<38} {d['icone']:<50} ({d['score']}, '{d['alias_casado']}')")
    for ident, d in sorted(sem_match.items()):
        palpite = d["melhores_palpites"][0]["icone"] if d["melhores_palpites"] else "-"
        print(f"  ? {ident:<38} sem match (melhor palpite fraco: {palpite})")
    if avisos:
        print("\nAVISOS:")
        for a in avisos:
            print(f"  ! {a}")
    print(f"\n{args.saida} escrito.")
    if sem_match:
        print("Agora: python3 harvest-candidatos.py " + args.saida + " -o candidatos/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
