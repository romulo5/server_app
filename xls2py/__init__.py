import locale
import pyexcel
import pyexcel.ext.xls
import json

# Importa os dados das planilhas excel utilizando a biblioteca pyexcel e gera um json com os dados.

def convert():

    #Definir formato de localização dos dados
    locale.setlocale(locale.LC_ALL, 'en_US')

    #Planilha - GND
    # Importa dados da planilha de Grandes Grupos de Despesa
    raw_sheet_gnd = pyexcel.get_sheet(file_name="/home/romulofloresta/server_app/xls2py/gnd-raw.xls")

    #Remove linhas e colunas desnecessárias
    raw_sheet_gnd.delete_rows(list(range(4))) #deleta linhas acima
    for i in range(3):
        raw_sheet_gnd.delete_rows([-1]) #deleta linhas abaixo
    raw_sheet_gnd.delete_columns([0, 2, 4, 5, 7])

    #Converte para tipo de dados python
    raw_sheet_gnd.name_columns_by_row(0)
    py_records_gnd = raw_sheet_gnd.to_records()

    #formata os valores de moeda
    for record in py_records_gnd:
        record['Autorizado'] = locale.currency(record["Autorizado"], symbol=None)
        record['Pago'] = locale.currency(record["Pago"], symbol=None)

    # Funções
    # Importa dados da planilha de Funções
    raw_sheet_func = pyexcel.get_sheet(file_name="/home/romulofloresta/server_app/xls2py/funcoes-raw.xls")

    #Remove linhas e colunas desnecessárias
    raw_sheet_func.delete_rows(list(range(4))) #deleta linhas acima
    for i in range(4):
        raw_sheet_func.delete_rows([-1]) #deleta linhas abaixo
    raw_sheet_func.delete_columns([1, 3, 4, 6])

    #Alterar título da coluna
    raw_sheet_func[0,0] = 'Funcao'

    #Converte para tipo de dados python
    raw_sheet_func.name_columns_by_row(0)
    py_records_func = raw_sheet_func.to_records()

    # Formata os campos
    for record in py_records_func:
        record['Funcao'] = record['Funcao'][4:]
        record['Autorizado'] = locale.currency(record["Autorizado"], symbol=None)
        record['Pago'] = locale.currency(record["Pago"], symbol=None)

    #Pega a versão do banco de dados
    with open('server_app/version.json') as f:
        data_version = json.load(f)
        f.close()

    # Retorna json com os dados
    response = json.dumps({'Funcao': py_records_func, 'GND': py_records_gnd, 'version': data_version['version'], 'updated':data_version['date']})
    return response