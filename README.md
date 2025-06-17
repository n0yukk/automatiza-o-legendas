# Legenda Automática de Fotos

Este projeto aplica legendas em lote em fotos com base em um arquivo CSV de referência, adicionando automaticamente uma caixinha preta ao fundo do texto para melhor legibilidade.

## Como funciona

- Lê o CSV com nomes dos arquivos e legendas.
- Abre cada imagem, centraliza o texto na parte inferior.
- Adiciona quebra automática de linha para evitar cortes.
- Gera uma imagem final na pasta `saida/`.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `Pillow`
  - `pandas`

Instale as dependências com:
```bash
pip install pillow pandas
