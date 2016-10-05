#!/usr/bin/python
# 
# Script para converter a base de dados de .mdb para sql
# Utiliza o programa MdbTools para extrair os dados do arquivo .mdb  
# 
# Para utilizar copie o arquivo com nome data.mdb para a pasta sql e chame as duas funcoes na sequencia 
# 

import subprocess
import mysql.connector as mariadb
import resources
from datetime import datetime
from sql import sql


tables_schemas = [("EXECUÇÃO", "shemaexec"), ("ORZARE_FUNCAO","schemafunc"), ("ORZARE_GND","schemagnd"), ("ORZARE_PROGRAMA","schemaprog")]
MDB_FILE = "sql/data.mdb"
SQL_CMD = resources.SQL_CMD
SQL_DB = resources.DB_NAME
SQL_DUMP_CMD = resources.SQL_DUMP_CMD
SQL_FILE ="sql/datadb.sql"
mariadb_connection = mariadb.connect(user=resources.DB_USER, password=resources.DB_PASSWD)
cursor = mariadb_connection.cursor()


def create_db():
    print("----- Creating DB -------")
    startTime = datetime.now()
    print("Start at: {}".format(startTime))
    print(" ")
    cursor.execute('CREATE DATABASE IF NOT EXISTS  {};'.format(SQL_DB))
    for (table,schema) in tables_schemas:
        subprocess.call('mdb-schema -T {} {} mysql > {}.sql'.format(table, MDB_FILE, schema), shell=True)

    for (_,schema) in tables_schemas:
        subprocess.call('{} {} < {}.sql '.format(SQL_CMD, SQL_DB,schema), shell=True)
    print(" ")
    print("----- DB Created -------")
    print(" ")
    print("Time expent: {}".format(datetime.now() - startTime))
    print(" ")


def insert_data():
    print("----- Populating DB -------")
    startTime = datetime.now()
    print("Start at: {}".format(startTime))
    print(" ")
    cursor.execute('USE {}'.format(SQL_DB))
    subprocess.call('for i in $( mdb-tables {} ); do echo $i ; mdb-export -D "%Y-%m-%d %H:%M:%S" -H -I mysql {} $i > $i.sql; done'.format(MDB_FILE, MDB_FILE), shell=True)
    for (table,_) in tables_schemas:
        cursor.execute('TRUNCATE TABLE {}'.format(table))
        subprocess.call('{} {} < {}.sql'.format(SQL_CMD, SQL_DB,table), shell=True)
    subprocess.call("rm *.sql", shell=True)
    sql.save_json_data_file()
    print(" ")
    print("----- DB Populated -------")
    print(" ")
    print("Time expent: {}".format(datetime.now() - startTime))
    print(" ")



def exportsql():
    print("----- Exporting SQL File -------")
    startTime = datetime.now()
    print("Start at: {}".format(startTime))
    print(" ")
    subprocess.call('{} {} > {}'.format(SQL_DUMP_CMD, SQL_DB, SQL_FILE), shell=True)    
    print("----- Finished! -------")
    print("Time expent: {}".format(datetime.now() - startTime))



if __name__=="__main__":
    create_db()
    insert_data()
    exportsql()

