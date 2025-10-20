from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import re
import textwrap

def criar_pdf(texto, pasta_pdf, prefixo):
    if not os.path.exists(pasta_pdf):
        os.makedirs(pasta_pdf)

    # Determina próximo número
    arquivos = os.listdir(pasta_pdf)
    numeros = []
    for arquivo in arquivos:
        match = re.match(rf"{prefixo}(\d+)\.pdf", arquivo)
        if match:
            numeros.append(int(match.group(1)))
    proximo_numero = max(numeros, default=0) + 1

    caminho_pdf = os.path.join(pasta_pdf, f"{prefixo}{proximo_numero}.pdf")

    # Cria PDF
    largura, altura = A4
    pdf = canvas.Canvas(caminho_pdf, pagesize=A4)

    # Configuração
    margem = 20 * mm
    largura_util = largura - 2 * margem
    altura_inicial = altura - margem
    espacamento_linha = 12

    # Quebra texto em linhas que cabem na largura
    linhas = []
    for paragrafo in texto.split("\n"):
        linhas.extend(textwrap.wrap(paragrafo, width=95))  # Ajuste width conforme necessário
        linhas.append("")  # linha em branco entre parágrafos

    y = altura_inicial
    for linha in linhas:
        if y < margem:
            pdf.showPage()
            y = altura_inicial
        pdf.drawString(margem, y, linha)
        y -= espacamento_linha

    pdf.save()
    print(f"✅ PDF salvo em: '{caminho_pdf}'")

# --- Função principal ---
def gerar_pdfs_automatico(arquivo_txt, tipo_noticia):
    if tipo_noticia == "f":
        pasta_pdf = r"C:\Users\davin\Desktop\DevPast\AletheIA\Dataset\noticias_falsas"
        prefixo = "noticia_falsa_"
    elif tipo_noticia == "v":
        pasta_pdf = r"C:\Users\davin\Desktop\DevPast\AletheIA\Dataset\noticias_verdadeiras"
        prefixo = "noticia_verdadeira_"
    else:
        print("Opção inválida! Use 'f' ou 'v'.")
        return

    with open(arquivo_txt, "r", encoding="utf-8") as f:
        conteudo = f.read()

    noticias = [n.strip() for n in conteudo.split("\n\n") if n.strip()]

    for noticia in noticias:
        criar_pdf(noticia, pasta_pdf, prefixo)

# --- Entrada do usuário ---
if __name__ == "__main__":
    tipo = input("Digite 'f' para NOTÍCIA FALSA ou 'v' para NOTÍCIA VERDADEIRA:\n").lower()
    arquivo_txt = input("Digite o caminho completo do arquivo .txt com as notícias:\n")
    gerar_pdfs_automatico(arquivo_txt, tipo)
