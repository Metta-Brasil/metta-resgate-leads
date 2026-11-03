#!/usr/bin/env python3
"""Envio pela API da Clint (só número WhatsApp Oficial). Usado pela skill resgate-envio.

Token: variável CLINT_API_TOKEN ou arquivo ~/Metta-Resgate/.clint_token (uma linha, chmod 600).
Use uma chave de API com permissão só de leitura de conversas/contatos e escrita de mensagens.

Comandos (os três primeiros só leem):
  numeros                                  números conectados e tipo
  modelos --numero ID                      modelos do número (nome, status, categoria, texto)
  conversa --contato ID                    conversas do contato: número, última mensagem, fim da janela
  enviar --numero ID --contato ID --tipo {modelo,texto,imagem,video,documento} --lida-ate ISO [...]
         sem --confirmo, só mostra o que seria enviado (nada sai)

Antes de enviar, o script confere: número oficial e conectado; nenhuma mensagem nova na conversa
depois de --lida-ate; janela de 24 h aberta (para texto e mídia); horário comercial; envio repetido.
Erro da API volta como está, sem nova tentativa.
"""
import argparse, datetime, hashlib, json, os, sys, urllib.error, urllib.parse, urllib.request

API = "https://api.clint.digital"
RAIZ = os.path.expanduser(os.environ.get("RESGATE_RAIZ", "~/Metta-Resgate"))
TZ = datetime.timezone(datetime.timedelta(hours=-3))


def token():
    t = os.environ.get("CLINT_API_TOKEN")
    p = os.path.join(RAIZ, ".clint_token")
    if not t and os.path.exists(p):
        t = open(p).read().strip()
    if not t:
        sys.exit("Sem token da Clint. Defina CLINT_API_TOKEN ou crie ~/Metta-Resgate/.clint_token")
    return t


def chamar(metodo, caminho, corpo=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(API + caminho, data=dados, method=metodo, headers={
        "api-token": token(), "accept": "application/json", "content-type": "application/json",
        "user-agent": "curl/8.5.0"})  # sem user-agent o Cloudflare devolve 403 (erro 1010)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        corpo_err = e.read()
        try:
            return e.code, json.loads(corpo_err)
        except Exception:
            return e.code, {"raw": corpo_err[:300].decode("utf-8", "replace")}


def dados(resp):
    return resp.get("data", resp) if isinstance(resp, dict) else resp


def iso(s):
    d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=TZ)


def cmd_numeros(a):
    st, r = chamar("GET", "/v2/channel-accounts?limit=100")
    for c in dados(r) if st == 200 else []:
        print(f"{c['id']}  {c.get('type',''):18} {c.get('status',''):10} {c.get('name','')}")
    if st != 200:
        print(st, r)


def cmd_modelos(a):
    st, r = chamar("GET", f"/v2/message-templates?channel_account_id={a.numero}&limit=200")
    if st != 200:
        sys.exit(f"{st} {r}")
    for t in dados(r):
        corpo = next((c.get("text", "") for c in t.get("components") or [] if (c.get("type") or "").upper() == "BODY"), "")
        print(f"{t['id']}  {t.get('status',''):17} {t.get('category',''):10} {t.get('name','')}\n    {corpo[:160]!r}")


def conversas(contato):
    st, r = chamar("GET", f"/v2/chats/contact/{contato}?limit=50")
    if st != 200:
        sys.exit(f"Não consegui ler as conversas do contato: {st} {r}")
    return dados(r)


def cmd_conversa(a):
    for c in conversas(a.contato):
        print(json.dumps({k: c.get(k) for k in ("id", "channel_account_id", "status", "last_message_at",
                                               "close_window_at", "thread_ownership")}, ensure_ascii=False))


def mensagens_depois(chat_id, desde):
    q = urllib.parse.quote(desde.astimezone(datetime.timezone.utc).isoformat())
    st, r = chamar("GET", f"/v2/messages/chat/{chat_id}?created_at_start={q}&limit=50")
    if st != 200:
        sys.exit(f"Não consegui ler as mensagens da conversa {chat_id}: {st} {r}")
    return [m for m in dados(r) if iso(m["created_at"]) > desde]


def horario_ok():
    cfg_p = os.path.join(RAIZ, "config.json")
    h = json.load(open(cfg_p)).get("horario_comercial", {}) if os.path.exists(cfg_p) else {}
    agora = datetime.datetime.now(TZ)
    ini, fim = h.get("inicio", "09:00"), h.get("fim", "18:00")
    dentro = ini <= agora.strftime("%H:%M") <= fim and agora.weekday() < 5
    return dentro, f"{agora:%a %H:%M} (permitido seg-sex {ini}-{fim})"


