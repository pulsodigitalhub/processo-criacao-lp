"""Le a base de conceitos de uma especialidade (`especialidades/<esp>/conceitos.md`).

Existe por causa de uma falha real: um agente precisava escolher 72 icones para
LPs de ortopedia, ignorou este arquivo, foi direto na API do Iconify inventando
termo em ingles, e entregou balanca de tribunal para "instabilidade" e balao de
festa para "inchaco" -- ambos com resposta ja validada nas tabelas daqui.

O conserto nao e "lembrar de ler o markdown": e tornar a base consultavel por
script, para que reaproveitar seja mais barato que buscar de novo.

O markdown continua sendo a UNICA fonte -- nao existe json/yaml paralelo. O
arquivo e editado a mao por mais de uma pessoa, e um gerador criaria dois
artefatos que divergem na primeira edicao manual.

Uso como modulo:
    from conceitos import carregar
    base = carregar("especialidades/ortopedia/conceitos.md")
    base.buscar("dor ao dormir de lado")   -> [Match(...), ...]

Uso como CLI (inspecao rapida):
    python3 conceitos.py especialidades/ortopedia/conceitos.md
    python3 conceitos.py especialidades/ortopedia/conceitos.md --buscar "inchaco"
"""

import argparse
import re
import sys
import unicodedata
from collections import namedtuple

# Cabecalhos esperados. Sao contrato: se mudarem, o parser para com erro
# explicito em vez de ler errado em silencio -- ler errado e pior que nao ler,
# porque o agente confia no resultado.
COLUNAS_CONCEITO = ["conceito", "icone", "aliases", "procedencia"]
COLUNAS_ICONE = ["icone", "meio", "descricao visual", "conceitos que ja cobriu"]

TITULO_TABELA_ICONES = "icones - descricoes e conexoes"
TITULO_SEM_LITERAL = "sem icone literal em lugar nenhum"

MEIOS_VALIDOS = {"flat-mono", "color-emoji", "3d-clay", "line-art", "duotone", "ilustracao"}

Conceito = namedtuple("Conceito", "conceito icone aliases procedencia secao")
IconeInfo = namedtuple("IconeInfo", "icone meio descricao conceitos")
Match = namedtuple("Match", "conceito icone alias_casado procedencia secao score")


class ErroDeEsquema(Exception):
    """Cabecalho fora do contrato. Falhar alto, nunca ler errado."""


def normalizar(txt):
    """Minusculas, sem acento, sem pontuacao de borda. Usado em comparacao."""
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    txt = txt.lower().strip()
    txt = re.sub(r"[`*_]", "", txt)
    # travessao/meia-risca viram hifen: "Icones — descricoes" e "Icones - descricoes"
    # tem que casar, senao o titulo da secao nunca bate com a constante.
    txt = txt.replace("—", "-").replace("–", "-").replace("−", "-")
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip(" .;:-")


def _celulas(linha):
    """Quebra uma linha de tabela GFM em celulas, sem os pipes das bordas."""
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def _e_separador(linha):
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", linha.strip())) and "-" in linha


def _partir_lista(txt):
    """`a; b; c` -> [a, b, c]. Ponto-e-virgula porque virgula aparece dentro de conceito."""
    return [p.strip() for p in txt.split(";") if p.strip()]


def _limpar_icone(txt):
    return txt.strip().strip("`").strip()


class Base:
    def __init__(self, conceitos, icones, sem_literal, caminho):
        self.conceitos = conceitos
        self.icones = icones
        self.sem_literal = sem_literal
        self.caminho = caminho

    def buscar(self, termo, limite=5):
        """Casa `termo` contra conceito e aliases. Devolve Match ordenado por score.

        Score maior = melhor. Exato vale mais que contido, para o caso comum de
        um alias curto ("dor") aparecer dentro de varios conceitos.
        """
        alvo = normalizar(termo)
        if not alvo:
            return []
        achados = []
        for c in self.conceitos:
            candidatos = [c.conceito] + c.aliases
            melhor = None
            for cand in candidatos:
                n = normalizar(cand)
                if not n:
                    continue
                if n == alvo:
                    score = 100
                elif alvo in n or n in alvo:
                    # proporcional ao quanto se sobrepoe, para "dor" nao ganhar de
                    # "dor ao dormir de lado" quando o alvo e a frase inteira
                    score = 60 + int(30 * min(len(n), len(alvo)) / max(len(n), len(alvo)))
                else:
                    palavras_a = set(alvo.split())
                    palavras_n = set(n.split())
                    comuns = palavras_a & palavras_n
                    if not comuns:
                        continue
                    score = int(50 * len(comuns) / len(palavras_a | palavras_n))
                if melhor is None or score > melhor[0]:
                    melhor = (score, cand)
            if melhor and melhor[0] >= 30:
                achados.append(Match(c.conceito, c.icone, melhor[1], c.procedencia, c.secao, melhor[0]))
        achados.sort(key=lambda m: (-m.score, m.conceito))
        return achados[:limite]

    def meio_de(self, icone):
        for i in self.icones:
            if i.icone == icone:
                return i.meio
        return None

    def e_sem_literal(self, termo):
        """True se o termo cai na lista de conceitos sem icone literal."""
        alvo = normalizar(termo)
        for s in self.sem_literal:
            n = normalizar(s)
            if n and (n in alvo or alvo in n):
                return s
        return None


