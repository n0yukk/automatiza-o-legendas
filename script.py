vfrom PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import sys

caminho_csv = "Acervo Fotográfico - Legendas.xlsx - Antigas - SACI Antigo.csv"
pasta_imagens = "fotos"
pasta_saida = "saida"
fonte_path = "arial.ttf"

tamanho_fonte = 32
cor_texto = (255, 255, 255, 255)
margem_inferior = 10
margem_caixa = 10
margem_lateral = 40
cor_caixa = (0, 0, 0, 200)

os.makedirs(pasta_saida, exist_ok=True)

df = pd.read_csv(caminho_csv)
df.columns = df.columns.str.strip()

fonte = ImageFont.truetype(fonte_path, tamanho_fonte)

for _, linha in df.iterrows():
    nome_imagem = linha["Nome Arquivo"]
    texto = str(linha["Legenda"])
    caminho_imagem = os.path.join(pasta_imagens, nome_imagem)

    try:
        imagem = Image.open(caminho_imagem).convert("RGBA")
    except FileNotFoundError:
        print(f"⚠️ Imagem não encontrada: {nome_imagem}")
        continue

    txt_layer = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    max_largura = imagem.width - 2 * margem_lateral

    palavras = texto.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste_linha = linha_atual + (" " if linha_atual else "") + palavra
        largura_teste = draw.textbbox((0, 0), teste_linha, font=fonte)[2]
        if largura_teste <= max_largura:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)

    altura_total = sum(draw.textbbox((0, 0), l, font=fonte)[3] - draw.textbbox((0, 0), l, font=fonte)[1] for l in linhas)
    y = imagem.height - altura_total - margem_inferior - margem_caixa

    caixa_y0 = y - margem_caixa
    caixa_y1 = imagem.height
    draw.rectangle([0, caixa_y0, imagem.width, caixa_y1], fill=cor_caixa)

    for linha_txt in linhas:
        bbox = draw.textbbox((0, 0), linha_txt, font=fonte)
        largura_linha = bbox[2] - bbox[0]
        altura_linha = bbox[3] - bbox[1]
        x = (imagem.width - largura_linha) / 2
        draw.text((x, y), linha_txt, font=fonte, fill=cor_texto)
        y += altura_linha

    imagem_final = Image.alpha_composite(imagem, txt_layer).convert("RGB")
    caminho_saida = os.path.join(pasta_saida, nome_imagem)
    imagem_final.save(caminho_saida)
    print(f"✅ Imagem salva: {caminho_saida}")
