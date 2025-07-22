import pdfplumber
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import time
import os






while True:
    print("\n\nDigite o número baseado na ação que deseja executar:\n[1] Extrair PDF e preencher planilha [2] Separar Canhotos de Faturas [3] Fechar")
    
    opcao = input("Escolha uma opção: ")
    resultados = []
    count = 0
    countcedrap=0
    countedp=0
    countelektro=0
    if opcao == "1": 
        
        print("Abrindo caixa de seleção de PDF...")  
        Tk().withdraw()

        arquivos_pdf = filedialog.askopenfilenames(
            title="Selecione os PDFs",
            filetypes=[("Arquivos PDF", "*.pdf")]
            
        )

        print(f"{arquivos_pdf}\n\n") 
        inicio = time.time()
        for caminho_pdf in arquivos_pdf:
            with pdfplumber.open(caminho_pdf) as pdf:
                pagina = pdf.pages[0]
                texto = pagina.extract_text()
                linhas = texto.split('\n')
                conteudo_unificado = " ".join(linhas).lower()  # Para comparação robusta

                if "cedrap" in conteudo_unificado:
                    countcedrap += 1
                    print("Fatura CEDRAP detectada.")
                    linha_principal = len(linhas) - 3
                    linha_alvo = linhas[linha_principal]
                    partes = linha_alvo.split(" ", 2)
                    print(f"{countcedrap}:{caminho_pdf}\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}\n")
                    resultado = f"CEDRAP:\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}"
                    resultados.append(resultado)
                    
                elif "nota fiscal/conta de energia elétrica" in conteudo_unificado:
                    countedp += 1
                    print("Fatura EDP - SÃO PAULO detectada.")
                    if len(linhas) > 43:
                        print("Segundo template de fatura detectado.")
                        linha_principal = len(linhas) - 3
                    else:
                        print("Primeiro template de fatura detectado.")
                        linha_principal = len(linhas) - 4
                    linha_alvo = linhas[linha_principal]
                    partes = linha_alvo.split(" ", 2)
                    print(f"{countedp}: {caminho_pdf}\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}\n")
                    resultado = f"EDP:\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}"
                    resultados.append(resultado)
                   
                elif "nota fiscal/conta de energia elétrica" in conteudo_unificado:
                    countedp += 1
                    print("Fatura EDP - SÃO PAULO detectada.")
                    if len(linhas) > 43:
                        print("Segundo template de fatura detectado.")
                        linha_principal = len(linhas) - 3
                    else:
                        print("Primeiro template de fatura detectado.")
                        linha_principal = len(linhas) - 4
                    linha_alvo = linhas[linha_principal]
                    partes = linha_alvo.split(" ", 2)
                    print(f"{countedp}: {caminho_pdf}\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}\n")
                    resultado = f"EDP:\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}"
                    resultados.append(resultado)
                elif "elektro" in conteudo_unificado:
                    countelektro = countelektro + 1
                    print("Fatura ELEKTRO detectada.")
                    
                    linha5 = [linhas[5]]  
                    vencimento = linha5[0].split(' ')[3] 
                    valor = linha5[0].split(' ')[5]  
                    
                    
                    print(f"{countelektro}: {caminho_pdf}\nID Unidade Consumidora:  {linhas[0]}, Vencimento: {vencimento}, Valor: {valor}\n")
                    resultado = f"ELEKTRO:\nID Unidade Consumidora: {linhas[0]}, Vencimento: {vencimento}, Total a Pagar: R${valor}"
                    resultados.append(resultado)
            
                else:
                    print(f"{count}:{caminho_pdf} - Fatura não reconhecida\nConteúdo extraído: {conteudo_unificado[:300]}...")  # Mostra os primeiros 300 chars para debug

                count = count+1
        fim = time.time()
        tempo_total = fim - inicio
        
        print("\nRESULTADOS ENCONTRADOS: ")
        for resultado in resultados:
            print(f"\n{resultado}") 
        print(f"\nTempo total de execução: {tempo_total:.2f} segundos")                
        print(f"Total de faturas CEDRAP: {countcedrap}")
        print(f"Total de faturas ELEKTRO: {countelektro}")
        print(f"Total de faturas EDP: {countedp}")
        print("✅ Arquivo salvo com sucesso! Abrindo a Planilha...")
        countedp = 0
        countcedrap = 0
        countelektro = 0
        count = 0       
                   
    elif opcao == "2":
        pasta_documentos = Path.home() / "Documents"
        nome_subpasta = "paginas_impares_pdf"
        caminho_pasta = pasta_documentos / nome_subpasta
        os.makedirs(caminho_pasta, exist_ok=True)
        print(f"Pasta criada em: {caminho_pasta}")#makedir cria uma pasta com o nome passado como parametro, se existir ja n faz nada
        
        print("Abrindo caixa de seleção de PDF...") 
        Tk().withdraw()

        arquivo_pdf = filedialog.askopenfilename(
            title="Selecione o PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
            
        )
        if not arquivo_pdf:
            print("Nenhum arquivo selecionado.")
            exit()
            
        pasta_base = filedialog.askdirectory(
            title="Escolha onde salvar as páginas ímpares", 
            initialdir=(caminho_pasta)
            )
        reader = PdfReader(arquivo_pdf) #le o pdf gigante
        
        
        
        contador = 1
        for i in range(len(reader.pages)):
            if i % 2 == 0:
                 #filtra as paginas impares e cria um novo arquivo
                writer = PdfWriter()  # cria um novo writer para cada página
                writer.add_page(reader.pages[i])  # adiciona só uma página
            
                nome_base = os.path.basename(arquivo_pdf).replace(".pdf", "") #basename pega e tira o nome e extensao do arquivo
                nome_arquivo = f"{nome_base}_{contador}.pdf"  # e aqui eu passo o nome base e o numero dele
                caminho_completo = caminho_pasta / nome_arquivo
           
                caminho_completo = os.path.join(caminho_pasta, nome_arquivo) #junta o nome da pasta com o nome do arquivo
                with open(caminho_completo, "wb") as f: #ele abre o array com os caminhos e dentro dele, cada pagina ele chama de f 
                    writer.write(f) #escreve um novo pdf, basicamente ele escreve o conteudo de writer em cada pagina(f)
                print(f"Página {contador} salva em: {caminho_completo}")
                contador +=1 
        print(f"Total de arquivos criados: {contador}")
            
            


        
        
        print("✅ PDF separado com sucesso! Ele se encontra no caminho: \nEstou abrindo a pasta com todos os PDFs pra você...")
        os.startfile(caminho_pasta)
        
        
    else:
        print(f"\nVocê digitou: {repr(opcao)}\n!!! Opção inválida. Digite 1 ou 2. !!!\n")    
