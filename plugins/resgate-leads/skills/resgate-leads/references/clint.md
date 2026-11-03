# Clint: onde está cada informação

Tudo aqui é leitura.

## Selecionar os negócios do pedido (uma consulta só)

Não leia contato por contato para filtrar, e não use a data de criação de outro negócio como atalho: use `execute_indicator_query`, que devolve a lista exata. Exemplo para "tags Sessão estratégica e Resgate Novembro, inscritos de 01 a 10/10/2026":

```json
{"query": {
  "dimensions": ["Deal.id", "Contact.id", "Contact.name", "ContactFields.field_data_de_inscricao", "TagsList.tagsContact"],
  "filters": [
    {"member": "Origin.name", "operator": "equals", "values": ["Campanha Resgate, Nov, Dez e Jan"]},
    {"member": "Deal.status", "operator": "equals", "values": ["OPEN"]},
    {"member": "TagsList.tagsContact", "operator": "contains", "values": ["Resgate Novembro"]},
    {"member": "TagsList.tagsContact", "operator": "contains", "values": ["Sessão estratégica"]},
    {"member": "ContactFields.field_data_de_inscricao", "operator": "inDateRange", "values": ["2026-10-01", "2026-10-10"]}
  ],
  "order": {"ContactFields.field_data_de_inscricao": "asc"},
  "limit": 200}}
```

- Um filtro `contains` por tag pedida. Sem data no pedido, tire o filtro de data.
- Motivo de perda também é tag: `{"member": "TagsList.tagsContact", "operator": "contains", "values": ["Motivo: Interesse futuro"]}`.
- Mais de 200 resultados: pagine com `"offset"`.
- Em 03/11/2026 essa consulta devolveu 26 negócios.

## Chamadas, por lead

| Para | Chamada |
|---|---|
| Card do resgate e tags do contato | `search_deals` (origin_id do resgate + contact_id) |
| Todos os negócios do contato | `search_deals` (contact_id) |
| Cadastro, perfil, dor e UTMs | `get_contact_fields` (contact_id) |
| Ligações, notas, etapas e perda | `get_contact_history` (contact_id, deal_ids do negócio original, order ASC, limit 200) |
| Conversas de WhatsApp | `list_contact_chats` + `get_chat_messages` de cada conversa (order ASC, limit 100) |
| Ligações com duração | `list_calls` (contact_id, janelas de até 31 dias) |

## Campos

- **Contato:** `data_de_inscricao`, `funil`, `role` (cargo), `faturamento`, `segmento_de_mercado`, `subsegmento`, `desafio_do_lead` (dor do formulário), `utm_content`.
- **Negócio:** `principal_dor`, `principal_desafio_de`, `dores_do_cliente` (dor anotada pela SDR), `data_da_reuniao_agen` (reunião).

## Cuidado

- O card do resgate não traz a história do lead. Ela está no negócio original (em geral no Pipeline de Vendas Funil Perpétuo).
- O motivo da perda está na tag "Motivo: ..." do contato, não no campo do negócio.
- Mensagens e histórico vêm em UTC; mostre em horário de Brasília.
- Nas mensagens, `role` USER é a Metta e CUSTOMER é o lead. Mensagem com `error_code` não foi entregue. O texto vem cortado em 500 caracteres.
- Reunião realizada ou proposta enviada aparece nas etapas do negócio original ("Reunião Realizada" ou depois).
