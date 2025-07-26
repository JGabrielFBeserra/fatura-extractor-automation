import pdfplumber
from tkinter import Tk, filedialog

Tk().withdraw()

arquivos_pdf = filedialog.askopenfilenames(
    title="Selecione os PDFs",
    filetypes=[("Arquivos PDF", "*.pdf")]
)

print(arquivos_pdf)

for caminho_pdf in arquivos_pdf:
    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()

        linhas = texto.split('\n')  

        for i, linha in enumerate(linhas):
            print(f"{i}: {linha}")

        if len(linhas) > 43:
            print("Segundo template de fatura detectado.")
            linha_principal = len(linhas) - 3  # linha principal é a antepenultima linha da pagina (a linha onde fica oque eu quero)
            linha_alvo = linhas[linha_principal] 
            print(linha_alvo)
            partes = (linha_alvo.split(" ", 2))
            print(partes)
            print(f"ID Unidade Consumidora: {partes[0]}\n Vencimento: {partes[1]}\nTotal a Pagar: {partes[2]}\n")
            continue
        else:
            print("Primeiro template de fatura detectado.")
            linha_principal = len(linhas) - 4
            linha_alvo = linhas[linha_principal] 
            print(linha_alvo)
            partes = (linha_alvo.split(" ", 2))
            print(partes)
            print(f"ID Unidade Consumidora: {partes[0]}\nVencimento: {partes[1]}\nTotal a Pagar: {partes[2]}\n")
            continue