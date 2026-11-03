# Ficha do anúncio

## Modelo

```
# <ID> · <formato: estático | carrossel | vídeo>

Arquivo(s) de envio: <caminhos, na ordem de envio>
Origem no Drive: <caminhos>

## O que o anúncio diz
- Tema: <do que ele fala, em uma frase>
- Gancho: "<primeira frase, literal>"
- Dor tratada: <frase curta, do ponto de vista do dono, ex.: "o time não bater a meta todo mês">
- Promessa: "<literal>"
- Chamada final: "<literal>"

## Texto do anúncio
<vídeo: transcrição limpa + texto que aparece na tela, por quadro>
<estático/carrossel: texto de cada lâmina, numerado>

## Conferência de conteúdo
- Cliente proibido: <não | qual>
- Número desatualizado: <não | qual>
- Data, vaga, evento ou oferta vencida: <não | qual>
- Preço: <não | qual>
- Posicionamento antigo ("ecossistema de inteligência comercial"): <não | sim>
- Resultado: <ok | datado: motivo | proibido: motivo>
```

## Regras

- **Dor tratada** é a frase que a mensagem 2 usa quando o lead não declarou dor (variante "sem dor"). Ela precisa caber em "você se cadastrou por meio desse anúncio, que fala sobre *<dor tratada>*". Escreva como problema da operação, nunca como culpa do dono ou do time (teste: o dono leria e pensaria "então a culpa é minha?"). Se o anúncio não trata dor nenhuma (institucional, notícia), escreva "sem dor clara": esses leads, sem dor declarada, vão para REVISAR.
- **Literal é literal.** Gancho, promessa e chamada vêm com as palavras do anúncio.
- **Transcrição de vídeo:** corrija só o que o Whisper errou de forma evidente (nome da Metta, do Tiago). Na dúvida, mantenha e marque `[?]`.

## Conferência de conteúdo (o anúncio volta meses depois)

| Item | O que procurar | Resultado |
|---|---|---|
| Cliente proibido | qualquer nome da lista `clientes_proibidos` do `~/Metta-Resgate/config.json` (nome, logo, depoimento). Lista vazia: pergunte ao usuário antes de validar | proibido |
| Número desatualizado | "R$ 8,2 bi", "800 empresas" ou outro número de resultado da Metta diferente de "R$ 8,5 bi em metas batidas" e "+1.000 empresas" | datado |
| Data vencida | evento, live, workshop, "inscrições até", "vagas", "só esta semana", mês ou semestre passados | datado |
| Oferta | preço, desconto, condição, Black | datado |
| Posicionamento antigo | "ecossistema de inteligência comercial" | datado |

Na dúvida, marque `datado` e explique: é melhor o lead seguir sem anexo do que receber um anúncio vencido.
