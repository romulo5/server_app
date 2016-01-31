import pyexcel
import pyexcel.ext.xls
import json

# Este módulo importa os dados das planilhas excel utilizando a biblioteca pyexcel e gera um json com os dados das planilhas.



# importa dados da planilha de Grandes Grupos
raw_sheet_gnd = pyexcel.get_sheet(file_name="pyex/gnd.xls")
raw_sheet_gnd.name_columns_by_row(0)
converted_sheet_gnd = raw_sheet_gnd.to_records()

# importa dados da planilha de Funções
raw_sheet_func = pyexcel.get_sheet(file_name="pyex/funcoes.xls")
raw_sheet_func.name_columns_by_row(0)
converted_sheet_func = raw_sheet_func.to_records()

# Retorna json com os dados das planilhas
response = json.dumps([converted_sheet_func,converted_sheet_gnd])

