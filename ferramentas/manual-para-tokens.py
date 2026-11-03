"""Converte um manual de marca do cliente em design tokens CSS.

Este e o motor da diferenciacao estetica entre clientes, e nao e teoria: a LP da
Dra. Genesia Regina foi construida a partir do manual dela, e cruzando o `.docx`
com os tokens `:root` da pagina publicada, **8 de 8 cores e 2 de 2 fontes batem
literalmente** (#7E552F->--brown, #5C3F23->--ink, #90A570->--sage,
#C5C381->--olive, #C6A971->--sand, #EEBC9C->--peach, #8CBEC6->--blue,
#FFFCED->--cream, Playfair Display->--serif, Poppins->--sans).

A estetica nao veio de gosto: veio de um documento estruturado transcrito 1:1.
Isso explica por que as outras LPs se parecem -- a maioria dos clientes nao tem
manual, entao nao ha fonte estruturada e o build cai no tokens.css padrao.

O manual da tambem o que paleta nenhuma da: a **metafora condutora** (na
Genesia, a arvore da vida: raizes -> florescimento) e a lista de "o que nao
fazer". Sao esses dois que sustentam a diferenciacao, mais que o hex.

Uso:
    python3 manual-para-tokens.py "Identidade Visual - Cliente.docx"
    python3 manual-para-tokens.py manual.docx --prefixo marca -o tokens-cliente.css

Formatos aceitos: .docx e .md/.txt. PDF nao (exigiria dependencia externa; a
restricao do repo e stdlib apenas). Para PDF, exporte para docx antes.
"""

import argparse
import html
import os
import re
import sys
import unicodedata
import zipfile

# Nomes de cor comuns em manual de marca PT-BR -> sugestao de token.
# Nao e traducao automatica: e um chute inicial que o humano revisa. O papel
# declarado no manual manda mais que o nome da cor.
SUGESTAO_TOKEN = {
    "marrom": "brown", "verde": "green", "salvia": "sage", "oliva": "olive",
    "dourado": "gold", "areia": "sand", "bege": "beige", "terracota": "terracotta",
    "pessego": "peach", "azul": "blue", "creme": "cream", "branco": "white",
    "preto": "black", "cinza": "gray", "vermelho": "red", "rosa": "pink",
    "roxo": "purple", "amarelo": "yellow", "laranja": "orange", "navy": "navy",
    "grafite": "graphite", "carvao": "charcoal", "vinho": "wine",
}

PAPEL_ESTRUTURAL = [
    (r"fundo|background", "fundo"),
    (r"texto|tipografia de apoio|corpo", "texto"),
    (r"prim[aá]ria|principal|logotipo", "primaria"),
    (r"acento|destaque|acabamento", "acento"),
    (r"secund[aá]ri", "secundaria"),
    (r"complementar|apoio", "complementar"),
]


def sem_acento(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def ler_docx(caminho):
    z = zipfile.ZipFile(caminho)
    xml = z.read("word/document.xml").decode("utf-8", "ignore")
    paras = []
    for bloco in re.split(r"</w:p>", xml):
        txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", bloco, re.S))
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt)).strip()
        if txt:
            paras.append(txt)
    return paras


def ler_texto(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return [l.strip() for l in fh if l.strip()]


def sugerir_nome(rotulo, usados):
    base = None
    s = sem_acento(rotulo)
    for chave, token in SUGESTAO_TOKEN.items():
        if chave in s:
            base = token
            break
    if not base:
        base = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:14] or "cor"
    nome, i = base, 2
    while nome in usados:
        nome = f"{base}-{i}"
        i += 1
    usados.add(nome)
    return nome


