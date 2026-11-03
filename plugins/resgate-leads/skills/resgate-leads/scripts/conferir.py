#!/usr/bin/env python3
"""Confere as mensagens do resgate antes de irem para a SDR.

Uso:
  python3 conferir.py <arquivo-do-lead.md | pasta Metta-Resgate/leads>

Cada bloco de código do arquivo é uma mensagem para o lead. O script confere cada um.
"[dia e hora]" é permitido: a SDR preenche com os horários reais.
Sai com código 1 se encontrar problema.
"""
import os, re, sys

TERMOS = [
    (r"r\$|\bpre[çc]o|\bvalor(es)?\b|\bparcela|\bdesconto|\bplano(s)?\b|\bblack\b|\bcondi[çc][ãa]o", "preço ou condição comercial"),
    (r"\bmql\b|\bsql\b|\bperfil\b|qualifica[çc]", "rótulo interno"),
    (r"\bmotivo\b|\bperdid[oa]\b", "dado interno"),
    (r"grava[çc][ãa]o|gravad[ao]", "menção a gravação"),
    (r"\bcriativo", "use \"anúncio\", nunca \"criativo\""),
    (r"\bespecial\b", "palavra \"especial\""),
    (r"alavanc|potencializ|framework|destrave|mindset|\bjornada\b|transforma", "palavra banida"),
    (r"https?://|www\.", "link"),
]
RE_EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F2FF\U00002600-\U000026FF]")


def conferir_bloco(txt):
    prob = []
    sem_horario = txt.replace("[dia e hora]", "")
    if re.search(r"\[|\]", sem_horario):
        prob.append("tem colchete: campo não preenchido")
    baixo = txt.lower()
    for padrao, nome in TERMOS:
        m = re.search(padrao, baixo)
        if m:
            prob.append(f"{nome}: \"{m.group(0)}\"")
    if RE_EMOJI.search(txt):
        prob.append("emoji")
    if "—" in txt or " – " in txt:
        prob.append("travessão")
    if txt.count("?") > 1:
        prob.append("mais de uma pergunta")
    if "**" in txt:
        prob.append("negrito com dois asteriscos (no WhatsApp é um só)")
    if txt.count("*") % 2:
        prob.append("asterisco sem par")
    if not txt.strip():
        prob.append("mensagem vazia")
    return prob


def conferir_arquivo(caminho):
    texto = open(caminho, encoding="utf-8").read()
    blocos = re.findall(r"```[^\n]*\n(.*?)\n```", texto, re.S)
    total = 0
    for i, b in enumerate(blocos, 1):
        prob = conferir_bloco(b)
        print(f"{os.path.basename(caminho)} · bloco {i}: {'OK' if not prob else 'PROBLEMA'}")
        for p in prob:
            print(f"   - {p}")
        total += len(prob)
    return total


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    alvo = sys.argv[1]
    arquivos = [alvo] if os.path.isfile(alvo) else sorted(
        os.path.join(alvo, f) for f in os.listdir(alvo) if f.endswith(".md"))
    total = sum(conferir_arquivo(f) for f in arquivos)
    print(f"\n{total} problema(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
