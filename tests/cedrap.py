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
        conteudo_unificado = " ".join(linhas).lower()  # array 

        for i, linha in enumerate(linhas):
            print(f"{i}: {linha}")
            if "DATA DE EMISSÃO: " in linha:
                emissao = valor = linha.split(":")[1]

        print("Fatura CEDRAP detectada.")
        linha_principal = len(linhas) - 3  # linha principal é a antepenultima linha da pagina (a linha onde fica oque eu quero)
        dados_pricipais = linhas[linha_principal] 
        dados_pricipais = dados_pricipais + emissao
        print(f"{dados_pricipais}")
        partes = dados_pricipais.split(" ")
        print(partes)
        print(f"ID Unidade Consumidora: {partes[0]}\nVencimento: {partes[1]}\nTotal a Pagar: {partes[2]}\nData de Emissão: {partes[3]}")

    
