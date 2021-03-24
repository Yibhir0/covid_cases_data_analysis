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
            print(self.__cursr)
            column_str = ','.join(column_str)

        sql_stm = "select " + column_str + " from " + tableName + " " + criteria_str
        try:
            self.__cursr.execute(sql_stm)
            self.__query_result = self.__cursr.fetchall()
        except mysql.connector.Error as err:
            print('Cannot query from table {}'.format(err))
        finally:
            self.__conn.commit()

    def get_query_result(self):
        return self.__query_result


# get results of the specified columns of the specified table
def get_colums_data(country, columns_str):
    dbms = dbm()
    dbms.connection_db('covid_corona_db_dp_yi')
    con = dbms.get_connection()
    cur = dbms.get_cursor()
    dba = DataBaseAPI(con, cur)
    # columns_str = ['NewCases', 'NewDeaths', 'NewRecovered']
    table_corona = 'corona_table'
    criteria1 = ' where country_other = "' + country + '" ;'
    dba.set_query_toTuples(columns_str, table_corona, criteria1)
    columns_result = dba.get_query_result()
    print(columns_result)
    return columns_result


def get_border_countries(country,limit):
    dbms = dbm()
    dbms.connection_db('covid_corona_db_dp_yi')
    con = dbms.get_connection()
    cur = dbms.get_cursor()
    columns_str1 = 'border_country'
    table_borders = 'country_borders_table'
    criteria2 = ' where country_other = "' + country + '"   order by distance desc limit' + limit+ ';'
    dba = DataBaseAPI(con, cur)
    dba.set_query_toTuples(columns_str1, table_borders, criteria2)
    country_border = dba.get_query_result()
    print(country_border)
