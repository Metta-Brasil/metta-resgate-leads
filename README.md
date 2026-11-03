# Resgate de leads · Metta

## Baixar o plugin

**[Baixar resgate-leads-plugin.zip](https://github.com/Metta-Brasil/metta-resgate-leads/releases/latest/download/resgate-leads-plugin.zip)**

Link direto: `https://github.com/Metta-Brasil/metta-resgate-leads/releases/latest/download/resgate-leads-plugin.zip`

Para instalar no app do Claude: abra a tela de **Plugins**, clique em **Enviar um plugin** e escolha esse arquivo. O zip é atualizado sozinho a cada mudança no plugin, e o link continua o mesmo. Quando o plugin mudar, baixe e envie de novo.

Não use o botão verde **Code > Download ZIP** do GitHub: ele baixa o repositório inteiro, e o Claude recusa com o erro "plugin.json must be at .claude-plugin/plugin.json".

## Para que serve

Trabalhar os leads da **Campanha Resgate** na Clint: gente que se cadastrou, nunca teve reunião e esfriou.

A Larissa pede ao Claude os negócios que quer trabalhar, e o plugin entrega, para cada lead, a mensagem pronta para ela enviar, com o anúncio pelo qual o lead se cadastrou.

## Como funciona

<a href="docs/fluxograma.png"><img src="docs/fluxograma.png" alt="Fluxograma do resgate" width="100%"></a>

Clique no fluxograma para ver em tamanho real.

1. **Pesquisa os negócios.** O Claude busca na Clint os negócios da Campanha Resgate com o critério do pedido, por exemplo "5 negócios com a tag Resgate Novembro".
2. **Puxa as informações.** Para cada lead, ele levanta:
   - quando se cadastrou;
   - o problema que contou;
   - quando foi atendido e o que foi conversado;
   - por que foi perdido;
   - a conversa de WhatsApp de agora.
3. **Identifica o anúncio que converteu o lead.** O nome do anúncio está no cadastro (utm_content).
4. **Acha o anúncio no Drive, baixa e lê.** Imagem ou carrossel: lê o texto. Vídeo: transcreve. A leitura fica guardada, e da próxima vez o Claude não precisa ler de novo.
5. **Escreve a mensagem.** Com a conversa, as informações do lead e o que o anúncio diz, o Claude escreve a mensagem a partir dos exemplos da Larissa:
   - **mensagem 2:** para quando o lead responde à ativação. Vai com o anúncio, a data do cadastro e o problema dele;
   - **mensagem 3:** para quando ele responde à mensagem 2. Ela parte do que ele disse.

   A ativação ("Olá, neste número ainda falo com...?") é a SDR que manda.
6. **A Larissa aprova** ou pede ajuste.
7. **Ela envia**, ou pede para o Claude enviar pela Clint.

## Usar

Abra o Claude e peça, por exemplo:

| Para | Peça |
|---|---|
| Começar | `Use o resgate-leads: 5 negócios da Campanha Resgate com a tag Resgate Novembro` |
| Um lead respondeu | `O Márcio respondeu no resgate` |
| Enviar pela Clint | `Envia pela Clint a mensagem do Márcio` |

Cada mensagem vem num bloco, com a formatação do WhatsApp. Copie só o que está dentro do bloco.

O plugin cria a pasta `Metta-Resgate` na pasta de trabalho:
- `criativos/`: a leitura de cada anúncio;
- `leads/`: as mensagens de cada lead.

## O que o Claude precisa

- A **Clint** conectada.
- O **Google Drive** conectado (ou a pasta do Drive no computador). Se não conseguir baixar um anúncio, ele pede para você arrastar o arquivo para o chat.
- Para **enviar pela Clint**: o token da API da Clint, que ele pede na primeira vez, e um número WhatsApp Oficial.

## Instalar pelo Claude Code (opcional)

```
/plugin marketplace add Metta-Brasil/metta-resgate-leads
/plugin install resgate-leads@metta-resgate
```

## Como o repositório é organizado

```
metta-resgate-leads/
├── README.md                          → este guia
├── docs/fluxograma.png                → o fluxograma (fonte: docs/gerar_fluxograma.py)
├── .github/workflows/plugin-zip.yml   → gera o zip do plugin a cada mudança
├── .claude-plugin/marketplace.json    → para instalar pelo Claude Code
└── plugins/resgate-leads/             → o plugin
    ├── .claude-plugin/plugin.json
    ├── .mcp.json                      → conector da Clint
    └── skills/
        ├── resgate-leads/             → pesquisa, anúncio e mensagem
        │   ├── references/clint.md
        │   ├── references/criativos.md
        │   ├── references/mensagens.md
        │   └── scripts/               → conferir.py, midia.py
        └── resgate-envio/             → envio pela Clint, quando pedido
            └── scripts/enviar_clint.py
```

## Importante

Este repositório é público. Nunca suba dado de lead, conversa, anúncio baixado ou token.
