# Yassine Ibhir & David Pizzolongo


import mysql.connector

from Database_management import My_DB_SQL as dbm


class DataBaseAPI:
    def __init__(self, conn, cursr):
        self.__conn = conn
        self.__query_result = None
        self.__cursr = cursr

    def set_query_toTuples(self, column_str, tableName, criteria_str):

        if type(column_str) is list:
            column_str = ','.join(column_str)

        sql_stm = "select " + column_str + " from " + tableName + " " + criteria_str
        print(sql_stm)
        try:
            self.__cursr.execute(sql_stm)
            self.__query_result = self.__cursr.fetchall()
        except mysql.connector.Error as err:
            print('Cannot query from table {}'.format(err))
        finally:
            self.__conn.commit()

    def get_query_result(self):
        return self.__query_result


