# Yassine Ibhir & David Pizzolongo
from datetime import datetime as dt, timedelta as td

import pandas as pd
import matplotlib.pyplot as plt
from Database_management import My_DB_SQL as dbm
import data_base_schema as schema
import Global_variables as gv

from ScrapeClass import get_date_of_file

# This class is responsible for creating and plotting a dataframe that uses 
# the country the user provided and its farthest borders.  
class DataAnalysis:

    def __init__(self, query, conn):

        self.__df = pd.read_sql_query(query, conn)

        if not self.__df.empty:
            #sets labels for the x axis to be the dates
            self.__df.set_index(['date_cases'], inplace=True)

        self.__df_list = []  # This will contain a list of dataframes to merge and plot

    # This function plots the New Cases, New Deaths and New Recovered pertaining 
    # to the single country.
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

    # This method generates a list of dataframes matching every country in country_border
    # and sets the value to object list.
    def generate_list_df(self, country_border):
        for country in country_border:
            cond = self.__df['country_other'] == country
            out = self.__df[cond]
            self.__df_list.append(out)

    # returns the index of the first occurrence of a complete dataframe else -1.
    def __get_full_datFrame_index(self):

        for i in range(0, len(self.__df_list)):
            if not self.__df_list[i].empty:
                return i
            return -1

    
    # This method changes the column names and the values of the dataframe to be compatible with plotting.
    # It creates a dictionary with date_cases as indexes and a list of column entries as values for that day.
    # It also creates the columns of the new Data frame. It sets the value of the original dataframe to the new generated one.
    def reformat_df_list(self, borders, val):
        iDf = self.__get_full_datFrame_index()
        if iDf != -1:
            data_dict = {}
            colmns = []
            len_row = len(borders)
            #iterates over each row in the list
            for i, row in self.__df_list[0].iterrows():
                rows = []
                #for each border, gets the required information if it is not empty
                for j in range(0, len(borders)):
                    if not self.__df_list[j].empty:
                        #retrieves NewCases and Deaths/1M values at the index of the row
                        rows.append(self.__df_list[j].loc[i][val])
                        
                        #ensures that the column list has the same length as the number of rows,
                        #applies the format that appears in the legend
                        if len(colmns) < len_row:
                            colmns.append(val + '-' + borders[j])
                    else:
                        print('Sorry no Data found for----> ', borders[j])
                len_row = len(rows)
                data_dict.update({i: rows})
            # dataFrame to plot
            self.__df = pd.DataFrame.from_dict(data_dict, orient='index', columns=colmns)
        else:
            #country not found
            print('No Data available for ------>', borders)

    #plots the bar chart for DeathsPM, in comparison with at most 3 of its neighbors
    def plot_3days(self, country):
        if not self.__df.empty:
            self.__df.plot(kind='bar', width=0.3, rot=0)
            plt.title(f'3-Days Deaths/1M pop Comparison - {country} with 3 Neighbours')
            plt.xlabel("Date")
            plt.ylabel("Deaths 1/M pop")
            plt.show()

        else:
            print('Sorry No data found for plotting  ', country)

    #plots the bar chart for New Cases, in comparison with its most distanced neighbor
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

# main method that asks for the day and country to explore and plot the 3 graphs
def explore_saved_data_main_program():
    choice = input('Enter the name of the country you want to explore?')
    country = choice.capitalize()
    explore_6days_indicators(country)
    explore_6days_newCases_longest_neighbor(country)
    explore_3days_DeathsPm_longest_neighbors(country)


# gets the list of the country_borders with a set limit
def get_border_countries(country, limit):
    dbms = dbm()
    dbms.connection_db(schema.data_base_name)
    colBorder = 'border_country'
    table_borders = schema.country_borders_table_name
    criteria = ' where country_other = "' + country + '"   order by distance desc limit ' + str(limit) + ';'
    #gets list of tuples from the query
    country_border = dbms.get_country_borders(colBorder, table_borders, criteria)
    #computes a list of the borders (the item in each tuple result)
    countries = [item for bor in country_border for item in bor]
    countries.append(country)  # adds the chosen country to the list of border countries
    dbms.close_connection()
    return countries


# builds an SQL query that will represent the data in the Data Frame. The fields are 
# combined with a comma as separator and are selected from the corona_table, where the data
# matches the country or countries in question.
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


# This method first prepares the query and connection for the DataFrame object
# and then calls the plotting method for 6Days Indicators.
def explore_6days_indicators(country):
    columns_str = ['date_cases', 'NewCases', 'NewDeaths', 'NewRecovered']
    query = build_query(country, columns_str)
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    df.plot_6Days_3Indicators(country)
    dbs.close_connection()


# This method first prepares the query and connection for the DataAnalysis object
# and then calls the plotting method for NewCases indicator.
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

# This method calculates the first 3 days of the second file (March 22-24), gets
# the 3 longuest neighbors and then proceeds to plot the df representing the Deaths Per Million
# from these countries during the 3 days. 
def explore_3days_DeathsPm_longest_neighbors(country):
    dates = gv.HTML_FILES_LIST
    file1 = dates[0]
    #sets full date of the file to date1
    date1 = get_date_of_file(file1)
    date1 = dt.strptime(date1, '%Y-%m-%d')
    date1 = str(date1 + td(days=1))
    file2 = dates[1]
    date2 = get_date_of_file(file2)
    #gets longuest country borders (maximum 3) and the country itself
    borders = get_border_countries(country, 3)
    columns_str = ['date_cases', 'deathsPM', 'country_other']
    query = build_query(borders, columns_str)
    query = query + ' and date_cases between ' '"' + date1 + '"' + ' and ' '"' + date2 + '"'
    dbs = dbm()
    dbs.connection_db(schema.data_base_name)
    con = dbs.get_connection()
    df = DataAnalysis(query, con)
    #sets starting df list
    df.generate_list_df(borders)
    #sets final df with deathsPM numbers and plots it 
    df.reformat_df_list(borders, 'deathsPM')
    df.plot_3days(country)
    dbs.close_connection()
