# Yassine Ibhir & David Pizzolongo

import pandas as pd
import matplotlib.pyplot as plt
from Database_management import My_DB_SQL as dbm
import data_base_schema as schema
import mysql.connector


class DataAnalysis:

    def __init__(self, query, conn):

        self.__df = pd.read_sql_query(query, conn)


    # def plot 6 day indicators
    def plot_6Days_3Indicators(self, country):
        if not self.__df.empty:
            self.__df.set_index('date_cases', inplace=True)
            ax = self.__df.plot(kind='bar', title='6-days indicators evolution of ' + country, figsize=(8, 6))
            ax.set_xlabel("date")
            ax.set_ylabel("3 main indicators")
            plt.xticks(rotation=0)
            plt.show()
        else:
            print('Sorry no data for ', country)


# Module's methods for exploring and plotting

# main method to ask for the day and country to explore by plotting the 3 graphs
def explore_saved_data_main_program():
    choice = input('Enter the name of the country you want to explore?')
    country = choice.capitalize()
    explore_6days_indicators(country)


# get list of the country borders
def get_border_countries(country, limit):
    dbms = dbm()
    dbms.connection_db('covid_corona_db_dp_yi')
    col = 'border_country'
    table_borders = 'country_borders_table'
    criteria = ' where country_other = "' + country + '"   order by distance desc limit ' + str(limit) + ';'
    country_border = dbms.get_country_borders(col, table_borders, criteria)
    dbms.close_connection()
    countries = [item for bor in country_border for item in bor]
    countries.append(country)  # add the chosen country to the list of border countries
    dbms.close_connection()
    return countries


# build a query that we will with Data Frame
def build_query(countries, columns_str):
    fields = ','.join(columns_str)
    query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other = ' '"' + countries + '"' + ';'
    if type(countries) is list:
        countries = tuple(countries)
        query = 'select ' + fields + ' from ' + schema.corona_table_name + ' where country_other in {};'.format(
            countries)

    return query


# this method first prepares the query and connection for dataFrame Object
# and then calls the plotting method for 6Days Indicators
def explore_6days_indicators(country):
    # borders = get_border_countries(country)
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
# def explore_6days_newCases_farthest_neighbor(country):
#     borders = get_border_countries(country, 1)
#     columns_str = ['date_cases', 'NewCases', 'country_other']
#     query = build_query(borders, columns_str)
#     dbs = dbm()
#     dbs.connection_db(schema.data_base_name)
#     con = dbs.get_connection()
#     df = DataAnalysis(query, con)
#     # df.plot_6Days_3Indicators()
#     dbs.close_connection()
#
#
# def explore_3days_DeathsPm_2farthest_neighbors(country, first_day):
#     datetime.now() + datetime.timedelta(days=1)
#     last_day = first_day + 2
#     borders = get_border_countries(country, 2)
#     columns_str = ['date_cases', 'deathsPM', 'country_other']
#     query = build_query(borders, columns_str)
#     query += query + ' and date_cases between  {} and {};'.format(first_day, last_day)
#     dbs = dbm()
#     dbs.connection_db(schema.data_base_name)
#     con = dbs.get_connection()
#     df = DataAnalysis(query, con)
