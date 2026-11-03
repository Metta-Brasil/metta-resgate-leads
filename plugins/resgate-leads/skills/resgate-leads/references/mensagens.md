# Mensagens do resgate

A copy das mensagens 1 e 2 é da Larissa. Use o texto como está: só os campos entre colchetes mudam. A mensagem 3 não tem texto fixo: ela é escrita para cada lead, a partir do que ele respondeu, pelas regras deste arquivo.

## Mensagem 1 · ativação

```
Olá, neste número ainda falo com [Nome]?
```

- **[Nome]:** primeiro nome do contato, só a inicial maiúscula ("JOÃO CARLOS" → "João"). Nome que parece empresa, apelido, só sobrenome ou vazio: REVISAR.
- Vai sozinha: sem anúncio, sem contexto.
- No número oficial, ela só sai como modelo aprovado pela Meta. Quem envia escolhe o modelo na caixa da Clint (ou a skill `resgate-envio`, com autorização).

## Portão 1 · resposta à mensagem 1

A mensagem 2 traz data do cadastro, dor e anúncio. Ela só sai para o próprio lead. Leia **tudo** o que ele mandou depois da mensagem 1, em todos os números.

| Resposta | Exemplo | O que fazer |
|---|---|---|
| Confirma | "Sim", "sou eu", "pois não", "ele mesmo" | Mensagem 2 |
| Confirma e pergunta quem é | "Sim, quem fala?" | Mensagem 2, abrindo com "Aqui é a [nome da SDR], da Metta." logo depois da primeira linha |
| Só pergunta quem é | "Quem é?", "quem fala?" | Bloco curto: `Aqui é a [nome da SDR], da Metta. Falo com [Nome]?` A mensagem 2 só depois do "sim" |
| Outra pessoa ou número da empresa | "É a secretária", "ele não está", "é da loja" | Bloco curto: `Obrigada! Qual o melhor jeito de falar com [Nome]?` Nada do cadastro |
| Número errado | "Não conheço", "número errado" | Bloco curto: `Desculpe o engano. Obrigada por avisar.` Status: número errado. Fim |
| Pedido para parar ou irritação | "Não quero", "como conseguiu meu número?" | Bloco curto: `Desculpe o incômodo. Não vou mais te procurar por aqui.` Status: não abordar. Fim |
| Áudio | | Transcreva e classifique. Sem transcrição: REVISAR, a SDR ouve |
| Outra coisa (emoji, figurinha, assunto solto) | | REVISAR: a SDR decide |

## Mensagem 2 · com o anúncio

**Texto base (Larissa):**

```
Ah, maravilha, [Nome]!

No dia *[data]*, você se cadastrou por meio desse anúncio, demonstrando interesse em resolver *[DOR DO LEAD].*

Sei que muita coisa pode ter mudado desde então, mas ainda tenho seu diagnóstico disponível com a equipe da Metta para ajudar sua empresa a chegar em 2027 mais preparada para crescer.

*Me conta: esse desafio ainda é uma realidade na sua empresa hoje?*
```

**Campos:**
- **[data]:** `data_de_inscricao` do contato, no formato "14 de março" (com o ano só se não for o ano corrente: "14 de março de 2025"). Contato com mais de um cadastro: REVISAR.
- **[DOR DO LEAD]:** nesta ordem: `desafio_do_lead` do formulário; campos da SDR (`principal_dor`, `principal_desafio_de`, `dores_do_cliente`); o que ele disse na conversa ou na ligação. Reescreva como frase curta que caiba em "interesse em resolver ___", em minúsculas, como problema da operação e nunca como culpa do dono ou do time. Ex.: "Meu time não bate meta" → "o time não bater a meta". Mostre ao lado a frase original e a fonte.
- **Anúncio:** os arquivos de envio da ficha validada na biblioteca, com o mesmo ID do `utm_content`. Vão **antes** do texto, para "desse anúncio" apontar para o que está logo acima. Carrossel: todas as lâminas, na ordem.

**Variantes (mesmo texto, só muda o necessário):**

Sem dor declarada, com anúncio validado que tem "dor tratada":

```
Ah, maravilha, [Nome]!

No dia *[data]*, você se cadastrou por meio desse anúncio, que fala sobre *[dor tratada no anúncio]*.

Sei que muita coisa pode ter mudado desde então, mas ainda tenho seu diagnóstico disponível com a equipe da Metta para ajudar sua empresa a chegar em 2027 mais preparada para crescer.

*Me conta: esse ainda é um desafio na sua empresa hoje?*
```

Sem anúncio utilizável (orgânico, Google, UTM vazia, não localizado, datado ou proibido), com dor declarada. Vai sem anexo:

```
Ah, maravilha, [Nome]!

No dia *[data]*, você se cadastrou com a gente, demonstrando interesse em resolver *[DOR DO LEAD].*

Sei que muita coisa pode ter mudado desde então, mas ainda tenho seu diagnóstico disponível com a equipe da Metta para ajudar sua empresa a chegar em 2027 mais preparada para crescer.

*Me conta: esse desafio ainda é uma realidade na sua empresa hoje?*
```

