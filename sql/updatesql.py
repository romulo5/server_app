#!/usr/bin/python
import subprocess
import mysql.connector as mariadb
import resources
from sql import sql


# tables_schemas = [("EXECUÇÃO", "shemaexec"), ("ORZARE_FUNCAO","schemafunc"), ("ORZARE_GND","schemagnd"), ("ORZARE_PROGRAMA","schemaprog")]
DB_FILE = "sql/datadb.sql"
SQL_CMD = resources.SQL_CMD
SQL_DROP = resources.SQL_DROP
SQL_CREATE = resources.SQL_CREATE
SQL_DB = resources.DB_NAME

# mariadb_connection = mariadb.connect(user=resources.DB_USER, password=resources.DB_PASSWD)
# cursor = mariadb_connection.cursor()


def create_db():
    subprocess.call('{} {}'.format(SQL_CREATE, SQL_DB), shell=True)

    # cursor.execute('CREATE DATABASE {};'.format(SQL_DB))

#     for (table,schema) in tables_schemas:
#         subprocess.call('mdb-schema -T {} {} mysql > {}.sql'.format(table, MDB_FILE, schema), shell=True)
#
#     for (_,schema) in tables_schemas:
#         subprocess.call('{} {} < {}.sql '.format(SQL_CMD, SQL_DB,schema), shell=True)
#
#
# def insert_data():
#     cursor.execute('USE {}'.format(SQL_DB))
#     subprocess.call('for i in $( mdb-tables {} ); do echo $i ; mdb-export -D "%Y-%m-%d %H:%M:%S" -H -I mysql {} $i > $i.sql; done'.format(MDB_FILE, MDB_FILE), shell=True)
#     for (table,_) in tables_schemas:
#         cursor.execute('TRUNCATE TABLE {}'.format(table))
#         subprocess.call('{} {} < {}.sql'.format(SQL_CMD, SQL_DB,table), shell=True)
#     subprocess.call("rm *.sql", shell=True)
#     sql.save_json_data_file()


def import_data():
    subprocess.call('{} {} < {}'.format(SQL_CMD, SQL_DB, DB_FILE), shell=True)


def drop_db():
    subprocess.call('{} -f {}'.format(SQL_DROP, SQL_DB), shell=True)

     # cursor.execute('DROP DATABASE {};'.format(SQL_DB))

