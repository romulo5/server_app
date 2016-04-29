#!/usr/bin/python
# -*- coding: UTF-8 -*-

import collections

import json
import mysql.connector as mariadb

import resources

mariadb_connection = mariadb.connect(user=resources.DB_USER, password=resources.DB_PASSWD)
cursor = mariadb_connection.cursor()

FUNCAO_QUERY = '''SELECT f.NOM_FUNCAO, SUM(ex.Autorizado), SUM(ex.Pago)
    from ORZARE_FUNCAO AS f
    INNER JOIN EXECUÇÃO AS ex
    ON f.COD_FUNCAO = ex.Funcão__Cod_
    GROUP BY f.COD_FUNCAO, f.NOM_FUNCAO;'''

GND_QUERY = '''SELECT g.DES_GND, SUM(ex.Autorizado), SUM(ex.Pago)
                    from ORZARE_GND AS g
                    INNER JOIN EXECUÇÃO AS ex
                    ON g.COD_GND = ex.GND__Cod_
                    GROUP BY g.COD_GND, g.DES_GND;'''
PROGRAMA_QUERY = """SELECT p.DES_PROGRAMA, SUM(ex.Autorizado), SUM(ex.Pago), f.NOM_FUNCAO
                    from ORZARE_PROGRAMA AS p
                    INNER JOIN EXECUÇÃO AS ex
                    ON p.COD_PROGRAMA = ex.Programa__Cod_
                    INNER JOIN ORZARE_FUNCAO AS f
                    ON f.COD_FUNCAO = ex.Funcão__Cod_
                    GROUP BY p.DES_PROGRAMA, f.NOM_FUNCAO;"""

FUNCAO = "Funcao"
GND = "GND"
PROGRAMA = "Programa"

def get_data(query, dado):
    cursor.execute('USE {}'.format(resources.DB_NAME))
    cursor.execute(query)
    rows = cursor.fetchall()
    objects_list = []
    if dado == PROGRAMA:
        for (tipo_dado, autorizado, pago, funcao) in rows:
            d = collections.OrderedDict()
            d[dado] = tipo_dado
            d['Autorizado'] = autorizado
            d['Pago'] = pago
            d['Funcao'] = funcao
            objects_list.append(d)
    else:
        for (tipo_dado, autorizado, pago) in rows:
            d = collections.OrderedDict()
            d[dado] = tipo_dado
            d['Autorizado'] = autorizado
            d['Pago'] = pago
            objects_list.append(d)

    return objects_list

def save_json_data_file():
    funcoes = get_data(FUNCAO_QUERY, FUNCAO)
    gnds = get_data(GND_QUERY,GND)
    programas = get_data(PROGRAMA_QUERY, PROGRAMA)

    with open("version.json") as f:
        data_version = json.load(f)
        f.close()

    response = json.dumps({"Funcao": funcoes, "GND": gnds, "Programa": programas,'version': data_version['version'], 'updated':data_version['date']}, ensure_ascii=False)

    with open("response.json", 'w+') as f:
            f.write(response)
            f.close()



