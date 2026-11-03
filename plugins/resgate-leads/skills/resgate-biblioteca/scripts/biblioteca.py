#!/usr/bin/env python3
"""Biblioteca de anúncios do resgate: pasta de trabalho, índice e localização do anúncio na pasta do Drive.

A biblioteca fica FORA do plugin (padrão: ~/Metta-Resgate/biblioteca), porque a atualização do
plugin substitui a pasta dele. Assim o que já foi lido e validado não se perde.

Comandos:
  init [--raiz DIR] [--drive PASTA]        cria a pasta de trabalho e o config.json (não sobrescreve)
  config                                   mostra o config.json
  id <utm_content>                         extrai o ID do anúncio (ex.: PP-APLI-223)
  localizar <ID> [--drive PASTA]           procura os arquivos do anúncio na pasta do Drive
  listar [--status S]                      lista o índice
  ver <ID>                                 mostra o registro de um anúncio
  registrar <ID> --formato F --origem ARQ... [--envio ARQ...] [--status S] [--obs TEXTO]
  status <ID> <validado|pendente|datado|proibido|nao_localizado> [--por NOME] [--obs TEXTO]
"""
import argparse, json, os, re, sys, datetime, unicodedata

RAIZ_PADRAO = os.path.expanduser("~/Metta-Resgate")
STATUS = ["validado", "pendente", "datado", "proibido", "nao_localizado"]
EXT_IMG = {".png", ".jpg", ".jpeg", ".webp"}
EXT_VID = {".mp4", ".mov", ".m4v", ".3gp"}
EXT_DOC = {".pdf"}
RE_ID = re.compile(r"^(PP-[A-Z]+(?:-[A-Z]+)*?-\d{2,4})(?!\d)")


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def raiz(args=None):
    r = getattr(args, "raiz", None) or os.environ.get("RESGATE_RAIZ") or RAIZ_PADRAO
    return os.path.expanduser(r)


def carregar_config(r):
    p = os.path.join(r, "config.json")
    if not os.path.exists(p):
        sys.exit(f"Sem config em {p}. Rode: biblioteca.py init")
    return json.load(open(p, encoding="utf-8"))


def caminho_indice(r):
    return os.path.join(r, "biblioteca", "indice.json")


