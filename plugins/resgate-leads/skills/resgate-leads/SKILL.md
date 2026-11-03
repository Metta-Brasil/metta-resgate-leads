---
name: resgate-leads
description: Use quando for trabalhar a Campanha Resgate da Metta na Clint (leads que nunca tiveram reunião), ao montar um lote de resgate, ao pedir para ver quem respondeu, ou quando a SDR colar a resposta de um lead do resgate. Lê o lead na Clint, aplica as travas, monta o dossiê e escreve a próxima mensagem (1, 2 ou 3) com o anúncio da biblioteca, conferida e pronta para a SDR aprovar e enviar.
---

# Resgate de leads (Campanha Resgate)

Para cada lead da origem "Campanha Resgate" na Clint, a skill descobre em que ponto da conversa ele está e prepara a próxima mensagem, pronta para a SDR:

1. **Mensagem 1 (ativação):** confirma se o número ainda é do lead.
2. **Mensagem 2 (anúncio + dor):** só depois de o próprio lead confirmar. Vai com o anúncio pelo qual ele se cadastrou.
3. **Mensagem 3 (resposta):** escrita a partir do que ele respondeu à mensagem 2, para levar ao agendamento do diagnóstico.

**Duas regras que valem para tudo:**
- Nenhuma mensagem é montada sem ler antes a conversa atual do lead na Clint, em todos os números.
- Nenhuma mensagem sai sem a SDR aprovar, uma por uma. Esta skill **não envia**. O envio é manual, pela Clint. O envio automático existe só pela skill `resgate-envio`, com autorização explícita do usuário.

## Antes de começar

1. **Conector da Clint:** confirme que as ferramentas `search_deals`, `get_contact_fields`, `list_contact_chats` e `get_chat_messages` respondem. Se não, peça para conectar a Clint (`/mcp`) e pare.
2. **Pasta de trabalho:** `~/Metta-Resgate/` com `config.json`. Se não existir (ou se pedirem "Configura o resgate"), rode o `init` da skill `resgate-biblioteca` e pergunte o que estiver vazio no `config.json`: a pasta local do drive de criativos (`pasta_drive_anuncios`), quem envia as mensagens (`nome_sdr`) e os clientes que não podem aparecer em material (`clientes_proibidos`). Grave as respostas.
3. **Leia inteiros:** `references/leitura-clint.md` e `references/mensagens.md`.
4. **Data e hora de agora**, em Brasília.

## Pedidos

| O usuário pede | O que fazer |
|---|---|
| "Monta o lote ..." (motivo de perda, anúncio, lista de negócios ou quantidade) | **Lote** (abaixo) e mensagem 1 dos aptos |
| "Ver respostas do resgate" | Para cada lead com arquivo em `saida/`, ler a conversa e, se ele respondeu, seguir o ponto da conversa |
| "Resposta do <lead>: ..." ou "o <lead> respondeu" | Só esse lead: ler a conversa na Clint (não confiar só no texto colado) e seguir o ponto da conversa |
| "Monta a biblioteca" | Skill `resgate-biblioteca` |
| "Configura o resgate" | Passo 2 de "Antes de começar" |

## Lote

1. Liste os negócios abertos da origem do resgate (`search_deals` com `origin_id` do `config.json`, páginas de 100) e aplique o filtro pedido.
2. Para cada negócio, **um de cada vez**, leia o lead conforme `leitura-clint.md` e monte o dossiê. Com mais de 10 leads, use um subagente por lead, passando os caminhos deste SKILL.md, das referências e do `config.json` e a hora de agora. Nunca misture dois leads no mesmo contexto.
3. Aplique as travas de `leitura-clint.md`. Para a mensagem 1, valem também:
   - mensagem do resgate já enviada → BLOQUEADO;
   - conversa nos últimos `dias_conversa_em_andamento` dias → BLOQUEADO.
4. **Anúncio:** procure o ID na biblioteca (`resgate-biblioteca/scripts/biblioteca.py ver <ID>`).
   - Validado: segue.
   - Não está no índice: chame a skill `resgate-biblioteca` para esse ID. O lead fica AGUARDA até a validação.
   - Datado, proibido ou não localizado: segue sem anexo.
5. **Limite do dia:** só os primeiros `limite_diario_mensagem_1` aptos recebem a mensagem 1. Os demais ficam para o próximo dia, na ordem.
6. Escreva o arquivo de cada lead (formato abaixo) e o resumo `saida/_lote_<AAAA-MM-DD>.md`, com uma linha por lead: nome, telefone, anúncio, dor, status.
7. Rode o conferidor e corrija até zerar:
   ```
   python3 <pasta-da-skill>/scripts/conferir.py ~/Metta-Resgate/saida
   ```
