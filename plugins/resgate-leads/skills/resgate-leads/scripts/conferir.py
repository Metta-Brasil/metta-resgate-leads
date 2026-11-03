#!/usr/bin/env python3
"""Confere as mensagens do resgate antes de irem para a SDR.

Uso:
  python3 conferir.py <arquivo-do-lead.md | pasta-saida> [--raiz ~/Metta-Resgate]

Lê cada seção que começa com "## Mensagem" ou "## Resposta" e confere o bloco de código dela
(o texto que vai para o lead). Também confere a lista "Anexo:" da seção, se houver.
Sai com código 1 se encontrar problema. Mensagem com problema não vai para a SDR.
"""
import argparse, json, os, re, sys

TERMOS = [
    (r"r\$|\bpre[çc]o|\bvalor(es)?\b|\bparcela|\bdesconto|\bplano(s)?\b|\bblack\b|\bcondi[çc][ãa]o", "preço ou condição comercial"),
    (r"\bmql\b|\bsal\b|\bsql\b|\bperfil\b|qualifica[çc]", "rótulo interno de qualificação"),
    (r"\bmotivo\b|\bperdid[oa]\b|\bnota interna", "dado interno"),
    (r"grava[çc][ãa]o|gravad[ao]|\bgravei\b", "menção a gravação"),
    (r"\bcriativo", "use \"anúncio\", nunca \"criativo\""),
    (r"\bespecial\b", "palavra \"especial\""),
    (r"alavanc|potencializ|framework|destrave|mindset|\bjornada\b|transforma", "palavra banida"),
    (r"https?://|www\.|\.com\b|\.com\.br\b", "link"),
]
RE_EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F2FF\U00002600-\U000026FF]")
MAX_VIDEO = 16 * 1024 * 1024
MAX_IMG = 5 * 1024 * 1024


def secoes(texto):
    partes = re.split(r"(?m)^## ", texto)
    for p in partes[1:]:
        titulo, _, corpo = p.partition("\n")
        if re.match(r"(Mensagem|Resposta)", titulo, re.I):
            yield titulo.strip(), corpo


def blocos(corpo):
    return re.findall(r"```[^\n]*\n(.*?)\n```", corpo, re.S)


def anexos(corpo):
    m = re.search(r"(?mi)^Anexo:\s*\n((?:\s*-\s+.+\n?)+)", corpo)
    return [l.strip()[2:].strip() for l in m.group(1).splitlines() if l.strip().startswith("-")] if m else []


def conferir_bloco(txt, proibidos):
    prob = []
    if re.search(r"\[|\]", txt):
        prob.append("tem colchete: campo não preenchido")
    baixo = txt.lower()
    for padrao, nome in TERMOS:
        if re.search(padrao, baixo):
            prob.append(f"{nome}: \"{re.search(padrao, baixo).group(0)}\"")
    for c in proibidos:
        if c and c.lower() in baixo:
            prob.append(f"cliente proibido: {c}")
    if RE_EMOJI.search(txt):
        prob.append("emoji")
    if "—" in txt or " – " in txt:
        prob.append("travessão")
    if txt.count("!") > 1:
        prob.append("mais de uma exclamação")
    if txt.count("?") > 1:
        prob.append("mais de uma pergunta")
    if "**" in txt:
        prob.append("negrito com dois asteriscos (no WhatsApp é um só)")
    if txt.count("*") % 2:
        prob.append("asterisco sem par")
    if len(txt) > 1000:
        prob.append(f"longa demais ({len(txt)} caracteres)")
    if not txt.strip():
        prob.append("bloco vazio")
    return prob


def conferir_anexos(lista, corpo_txt):
    prob = []
    if "desse anúncio" in corpo_txt and not lista:
        prob.append("fala de \"desse anúncio\" mas não tem anexo")
    for a in lista:
        if not os.path.exists(os.path.expanduser(a)):
            prob.append(f"anexo não existe: {a}")
            continue
        tam = os.path.getsize(os.path.expanduser(a))
        ext = os.path.splitext(a)[1].lower()
        if ext in {".mp4", ".3gp"} and tam > MAX_VIDEO:
            prob.append(f"vídeo acima de 16 MB: {a}")
        if ext in {".jpg", ".jpeg", ".png", ".webp"} and tam > MAX_IMG:
            prob.append(f"imagem acima de 5 MB: {a}")
    return prob


def conferir_arquivo(caminho, proibidos):
    texto = open(caminho, encoding="utf-8").read()
    total = 0
    for titulo, corpo in secoes(texto):
        bs = blocos(corpo)
        prob = []
        if len(bs) != 1:
            prob.append(f"precisa de exatamente 1 bloco de código, tem {len(bs)}")
        for b in bs:
            prob += conferir_bloco(b, proibidos)
            prob += conferir_anexos(anexos(corpo), b)
        estado = "OK" if not prob else "PROBLEMA"
        print(f"{os.path.basename(caminho)} · {titulo}: {estado}")
        for p in prob:
            print(f"   - {p}")
        total += len(prob)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo")
    ap.add_argument("--raiz", default=os.environ.get("RESGATE_RAIZ", os.path.expanduser("~/Metta-Resgate")))
    a = ap.parse_args()
    cfg_p = os.path.join(os.path.expanduser(a.raiz), "config.json")
    proibidos = json.load(open(cfg_p, encoding="utf-8")).get("clientes_proibidos", []) if os.path.exists(cfg_p) else []
    arquivos = [a.alvo] if os.path.isfile(a.alvo) else sorted(
        os.path.join(a.alvo, f) for f in os.listdir(a.alvo) if f.endswith(".md") and not f.startswith("_"))
    total = sum(conferir_arquivo(f, proibidos) for f in arquivos)
    print(f"\n{total} problema(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
