---
name: resgate-envio
description: Use somente quando o usuário autorizar de forma explícita o envio automático de mensagens do resgate pela Clint (ex.: "autorizo enviar pela Clint"). Envia pela API da Clint, uma mensagem aprovada por vez, só em número WhatsApp Oficial, depois de conferir que nada mudou na conversa. Sem essa autorização, o envio é manual e esta skill não roda.
---

# Envio automático pela Clint (opcional)

O padrão do resgate é envio manual: a SDR envia pela caixa de conversas da Clint a mensagem que a skill `resgate-leads` preparou. Esta skill só existe para quando o usuário quiser que o Claude envie.

## Quando pode rodar

Todas as condições, sempre:
1. **Autorização explícita do usuário nesta conversa**, com o lote ou o lead a que ela se aplica. "Pode seguir", "ok" ou silêncio não valem. Na dúvida, pergunte: "Autoriza enviar pela Clint as mensagens aprovadas de <quem>?"
2. **A mensagem foi aprovada pela SDR** e passou no conferidor (`resgate-leads/scripts/conferir.py`).
3. **Número WhatsApp Oficial.** Número de QR code não envia pela API: o envio é manual.
4. **Token da Clint** configurado (`CLINT_API_TOKEN` ou `~/Metta-Resgate/.clint_token`). Sem token, avise e pare.

## Passo a passo, por mensagem

1. **Números:** `python3 <pasta-da-skill>/scripts/enviar_clint.py numeros`. Use o número oficial combinado com o usuário.
2. **Releia a conversa** do lead pela skill `resgate-leads` (checagem final). Anote a data e a hora da última mensagem lida.
3. **Monte o envio conforme a mensagem:**
   - **Mensagem 1:** só como modelo aprovado. Liste com `enviar_clint.py modelos --numero <ID>` e use o que o usuário indicar para a ativação (variável `{{1}}` = primeiro nome). Sem modelo combinado, pergunte e pare.
   - **Mensagens 2 e 3 e respostas curtas:** texto (`--tipo texto --arquivo-texto <arquivo só com o texto do bloco>`), dentro da janela de 24 horas.
   - **Anúncio da mensagem 2:** a API envia mídia por endereço público e direto do arquivo (`--url`). Sem esse endereço, a mensagem 2 inteira é manual. Não mande o texto sem o anúncio que ele cita.
4. **Prévia, sem enviar:**
   ```
   python3 <pasta-da-skill>/scripts/enviar_clint.py enviar --numero <ID> --contato <contact_id> --tipo <...> --lida-ate <ISO> [...]
   ```
   O script confere:
   - número oficial e conectado;
   - nenhuma mensagem nova depois de `--lida-ate`;
   - janela aberta (texto e mídia);
   - conversa sem outro parceiro;
   - horário comercial;
   - envio repetido.

   Problema: **não envie**. Leve o motivo para a SDR.
5. **Mostre a prévia** ao usuário (para quem, por qual número, o texto). Com o "ok" dele para aquela mensagem, repita o comando com `--confirmo`.
6. **Resultado:** registre no arquivo do lead, em `saida/`, a linha `Enviado pela Clint em <dd/mm hh:mm> (<tipo>)` ou o erro.
   - Erro da API: não tente de novo.
   - 402 = sem saldo na carteira.
   - 409 = conversa de outro parceiro.
   - 400 = ler a mensagem do erro.
   - Erro 131049 aparecendo depois, na conversa: a Meta segurou o envio por baixa interação. Pause o lote e avise.

## Lote da mensagem 1

- Respeite `limite_diario_mensagem_1` do `config.json` e o horário comercial.
- Envie um por vez, na ordem da lista aprovada, com a checagem completa para cada lead.
- Pause e avise quando:
  - aparecer erro 131049 ou bloqueio;
  - mais de 2 envios seguidos derem erro.

## O que nunca fazer

- Enviar sem a autorização explícita e sem o "ok" da prévia.
- Usar `--confirmo` depois de uma checagem que falhou.
- Repetir um envio que deu erro.
- Enviar por número de QR code, ou texto livre com a janela fechada.
- Mandar a mensagem 2 sem o anúncio que ela cita.
