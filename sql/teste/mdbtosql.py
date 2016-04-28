#!/usr/bin/ python
import subprocess

if __name__ == "__main__":

    import sys

    #("EXECUÇÃO","shemaexec"),
    tables_schemas = [("ORZARE_FUNCAO","schemafunc"), ("ORZARE_GND","schemagnd"), ("ORZARE_PROGRAMA","schemaprog")]
    MDB_FILE = "{}".format(sys.argv[1])
    SQL_TABLEls_CMD = "mysql  -uromulo -pfortuna"
    SQL_INSERT_CMD ="mysql -uromulo -pfortuna"
    SQL_DB = "testedb"

    for (table,schema) in tables_schemas:
        subprocess.call('mdb-schema -T {} {} mysql > {}.sql'.format(table, MDB_FILE, schema), shell=True)

    for (_,schema) in tables_schemas:
        subprocess.call('{} {} < {}.sql '.format(SQL_INSERT_CMD, SQL_DB,schema), shell=True)

    subprocess.call('for i in $( mdb-tables {} ); do echo $i ; mdb-export -D "%Y-%m-%d %H:%M:%S" -H -I mysql {} $i > $i.sql; done'.format(MDB_FILE, MDB_FILE), shell=True)
    for (table,_) in tables_schemas:
        subprocess.call('{} {} < {}.sql'.format(SQL_INSERT_CMD, SQL_DB,table), shell=True)











