# Yassine Ibhir & David Pizzolongo
import mysql.connector
import os

import data_base_schema as schema


class My_DB_SQL:

    # holds private information and initializes database connection and cursor as None
    def __init__(self):
        self.__usr = "coviduser"
        self.__hst = 'localhost'
        self.__pwd = "covidpass"
        self.__conn = None
        self.__cursr = None


    # This function makes a new connection to the database, creates a cursor to execute 
    # MySQL statements, and creates and selects the database, by calling their respective methods. 
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

    # creates the database if it does not exist
    def __create_db(self, db_name):
        sql_stm = " create database if not exists " + db_name
        self.__cursr.execute(sql_stm)

    # uses the specified database name
    def __select_db(self, db_name):
        self.__cursr.execute("use " + db_name)

    # creates table in the active database
    def __create_table(self, table_name, table_schema):
        sql_stm = " create table if not exists " + table_name + " " + table_schema
        self.__cursr.execute(sql_stm)

    # The method populate_table creates a table with the given name and schema, 
    # and inserts into to the appropriate table the list of clean tuples,
    # while handling any SQL errors. This method is called twice for the country_borders_table 
    # and corona_table. 
    def populate_table(self, table_name, table_schema, list_tuples):
        sql_stm = ""
        if table_name == schema.corona_table_name:
            # number of columns minus one
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

        # once it is finished inserting, it commits the changes
        finally:
            self.__conn.commit()

    # calls methods to create and select database and table.
    # Uses data_base_schema class (schema).
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
