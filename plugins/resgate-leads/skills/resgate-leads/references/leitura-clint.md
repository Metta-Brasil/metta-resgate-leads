# Leitura do lead na Clint

Tudo aqui é leitura. Esta skill não move card, não altera campo nem tag e não envia mensagem pelo conector.

## Chamadas do conector da Clint, por lead

| Passo | Chamada | Para quê |
|---|---|---|
| 1 | `search_deals` (origin_id do resgate + contact_id) ou `search_deals` (deal_id) | O card da campanha e as tags do contato (motivo de perda em "Motivo: ...") |
| 2 | `search_deals` (contact_id) | Todos os negócios do contato: origem, etapa, status, campos |
| 3 | `get_contact_fields` (contact_id) | Funil, inscrição, perfil, dor do formulário e UTMs |
| 4 | `get_contact_history` (contact_id, deal_ids do negócio original, order ASC, limit 200) | Ligações, atividades, mudanças de etapa, perda |
| 5 | `list_contact_chats` (limit 20) + `get_chat_messages` de cada conversa (order ASC, limit 100, paginando) | Todas as conversas de WhatsApp e Instagram, em todos os números |
| 6 | `list_calls` (contact_id, janelas de até 31 dias, da inscrição até hoje) | Ligações com status, duração e gravação |
| 7 | `list_transcriptions` / `get_transcription` | Transcrição de ligação ou reunião, quando houver |

**Lote:** `search_deals` com `origin_id` do resgate (está no `config.json`), `limit` 100, paginando por `offset`. O payload é `{ deals, total_count }`. Filtro por motivo de perda: tag "Motivo: ..." do contato. Se o payload do lote não trouxer as tags, leia no passo 1 de cada lead.

**Lead pelo nome:** `search_contacts` é busca parcial e devolve homônimos. Fica o contato que tem card na origem do resgate. Se sobrar mais de um, mostre nome, telefone, e-mail e data de cadastro e pergunte. Nunca escolha.

## Campos

- **Contato:** `funil`, `data_de_inscricao`, `role` (cargo), `faturamento`, `qualificacao`, `segmento_de_mercado`, `subsegmento`, `numero_de_vendedores`, `desafio_do_lead`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
- **Negócio:** `sdr`, `closer`, `data_da_reuniao_agen` (reunião), `data_de_agendamento`, `principal_dor`, `principal_desafio_de`, `dores_do_cliente`, `sonhodesejo`, `media_de_faturamento`, `numero_vendedores`, `poder_decisao`, `motivo_no_show`, `resumo_reuniao`, `notes`.

## Armadilhas

- O card do resgate não traz o histórico da primeira passagem. A história está no negócio original (em geral no Pipeline de Vendas Funil Perpétuo).
- `motivo_perda` vem vazio nos negócios originais. O motivo está na tag "Motivo: ..." do contato.
- Histórico e mensagens vêm em UTC; ligações, em horário de Brasília. Mostre tudo em Brasília.
- Mensagens: `role` USER = Metta (automação quando há `sourceMetadata.automationName`), CUSTOMER = lead. `content_object.error_code` preenchido = não entregue (não conta como contato). `content` vem cortado em 500 caracteres. `source: "PARTNER"` = outro parceiro de WhatsApp escreveu.
- `list_calls`: ligações de outros usuários só aparecem para admin ou para quem configura a telefonia. `recording_url` vale 7 dias.
- Áudio do lead no WhatsApp e gravação de ligação: transcreva (mesmo método do vídeo na skill `resgate-biblioteca`) antes de usar.

## Anúncio de origem (`utm_content`)

ID = começo do `utm_content` em maiúsculas: `python3 <pasta-da-skill-resgate-biblioteca>/scripts/biblioteca.py id "<utm_content>"`.

| utm_source | utm_content | Leitura |
|---|---|---|
| fbads_*, facebook | começa com PP- | Anúncio do Meta: vai para a biblioteca |
| organico, ig | bio-ig-..., collab-..., link_in_bio, destaques-..., isca-... | Instagram orgânico: sem anúncio |
| gads... | qualquer | Google Ads: sem anúncio (a busca está no utm_term) |
| fbads_* | {{ad.name}} | Anúncio sem nome na UTM: sem anúncio |
| qualquer | vazio ou número longo | Sem anúncio |

## Situação na primeira passagem

| Situação | Como identificar |
|---|---|
| A · Não houve conversa | Nenhuma ligação atendida e nenhuma resposta do lead |
| B · Conversou e não agendou | Ligação atendida ou resposta no WhatsApp, sem reunião |
| C · Agendou e não compareceu | Reunião marcada, sem "Reunião Realizada" no histórico |
| D · Fez a reunião | "Reunião Realizada" ou etapa posterior |

## Travas (cada lead sai com um status)

| Encontrou | Status |
|---|---|
| Situação D (já fez reunião) | BLOQUEADO: fica com o Iago |
| Negócio aberto em outro funil | BLOQUEADO: mostrar funil, etapa e dono |
| Pedido para não ser procurado, em qualquer conversa ("não quero", "pare", "me tira da lista", "não tenho interesse, não me procure") | BLOQUEADO sem prazo |
| Mensagem do resgate já enviada, por qualquer número ou pessoa, desde `inicio_campanha` | BLOQUEADO: não duplica (se foi pelo fluxo, o lead está em outra fase: ver SKILL.md) |
| Mensagem do lead ou da Metta nos últimos `dias_conversa_em_andamento` dias | BLOQUEADO: segue com quem está conversando |
| Telefone vazio, inválido, ou conversa em que alguém disse que o número é de outra pessoa | BLOQUEADO |
| Contato com mais de um cadastro (mais de um negócio original) | REVISAR: confirmar data e anúncio |
| Faturamento abaixo de R$ 150 mil por mês, ou cargo de gerente | REVISAR: a SDR decide |
| Sem dor declarada e sem anúncio utilizável | REVISAR: a SDR escreve |
| Anúncio pendente na biblioteca | AGUARDA: validar o anúncio |
| Nada acima | APTO |

## Dossiê (vai no arquivo do lead)

```
DOSSIÊ · <nome> · <empresa, se houver>
<telefone> · <e-mail> · contato <contact_id> · card <deal_id>

1. QUEM É
Cargo · Segmento / subsegmento · Faturamento · Vendedores

2. COMO CHEGOU
Funil · Inscrição: <dd/mm/aaaa>
Anúncio: <ID> · <formato> · status na biblioteca · onde viu: <utm_term>

3. LINHA DO TEMPO (Brasília)
<dd/mm hh:mm> Cadastro
<dd/mm hh:mm> Primeira tentativa: <ligação perdida | WhatsApp>
<dd/mm hh:mm> Primeira conversa: <ligação atendida, X min | resposta no WhatsApp>
<dd/mm hh:mm> Reunião: <marcada para dd/mm · realizada | no-show | sem registro>
<dd/mm hh:mm> Perdido na etapa <...> · motivo: <tag>
<dd/mm hh:mm> Último contato

4. O QUE ELE DISSE
Dor: "<texto>" (fonte: formulário | campo da SDR | conversa de dd/mm | ligação de dd/mm)

5. SITUAÇÃO E STATUS
Situação: <A | B | C | D> · Status: <APTO | REVISAR: motivo | BLOQUEADO: motivo | AGUARDA: motivo>

6. CONVERSA LIDA ATÉ
<data e hora da última mensagem lida, em qualquer número>
```

Cada informação leva a fonte. O que não está registrado aparece como "não encontrado".
