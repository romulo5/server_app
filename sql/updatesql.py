#!/usr/bin/python
import subprocess
import resources



DB_FILE = "/home/romulofloresta/server_app/sql/datadb.sql"
SQL_CMD = resources.SQL_CMD
SQL_DROP = resources.SQL_DROP
SQL_CREATE = resources.SQL_CREATE
SQL_DB = resources.DB_NAME



def create_db():
    subprocess.call('{} {}'.format(SQL_CREATE, SQL_DB), shell=True)


def import_data():
    subprocess.call('{} \'{}\' < {}'.format(SQL_CMD, SQL_DB, DB_FILE), shell=True)


def drop_db():
    subprocess.call('{} -f {}'.format(SQL_DROP, SQL_DB), shell=True)


