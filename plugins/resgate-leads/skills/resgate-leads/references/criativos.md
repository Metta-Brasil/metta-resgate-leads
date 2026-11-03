# Anúncio: achar, baixar, ler e guardar

## Achar no Drive

Use o acesso ao Drive que a sessão tiver: o conector do Google Drive ou a pasta do Google Drive no computador.

1. Busque pelo ID (ex.: `PP-SE-928`). Vale o arquivo ou a pasta cujo nome **começa** com o ID. Cuidado: `PP-APLI-1159-...-NOVO-223` não é o `PP-APLI-223`.
2. Não achou: abra a planilha "Blueprint_[PERPÉTUO] - 2025" (`1RvS3Iz-AemmR-LYPtDOMqq9IaKBVaPN6VNujKRUNV3U`), aba Criativos, na linha do ID. A coluna "Link no Drive" leva à pasta do lote. Dentro dela, o anúncio é o arquivo ou a subpasta que começa com o ID ou com o número (pasta `989`, arquivos `1140-1.jpg`). A planilha também traz tipo, headline e ângulo.
3. Ainda não achou: peça para a Larissa arrastar o arquivo do anúncio para o chat. Se ela não tiver, siga sem anúncio.

Versões Feed e Story do mesmo estático são o mesmo anúncio: use uma.

## Ler

- **Estático e carrossel:** abra cada imagem, na ordem, e leia o texto.
- **Vídeo:** se der para rodar scripts com ffmpeg, `python3 <pasta-da-skill>/scripts/midia.py video "<arquivo>" --id <ID>` gera a transcrição e quadros para ler o texto da tela. Se não der, use a headline e o ângulo da planilha e escreva "vídeo não transcrito" na ficha.

## Guardar

`Metta-Resgate/criativos/<ID>.md`, na pasta de trabalho:

```
# <ID> · <estático | carrossel | vídeo>
Onde está: <link ou caminho no Drive>
Tema: <uma frase>
Dor que o anúncio trata: <frase curta, do ponto de vista do dono>
Copy: <texto das lâminas ou transcrição>
Atenção: <oferta, evento ou data que já passou | nada>
```

Se o anúncio fala de oferta, evento ou data que já passou, escreva em "Atenção". Esse anúncio não vai para o lead: a mensagem segue na variante sem anexo.
