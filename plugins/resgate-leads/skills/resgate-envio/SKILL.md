---
name: resgate-envio
description: Use quando o usuário (SDR ou outra pessoa do time comercial) pedir para enviar pela Clint uma mensagem do resgate que a skill resgate-leads escreveu. Envia pela API da Clint, pelo número WhatsApp Oficial, depois de conferir que nada mudou na conversa. Sem esse pedido, nada é enviado.
---

# Enviar pela Clint

O pedido do usuário ("envia pela Clint", "manda pro Márcio") é a autorização para aquela mensagem. Sem pedido, não envie.

## Precisa

- **Token da API da Clint.** Na primeira vez, peça ao usuário e grave em `Metta-Resgate/.clint_token`, na pasta de trabalho.
- **Número WhatsApp Oficial.** Use o número oficial em que está a conversa com o lead. Se não houver conversa em número oficial, ou houver em dois, pergunte qual usar. Número de QR code não envia pela API: o usuário envia pela caixa da Clint.

## Passos

1. Releia a conversa do lead na Clint e anote a data e a hora da última mensagem.
2. Envie:
   ```
   python3 <pasta-da-skill>/scripts/enviar_clint.py enviar --numero <id do número> --contato <contact_id> --tipo texto --arquivo-texto <arquivo só com o texto da mensagem> --lida-ate <data e hora ISO da última mensagem> --confirmo
   ```
   Antes de enviar, o script confere três coisas:
   - nada novo entrou na conversa desde a leitura;
   - a janela de 24 horas está aberta;
   - a mesma mensagem não foi enviada antes.

   Se alguma falhar, ele não envia e diz o motivo.
3. Registre no arquivo do lead: `Enviado pela Clint em <dd/mm hh:mm>`, ou o erro.

## Cuidado

- **Mensagem 2 com anúncio:** a API só manda arquivo por link público direto (`--tipo imagem` ou `--tipo video` com `--url`). Sem esse link, avise o usuário para enviar a mensagem 2 pela caixa da Clint: o texto fala "desse anúncio" e não vai sozinho.
- **Janela fechada** (o lead não escreveu nas últimas 24 horas): texto livre não sai. Avise.
- **Erro da API:** não tente de novo. Mostre o erro (402 = sem saldo na Clint; 409 = conversa com outro parceiro).
- **Números e modelos:** `enviar_clint.py numeros` e `enviar_clint.py modelos --numero <id>` listam o que existe.