def _ler_tabelas(texto, caminho):
    """Varre o markdown coletando tabelas por secao (## titulo)."""
    secao = None
    tabelas = []  # (secao, cabecalho, [linhas])
    atual = None
    for linha in texto.splitlines():
        if linha.startswith("## "):
            secao = linha[3:].strip()
            atual = None
            continue
        if linha.strip().startswith("|"):
            if atual is None:
                atual = {"secao": secao, "cabecalho": _celulas(linha), "linhas": []}
                tabelas.append(atual)
            elif _e_separador(linha):
                continue
            else:
                atual["linhas"].append(_celulas(linha))
        else:
            atual = None
    return tabelas


def _ler_sem_literal(texto):
    """Extrai os conceitos em negrito da secao 'Sem icone literal'."""
    m = re.search(r"^##\s+Sem .cone literal.*?$(.*?)(?=^##\s|\Z)", texto, re.S | re.M)
    if not m:
        return []
    bloco = m.group(1)
    negrito = re.findall(r"\*\*(.+?)\*\*", bloco, re.S)
    if not negrito:
        return []
    # Só o PRIMEIRO negrito é a lista de conceitos. Os demais negritos da seção
    # são ênfase de prosa ("mesma região", "remover o card") e entrariam como
    # conceito falso, fazendo e_sem_literal() casar com qualquer coisa.
    n = re.sub(r"\se\s", ", ", negrito[0])
    itens = []
    for p in n.split(","):
        p = p.strip()
        if p and len(p) < 40:
            itens.append(p)
    return itens


def carregar(caminho):
    with open(caminho, encoding="utf-8") as fh:
        texto = fh.read()

    tabelas = _ler_tabelas(texto, caminho)
    if not tabelas:
        raise ErroDeEsquema(f"{caminho}: nenhuma tabela encontrada.")

    conceitos, icones = [], []
    vistas_conceito = 0

    for t in tabelas:
        cab = [normalizar(c) for c in t["cabecalho"]]
        secao_norm = normalizar(t["secao"] or "")

        if secao_norm == TITULO_TABELA_ICONES:
            if cab != COLUNAS_ICONE:
                raise ErroDeEsquema(
                    f"{caminho}: tabela de icones (secao '{t['secao']}') com cabecalho "
                    f"{cab}, esperado {COLUNAS_ICONE}. Corrija o markdown ou atualize "
                    f"COLUNAS_ICONE em ferramentas/conceitos.py -- nao ignore."
                )
            for l in t["linhas"]:
                if len(l) != len(COLUNAS_ICONE):
                    continue
                meio = normalizar(l[1])
                if meio not in MEIOS_VALIDOS:
                    raise ErroDeEsquema(
                        f"{caminho}: meio '{l[1]}' invalido para {l[0]}. "
                        f"Validos: {sorted(MEIOS_VALIDOS)}"
                    )
                icones.append(IconeInfo(_limpar_icone(l[0]), meio, l[2], _partir_lista(l[3])))
            continue

        # Toda tabela que nao e a de icones TEM que ser tabela de conceito.
        # Nao existe escapatoria de "tabela de outra natureza": ela permitia
        # que um cabecalho com colunas trocadas fosse pulado em silencio, e o
        # arquivo carregasse com 43 conceitos em vez de 60 sem ninguem notar.
        if cab != COLUNAS_CONCEITO:
            raise ErroDeEsquema(
                f"{caminho}: tabela de conceitos (secao '{t['secao']}') com cabecalho "
                f"{cab}, esperado {COLUNAS_CONCEITO}. Corrija o markdown ou atualize "
                f"COLUNAS_CONCEITO em ferramentas/conceitos.py -- nao ignore."
            )
        vistas_conceito += 1
        for l in t["linhas"]:
            if len(l) != len(COLUNAS_CONCEITO):
                continue
            conceitos.append(
                Conceito(l[0].strip(), _limpar_icone(l[1]), _partir_lista(l[2]),
                         l[3].strip(), t["secao"])
            )

    if vistas_conceito == 0:
        raise ErroDeEsquema(
            f"{caminho}: nenhuma tabela de conceitos valida. Cabecalho esperado: "
            f"{COLUNAS_CONCEITO}"
        )

    return Base(conceitos, icones, _ler_sem_literal(texto), caminho)


def main():
    ap = argparse.ArgumentParser(description="Inspeciona a base de conceitos de icones.")
    ap.add_argument("conceitos")
    ap.add_argument("--buscar", help="termo para testar o casamento")
    args = ap.parse_args()

    try:
        base = carregar(args.conceitos)
    except ErroDeEsquema as e:
        print(f"ERRO DE ESQUEMA: {e}", file=sys.stderr)
        return 2

    if args.buscar:
        achados = base.buscar(args.buscar)
        sem_lit = base.e_sem_literal(args.buscar)
        if sem_lit:
            print(f"! '{sem_lit}' esta na lista SEM ICONE LITERAL.")
            print("  Usar o anatomico da mesma regiao, ou remover o card. Nunca forma abstrata.\n")
        if not achados:
            print("nenhum match -- este card vai para o harvest.")
        for m in achados:
            print(f"{m.score:3d}  {m.icone:<52} <- '{m.alias_casado}'  [{m.secao}]")
        return 0

    print(f"{len(base.conceitos)} conceitos, {len(base.icones)} icones descritos, "
          f"{len(base.sem_literal)} sem icone literal")
    secoes = {}
    for c in base.conceitos:
        secoes[c.secao] = secoes.get(c.secao, 0) + 1
    for s, n in secoes.items():
        print(f"  {n:3d}  {s}")
    if base.sem_literal:
        print("\nsem icone literal: " + ", ".join(base.sem_literal))
    return 0


if __name__ == "__main__":
    sys.exit(main())
