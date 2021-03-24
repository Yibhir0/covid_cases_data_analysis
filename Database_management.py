# Yassine Ibhir & David Pizzolongo
import mysql.connector
import os

import data_base_schema as schema


class My_DB_SQL:

    def __init__(self):
        self.__usr = 'root'  # os.environ['MYSQL_USR']
        self.__hst = 'localhost'
        self.__pwd = 'Flous101992'  # os.environ['MYSQL_PWD']
        self.__conn = None
        self.__cursr = None

    # connect to the given database or create a new connection
    def connection_db(self, db_name):
        try:
            if db_name == None:
                self.__conn = mysql.connector.connect(host=self.__hst,
                                                      user=self.__usr,
                                                      passwd=self.__pwd)

            else:
                self.__conn = mysql.connector.connect(host=self.__hst,
                                                      user=self.__usr,
                                                      passwd=self.__pwd,
                                                      database=db_name)
            self.__cursr = self.__conn.cursor()
        except mysql.connector.Error as err:
            print('problem with database {}'.format(err))

    def get_connection(self):
        return self.__conn

    def get_cursor(self):
        return self.__cursr

    # close cursor and connection
    def close_connection(self):
        self.__cursr.close()
        self.__conn.close()

    # create database if it does not exist
    def __create_db(self, db_name):
        sql_stm = " create database if not exists " + db_name
        self.__cursr.execute(sql_stm)

    # use the specified database param
    def __select_db(self, db_name):
        self.__cursr.execute("use " + db_name)

    # create table in the database used
    def __create_table(self, table_name, table_schema):
        sql_stm = " create table if not exists " + table_name + " " + table_schema
        self.__cursr.execute(sql_stm)

    # calls other methods to create table and insert values in that table
    def populate_table(self, table_name, table_schema, list_tuples):
        sql_stm = ""
        if table_name == 'corona_table':
            columns = len(list_tuples[0]) - 1
            columns_format = '(' + '%s,' * columns + '%s )'
            sql_stm = "insert into " + table_name + " values" + columns_format
        elif table_name == 'country_borders_table':
            sql_stm = "insert into " + table_name + " values(%s, %s, %s)"

        try:
            self.__create_db_table_keys(table_name, table_schema)
            self.__cursr.executemany(sql_stm, list_tuples)
        except mysql.connector.Error as err:
            print('Cannot populate table {}'.format(err))

        finally:
            self.__conn.commit()

    # calls methods to create and select database and table.
    def __create_db_table_keys(self, table_name, table_schema):

        self.__create_db(schema.data_base_name)

        self.__select_db(schema.data_base_name)

        self.__create_table(table_name, table_schema)