def cmd_enviar(a):
    problemas = []
    # 1. número oficial e conectado
    st, r = chamar("GET", f"/v2/channel-accounts/{a.numero}")
    num = dados(r) if st == 200 else {}
    if num.get("type") != "WHATSAPP_OFFICIAL":
        problemas.append(f"o número não é WhatsApp Oficial ({num.get('type')}): envio pela API não é possível")
    if num.get("status") != "CONNECTED":
        problemas.append(f"o número não está conectado ({num.get('status')})")
    # 2. nada novo na conversa depois da leitura
    lida = iso(a.lida_ate)
    chats = conversas(a.contato)
    novas = []
    for c in chats:
        if c.get("last_message_at") and iso(c["last_message_at"]) > lida:
            novas += mensagens_depois(c["id"], lida)
    if novas:
        problemas.append(f"{len(novas)} mensagem(ns) nova(s) na conversa depois de {a.lida_ate}: releia e refaça a mensagem")
    # 3. janela para texto e mídia
    chat_num = next((c for c in chats if c.get("channel_account_id") == a.numero), None)
    if a.tipo != "modelo":
        fim = chat_num and chat_num.get("close_window_at")
        if not fim or iso(fim) < datetime.datetime.now(TZ) + datetime.timedelta(minutes=5):
            problemas.append("janela de 24 h fechada neste número: só modelo aprovado")
    if chat_num and chat_num.get("thread_ownership") not in (None, "", "CLINT"):
        problemas.append(f"a conversa está com outro parceiro ({chat_num.get('thread_ownership')})")
    # 4. horário
    ok, quando = horario_ok()
    if not ok:
        problemas.append(f"fora do horário comercial: {quando}")
    # 5. corpo
    texto = open(a.arquivo_texto, encoding="utf-8").read().strip() if a.arquivo_texto else (a.texto or "")
    if "[" in texto or "]" in texto:
        problemas.append("o texto ainda tem colchete")
    corpo = {"channel_account_id": a.numero, "contact_id": a.contato}
    if chat_num:
        corpo["chat_id"] = chat_num["id"]
    if a.tipo == "modelo":
        corpo["template_id"] = a.modelo
        corpo["parameters"] = {"body": a.variaveis or []}
        if a.url:
            corpo["parameters"]["header"] = {"url": a.url}
        rota = "/v2/messages/template"
    elif a.tipo == "texto":
        corpo["message"] = texto
        rota = "/v2/messages/text"
    else:
        if not a.url:
            problemas.append("mídia precisa de --url pública e direta do arquivo (a Meta busca o arquivo nesse endereço)")
        corpo["url"] = a.url
        if texto:
            corpo["caption"] = texto
        if a.tipo == "documento":
            corpo["filename"] = a.nome_arquivo or "anuncio.pdf"
        rota = {"imagem": "/v2/messages/image", "video": "/v2/messages/video", "documento": "/v2/messages/document"}[a.tipo]
    # 6. repetido
    log = os.path.join(RAIZ, "envios.jsonl")
    chave = hashlib.sha256(json.dumps([a.contato, rota, corpo.get("message"), corpo.get("url"),
                                       corpo.get("template_id"), corpo.get("parameters")], sort_keys=True).encode()).hexdigest()
    if os.path.exists(log) and any(json.loads(l).get("chave") == chave for l in open(log) if l.strip()):
        problemas.append("este mesmo envio já foi feito para este contato")

    print("ENVIO:", rota)
    print(json.dumps(corpo, ensure_ascii=False, indent=1))
    if problemas:
        print("\nNÃO ENVIADO:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    if not a.confirmo:
        print("\nTudo conferido. Nada foi enviado (falta --confirmo).")
        return
    st, r = chamar("POST", rota, corpo)
    registro = {"quando": datetime.datetime.now(TZ).isoformat(timespec="seconds"), "contato": a.contato,
                "numero": a.numero, "rota": rota, "status_http": st, "resposta": r, "chave": chave}
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    print(f"\nRESPOSTA {st}: {json.dumps(r, ensure_ascii=False)}")
    if st >= 300:
        print("Não repita o envio. Leve o erro para a SDR (402 = sem saldo; 409 = conversa de outro parceiro; 400 = ver mensagem).")
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("numeros").set_defaults(f=cmd_numeros)
    x = s.add_parser("modelos"); x.add_argument("--numero", required=True); x.set_defaults(f=cmd_modelos)
    x = s.add_parser("conversa"); x.add_argument("--contato", required=True); x.set_defaults(f=cmd_conversa)
    x = s.add_parser("enviar")
    x.add_argument("--numero", required=True); x.add_argument("--contato", required=True)
    x.add_argument("--tipo", required=True, choices=["modelo", "texto", "imagem", "video", "documento"])
    x.add_argument("--lida-ate", required=True, help="data e hora ISO da última mensagem lida na conversa")
    x.add_argument("--texto"); x.add_argument("--arquivo-texto"); x.add_argument("--modelo")
    x.add_argument("--variaveis", nargs="*"); x.add_argument("--url"); x.add_argument("--nome-arquivo")
    x.add_argument("--confirmo", action="store_true")
    x.set_defaults(f=cmd_enviar)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
