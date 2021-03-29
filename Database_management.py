# Yassine Ibhir & David Pizzolongo
import mysql.connector
import os

import data_base_schema as schema


class My_DB_SQL:

    def __init__(self):
        self.__usr = os.environ['MYSQL_USR']
        self.__hst = 'localhost'
        self.__pwd = os.environ['MYSQL_PWD']
        self.__conn = None
        self.__cursr = None

    # connect to the given database or create a new connection
    def connection_db(self, db_name):

        try:

            self.__conn = mysql.connector.connect(host=self.__hst,
                                                      user=self.__usr,
                                                      passwd=self.__pwd)
            self.__cursr = self.__conn.cursor()
            self.__create_db(db_name)
            self.__select_db(db_name)


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
        if table_name == schema.corona_table_name:
            columns = len(list_tuples[0]) - 1
            columns_format = '(' + '%s,' * columns + '%s )'
            sql_stm = "insert into " + table_name + " values" + columns_format
        elif table_name == schema.country_borders_table_name:
            sql_stm = "insert into " + table_name + " values(%s, %s, %s)"

        try:
            self.__create_db_table_keys(table_name, table_schema)
            self.__cursr.executemany(sql_stm, list_tuples)
            print('Data is stored into ', table_name)
        except mysql.connector.Error as err:
            print('Cannot populate table {}'.format(err))

        finally:
            self.__conn.commit()

    # calls methods to create and select database and table.
    # Uses data_base_schema class (schema)
    def __create_db_table_keys(self, table_name, table_schema):

        self.__create_db(schema.data_base_name)

        self.__select_db(schema.data_base_name)

        self.__create_table(table_name, table_schema)

    # returns the borders of a country based on the given criteria
    def get_country_borders(self, column_str, tableName, criteria_str):

        query_result = None
        sql_stm = "select distinct " + column_str + " from " + tableName + " " + criteria_str


        try:
            self.__cursr.execute(sql_stm)
            query_result = self.__cursr.fetchall()
        except mysql.connector.Error as err:
            print('Cannot query from table {}'.format(err))
        finally:
            self.__conn.commit()

        return query_result
