# Yassine Ibhir & David Pizzolongo
from datetime import datetime as dt, timedelta as td

import pandas as pd
import matplotlib.pyplot as plt
from Database_management import My_DB_SQL as dbm
import data_base_schema as schema
import Global_variables as gv

from ScrapeClass import get_date_of_file


class DataAnalysis:

    def __init__(self, query, conn):

        self.__df = pd.read_sql_query(query, conn)

        if not self.__df.empty:
            self.__df.set_index(['date_cases'], inplace=True)

        self.__df_list = []  # This will contain a list of dataframes to merge and plot

    # def plot 6 day indicators
    def plot_6Days_3Indicators(self, country):

        if not self.__df.empty:
            if not self.__df.empty:
                self.__df.plot(kind='bar', width=0.4, rot=0)
                plt.title(f'6-Days 3 Key Indicators Evolution - {country}')
                plt.xlabel("Date")
                plt.ylabel("New cases")
                plt.show()
            else:
                print('Sorry No data found for plotting  ', country)

    # This method generates a list of dataframes and sets the value to object list
    def generate_list_df(self, country_border):
        for country in country_border:
            cond = self.__df['country_other'] == country
            out = self.__df[cond]
            self.__df_list.append(out)

    # returns the index of first occurrence of a full dataframe else -1
    def __get_full_datFrame_index(self):

        for i in range(0, len(self.__df_list)):
            if not self.__df_list[i].empty:
                return i
            return -1

    '''
    This method changes the column names and the values of the dataframe to be compatible with plotting.
    It creates a dictionary with date_cases as indexes and a list of column entries as values for that day
    it also creates the columns of the new Data frame.It sets the value of the original dataframe to the new generated one.
    '''

    def reformat_df_list(self, borders, val):
        iDf = self.__get_full_datFrame_index()
        if iDf != -1:
            data_dict = {}
            colmns = []
            len_row = len(borders)
            for i, row in self.__df_list[0].iterrows():
                rows = []
                for j in range(0, len(borders)):
                    if not self.__df_list[j].empty:
                        rows.append(self.__df_list[j].loc[i][val])
                        if len(colmns) < len_row:
                            colmns.append(val + '-' + borders[j])
                    else:
                        print('Sorry no Data found for----> ', borders[j])
                len_row = len(rows)
                data_dict.update({i: rows})
            # dataFrame to plot
            self.__df = pd.DataFrame.from_dict(data_dict, orient='index', columns=colmns)
        else:
            print('No Data available for ------>', borders)

    def plot_3days(self, country):
        if not self.__df.empty:
            self.__df.plot(kind='bar', width=0.3, rot=0)
            plt.title(f'3-Days Deaths/1M pop Comparison - {country} with 3 Neighbours')
            plt.xlabel("Date")
            plt.ylabel("Deaths 1/M pop")
            plt.show()

        else:
            print('Sorry No data found for plotting  ', country)

    def plot_6days(self, country):
        if not self.__df.empty:

            self.__df.plot(kind='bar', width=0.3, rot=0)
            plt.title(f'6-Days New Cases Comparison - {country} with longest border Neighbor')
            plt.xlabel("Date")
            plt.ylabel("New cases")
            plt.show()

        else:
            print('Sorry No data found for plotting', country)


# Module's methods for exploring and plotting

# main method to ask for the day and country to explore by plotting the 3 graphs
def explore_saved_data_main_program():
    choice = input('Enter the name of the country you want to explore?')
    country = choice.capitalize()
    explore_6days_indicators(country)
    explore_6days_newCases_longest_neighbor(country)
    explore_3days_DeathsPm_longest_neighbors(country)


# get list of the country borders
def get_border_countries(country, limit):
    dbms = dbm()
    dbms.connection_db(schema.data_base_name)
    colBorder = 'border_country'
    table_borders = schema.country_borders_table_name
    criteria = ' where country_other = "' + country + '"   order by distance desc limit ' + str(limit) + ';'
    country_border = dbms.get_country_borders(colBorder, table_borders, criteria)
    countries = [item for bor in country_border for item in bor]
    countries.append(country)  # add the chosen country to the list of border countries
    dbms.close_connection()
    return countries


# build a query that we will with Data Frame
def build_query(countries, columns_str):
    fields = ','.join(columns_str)
    query = ''
    if type(countries) is list:
        if len(countries) > 1:
            countries = tuple(countries)
            query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other in {} '.format(
                countries)
        else:
            query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other = ' '"' + \
                    countries[0] + '"'
    else:
        query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other = ' '"' + countries + '"'
    return query


# this method first prepares the query and connection for dataFrame Object
# and then calls the plotting method for 6Days Indicators

def explore_6days_indicators(country):
    columns_str = ['date_cases', 'NewCases', 'NewDeaths', 'NewRecovered']
    query = build_query(country, columns_str)
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.plot_6Days_3Indicators(country)
    dbs.close_connection()


# this method first prepares the query and connection for dataFrame Object
# and then calls the plotting method for NewCases indicator

