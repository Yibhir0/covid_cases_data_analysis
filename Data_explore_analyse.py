# Yassine Ibhir & David Pizzolongo
from datetime import datetime as dt, timedelta as td

import pandas as pd
import matplotlib.pyplot as plt
from Database_management import My_DB_SQL as dbm
import data_base_schema as schema
import Global_variables as gv
import mysql.connector

from ScrapeClass import get_date_of_file


class DataAnalysis:

    def __init__(self, query, conn):

        self.__df = pd.read_sql_query(query, conn)

    # def plot 6 day indicators
    def plot_6Days_3Indicators(self, country):

        if not self.__df.empty:
            self.impute_null_values()
            self.__df.set_index('date_cases', inplace=True)
            ax = self.__df.plot(kind='bar', title='6-days indicators evolution of ' + country, figsize=(8, 6))
            ax.set_xlabel("date")
            ax.set_ylabel("3 main indicators")
            plt.xticks(rotation=0)
            plt.show()
        else:
            print('Sorry no data for ', country)

    def plot_6Days_newCases(self, country_and_borders):
        if not self.__df.empty:
            self.impute_null_values()
            self.__df.set_index(['date_cases'], inplace=True)
            cond1 = self.__df['country_other'] == country_and_borders[1]
            out1 = self.__df[cond1]
            print(out1)
            titlle = '6-days new cases comparison ' + country_and_borders[1] + " with neighbor " + country_and_borders[
                0]
            label1 = "new cases - " + country_and_borders[1]
            ax = out1.plot(kind='bar', title=titlle, figsize=(8, 6),
                           color='blue', width=0.4, rot=0)
            label2 = "new cases - " + country_and_borders[0]

            cond2 = self.__df['country_other'] == country_and_borders[0]
            out2 = self.__df[cond2]
            print(out2)
            out2.plot(kind='bar', ax=ax, width=0.2, color='red', linewidth=3, alpha=.5, rot=0)
            ax.legend([label1, label2])
            ax.set_xlabel("date")
            plt.show()


        else:
            print('Sorry no data for ', country_and_borders[len(country_and_borders) - 1])

    def impute_null_values(self):
        self.__df.fillna(100, inplace=True)

    def plot_3days_deathPM(self,country_and_borders):
        if not self.__df.empty:
            self.impute_null_values()
            self.__df.set_index(['date_cases'], inplace=True)
            cond1 = self.__df['country_other'] == country_and_borders[2]
            out1 = self.__df[cond1]
            print(out1)
            titlle = '3-days Deaths1MP comparison ' + country_and_borders[2] + " with 2 neighborS "
            label1 = "Deaths 1MP - " + country_and_borders[2]
            ax = out1.plot(kind='bar', title=titlle, figsize=(8, 6),
                           color='blue', width=0.4, rot=0)
            label2 = "Deaths 1MP - " + country_and_borders[1]

            cond2 = self.__df['country_other'] == country_and_borders[1]
            out2 = self.__df[cond2]
            print(out2)
            out2.plot(kind='bar', ax=ax, width=0.2, color='red', linewidth=3, alpha=.5, rot=0)

            label3 = "Deaths 1MP - " + country_and_borders[0]

            cond3 = self.__df['country_other'] == country_and_borders[0]
            out3 = self.__df[cond3]
            print(out3)
            out2.plot(kind='bar', ax=ax, width=0.1, color='green', linewidth=3, alpha=.5, rot=0)
            ax.legend([label1, label2,label3])
            ax.set_xlabel("date")
            plt.show()



# Module's methods for exploring and plotting

# main method to ask for the day and country to explore by plotting the 3 graphs
def explore_saved_data_main_program():
    choice = input('Enter the name of the country you want to explore?')
    country = choice.capitalize()
    explore_6days_indicators(country)
    explore_6days_newCases_farthest_neighbor(country)
    explore_3days_DeathsPm_2farthest_neighbors(country)


# get list of the country borders
def get_border_countries(country, limit):
    dbms = dbm()
    dbms.connection_db(schema.data_base_name)
    colBorder = 'border_country'
    table_borders = schema.country_borders_table_name
    criteria = ' where country_other = "' + country + '"   order by distance desc limit ' + str(limit) + ';'
    country_border = dbms.get_country_borders(colBorder, table_borders, criteria)
    dbms.close_connection()
    countries = [item for bor in country_border for item in bor]
    countries.append(country)  # add the chosen country to the list of border countries
    dbms.close_connection()
    return countries


# build a query that we will with Data Frame
def build_query(countries, columns_str):
    fields = ','.join(columns_str)
    query = None
    if type(countries) is list:
        countries = tuple(countries)
        query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other in {}'.format(
            countries)
    else:
        query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other = ' '"' + countries + '"' + ';'
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

def explore_6days_newCases_farthest_neighbor(country):
    country_and_borders = get_border_countries(country, 1)
    columns_str = ['date_cases', 'NewCases', 'country_other']
    query = build_query(country_and_borders, columns_str)
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.plot_6Days_newCases(country_and_borders)
    dbs.close_connection()


def explore_3days_DeathsPm_2farthest_neighbors(country):
    dates = gv.HTML_FILES_LIST
    file1 = dates[0]
    date1 = get_date_of_file(file1)
    date1 = dt.strptime(date1, '%Y-%m-%d')
    date1 = str(date1 + td(days = 1))
    file2 = dates[1]
    date2 = get_date_of_file(file2)
    borders = get_border_countries(country, 2)
    columns_str = ['date_cases', 'deathsPM', 'country_other']
    query = build_query(borders, columns_str)
    query = query + ' and date_cases between' '"' + date1 + '"' + ' and ' '"' + date2 + '"' + ';'
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.plot_3days_deathPM(borders)
