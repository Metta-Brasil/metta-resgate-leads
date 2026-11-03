#!/usr/bin/env python3
"""Gera o fluxograma horizontal do plugin resgate-leads (SVG + PNG)."""
import sys, html

W, H = 3180, 530
T, M, B = 100, 270, 440
FONT = "Liberation Sans, Arial, Helvetica, sans-serif"
COR = {
    "proc": ("#ffffff", "#333333"),
    "dec": ("#fff4cc", "#b8860b"),
    "res": ("#e3f4e6", "#2e7d32"),
    "pula": ("#fde7e5", "#c0392b"),
    "guarda": ("#e6eefb", "#3f6db3"),
    "ponta": ("#eeeeee", "#555555"),
}
out = []


def txt(cx, cy, linhas, tam=15):
    alt = {"b": tam, "n": tam - 1, "s": tam - 3, "g": tam - 3}
    total = sum(alt[e] + 4 for _, e in linhas) - 4
    y = cy - total / 2
    for t, e in linhas:
        y += alt[e]
        peso = "bold" if e == "b" else "normal"
        cor = "#666666" if e == "g" else "#111111"
        estilo = "italic" if e == "g" else "normal"
        out.append(f'<text x="{cx}" y="{y - 2:.1f}" font-family="{FONT}" font-size="{alt[e]}" '
                   f'font-weight="{peso}" font-style="{estilo}" fill="{cor}" text-anchor="middle">{html.escape(t)}</text>')
        y += 4