def extrair(paras):
    """Devolve (cores, fontes, metafora, nao_fazer).

    cores: lista de (rotulo, hex, papel_declarado)
    O manual escreve tipicamente em 3 linhas seguidas:
        Marrom Tronco / #7E552F / Cor primaria da marca. Logotipo, titulos.
    """
    cores, fontes, nao_fazer = [], [], []
    metafora = []

    for i, p in enumerate(paras):
        m = re.fullmatch(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})", p.strip())
        if m:
            rotulo = paras[i - 1].strip() if i > 0 else "cor"
            papel = paras[i + 1].strip() if i + 1 < len(paras) else ""
            # rotulo nao pode ser outro hex nem cabecalho de secao
            if re.fullmatch(r"#[0-9A-Fa-f]{3,6}", rotulo) or len(rotulo) > 60:
                rotulo = "cor"
            if re.fullmatch(r"#[0-9A-Fa-f]{3,6}", papel) or len(papel) > 200:
                papel = ""
            cores.append((rotulo, "#" + m.group(1).upper(), papel))

        # "Fonte de destaque — Playfair Display" / "Fonte de apoio — Poppins"
        f = re.match(r"fonte\s+(?:de\s+)?([\w\s]+?)\s*[—\-–:]\s*(.+)", p, re.I)
        if f:
            fontes.append((f.group(1).strip(), f.group(2).strip()))

    texto = "\n".join(paras)
    mm = re.search(r"(?:conceito da marca|conceito)\s*(.{40,900}?)(?=\n[A-Z0-9]{2}\s|\n#|\Z)",
                   texto, re.S | re.I)
    if mm:
        metafora = [l.strip() for l in mm.group(1).split("\n") if len(l.strip()) > 30][:3]

    nf = re.search(r"o que n[aã]o fazer(.*?)(?=\n\d{2}\s|\Z)", texto, re.S | re.I)
    if nf:
        nao_fazer = [l.strip() for l in nf.group(1).split("\n")
                     if l.strip().lower().startswith("n") and len(l.strip()) > 12][:10]

    return cores, fontes, metafora, nao_fazer


def main():
    ap = argparse.ArgumentParser(description="Manual de marca -> design tokens.")
    ap.add_argument("manual")
    ap.add_argument("-o", "--saida")
    ap.add_argument("--prefixo", default="", help="prefixo dos tokens, ex: marca")
    args = ap.parse_args()

    if not os.path.exists(args.manual):
        print(f"nao encontrado: {args.manual}", file=sys.stderr)
        return 1

    if args.manual.lower().endswith(".docx"):
        paras = ler_docx(args.manual)
    elif args.manual.lower().endswith((".md", ".txt")):
        paras = ler_texto(args.manual)
    else:
        print("formato nao suportado. Use .docx, .md ou .txt "
              "(PDF exigiria dependencia externa; exporte antes).", file=sys.stderr)
        return 1

    cores, fontes, metafora, nao_fazer = extrair(paras)
    if not cores:
        print("Nenhuma cor encontrada. O extrator espera o hex numa linha propria, "
              "com o nome da cor na linha anterior e o papel na seguinte -- que e "
              "como manuais costumam sair de .docx. Confira o arquivo e, se o "
              "formato for outro, transcreva a paleta a mao.", file=sys.stderr)
        return 2

    pre = f"{args.prefixo}-" if args.prefixo else ""
    usados = set()
    L = []
    L.append("/* Tokens derivados do manual de marca do cliente.")
    L.append(f" * Fonte: {os.path.basename(args.manual)}")
    L.append(" *")
    L.append(" * Transcricao, nao interpretacao: cada valor abaixo esta declarado no")
    L.append(" * manual. Fugir de um token e decisao que se registra no visual-map")
    L.append(" * com justificativa -- nunca ajuste silencioso.")
    if metafora:
        L.append(" *")
        L.append(" * METAFORA CONDUTORA (o que de fato diferencia a LP, mais que o hex):")
        for l in metafora:
            L.append(f" *   {l[:150]}")
    L.append(" */")
    L.append(":root {")
    for rotulo, hexa, papel in cores:
        nome = sugerir_nome(rotulo, usados)
        comentario = f"  /* {rotulo}" + (f" — {papel[:80]}" if papel else "") + " */"
        L.append(f"  --{pre}{nome}: {hexa};{comentario}")
    if fontes:
        L.append("")
        for papel_f, familia in fontes:
            slug = re.sub(r"[^a-z0-9]+", "-", sem_acento(papel_f)).strip("-") or "font"
            L.append(f"  --{pre}font-{slug}: \"{familia}\";")
    L.append("}")

    css = "\n".join(L)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(css + "\n")
        print(f"tokens -> {args.saida}", file=sys.stderr)
    else:
        print(css)

    print(f"\n/* {len(cores)} cores, {len(fontes)} fontes extraidas. */", file=sys.stderr)
    if nao_fazer:
        print("\n/* RESTRICOES DECLARADAS NO MANUAL — sao contrato, nao sugestao: */",
              file=sys.stderr)
        for n in nao_fazer:
            print(f" * - {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
