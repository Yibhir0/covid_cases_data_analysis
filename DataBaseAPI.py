# Yassine Ibhir & David Pizzolongo
import mysql.connector
import data_base_schema as schema
from FileIO import FileIO
from ScrapeClass import ScrapeClass


class My_DB_SQL:

    def __init__(self):
        self.__usr = 'root'
        self.__hst = 'localhost'
        self.__pwd = 'Flous101992'
        self.__conn = None
        self.__cursr = None

    # connect to the given database or create a new connection
    def connection_db(self, db_name):
        try:
            if db_name == None:
                self.__conn = mysql.connector.connect(host=self.__hst,
                                                      user=self.__usr,
                                                      passwd=self.__pwd)
                self.__cursr = self.__conn.cursor()
            else:
                self.__conn = mysql.connector.connect(host=self.__hst,
                                                      user=self.__usr,
                                                      passwd=self.__pwd,
                                                      database=db_name)

        except mysql.connector.Error as err:
            print('problem with database {}'.format(err))

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

    # Execute and display a result of a query
    # def select_data_from_table(self, table_name, columns_str, criteria_str):
    #     sql_stm = "select " + columns_str + " from " + table_name + " " + criteria_str
    #     try:
    #         self.__cursr.execute(sql_stm)
    #         result = self.__cursr.fetchall()
    #         print(result)
    #     except mysql.connector.Error as err:
    #         print('Cannot select from table {}'.format(err))
    #     finally:
    #         self.__conn.commit()

    # calls other methods to create table and insert values in that table
    def populate_table(self, table_name, table_schema, list_tuples):
        sql_stm = ""
        if table_name == 'corona_table':
            columns = len(list_tuples[0]) - 1
            print('-------', columns)
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


#  Testing

data_days = ['2021-03-18', '2021-03-17', '2021-03-16']

filename = "local_html/local_page2021-03-18.html"
html_file = FileIO(filename)
html_file.read_html_binary()
html_binary = html_file.get_data_file_result()
scr = ScrapeClass(html_binary)
scr.scrape_tables(data_days)
data_of_3_days = scr.get_lst_tuples()

dbs_obj = My_DB_SQL()
dbs_obj.connection_db(None)

# json_obj = FileIO('countries_json/country_neighbour_dist_file.json')
# json_obj.readJsonFile()
# json_obj.format_json_to_tuples()
# countries_tuples = json_obj.get_list_countries_tuples()
dbs_obj.populate_table('corona_table', schema.corona_table, data_of_3_days)