def caixa(cx, cy, w, h, linhas, tipo="proc", raio=6):
    f, s = COR[tipo]
    out.append(f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="{raio}" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    txt(cx, cy, linhas)


def pilula(cx, cy, w, h, linhas):
    caixa(cx, cy, w, h, linhas, "ponta", raio=h / 2)


def losango(cx, cy, w, h, linhas):
    f, s = COR["dec"]
    out.append(f'<polygon points="{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    txt(cx, cy, linhas, 14)


def cilindro(cx, cy, w, h, linhas):
    f, s = COR["guarda"]
    e = 10
    x0, x1, y0, y1 = cx - w/2, cx + w/2, cy - h/2, cy + h/2
    out.append(f'<path d="M{x0},{y0 + e} A{w/2},{e} 0 0 1 {x1},{y0 + e} L{x1},{y1 - e} A{w/2},{e} 0 0 1 {x0},{y1 - e} Z" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    out.append(f'<path d="M{x0},{y0 + e} A{w/2},{e} 0 0 0 {x1},{y0 + e}" fill="none" stroke="{s}" stroke-width="1.6"/>')
    txt(cx, cy + 5, linhas)


def seta(pontos, tracejada=False, duas=False):
    d = "M" + " L".join(f"{x},{y}" for x, y in pontos)
    extra = ' stroke-dasharray="7,5"' if tracejada else ""
    ini = ' marker-start="url(#ini)"' if duas else ""
    out.append(f'<path d="{d}" fill="none" stroke="#555555" stroke-width="1.6"{extra}{ini} marker-end="url(#fim)"/>')


def rotulo(x, y, t, ancora="middle", tam=13):
    largura = len(t) * tam * 0.53 + 8
    x0 = x - largura / 2 if ancora == "middle" else (x if ancora == "start" else x - largura)
    out.append(f'<rect x="{x0}" y="{y - tam + 1}" width="{largura}" height="{tam + 5}" fill="#ffffff"/>')
    out.append(f'<text x="{x0 + largura/2}" y="{y + 1}" font-family="{FONT}" font-size="{tam}" fill="#333333" text-anchor="middle">{html.escape(t)}</text>')


# ---------- caminho principal
pilula(95, M, 170, 72, [("Pedido do usuário", "b"), ("ex.: 5 negócios com a", "s"), ("tag Resgate Novembro", "s")])
seta([(180, M), (214, M)])
caixa(289, M, 150, 62, [("1. Pesquisa os", "b"), ("negócios na Clint", "b")])
seta([(364, M), (392, M)])
losango(475, M, 160, 106, [("Fica fora", "n"), ("do resgate?", "n")])
seta([(475, M - 53), (475, T + 38)]); rotulo(489, 188, "sim", "start")
caixa(475, T, 236, 76, [("Pula e pega o próximo", "b"), ("já teve reunião ou proposta", "s"), ("(fica com o Iago) ou pediu", "s"), ("para não ser procurado", "s")], "pula")
seta([(555, M), (586, M)]); rotulo(572, M - 12, "não")
caixa(691, M, 210, 80, [("2. Puxa as informações", "b"), ("cadastro, dor, atendimento,", "s"), ("conversas, motivo da perda", "s")])
seta([(796, M), (830, M)])
caixa(935, M, 210, 62, [("3. Identifica o anúncio", "b"), ("pela utm_content", "s")])
seta([(1040, M), (1074, M)])
losango(1151, M, 154, 104, [("Anúncio já", "n"), ("guardado?", "n")])
seta([(1228, M), (1728, M)]); rotulo(1478, M - 12, "sim, ou lead sem anúncio")

# ---------- ramo do anúncio
seta([(1151, M + 52), (1151, B - 36)]); rotulo(1165, 355, "não", "start")
caixa(1151, B, 184, 72, [("4. Procura no Drive", "b"), ("e baixa", "b"), ("não achou: pede o arquivo", "g")])
seta([(1243, B), (1275, B)])
losango(1335, B, 120, 88, [("Formato?", "n")])
seta([(1335, B - 44), (1335, B - 62), (1525, B - 62)]); rotulo(1430, B - 70, "estático ou carrossel", tam=12)
caixa(1610, B - 62, 170, 46, [("Lê a copy das imagens", "n")])
seta([(1335, B + 44), (1335, B + 62), (1525, B + 62)]); rotulo(1430, B + 54, "vídeo", tam=12)
caixa(1610, B + 62, 170, 46, [("Transcreve o vídeo", "n")])
seta([(1695, B - 62), (1718, B - 62), (1718, B - 14), (1742, B - 14)])
seta([(1695, B + 62), (1718, B + 62), (1718, B + 14), (1742, B + 14)])
cilindro(1833, B, 182, 84, [("Anúncios guardados", "b"), ("copy e análise", "s")])

# ---------- análise
caixa(1600, T, 190, 56, [("Mensagens-modelo", "b"), ("do time, mensagens 2 e 3", "s")], "guarda")
seta([(1695, T), (1788, T), (1788, M - 42)])
caixa(1833, M, 210, 84, [("5. Claude analisa tudo", "b"), ("conversa + negócio +", "s"), ("copy do anúncio", "s")])
seta([(1833, B - 42), (1833, M + 42)], duas=True)
seta([(1938, M), (1972, M)])
losango(2042, M, 140, 104, [("Ponto da", "n"), ("conversa?", "n")])

seta([(2042, M - 52), (2042, T), (2172, T)])
caixa(2277, T, 210, 92, [("Mensagem 2", "b"), ("anúncio + data + dor", "n"), ("lead ainda não respondeu", "g"), ("ou respondeu à ativação", "g")], "res")
seta([(2112, M), (2172, M)])
caixa(2277, M, 210, 74, [("Mensagem 3", "b"), ("a partir da resposta dele", "n"), ("respondeu à mensagem 2", "g")], "res")
seta([(2042, M + 52), (2042, B), (2172, B)])
caixa(2277, B, 210, 74, [("Resposta curta", "b"), ("sem dados do cadastro", "n"), ("número errado, não é o lead", "g")], "res")
for y in (T, B):
    seta([(2382, y), (2402, y), (2402, M), (2425, M)])
seta([(2382, M), (2425, M)])

# ---------- aprovação e envio
caixa(2515, M, 180, 80, [("6. Mostra ao usuário", "b"), ("resumo do lead +", "s"), ("mensagem + anúncio", "s")])
seta([(2605, M), (2639, M)])
losango(2704, M, 130, 98, [("Aprovada?", "n")])
seta([(2704, M + 49), (2704, B - 26)]); rotulo(2718, 360, "não", "start")
caixa(2704, B, 150, 52, [("Refaz com", "n"), ("o feedback", "n")])
seta([(2629, B), (2515, B), (2515, M + 42)])
seta([(2769, M), (2813, M)]); rotulo(2791, M - 12, "sim")
losango(2883, M, 140, 104, [("Enviar pela", "n"), ("Clint?", "n")])
seta([(2883, M - 52), (2883, T + 30)]); rotulo(2897, 182, "sim", "start")
caixa(2883, T, 180, 60, [("Claude confere a", "n"), ("conversa e envia", "n")], "res")
seta([(2883, M + 52), (2883, B - 24)]); rotulo(2897, 360, "não", "start")
caixa(2883, B, 160, 48, [("Usuário envia", "n")], "res")
pilula(3063, M, 140, 56, [("Lead responde", "b")])
seta([(2973, T), (3063, T), (3063, M - 30)])
seta([(2963, B), (3063, B), (3063, M + 30)])

# lead respondeu: volta ao passo 5
seta([(3133, M), (3155, M), (3155, 22), (1878, 22), (1878, M - 42)], tracejada=True)
rotulo(2516, 27, "quando o lead responde, o Claude lê a resposta e escreve a próxima mensagem")

# legenda
lx, ly = 30, 420
for i, (tipo, nome) in enumerate([("dec", "decisão"), ("res", "resultado"), ("guarda", "guardado / base"), ("pula", "fica de fora")]):
    f, s = COR[tipo]
    y = ly + i * 24
    out.append(f'<rect x="{lx}" y="{y}" width="18" height="14" rx="3" fill="{f}" stroke="{s}" stroke-width="1.4"/>')
    out.append(f'<text x="{lx + 26}" y="{y + 12}" font-family="{FONT}" font-size="13" fill="#333333">{nome}</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       '<defs><marker id="fim" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
       '<path d="M0,0 L10,5 L0,10 z" fill="#555555"/></marker>'
       '<marker id="ini" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
       '<path d="M10,0 L0,5 L10,10 z" fill="#555555"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>' + "".join(out) + "</svg>")

svg_path, png_path = sys.argv[1], sys.argv[2]
open(svg_path, "w", encoding="utf-8").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=png_path, scale=1.5)
print("ok", svg_path, png_path)