Sem dor e sem anúncio utilizável, ou anúncio com "sem dor clara" e lead sem dor: REVISAR. A SDR escreve.

A dor do anúncio nunca vira algo que o lead disse.

## Portão 2 · resposta à mensagem 2

Base da mensagem 3:
1. a mensagem 2 **como saiu**, lida na Clint (a SDR pode ter editado; vale o que saiu);
2. **tudo** o que o lead mandou depois dela;
3. o dossiê.

Com mais de uma intenção na resposta, vale a de menor número. "Sim, mas quanto custa?" é a 2.

| # | O lead respondeu | Mensagem 3 | Status depois |
|---|---|---|---|
| 1 | Pediu para parar, se irritou, disse que não é ele | `Desculpe o incômodo, [Nome]. Não vou mais te procurar por aqui.` Se perguntou de onde veio o contato, acrescente que foi do cadastro do dia [data], num anúncio da Metta. Sem pergunta | Não abordar |
| 2 | Perguntou preço ou investimento | Explica que a solução é personalizada e depende do que o especialista mapear na operação, por isso a conversa vem antes. Fecha com dois horários. **Nunca escreva valor.** Se ele insistir, REVISAR: a SDR responde | Agendamento |
| 3 | Perguntou como funciona o diagnóstico | Uma frase: "O diagnóstico é uma análise da sua operação comercial com um especialista da Metta, não uma reunião de apresentação." Fecha com dois horários. Perguntou duração, formato ou quem conduz: REVISAR, a SDR responde | Agendamento |
| 4 | Confirmou o desafio | Reconhece com as palavras dele, uma frase do que o diagnóstico faz (a do item 3) e dois horários. Se faltar no dossiê cargo ou faturamento, pergunte só esse dado antes e deixe os horários para a próxima | Agendamento |
| 5 | Confirmou, mas o desafio agora é outro | Reconhece o desafio novo, com as palavras dele, e dois horários | Agendamento |
| 6 | Em parte: melhorou, mas não resolveu | Uma pergunta sobre o que ainda trava | Nova resposta: portão 2 |
| 7 | Já resolveu | `Que bom saber disso, [Nome].` + porta aberta, sem pergunta | Perdido: resolveu |
| 8 | Agora não, sem tempo, ano que vem | Propõe um momento concreto em uma pergunta ("Faz sentido eu te chamar na primeira semana de janeiro?") | Retorno na data |
| 9 | Não decide sozinho, tem sócio, saiu da empresa | Sócio: pede para o sócio estar junto na conversa, em uma pergunta. Saiu da empresa: agradece e encerra | Conforme o caso |
| 10 | Resposta curta ou ambígua ("ok", emoji) | Uma pergunta simples, sem repetir a mensagem 2 | Nova resposta: portão 2 |

**O que a mensagem 3 herda da 2:**
- não repete a data nem reenvia o anúncio;
- parte do que ele respondeu sobre a dor citada, com as palavras dele;
- mantém a oferta: diagnóstico com a equipe da Metta. Nada de duração, preço, plano ou nome de especialista que não esteja escrito aqui;
- não pergunta o que o dossiê já responde;
- acompanha o tamanho e o tom da resposta dele: resposta curta pede mensagem curta.

**Dois horários:** escreva `*[dia e hora]* ou *[dia e hora]*`. A SDR preenche com horários reais da agenda do especialista. Mensagem com colchete não passa no conferidor, então ela não sai sem horário.

**Exemplos de referência** (o tom, não um texto fixo):

Categoria 4:
```
Faz sentido, [Nome]. [O que ele contou, com as palavras dele.]

O diagnóstico é uma análise da sua operação comercial com um especialista da Metta, não uma reunião de apresentação.

Tenho *[dia e hora]* ou *[dia e hora]*. Qual fica melhor para você?
```

Categoria 7:
```
Que bom saber disso, [Nome].

Se em 2027 aparecer um desafio novo no comercial, é só me chamar por aqui.
```

## Regras de toda mensagem

- **WhatsApp:** cada mensagem num bloco de código único, parágrafos separados por linha em branco. Negrito com um asterisco (`*texto*`). Instrução e aviso sempre fora do bloco.
- Sem emoji, sem travessão, sem link, no máximo uma exclamação.
- Uma pergunta por mensagem, ou dois horários.
- Para o lead, a palavra é "anúncio", nunca "criativo".
- **Nunca aparece:**
  - preço, valor, parcela, desconto, plano, Black;
  - motivo de perda, MQL, SAL, "perfil", "qualificação";
  - nota interna, menção a gravação de ligação.
- **Sem "especial"**, sem palavra de coach ou de consultoria ("alavancar", "potencializar", "framework", "jornada", "transformar").
- **Culpa do sistema:** o dono leria e pensaria "então a culpa é minha?". Se sim, reescreva.
- **Não inventa:** dado que falta não vira suposição. Na dúvida, REVISAR com o motivo.
