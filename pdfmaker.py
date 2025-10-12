from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import re

def texto_para_pdf(texto, tipo_noticia):
    # Escolhe a pasta com base no tipo de notícia
    if tipo_noticia == "f":
        pasta_pdf = r"C:\Users\davin\Desktop\DevPast\AletheIA\Dataset\noticias_falsas"
        prefixo = "noticia_falsa_"
    elif tipo_noticia == "v":
        pasta_pdf = r"C:\Users\davin\Desktop\DevPast\AletheIA\Dataset\noticias_verdadeiras"
        prefixo = "noticia_verdadeira_"
    else:
        print("Opção inválida! Use 'f' para falsa ou 'v' para verdadeira.")
        return

    # Garante que a pasta existe
    if not os.path.exists(pasta_pdf):
        os.makedirs(pasta_pdf)

    # Determina o próximo número disponível
    arquivos = os.listdir(pasta_pdf)
    numeros = []
    for arquivo in arquivos:
        match = re.match(rf"{prefixo}(\d+)\.pdf", arquivo)
        if match:
            numeros.append(int(match.group(1)))
    proximo_numero = max(numeros, default=0) + 1

    # Nome final do PDF
    caminho_pdf = os.path.join(pasta_pdf, f"{prefixo}{proximo_numero}.pdf")

    # Cria o PDF
    largura, altura = A4
    pdf = canvas.Canvas(caminho_pdf, pagesize=A4)

    # Posição inicial do texto
    x = 50
    y = altura - 50

    # Escreve cada linha do texto
    for linha in texto.split("\n"):
        pdf.drawString(x, y, linha)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = altura - 50

    # Salva o PDF
    pdf.save()
    print(f"✅ PDF salvo em: '{caminho_pdf}'")

# --- Entrada do usuário ---
if __name__ == "__main__":
    texto = input("Digite o texto que deseja converter em PDF:\n")
    tipo = input("Digite 'f' para salvar como NOTÍCIA FALSA ou 'v' para NOTÍCIA VERDADEIRA:\n").lower()
    texto_para_pdf(texto, tipo)
