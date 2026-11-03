# Clint: onde está cada informação

Tudo aqui é leitura.

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
