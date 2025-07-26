from openpyxl import  load_workbook
import json


abrir = load_workbook(r"C:\Users\joao.beserra\Downloads\Power Automate - Controle de energias elétricas - 20251.xlsx")

planilha = abrir["ATUAL - POWER AUTOMATE"]

consultas = {}

with open("consultas.jsonl", "r", encoding="utf-8") as f:
    for linha in f:
        if linha.strip():
            linha_dict = json.loads(linha)
            consultas.update(linha_dict)
            
print(consultas.resultados)

# for row in planilha.iter_rows(min_col=3, max_col=3, min_row=1):
#     for cell in row:
#         if cell = 
#         print(cell.value)