def explore_6days_newCases_longest_neighbor(country):
    country_and_borders = get_border_countries(country, 1)
    columns_str = ['date_cases', 'NewCases', 'country_other']
    query = build_query(country_and_borders, columns_str)
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.generate_list_df(country_and_borders)
    df.reformat_df_list(country_and_borders, 'NewCases')
    df.plot_6days(country)
    dbs.close_connection()


def explore_3days_DeathsPm_longest_neighbors(country):
    dates = gv.HTML_FILES_LIST
    file1 = dates[0]
    date1 = get_date_of_file(file1)
    date1 = dt.strptime(date1, '%Y-%m-%d')
    date1 = str(date1 + td(days=1))
    file2 = dates[1]
    date2 = get_date_of_file(file2)
    borders = get_border_countries(country, 3)
    columns_str = ['date_cases', 'deathsPM', 'country_other']
    query = build_query(borders, columns_str)
    query = query + ' and date_cases between ' '"' + date1 + '"' + ' and ' '"' + date2 + '"'
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.generate_list_df(borders)
    df.reformat_df_list(borders, 'deathsPM')
    df.plot_3days(country)
    dbs.close_connection()

# def plot_6Days_newCases(self, country_and_borders):
#
#     if not self.__df.empty:
#
#         if len(country_and_borders) < 2:
#             print(country_and_borders[len(country_and_borders) - 1], ' has no neighbours.........')
#         ax = None
#         labels = []
#
#         # self.__df.set_index(['date_cases'], inplace=True)
#         cond1 = self.__df['country_other'] == country_and_borders[len(country_and_borders) - 1]
#         out1 = self.__df[cond1]
#         if not out1.empty:
#             titlle = '6-days new cases comparison ' + country_and_borders[
#                 len(country_and_borders) - 1] + " with neighbor " + \
#                      country_and_borders[
#                          0]
#             labels.append("new cases - " + country_and_borders[len(country_and_borders) - 1])
#             ax = out1.plot(kind='bar', title=titlle, figsize=(8, 6),
#                            color='blue', width=0.3, rot=0)
#
#         else:
#             print('Sorry no data for ', country_and_borders[len(country_and_borders) - 2])
#
#         if len(country_and_borders) > 1:
#             cond2 = self.__df['country_other'] == country_and_borders[len(country_and_borders) - 2]
#             out2 = self.__df[cond2]
#             if not out2.empty:
#                 out2.plot(kind='bar', ax=ax, width=0.2, color='red', linewidth=3, alpha=.5, rot=0)
#                 labels.append("new cases - " + country_and_borders[len(country_and_borders) - 2])
#             else:
#                 print('Sorry no data for ', country_and_borders[len(country_and_borders) - 2])
#         if ax is not None:
#             ax.legend(labels)
#             ax.set_xlabel("date")
#             plt.show()
#     else:
#         print('Sorry no data for ', country_and_borders[len(country_and_borders) - 1])
#
# def plot_3days_deathPM(self, country_and_borders):
#
#     if not self.__df.empty:
#         print(self.__df)
#         if len(country_and_borders) < 2:
#             print(country_and_borders[len(country_and_borders) - 1], ' has no neighbours.........')
#         ax = None
#         labels = []
#
#         self.__df.set_index(['date_cases'], inplace=True)
#         cond1 = self.__df['country_other'] == country_and_borders[len(country_and_borders) - 1]
#         out1 = self.__df[cond1]
#
#         if not out1.empty:
#             titlle = '3-days DeathsPM comparison ' + country_and_borders[
#                 len(country_and_borders) - 1] + " with 2 neighbors "
#             labels.append("DeathsPM - " + country_and_borders[len(country_and_borders) - 1])
#             ax = out1.plot(kind='bar', title=titlle, figsize=(8, 6),
#                            color='blue', width=0.3, rot=0)
#
#         else:
#             print('Sorry no data for ', country_and_borders[len(country_and_borders) - 1])
#
#         if len(country_and_borders) > 1:
#             cond2 = self.__df['country_other'] == country_and_borders[len(country_and_borders) - 2]
#             out2 = self.__df[cond2]
#             if not out2.empty:
#                 out2.plot(kind='bar', ax=ax, width=0.2, color='red', linewidth=3, alpha=.5, rot=0)
#                 labels.append("DeathsPM - " + country_and_borders[len(country_and_borders) - 2])
#             else:
#                 print('Sorry no data for ', country_and_borders[len(country_and_borders) - 2])
#
#         if len(country_and_borders) > 2:
#             cond3 = self.__df['country_other'] == country_and_borders[len(country_and_borders) - 3]
#             out3 = self.__df[cond3]
#             if not out3.empty:
#                 out3.plot(kind='bar', ax=ax, width=0.1, color='green', linewidth=3, alpha=.5, rot=0)
#                 labels.append("DeathsPM - " + country_and_borders[len(country_and_borders) - 3])
#             else:
#                 print('Sorry no data for ', country_and_borders[len(country_and_borders) - 3])
#
#         if ax is not None:
#             ax.legend(labels)
#             ax.set_xlabel("date")
#             plt.show()
#     else:
#         print('Sorry no data for ', country_and_borders[len(country_and_borders) - 1])
