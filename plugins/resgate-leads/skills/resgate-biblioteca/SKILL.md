---
name: resgate-biblioteca
description: Use quando a skill resgate-leads encontrar um anúncio que não está na biblioteca, quando pedirem para montar ou atualizar a biblioteca de anúncios do resgate, ou para validar um anúncio. Localiza o anúncio na pasta do Drive, lê (texto, imagem, transcrição do vídeo), escreve a ficha, confere o conteúdo contra as regras de hoje e prepara o arquivo de envio dentro dos limites do WhatsApp.
---

# Biblioteca de anúncios do resgate

Cada lead do resgate se cadastrou por um anúncio (o começo do `utm_content`, ex.: `PP-APLI-223`). A mensagem 2 manda esse anúncio de volta e fala do tema dele. Como um anúncio serve a dezenas de leads, ele é lido e conferido **uma vez** e guardado aqui. Uma leitura errada se repetiria em todas as mensagens daquele anúncio.

A biblioteca é atualizada sempre que o plugin roda e encontra anúncio novo. Ela fica fora do plugin, em `~/Metta-Resgate/biblioteca/`, porque a atualização do plugin substitui a pasta dele.

## Antes de começar

1. Pasta de trabalho e config:
   ```
   python3 <pasta-da-skill>/scripts/biblioteca.py init --drive "<pasta local do drive de criativos>"
   ```
   A pasta do Drive é a do Google Drive para computador, onde os criativos aparecem como arquivos. Se `pasta_drive_anuncios` estiver vazio no `config.json`, pergunte a pasta ao usuário e grave.
2. `ffmpeg` instalado (`brew install ffmpeg`). Para transcrever vídeo: `pip install faster-whisper`. Sem transcrição, o vídeo continua utilizável como anexo, mas a ficha fica `pendente` até alguém escrever o que o vídeo fala.
3. Leia `references/ficha-do-anuncio.md` inteiro.

## Para cada anúncio

1. **Já está no índice?** `biblioteca.py ver <ID>`. Se `validado`, use como está e pare.
2. **Localizar:** `biblioteca.py localizar <ID>`. O script procura arquivo cujo nome começa com o ID, pasta com o ID ou com o número do anúncio (ex.: pasta `989`), e lâminas `<número>-1.jpg`.
   - Nada encontrado: `biblioteca.py status <ID> nao_localizado --obs "procurado em <pasta>"`. O lead segue sem anexo.
   - Arquivos em mais de uma pasta, ou um nome com o mesmo número dentro de outro ID (ex.: `PP-APLI-1159-...-NOVO-223-...` não é o 223): **pare e mostre ao usuário**. Nunca escolha sozinha.
   - Quando houver versões Feed e Story do mesmo estático, vale uma (prefira a vertical 4:5 ou 1:1 à de 9:16).
3. **Ler e preparar:**
   - **Vídeo:** `python3 <pasta-da-skill>/scripts/midia.py video "<arquivo>" --id <ID>`. Leia a transcrição inteira e olhe cada quadro gerado, para o texto que aparece na tela. O script já gera a versão leve (até 16 MB).
   - **Estático ou carrossel:** `python3 <pasta-da-skill>/scripts/midia.py imagens <arquivos> --id <ID>`. Abra cada imagem gerada, na ordem, e leia o texto de cada lâmina.
4. **Escrever a ficha** em `~/Metta-Resgate/biblioteca/fichas/<ID>.md`, no modelo de `ficha-do-anuncio.md`. Só o que o anúncio diz, com as palavras dele.
5. **Conferir o conteúdo** (lista em `ficha-do-anuncio.md`). Achou cliente proibido, número desatualizado, oferta, vaga ou data vencida, ou preço: status `proibido` ou `datado`, com o motivo. Esse anúncio não volta para o lead.
6. **Registrar:**
   ```
   python3 <pasta-da-skill>/scripts/biblioteca.py registrar <ID> --formato <estatico|carrossel|video> --origem <arquivos do Drive> --envio <arquivos gerados>
   ```
   Entra como `pendente`.
7. **Pedir a validação** ao usuário: mostre a ficha e os arquivos de envio e pergunte se pode validar. Só com o "sim" dele:
   ```
   python3 <pasta-da-skill>/scripts/biblioteca.py status <ID> validado --por "<nome de quem conferiu>"
   ```

Anúncio `pendente` não vai para lead. Enquanto ele não for validado, o lead espera ou segue na variante sem anexo, se o usuário preferir.

## Montar a biblioteca inteira de uma vez

Quando pedirem para montar tudo antes do primeiro lote: liste os IDs dos negócios da origem do resgate (skill `resgate-leads`, passo de lote), conte quantos leads cada ID tem e processe do maior para o menor. Valide em blocos com o usuário, mostrando ficha e arquivo de cada um.

## O que nunca fazer

- Validar um anúncio sem o "sim" de uma pessoa.
- Escolher entre dois arquivos candidatos sem perguntar.
- Escrever na ficha o que o anúncio não diz.
- Guardar a biblioteca dentro da pasta do plugin.
