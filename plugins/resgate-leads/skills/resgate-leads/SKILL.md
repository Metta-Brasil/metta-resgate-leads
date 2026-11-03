---
name: resgate-leads
description: Use quando a Larissa (ou outra SDR) pedir para trabalhar leads da Campanha Resgate na Clint, ou disser que um lead do resgate respondeu. Pesquisa os negócios, puxa as informações, identifica o anúncio que converteu o lead, acha esse anúncio no Drive, lê e guarda a copy, e escreve a mensagem para ela enviar, com base nos exemplos da Larissa.
---

# Resgate de leads

A lógica é esta, nesta ordem:

1. Pesquisar os negócios na Clint, com o critério do pedido.
2. Puxar as informações de cada negócio.
3. Identificar o anúncio que converteu o lead.
4. Achar esse anúncio no Drive, baixar, ler e guardar.
5. Escrever a mensagem com o contexto da conversa, as informações do negócio e a copy do anúncio, usando como base os exemplos da Larissa.
6. Se ela pedir, enviar pela Clint (skill `resgate-envio`).

## 1. Pesquisar os negócios

- Origem "Campanha Resgate, Nov, Dez e Jan", `origin_id` `fe254f0e-36c1-4db8-a84e-c8f52bf75824`. Use `search_deals` com o `origin_id`, `limit` 100, paginando por `offset`.
- Aplique o critério do pedido (tag, data, motivo de perda, funil). Datas falam da **inscrição** do lead (campo `data_de_inscricao` do contato): os cards do resgate foram todos criados entre 28 e 30/10. Critério vago: use a leitura mais simples e diga em uma linha qual usou.
- Pediu N negócios: entregue N. Pule só quem não é do resgate e pegue o próximo:
  - já teve reunião ou recebeu proposta: fica com o Iago;
  - pediu para não ser procurado.

## 2. Informações do negócio

Chamadas e campos em `references/clint.md`. Para cada lead:
- quem é: nome, empresa ou segmento, cargo, faturamento;
- cadastro: data de inscrição, funil, `utm_content`;
- a dor que ele declarou;
- histórico: quando foi atendido, quando conversaram, o que foi dito, por que foi perdido;
- a conversa de WhatsApp de agora, em todos os números. É ela que diz qual mensagem escrever.

Um lead de cada vez: nunca misture as informações de dois leads.

## 3. Anúncio que converteu

O ID é o começo do `utm_content`, até o número: `PP-SE-928-Capt-FB-VID-1-A-PRA-UMA-EMPRESA` → `PP-SE-928`. Sem ID (orgânico, Google, vazio): segue sem anúncio.

## 4. Drive: achar, baixar, ler e guardar

Primeiro procure `Metta-Resgate/criativos/<ID>.md` na pasta de trabalho. Se existir, use. Se não, siga `references/criativos.md` e grave a ficha. Cada anúncio é lido uma vez, e a pasta cresce a cada rodada.

## 5. Mensagem

Siga `references/mensagens.md`. Qual mensagem escrever:

| Na conversa | Escreva |
|---|---|
| A SDR ainda não mandou a ativação, ou o lead ainda não respondeu | Mensagem 2, pronta para quando ele responder |
| Ele respondeu à ativação | Mensagem 2, ajustada ao que ele respondeu |
| Ele respondeu à mensagem 2 | Mensagem 3, a partir do que ele disse e do que a mensagem 2 falou |

A ativação ("Olá, neste número ainda falo com...?") é da SDR: não escreva.

## Entrega

Para cada lead, no chat e em `Metta-Resgate/leads/<Nome>.md`:

````
## <Nome> · <empresa ou segmento>
- Cadastro: <dd/mm> · <funil> · anúncio <ID> (<formato>)
- Histórico: <uma ou duas linhas: quando foi atendido, quando conversaram, por que foi perdido>
- Dor: "<o que ele disse>" (<formulário | SDR | conversa>)
- Anúncio para anexar: <link ou arquivo>

Mensagem <2 | 3> (<quando enviar>):
```
<mensagem>
```
````

No fim, uma linha com quem foi pulado e por quê. Nada além disso.

## Antes de entregar

- Confira cada mensagem pelas regras de `references/mensagens.md`. Se der para rodar scripts: `python3 <pasta-da-skill>/scripts/conferir.py Metta-Resgate/leads`.
- Dado que não existe não é inventado: sem dor, use a variante do anúncio; sem anúncio, a variante sem anexo.

## Nunca

- Escrever preço, condição ou plano.
- Mandar a mensagem 2 para quem não é o lead (número errado, outra pessoa): responda curto, sem nenhum dado do cadastro.
- Enviar sem a Larissa pedir.
- Mover card, mudar campo ou tag na Clint.
