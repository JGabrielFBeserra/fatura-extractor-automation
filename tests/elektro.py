import pdfplumber
from tkinter import Tk, filedialog

Tk().withdraw()

arquivos_pdf = filedialog.askopenfilenames(
    title="Selecione os PDFs",
    filetypes=[("Arquivos PDF", "*.pdf")]
)

print(f"{arquivos_pdf}\n\n")

for caminho_pdf in arquivos_pdf:
    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()

        linhas = texto.split('\n')  
        for i, linha in enumerate(linhas):
            print(f"{i}: {linha}")
            if "Emissão: " in linha:   
                emissao = valor = linha.split(" ")[-1]
        conteudo_unificado = " ".join(linhas).lower()  # array
        

        if "elektro" in conteudo_unificado:
            print("Fatura ELEKTRO detectada.")
            
            linha5 = [linhas[5]]  
            print(linha5)
            vencimento = linha5[0].split(' ')[3] 
            valor = linha5[0].split(' ')[5]  
            
            
            print(f"\nCódigo: {linhas[0]}, Vencimento: {vencimento}, Valor: {valor}")

        else:
            print(f"Fatura ELEKTRO não detectada no arquivo: {caminho_pdf}")
            