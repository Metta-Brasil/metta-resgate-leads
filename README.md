# Resgate de leads · Metta

## Para que serve este repositório

Este repositório tem uma função só: trabalhar a **Campanha Resgate** na Clint, os leads que se cadastraram, nunca tiveram reunião e esfriaram.

Para cada lead, o plugin:

- lê o lead na Clint: cadastro, anúncio, dor, histórico e conversas em todos os números;
- aplica as travas: quem já fez reunião, está em negociação em outro funil, pediu para parar ou já foi abordado não recebe mensagem;
- prepara a próxima mensagem, pronta para a SDR aprovar:
  - **mensagem 1**, a ativação;
  - **mensagem 2**, com o anúncio pelo qual ele se cadastrou e a dor dele;
  - **mensagem 3**, escrita a partir do que ele respondeu, para levar ao agendamento do diagnóstico.

**O envio é manual**, pela Clint, depois da aprovação da SDR. O envio automático pela API da Clint existe, mas só roda com autorização explícita de quem está usando.

## Como o repositório é organizado

```
metta-resgate-leads/
├── README.md                          → este guia
├── .gitignore                         → impede que dado de lead, anúncio baixado ou token subam
├── .claude-plugin/
│   └── marketplace.json               → a "loja" metta-resgate
└── plugins/
    └── resgate-leads/                 → o plugin que se instala
        ├── .claude-plugin/plugin.json
        ├── .mcp.json                  → conector da Clint
        └── skills/
            ├── resgate-leads/         → lote, travas, dossiê e mensagens 1, 2 e 3
            │   ├── references/leitura-clint.md
            │   ├── references/mensagens.md
            │   └── scripts/conferir.py
            ├── resgate-biblioteca/    → biblioteca de anúncios (lê, confere e prepara cada anúncio)
            │   ├── references/ficha-do-anuncio.md
            │   ├── scripts/biblioteca.py
            │   └── scripts/midia.py
            └── resgate-envio/         → envio pela API da Clint, só com autorização
                └── scripts/enviar_clint.py
```

## Instalar (uma vez)

O computador precisa ter:
- o Claude Code (no terminal ou na aba Code do app Claude, em sessão local);
- git e Python 3;
- ffmpeg (`brew install ffmpeg`);
- o **Google Drive para computador**, com o drive compartilhado dos criativos aparecendo como pasta;
- para transcrever os anúncios em vídeo: `pip3 install faster-whisper`.

No Claude Code, digite:

```
/plugin marketplace add Metta-Brasil/metta-resgate-leads
/plugin install resgate-leads@metta-resgate
```

Feche e abra o Claude Code. Depois, digite `/mcp`, escolha **clint** e faça o login na Clint.

Se o primeiro comando der erro de SSH, use o endereço completo:

```
/plugin marketplace add https://github.com/Metta-Brasil/metta-resgate-leads.git
```

**Primeira vez:** peça ao Claude "Configura o resgate". Ele cria a pasta `~/Metta-Resgate/` com o `config.json`. Informe:
- a pasta local do drive de criativos;
- o nome de quem envia as mensagens;
- a lista de clientes que não podem aparecer em material, que fica só no seu computador.

## Receber as atualizações

Digite `/plugin`, abra a aba **Marketplaces**, escolha **metta-resgate** e selecione **Enable auto-update**. Para atualizar na hora: `/plugin marketplace update metta-resgate`.

A biblioteca de anúncios, os arquivos de cada lead e o `config.json` ficam em `~/Metta-Resgate/`, fora do plugin. A atualização não apaga nada disso.

## Usar

Abra o Claude Code e peça:

| Para | Digite |
|---|---|
| Montar a biblioteca antes do primeiro lote | `Monta a biblioteca de anúncios do resgate` |
| Montar um lote e a mensagem 1 | `Monta o lote do resgate: motivo "Interesse futuro"` |
| Ver quem respondeu e preparar a próxima mensagem | `Ver respostas do resgate` |
| Um lead específico | `O <nome do lead> respondeu no resgate` |

O resultado fica em `~/Metta-Resgate/saida/`:
- um arquivo por lead, com o dossiê e as mensagens;
- `_lote_<data>.md`, com o status de cada lead.

Cada mensagem vem num bloco de código único, com a formatação do WhatsApp. Copie só o que está dentro do bloco. O que está fora é instrução para a SDR.

**Biblioteca de anúncios:** cada anúncio é lido uma vez e só vai para o lead depois que alguém valida a ficha. Quando o resgate encontra um anúncio novo, ele monta a ficha e pede a validação.

## Antes de enviar

- **Status REVISAR ou BLOQUEADO:** leia o motivo.
- **Mensagem 2:** mande o anúncio primeiro e o texto logo depois.
- **Mensagem 3 com horários:** preencha com horários reais da agenda do especialista. Com colchete, ela não passa na conferência.
- **Número oficial:** a mensagem 1 sai como modelo aprovado (escolha na caixa da Clint). As mensagens 2 e 3 só saem com texto livre até 24 horas depois da última mensagem do lead.
- **Na dúvida, peça a checagem final:** `Confere antes de eu enviar para o <lead>`. O Claude relê a conversa e diz se algo mudou.

## Envio automático (opcional)

Só roda se você autorizar de forma explícita: `Autorizo enviar pela Clint as mensagens aprovadas de <lead ou lote>`.

O que precisa:
- uma chave de API da Clint com permissão de mensagens, salva em `~/Metta-Resgate/.clint_token` (nunca neste repositório);
- número WhatsApp Oficial;
- para o anúncio, um endereço público e direto do arquivo.

Antes de cada envio, o Claude confere se a conversa mudou, se a janela está aberta e se é horário comercial, e mostra a prévia para o seu "ok".

## Importante

Este repositório é público. Nunca suba dado de lead, conversa, anúncio baixado, biblioteca, token ou lista de clientes.
