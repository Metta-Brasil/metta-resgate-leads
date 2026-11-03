# Resgate de leads · Metta

## Baixar o plugin

**[Baixar resgate-leads-plugin.zip](https://github.com/Metta-Brasil/metta-resgate-leads/releases/latest/download/resgate-leads-plugin.zip)**

Link direto: `https://github.com/Metta-Brasil/metta-resgate-leads/releases/latest/download/resgate-leads-plugin.zip`

Para instalar no app do Claude, o usuário abre a tela de **Plugins**, clica em **Enviar um plugin** e escolhe esse arquivo. O zip é atualizado sozinho a cada mudança no plugin, e o link continua o mesmo. Quando o plugin muda, o usuário baixa e envia o zip de novo.

O botão verde **Code > Download ZIP** do GitHub não serve: ele baixa o repositório inteiro, e o Claude recusa com o erro "plugin.json must be at .claude-plugin/plugin.json".

## Para que serve

Trabalhar os leads da **Campanha Resgate** na Clint: gente que se cadastrou, nunca teve reunião e esfriou.

O usuário do time comercial pede ao Claude os negócios que quer trabalhar, e o plugin entrega, para cada lead, a mensagem pronta para envio, com o anúncio pelo qual o lead se cadastrou.

## Como funciona

<a href="docs/fluxograma.png"><img src="docs/fluxograma.png" alt="Fluxograma do resgate" width="100%"></a>

O fluxograma abre em tamanho real com um clique.

1. **Pesquisa os negócios.** O Claude busca na Clint os negócios da Campanha Resgate com o critério do pedido, por exemplo "5 negócios com a tag Resgate Novembro".
2. **Puxa as informações.** Para cada lead, ele levanta:
   - quando se cadastrou;
   - o problema que contou;
   - quando foi atendido e o que foi conversado;
   - por que foi perdido;
   - a conversa de WhatsApp de agora.
3. **Identifica o anúncio que converteu o lead.** O nome do anúncio está no cadastro (utm_content).
4. **Acha o anúncio no Drive, baixa e lê.** Imagem ou carrossel: lê o texto. Vídeo: transcreve. A leitura fica guardada, e da próxima vez o Claude não precisa ler de novo.
5. **Escreve a mensagem.** Com a conversa, as informações do lead e o que o anúncio diz, o Claude escreve a mensagem a partir das mensagens-modelo do time:
   - **mensagem 2:** para quando o lead responde à ativação. Vai com o anúncio, a data do cadastro e o problema dele;
   - **mensagem 3:** para quando ele responde à mensagem 2. Ela parte do que ele disse.

   A ativação ("Olá, neste número ainda falo com...?") é a SDR que manda.
6. **O usuário aprova** ou pede ajuste.
7. **O usuário envia**, ou pede para o Claude enviar pela Clint.

## Usar

O usuário abre o Claude e pede, por exemplo:

| Para | Pedido |
|---|---|
| Começar | `Use o resgate-leads: 5 negócios da Campanha Resgate com a tag Resgate Novembro` |
| Um lead respondeu | `O Márcio respondeu no resgate` |
| Enviar pela Clint | `Envia pela Clint a mensagem do Márcio` |

Cada mensagem vem num bloco, com a formatação do WhatsApp. O usuário copia só o que está dentro do bloco.

O plugin cria a pasta `Metta-Resgate` na pasta de trabalho:
- `criativos/`: a leitura de cada anúncio;
- `leads/`: as mensagens de cada lead.

## O que o Claude precisa

- A **Clint** conectada.
- O **Google Drive** conectado (ou a pasta do Drive no computador). Se não conseguir baixar um anúncio, ele pede para o usuário arrastar o arquivo para o chat.
- Para **enviar pela Clint**: a configuração de envio abaixo (chave da Clint e, no Cowork, a liberação de rede) e um número WhatsApp Oficial.

## Envio pela Clint: configuração (uma vez)

O conector da Clint lê os dados, mas não envia mensagem. Quem envia é o Claude, pela API da Clint. Para isso, três coisas precisam estar prontas. O envio funciona no **Cowork** e no **Claude Code**. No chat não funciona, porque o chat não guarda pasta de uma conversa para outra.

### 1. Gerar a chave na Clint

Só um administrador da Clint vê essa tela.

1. Na Clint, clique no avatar no menu lateral e abra **Configurações**.
2. No grupo **Segurança**, clique em **API**.
3. Se a tela mostrar **Chaves de API**:
   1. Clique em **Nova chave**.
   2. Em **Nome**, escreva `Plugin resgate` (um nome por pessoa ajuda a saber quem usa).
   3. Em **Permissões**, marque só o que o envio usa: **Escrita** em Mensagens e **Leitura** em conversas, contatos e canais (números). Se faltar alguma, o plugin avisa que a Clint recusou a chave.
   4. Clique em **Gerar chave** e depois em **Copiar**. A chave aparece inteira só nessa hora. Se perder, gere outra.
   5. Clique em **Concluir**.
4. Se a tela não tiver **Chaves de API**, ela mostra um token único. Clique em **Copiar**. Esse token dá acesso total à conta da Clint: trate como senha.

Para cortar o acesso de uma chave, clique em **Revogar** na mesma tela. Vale na hora.

### 2. Colocar a chave no arquivo

1. No Claude, peça um envio, por exemplo `Envia pela Clint a mensagem do lead`.
2. Na primeira vez, o Claude cria o arquivo `chave-clint.env` dentro da pasta `Metta-Resgate` e tenta abrir no editor de texto. Se não abrir sozinho, ele diz onde o arquivo está.
   - **Cowork:** a pasta `Metta-Resgate` fica dentro da pasta que o usuário escolheu para a tarefa.
   - **Claude Code:** fica na pasta em que o Claude foi aberto.
3. No arquivo, cole a chave logo depois do sinal de igual da linha `CLINT_API_TOKEN=`, na mesma linha, sem espaço e sem aspas.
4. Salve, feche e diga "pronto" ao Claude.
5. O Claude testa a chave e mostra os números WhatsApp Oficial conectados. A partir daí, envia quando o usuário pedir.

A chave nunca vai pelo chat e nunca entra neste repositório. Só o script do envio lê o arquivo. Se alguém colar a chave na conversa, o Claude não usa e pede para colar no arquivo.

### 3. Liberar a Clint na rede do Claude (só no Cowork)

O código que o Claude roda no Cowork só acessa os endereços liberados na conta. Por padrão a Clint não está liberada. No **Claude Code** este passo não é necessário.

**Plano Team ou Enterprise** (quem faz é o Proprietário da organização no Claude):

1. Em claude.ai, abra **Configurações da organização > Capacidades** (Organization settings > Capabilities): https://claude.ai/admin-settings/capabilities
2. Em **Execução de código e criação de arquivos** (Code execution and file creation), deixe ligado.
3. Ligue **Permitir saída de rede** (Allow network egress).
4. Em **Lista de domínios permitidos** (Domain allowlist), escolha **Gerenciadores de pacotes e domínios específicos** (Package managers and specific domains).
5. Em **Domínios adicionais permitidos** (Additional allowed domains), adicione `api.clint.digital`. Se já houver outros domínios, mantenha e só acrescente.
6. Salve.

**Plano individual** (Pro ou Max; a própria pessoa faz):

1. No Claude, clique no seu nome no canto inferior esquerdo e abra **Configurações > Capacidades** (Settings > Capabilities): https://claude.ai/settings/capabilities
2. Siga os passos 2 a 5 acima.

Depois de liberar, abra uma **tarefa nova** no Cowork. A tarefa que já estava aberta continua com a regra antiga.

Se, mesmo liberado, o Claude disser "Sem acesso a api.clint.digital", há relatos de falha do Claude em respeitar essa lista. Nesse caso, use o Claude Code ou envie pela caixa da Clint.

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
            ├── scripts/enviar_clint.py
            └── templates/chave-clint.env → modelo do arquivo da chave (vazio)
```

## Importante

Este repositório é público. Nenhum dado de lead, conversa, anúncio baixado ou chave entra aqui.
