"""Valida um `mapa-icones.md` preenchido. Sai com 1 se a pagina nao pode fechar.

As tres regras abaixo ja existiam em `docs/repertorio-icones.md` e
`templates/mapa-icones.md`, mas so como texto -- dependiam de alguem reler o
markdown e reparar. Nao funcionou: numa entrega de 2026-08 saiu ao vivo uma LP
com `healthicons:spine-outline` repetido em 5 cards da mesma pagina, e outra com
o mesmo icone de pe em 3 cards.

Este script nao substitui a revisao visual (escolher icone continua sendo
decisao humana, olhando a 32px). Ele garante que a pagina nao FECHA o checklist
com erro mecanico -- que e o que estava passando.

Uso:
    python3 validar-mapa-icones.py projetos/<cliente>/mapa-icones.md
    python3 validar-mapa-icones.py <arquivo> --escopo secao   # repeticao por secao
"""

import argparse
import os
import re
import sys

COL_SECAO = "seção"
COL_CARD = "card"
COL_ARQUIVO = "arquivo"
COL_ORIGEM = "ícone de origem"
COL_CONFERIDO = "conferido a 32px"
COL_FONTE = "fonte"

OBRIGATORIAS = [COL_SECAO, COL_CARD, COL_ARQUIVO, COL_ORIGEM, COL_CONFERIDO]
FONTES_VALIDAS = {"conceitos.md", "harvest-novo", "externo"}


def _celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def _e_separador(linha):
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", linha.strip())) and "-" in linha


def _limpar(txt):
    return txt.strip().strip("`").strip()


def ler_linhas(caminho):
    """Devolve (linhas, mecanismo). Cada linha e um dict coluna->valor."""
    with open(caminho, encoding="utf-8") as fh:
        texto = fh.read()

    mecanismo = None
    m = re.search(r"^\s*(?:\*\*)?Mecanismo de renderiza[cç][aã]o(?:\*\*)?\s*:\s*(.+)$",
                  texto, re.M | re.I)
    if m:
        mecanismo = m.group(1).strip().strip("`")

    linhas, cabecalho = [], None
    for l in texto.splitlines():
        if not l.strip().startswith("|"):
            cabecalho = None
            continue
        cels = _celulas(l)
        if cabecalho is None:
            cabecalho = [c.strip().lower() for c in cels]
            continue
        if _e_separador(l):
            continue
        if len(cels) != len(cabecalho):
            continue
        linhas.append(dict(zip(cabecalho, cels)))
    return linhas, cabecalho, mecanismo


def main():
    ap = argparse.ArgumentParser(description="Valida mapa-icones.md preenchido.")
    ap.add_argument("mapa")
    ap.add_argument("--escopo", choices=["pagina", "secao"], default="pagina",
                    help="onde a repeticao e proibida (default: pagina inteira)")
    args = ap.parse_args()

    linhas, cabecalho, mecanismo = ler_linhas(args.mapa)
    erros, avisos = [], []

    if not linhas:
        print(f"ERRO: {args.mapa}: nenhuma linha de card encontrada.", file=sys.stderr)
        return 1

    faltando = [c for c in OBRIGATORIAS if c not in (cabecalho or [])]
    if faltando:
        print(f"ERRO: colunas obrigatorias ausentes: {faltando}\n"
              f"      cabecalho lido: {cabecalho}", file=sys.stderr)
        return 1

    if not mecanismo:
        avisos.append(
            "sem 'Mecanismo de renderizacao:' no topo do arquivo. Registrar "
            "(svg-local | css-mask-cdn | react-component | icon-font) -- LPs de "
            "clientes diferentes usam mecanismos diferentes e isso precisa ficar "
            "rastreavel."
        )

    # 1) conferido a 32px
    for i, l in enumerate(linhas, 1):
        v = l.get(COL_CONFERIDO, "").strip().lower()
        if v not in ("sim", "s", "x", "✓"):
            erros.append(
                f"linha {i} ({l.get(COL_CARD, '?')}): 'conferido a 32px' = "
                f"'{l.get(COL_CONFERIDO, '')}'. Icone nao conferido visualmente nao "
                f"passa -- escolher por nome e a falha original do processo."
            )

    # 2) repeticao de icone
    chave = (lambda l: "") if args.escopo == "pagina" else (lambda l: l.get(COL_SECAO, ""))
    usos = {}
    for l in linhas:
        origem = _limpar(l.get(COL_ORIGEM, ""))
        if not origem or origem in ("-", "—"):
            continue
        usos.setdefault((chave(l), origem), []).append(l.get(COL_CARD, "?"))
    for (esc, origem), cards in sorted(usos.items()):
        if len(cards) > 1:
            onde = f" em '{esc}'" if esc else ""
            erros.append(
                f"icone repetido{onde}: {origem} usado em {len(cards)} cards "
                f"({', '.join(cards)}). Usar variante distinta em todos menos um."
            )

    # 3) arquivo dentro da pasta da secao / do cliente
    for i, l in enumerate(linhas, 1):
        arq = _limpar(l.get(COL_ARQUIVO, ""))
        if not arq or arq in ("-", "—"):
            continue
        if "/" not in arq:
            erros.append(
                f"linha {i} ({l.get(COL_CARD, '?')}): arquivo '{arq}' sem pasta. "
                f"Regra estrutural: `<pasta-do-topico>/<slug>.svg` -- icone de outro "
                f"topico tem que ser geograficamente impossivel."
            )

    # 4) Fonte (coluna nova, opcional mas util para o loop de promocao)
    if COL_FONTE in (cabecalho or []):
        for i, l in enumerate(linhas, 1):
            v = l.get(COL_FONTE, "").strip().lower()
            if v and v not in FONTES_VALIDAS:
                avisos.append(
                    f"linha {i}: fonte '{v}' desconhecida "
                    f"(validas: {sorted(FONTES_VALIDAS)})"
                )
    else:
        avisos.append(
            "sem coluna 'Fonte' -- sem ela, promover-conceitos.py nao consegue "
            "distinguir o que e reaproveitamento do que e descoberta nova."
        )

    print(f"{os.path.basename(args.mapa)}: {len(linhas)} cards"
          + (f", mecanismo '{mecanismo}'" if mecanismo else ""))
    for a in avisos:
        print(f"  aviso: {a}")
    for e in erros:
        print(f"  ERRO: {e}")

    if erros:
        print(f"\n{len(erros)} erro(s). A pagina nao fecha o checklist.")
        return 1
    print("\nOK -- sem icone repetido, todos conferidos a 32px, arquivos em pasta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
