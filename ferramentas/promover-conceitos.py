"""Propoe promover para a base de conceitos os icones descobertos numa LP aprovada.

Este e o loop de aprendizado: cada LP entregue devolve para
`especialidades/<esp>/conceitos.md` os pares conceito->icone que ela validou, e a
proxima LP ja comeca com eles resolvidos.

Existe porque a promocao manual nao acontece. Em
`projetos/dr-rodrigo-pires/mapa-icones.md` o unico icone novo da entrega
(`healthicons:blood-cells-outline`) ficou registrado como "vale registrar em
conceitos.md numa proxima PR de manutencao do repo" -- e nunca foi. Boa intencao
escrita no meio de um markdown nao e mecanismo.

DUAS TRAVAS DE PROPOSITO:

1. So roda depois da LP aprovada. Icone escolhido mas nao publicado nao virou
   conhecimento ainda -- promover antes enche a base de ruido.
2. NAO ESCREVE no conceitos.md. Imprime o diff pronto para revisao. O arquivo e
   editado a mao por mais de uma pessoa e vive na branch de outro dono; escrever
   direto criaria conflito de merge silencioso.

Uso:
    python3 promover-conceitos.py projetos/<cliente>/mapa-icones.md \\
            especialidades/ortopedia/conceitos.md
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conceitos import carregar, normalizar, ErroDeEsquema  # noqa: E402


def _celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def _e_separador(linha):
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", linha.strip())) and "-" in linha


def ler_mapa(caminho):
    """Le mapa-icones.md preenchido -> lista de dicts."""
    linhas, cabecalho = [], None
    with open(caminho, encoding="utf-8") as fh:
        for l in fh:
            if not l.strip().startswith("|"):
                cabecalho = None
                continue
            cels = _celulas(l)
            if cabecalho is None:
                cabecalho = [c.strip().lower() for c in cels]
                continue
            if _e_separador(l):
                continue
            if len(cels) == len(cabecalho):
                linhas.append(dict(zip(cabecalho, cels)))
    return linhas


def main():
    ap = argparse.ArgumentParser(
        description="Propoe (sem escrever) o que promover para a base de conceitos."
    )
    ap.add_argument("mapa", help="projetos/<cliente>/mapa-icones.md de uma LP APROVADA")
    ap.add_argument("conceitos")
    ap.add_argument("--projeto", help="nome para a coluna Procedencia "
                                      "(default: nome da pasta do mapa)")
    args = ap.parse_args()

    try:
        base = carregar(args.conceitos)
    except ErroDeEsquema as e:
        print(f"ERRO DE ESQUEMA: {e}", file=sys.stderr)
        return 2

    projeto = args.projeto or os.path.basename(os.path.dirname(os.path.abspath(args.mapa)))
    linhas = ler_mapa(args.mapa)
    if not linhas:
        print(f"nenhuma linha de card em {args.mapa}", file=sys.stderr)
        return 1

    ja_conhecidos = {c.icone for c in base.conceitos}
    descritos = {i.icone for i in base.icones}

    novos_conceitos, novas_conexoes, sem_fonte = [], [], 0
    # Sem isto, um icone usado em varias paginas (ex.: bone-crack-outline em
    # joelho, ombro, quadril e punho-mao) seria proposto como conceito novo uma
    # vez por pagina, inflando a base com linhas duplicadas.
    propostos = set()
    vistos_par = set()
    for l in linhas:
        icone = (l.get("ícone de origem") or l.get("icone de origem") or "").strip("` ")
        card = l.get("card", "").strip()
        desc = l.get("o que o desenho mostra", "").strip()
        fonte = (l.get("fonte") or "").strip().lower()
        if not icone or not card:
            continue
        if not fonte:
            sem_fonte += 1

        # so promove o que a LP descobriu; reaproveitamento da base nao e novidade
        if fonte and fonte != "harvest-novo":
            continue
        if not fonte and icone in ja_conhecidos:
            continue

        par = (normalizar(card), icone)
        if par in vistos_par:
            continue  # mesmo conceito+icone repetido em outra pagina da LP
        vistos_par.add(par)

        if icone in ja_conhecidos or icone in propostos:
            # icone ja existe (na base ou proposto acima nesta execucao), mas
            # cobrindo outro conceito: so acrescenta a conexao, sem duplicar
            # linha de conceito
            novas_conexoes.append((icone, card, desc))
        else:
            novos_conceitos.append((icone, card, desc))
            propostos.add(icone)

    print(f"# Promocao proposta a partir de {args.mapa}")
    print(f"# projeto: {projeto} | {len(linhas)} cards lidos")
    if sem_fonte:
        print(f"# aviso: {sem_fonte} linhas sem coluna 'Fonte' -- sem ela nao da para "
              f"distinguir reaproveitamento de descoberta; promocao fica conservadora.")
    print("#")
    print("# NADA foi escrito. Revise e aplique a mao em:", args.conceitos)
    print()

    if not novos_conceitos and not novas_conexoes:
        print("Nada a promover: a LP nao introduziu conceito nem conexao nova.")
        return 0

    if novos_conceitos:
        print("## Linhas novas para a tabela de conceitos")
        print("## (escolha a secao certa: sintoma / anatomia / consulta)")
        print()
        for icone, card, desc in novos_conceitos:
            alias = normalizar(card)
            print(f"| {card} | `{icone}` | {alias} | {projeto} |")
        print()

    if novos_conceitos or novas_conexoes:
        print("## Linhas para a tabela 'Icones — descricoes e conexoes'")
        print()
        for icone, card, desc in novos_conceitos:
            if icone not in descritos:
                print(f"| `{icone}` | flat-mono | {desc or '[DESCREVER O DESENHO]'} | {card} |")
        for icone, card, _ in novas_conexoes:
            print(f"# em `{icone}`: acrescentar '{card}' na coluna "
                  f"'Conceitos que ja cobriu'")
        print()

    print(f"# {len(novos_conceitos)} conceito(s) novo(s), "
          f"{len(novas_conexoes)} conexao(oes) nova(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
