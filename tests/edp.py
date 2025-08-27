import pdfplumber
from datetime import datetime
from tkinter import Tk, filedialog

Tk().withdraw()

arquivos_pdf = filedialog.askopenfilenames(
    title="Selecione os PDFs",
    filetypes=[("Arquivos PDF", "*.pdf")]
)

print(arquivos_pdf)

for caminho_pdf in arquivos_pdf:
    print("\n"+caminho_pdf+"\n")
    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()

        linhas = texto.split('\n')  
        for i, linha in enumerate(linhas):
            print(f"{i}: {linha}")
            if "Emissão: " in linha:   
                emissao = valor = linha.split(" ")[-1]

        if len(linhas) > 43:
           
           
            print("Segundo template de fatura detectado.")
            linha_principal = len(linhas) - 3  # linha principal é a antepenultima linha da pagina (a linha onde fica oque eu quero)
            
            dados_pricipais = linhas[linha_principal] 
            dados_pricipais = dados_pricipais.split(" ")
            id = dados_pricipais[0]
            ven = dados_pricipais[1]
            val = dados_pricipais[3]
            print(f"{id}, {ven}, {val}, {emissao}")
            partes = [id, ven, val, emissao]
            print(f"ID Unidade Consumidora: {partes[0]}\nVencimento: {partes[1]}\nTotal a Pagar: {partes[2]}\nData de Emissão: {partes[3]}")
            continue
        else:
            print("Primeiro template de fatura detectado.")
            linha_principal = len(linhas) - 4
            
            dados_pricipais = linhas[linha_principal] 
            dados_pricipais = dados_pricipais.split(" ")
            id = dados_pricipais[0]
            ven = dados_pricipais[1]
            val = dados_pricipais[3]
            print(f"{id}, {ven}, {val}, {emissao}")
            partes = (id +" "+ ven +" "+ val +" "+ emissao).split(" ")
            print(partes)

            print(f"ID Unidade Consumidora: {partes[0]}\nVencimento: {partes[1]}\nTotal a Pagar: {partes[2]}\nData de Emissão: {partes[3]}")
            continue