8. Mostre o resumo e **peça que a SDR aprove a lista** antes de qualquer envio.

## Ponto da conversa (a cada leitura)

Leia todas as conversas do contato desde `inicio_campanha` e descubra a fase:

| Encontrou na conversa | Fase | O que preparar |
|---|---|---|
| Nenhuma mensagem do resgate | Antes da 1 | Mensagem 1 (só se APTO) |
| Mensagem 1 enviada, sem resposta do lead | Aguardando | Nada. Fica para a cadência de follow-up da SDR |
| Resposta do lead depois da mensagem 1, mensagem 2 não enviada | Portão 1 | Mensagem 2 ou resposta curta (`mensagens.md`) |
| Mensagem 2 enviada, sem resposta | Aguardando | Nada |
| Resposta do lead depois da mensagem 2 (ou da 3) | Portão 2 | Mensagem 3 (`mensagens.md`) |
| Horário combinado ou lead pediu para parar | Fim | Nada. Avisar a SDR |

A mensagem 1 é reconhecida por "ainda falo com" ou "falo com" mais o nome. A mensagem 2, por "você se cadastrou". Mensagem com erro de entrega não conta como enviada: avise a SDR.

**Janela de 24 horas (número oficial):** mostre quando ela fecha (última mensagem do lead + 24 h). A resposta ao lead deve sair em até 2 horas no horário comercial. Com a janela fechada, só sai modelo aprovado: avise a SDR em vez de preparar texto livre.

## Arquivo de cada lead

`~/Metta-Resgate/saida/<primeiro nome>_<8 primeiros caracteres do deal_id>.md`. As seções novas vão no fim do arquivo, sem apagar as anteriores.

````
# <Nome> · <empresa, se houver>
Status: <APTO | REVISAR: motivo | BLOQUEADO: motivo | AGUARDA: motivo>

<dossiê de leitura-clint.md>

## Mensagem 1 · ativação · preparada em <dd/mm hh:mm>

```
Olá, neste número ainda falo com João?
```

## Mensagem 2 · preparada em <dd/mm hh:mm> · janela fecha <dd/mm hh:mm>

Resposta do lead (não copiar): "<o que ele mandou>"
Portão 1: <categoria>
Anexo:
- <caminho do arquivo de envio 1>
- <caminho 2, se carrossel>

```
<mensagem>
```

Dados usados (não copiar): data <...> (fonte) · dor "<frase>" ← "<original>" (fonte) · anúncio <ID>

## Mensagem 3 · preparada em <dd/mm hh:mm> · janela fecha <dd/mm hh:mm>

Resposta do lead (não copiar): "<...>"
Portão 2: <número e nome da categoria>

```
<mensagem>
```

## Para a SDR (não copiar)
- <o que fazer: mandar o anúncio antes do texto, preencher os horários, avisos>
````

Resposta curta do portão 1 (número errado, quem é, outra pessoa, parar): seção `## Resposta · <motivo>` no mesmo formato.

## Aprovação

Mostre no chat, para cada mensagem preparada:
- o resumo do lead;
- a categoria da resposta e o trecho que levou a ela;
- a mensagem num bloco único e o anexo;
- os dados usados, com a fonte;
- os alertas.

A SDR aprova, edita, pede ajuste ou descarta:
- **Ajuste:** reescreva e rode o conferidor de novo.
- **Texto editado à mão:** grave no arquivo e rode o conferidor de novo.

## Checagem final (logo antes de a SDR enviar)

Quando a SDR disser que vai enviar, ou antes de passar para a skill `resgate-envio`, releia a conversa na Clint e confira:
1. o contato e o telefone são os do dossiê;
2. não entrou mensagem nova depois do "Conversa lida até", em nenhum número. Se entrou, a mensagem é refeita;
3. o negócio continua aberto e não apareceu negócio aberto em outro funil;
4. no número oficial, a janela está aberta (mensagens 2 e 3);
5. é horário comercial (`horario_comercial`);
6. a mesma mensagem não foi enviada antes.

Qualquer item falhou: não libere e diga qual.

## O que nunca fazer

- Mandar a mensagem 2 sem o "sim" do próprio lead, ou com data, dor ou anúncio para outra pessoa.
- Inventar dor, data ou anúncio. Dado que falta vai para REVISAR.
- Usar anúncio que não está validado na biblioteca.
- Escrever preço, condição, plano ou duração do diagnóstico.
- Montar mensagem sem reler a conversa na Clint.
- Enviar mensagem, mover card, alterar campo ou tag pelo conector.