def carregar_indice(r):
    p = caminho_indice(r)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def salvar_indice(r, idx):
    p = caminho_indice(r)
    tmp = p + ".tmp"
    json.dump(idx, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(tmp, p)


def extrair_id(utm):
    s = (utm or "").strip().upper()
    m = RE_ID.match(s)
    return m.group(1) if m else None


def numero(id_):
    return id_.rsplit("-", 1)[-1]


def norm(s):
    return unicodedata.normalize("NFC", s).strip().upper()


def cmd_init(a):
    r = raiz(a)
    for sub in ["biblioteca/fichas", "biblioteca/arquivos", "saida"]:
        os.makedirs(os.path.join(r, sub), exist_ok=True)
    p = os.path.join(r, "config.json")
    if os.path.exists(p):
        print(f"config já existe: {p}")
    else:
        cfg = {
            "pasta_drive_anuncios": a.drive or "",
            "nome_sdr": "",
            "horario_comercial": {"dias": "seg-sex", "inicio": "09:00", "fim": "18:00"},
            "limite_diario_mensagem_1": 50,
            "dias_conversa_em_andamento": 7,
            "clientes_proibidos": [],
            "inicio_campanha": "2026-10-28",
            "origem_resgate_id": "fe254f0e-36c1-4db8-a84e-c8f52bf75824",
            "planilha_criativos_id": "1RvS3Iz-AemmR-LYPtDOMqq9IaKBVaPN6VNujKRUNV3U",
        }
        json.dump(cfg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"config criado: {p}")
    if not os.path.exists(caminho_indice(r)):
        salvar_indice(r, {})
    print(f"pasta de trabalho: {r}")


def cmd_config(a):
    print(json.dumps(carregar_config(raiz(a)), ensure_ascii=False, indent=1))


def tipo_arquivo(nome):
    e = os.path.splitext(nome)[1].lower()
    return "imagem" if e in EXT_IMG else "video" if e in EXT_VID else "pdf" if e in EXT_DOC else None


def cmd_localizar(a):
    r = raiz(a)
    drive = os.path.expanduser(a.drive or carregar_config(r).get("pasta_drive_anuncios", ""))
    if not drive or not os.path.isdir(drive):
        sys.exit(f"Pasta do Drive não encontrada: '{drive}'. Ajuste pasta_drive_anuncios no config.json.")
    id_ = norm(a.id)
    num = numero(id_)
    por_nome, por_pasta = [], []
    re_lamina = re.compile(rf"^{re.escape(num)}-\d+\.", re.I)
    for base, dirs, files in os.walk(drive):
        for d in dirs:
            dn = norm(d)
            if RE_ID.match(dn) and RE_ID.match(dn).group(1) == id_:
                por_pasta.append(os.path.join(base, d))
            elif dn == num:
                por_pasta.append(os.path.join(base, d))
        for f in files:
            if not tipo_arquivo(f):
                continue
            fn = norm(f)
            m = RE_ID.match(fn)
            if (m and m.group(1) == id_) or re_lamina.match(f):
                por_nome.append(os.path.join(base, f))
    arquivos = set(por_nome)
    for pasta in por_pasta:
        for base, _, files in os.walk(pasta):
            for f in files:
                if tipo_arquivo(f):
                    arquivos.add(os.path.join(base, f))
    arquivos = sorted(arquivos)
    pastas_pai = sorted({os.path.dirname(x) for x in arquivos})
    tipos = sorted({tipo_arquivo(x) for x in arquivos})
    alerta = []
    if not arquivos:
        alerta.append("nada encontrado")
    if len(pastas_pai) > 1:
        alerta.append("arquivos em mais de uma pasta: confirmar qual é o anúncio")
    print(json.dumps({"id": id_, "arquivos": arquivos, "pastas": pastas_pai, "tipos": tipos,
                      "alertas": alerta}, ensure_ascii=False, indent=1))


def cmd_listar(a):
    idx = carregar_indice(raiz(a))
    linhas = [(k, v) for k, v in sorted(idx.items()) if not a.status or v.get("status") == a.status]
    for k, v in linhas:
        print(f"{k:16} {v.get('status') or '':15} {v.get('formato') or '-':10} {(v.get('atualizado_em') or '')[:10]}  {v.get('obs') or ''}")
    print(f"total: {len(linhas)}")


def cmd_ver(a):
    idx = carregar_indice(raiz(a))
    print(json.dumps(idx.get(norm(a.id)), ensure_ascii=False, indent=1))


def cmd_registrar(a):
    r = raiz(a)
    idx = carregar_indice(r)
    id_ = norm(a.id)
    reg = idx.get(id_, {})
    if reg.get("status") == "validado" and not a.forcar:
        sys.exit(f"{id_} já está validado. Use --forcar para registrar de novo (volta para pendente).")
    reg.update({
        "formato": a.formato,
        "arquivos_origem": a.origem,
        "arquivos_envio": a.envio or reg.get("arquivos_envio", []),
        "ficha": os.path.join(r, "biblioteca", "fichas", f"{id_}.md"),
        "status": a.status or "pendente",
        "atualizado_em": agora(),
    })
    if a.obs:
        reg["obs"] = a.obs
    reg.pop("validado_por", None)
    idx[id_] = reg
    salvar_indice(r, idx)
    print(json.dumps({id_: reg}, ensure_ascii=False, indent=1))


def cmd_status(a):
    r = raiz(a)
    idx = carregar_indice(r)
    id_ = norm(a.id)
    if a.novo not in STATUS:
        sys.exit(f"status inválido. Use: {', '.join(STATUS)}")
    reg = idx.get(id_)
    if reg is None:
        if a.novo != "nao_localizado":
            sys.exit(f"{id_} não está no índice. Registre antes.")
        reg = {"formato": None, "arquivos_origem": [], "arquivos_envio": []}
    if a.novo == "validado":
        if not a.por:
            sys.exit("Validação precisa de --por <nome de quem conferiu>.")
        if not os.path.exists(reg.get("ficha", "")):
            sys.exit("Sem ficha escrita para este anúncio: não dá para validar.")
        envio = [x for x in reg.get("arquivos_envio", []) if os.path.exists(x)]
        if not envio:
            sys.exit("Sem arquivo de envio pronto: não dá para validar.")
        reg["validado_por"] = a.por
    reg["status"] = a.novo
    reg["atualizado_em"] = agora()
    if a.obs:
        reg["obs"] = a.obs
    idx[id_] = reg
    salvar_indice(r, idx)
    print(f"{id_}: {a.novo}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raiz")
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("init"); x.add_argument("--drive"); x.set_defaults(f=cmd_init)
    x = s.add_parser("config"); x.set_defaults(f=cmd_config)
    x = s.add_parser("id"); x.add_argument("utm"); x.set_defaults(f=lambda a: print(extrair_id(a.utm) or "SEM_ID"))
    x = s.add_parser("localizar"); x.add_argument("id"); x.add_argument("--drive"); x.set_defaults(f=cmd_localizar)
    x = s.add_parser("listar"); x.add_argument("--status"); x.set_defaults(f=cmd_listar)
    x = s.add_parser("ver"); x.add_argument("id"); x.set_defaults(f=cmd_ver)
    x = s.add_parser("registrar"); x.add_argument("id"); x.add_argument("--formato", required=True,
        choices=["estatico", "carrossel", "video"]); x.add_argument("--origem", nargs="+", required=True)
    x.add_argument("--envio", nargs="*"); x.add_argument("--status", choices=STATUS); x.add_argument("--obs")
    x.add_argument("--forcar", action="store_true"); x.set_defaults(f=cmd_registrar)
    x = s.add_parser("status"); x.add_argument("id"); x.add_argument("novo"); x.add_argument("--por")
    x.add_argument("--obs"); x.set_defaults(f=cmd_status)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
