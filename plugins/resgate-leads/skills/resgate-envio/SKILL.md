---
name: resgate-envio
description: Use quando o usuário (SDR ou outra pessoa do time comercial) pedir para enviar pela Clint uma mensagem do resgate que a skill resgate-leads escreveu. O Claude envia pela API da Clint, pelo número WhatsApp Oficial, depois de conferir que nada mudou na conversa. Sem esse pedido, nada é enviado.
---

# Enviar pela Clint

O pedido do usuário ("envia pela Clint", "manda pro lead") é a autorização para aquela mensagem. Sem pedido, não envie.

## Chave da Clint (primeira vez)

A chave fica no arquivo `Metta-Resgate/chave-clint.env`, na pasta de trabalho do usuário. Nunca no chat.

1. Antes do primeiro envio, rode:
   ```
   python3 <pasta-da-skill>/scripts/enviar_clint.py configurar
   ```
2. Se a saída disser **SEM CHAVE DA CLINT**, o script já criou o arquivo e tentou abrir no editor de texto. Diga ao usuário, em linguagem simples:
   - o caminho do arquivo que o script mostrou (dentro da pasta Metta-Resgate);
   - colar a chave logo depois de `CLINT_API_TOKEN=`, salvar e fechar;
   - quem gera a chave é um administrador da Clint, em Configurações > Segurança > API;
   - avisar "pronto" quando terminar.

   Pare aqui até ele avisar. Depois rode `configurar` de novo.
3. **CHAVE OK** mostra os números WhatsApp Oficial conectados. Siga para o envio.

Regras da chave:
- Nunca peça a chave no chat. Se o usuário colar a chave na conversa, não use: peça para colar no arquivo.
- Nunca abra, leia ou mostre o arquivo `chave-clint.env` (nem com cat, nem com Read). Só o script lê.
- **"Sem acesso a api.clint.digital"**: no Cowork e no chat, o administrador do Claude da empresa precisa liberar esse endereço nas configurações de rede. Explique isso ao usuário. Sem a liberação, o envio fica com ele, pela caixa da Clint.
- **"A Clint recusou a chave"**: a chave está errada, foi revogada ou não tem permissão de mensagens. Peça para conferir o arquivo.

## Número

Use o número WhatsApp Oficial em que está a conversa com o lead. Se não houver conversa em número oficial, ou houver em dois, pergunte qual usar. Número de QR code não envia pela API: o usuário envia pela caixa da Clint.

## Passos do envio

1. Releia a conversa do lead na Clint e anote a data e a hora da última mensagem.
2. Grave o texto aprovado num arquivo só com a mensagem e envie:
   ```
   python3 <pasta-da-skill>/scripts/enviar_clint.py enviar --numero <id do número> --contato <contact_id> --tipo texto --arquivo-texto <arquivo só com o texto da mensagem> --lida-ate <data e hora ISO da última mensagem, com fuso> --confirmo
   ```
   Antes de enviar, o script confere:
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
