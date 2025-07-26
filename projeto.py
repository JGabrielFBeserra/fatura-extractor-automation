import pdfplumber
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from openpyxl import  load_workbook
import time
import os
from datetime import datetime
import json

abrir = load_workbook(r"C:\Users\joao.beserra\Downloads\Power Automate - Controle de energias elétricas - 20251.xlsx")

planilha = abrir["ATUAL - POWER AUTOMATE"]


consultas = {}
agora = datetime.now()
agora = (f"{agora.day}/{agora.month}/{agora.year} {agora.hour}:{agora.minute}:{agora.second}")

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

        print(f"{arquivos_pdf}\n") 
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
                    partes[0] = partes[0].split('/')[0]
                    print(f"{countcedrap}:{caminho_pdf}\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}\n")
                    resultado = f"CEDRAP:\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}"
                    resultado = {
                        "empresa": "CEDRAP",
                        "id": partes[0],
                        "vencimento": partes[1],
                        "valor": partes[2]
                    }
                    resultados.append(resultado)
                    
                elif "nota fiscal/conta de energia elétrica" in conteudo_unificado:
                    countedp += 1
                    empresa = ""
                    print("Fatura EDP - SÃO PAULO detectada.")
                    if len(linhas) > 43:
                        print("Segundo template de fatura detectado.")
                        linha_principal = len(linhas) - 3
                        empresa = "EDP-SP-MODELO02"
                    else:
                        print("Primeiro template de fatura detectado.")
                        linha_principal = len(linhas) - 4
                        empresa = "EDP-SP-MODELO01"
                    linha_alvo = linhas[linha_principal]
                    partes = linha_alvo.split(" ", 2)
                    print(f"{countedp}: {caminho_pdf}\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}\n")
                    resultado = f"EDP:\nID Unidade Consumidora: {partes[0]}, Vencimento: {partes[1]}, Total a Pagar: {partes[2]}"
                    partes[2] = partes[2].split(' ')[1]
                    resultado = {
                        "empresa": empresa,
                        "id": partes[0],
                        "vencimento": partes[1],
                        "valor": partes[2]
                    }
                    resultados.append(resultado)
                elif "elektro" in conteudo_unificado:
                    countelektro = countelektro + 1
                    print("Fatura ELEKTRO detectada.")
                    
                    linha5 = [linhas[5]]  
                    vencimento = linha5[0].split(' ')[3] 
                    valor = linha5[0].split(' ')[5]  
                    
                    
                    print(f"{countelektro}: {caminho_pdf}\nID Unidade Consumidora:  {linhas[0]}, Vencimento: {vencimento}, Valor: {valor}\n")
                    resultado = f"ELEKTRO:\nID Unidade Consumidora: {linhas[0]}, Vencimento: {vencimento}, Total a Pagar: R${valor}"
                    resultado = {
                        "empresa": "ELEKTRO",
                        "id": linhas[0],
                        "vencimento": vencimento,
                        "valor": valor
                    }
                    resultados.append(resultado)
            
                else:
                    print(f"{count}:{caminho_pdf} - Fatura não reconhecida\nConteúdo extraído: {conteudo_unificado[:300]}...")  # Mostra os primeiros 300 chars para debug

                count = count+1
                
        fim = time.time()
        tempo_total = fim - inicio
        
        consultas = {}

        if os.path.exists("consultas.jsonl"):
            # ler apenas para deifinir o tamanho da variavel id
            with open("consultas.jsonl", "r", encoding="utf-8") as f:
                for linha in f:
                    # pra cada linha no jsonl eu vou tirar os espaços e \n
                    if linha.strip():
                        # eu coloco tudo dentro de consultas, todas as linhas do jsonl
                        linha_dict = json.loads(linha)
                        consultas.update(linha_dict)
        else: 
            with open("consultas.jsonl", "w", encoding="utf-8") as f:
                print("criado do 0 consultas.jsol")

        # tiver dados ele pega o maior id e define
        if consultas:
            # vai estar assim ó consultas = { consulta_1: {...}, consulta_2: {...}} é só pegar os ids de cada linha e no final ele vai definir o maior+1=proximo
            ultimo_id = [int(key.split("_")[1]) for key in consultas.keys()]
            count_consulta = max(ultimo_id) + 1
        else:
            count_consulta = 1

        id_consulta = f"consulta_{count_consulta}"

        # nova entrada de consulta
        consultas[id_consulta] = {
            "timestamp": agora,
            "duracao_consulta": f"{tempo_total:.2f}s",
            "resultados": resultados,
        }
        # salva de volta no arquivo, usando o patametro "a"=ammend para adicionar no final
        with open("consultas.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({id_consulta: consultas[id_consulta]}, ensure_ascii=False) + "\n")
          
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
