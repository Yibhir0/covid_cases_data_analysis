# Yassine Ibhir & David Pizzolongo
from datetime import datetime as dt, timedelta as td
from bs4 import BeautifulSoup as bs
import Global_variables as gv
import data_base_schema as schema
from FileIO import FileIO
from Database_management import My_DB_SQL as dbm


# This class takes care of scraping all 3 days worth of table data from the html page,
# removes special characters, and casts the numbers to float or int.
class ScrapeClass:

    def __init__(self, binary_html):
        self.__binary_html = binary_html
        # makes a BeautifulSoup object
        self.__bs_obj = bs(self.__binary_html, features='html.parser')
        self.__lst_unclean_stats = None
        self.__lst_clean_stats = None
        self.__combined_tables_clean_stats = []
        self.__lst_clean_tuples = []

    # scrape_tables iterates over bs_obj, finds the table rows containing the statistics
    # and appends them to the list of unclean stats. This list is then cleaned for each day 
    # and is added to the final result, the combined_tables_clean_stats.
    def scrape_tables(self, table_days):

        table_list = self.__bs_obj.find_all('table')

        for tableIndex in range(0, len(table_list)):
            self.__lst_unclean_stats = []
            day_table = table_list[tableIndex].find('tbody')
            day_rows = day_table.find_all('tr')

            # excludes all rows with classes (the total_row_world row_continent)
            for trow in day_rows:
                if not trow.has_attr('class'):
                    self.__lst_unclean_stats.append(trow)
            self.__arrange_Stats(table_days[tableIndex])
            self.__combined_tables_clean_stats = self.__combined_tables_clean_stats + self.__lst_clean_stats

    # The arrange_Stats method adds data from the specific day to lst_clean_stats, by retrieving 
    # the text of every row, casting empty data to None, and converting the numbers to floats or ints.
    def __arrange_Stats(self, day):
        self.__lst_clean_stats = []
        for row in self.__lst_unclean_stats:

            row_td_fields = [day]

            all_td_row = row.find_all('td')

            for td_field in all_td_row:
                td_text = td_field.text
                # all possible empty values
                if len(td_text) == 0 or td_text == ' ' or td_text == "N/A":
                    td_text = None
                else:
                    td_text = td_text.replace(',', '')
                    td_text = td_text.replace('+', '')
                    # cast to the appropriate type
                    temp_text = None  # backup value in case an exception is thrown
                    try:
                        # only if number contains a decimal point, its type is casted to decimal
                        if td_text.find('.') > -1:
                            temp_text = td_text
                            td_text = float(td_text)
                        else:
                            temp_text = td_text
                            td_text = int(td_text)
                    except ValueError:
                        # text is a string
                        td_text = temp_text

                # appends the values of each row to their proper date
                row_td_fields.append(td_text)

            self.__lst_clean_stats.append(row_td_fields)

    # converts the inner lists of the combined tables data to tuples and 
    # returns lst_clean_tuples. 
    def get_lst_tuples(self):
        for lst_clean in self.__combined_tables_clean_stats:
            tup_clean = tuple(lst_clean)
            self.__lst_clean_tuples.append(tup_clean)

        return self.__lst_clean_tuples


# End of class

# Module's methods for scraping and saving to database

# clean and save json file data
def clean_save_json():
    country_borders = use_json()
    write_to_DB(schema.country_borders_table_name, schema.country_borders_keys, country_borders)


# This is the main function responsible of scraping and saving the html data of 3 days into the database.
# While validating user input, it gets the corresponding filename from the file system, gets the 
# second filename and calls prepare_three_days_and_store to scrape and format the table data. 
def scrape_save_main_program():
    file_name_to_scrape = None
    while not file_name_to_scrape:
        print('List of the available dates to scrape ,store and explore: ', gv.HTML_FILES_LIST)
        choice = input('Enter the day in digits (99) of the day to scrape and save in database (e.g o4 or 21):')
        file_name_to_scrape = get_file_to_scrape(choice)
        if file_name_to_scrape:
            prepare_three_days_and_store(file_name_to_scrape)
            second_file_to_scrape = find_other_file_name_to_scrape(file_name_to_scrape)
            if second_file_to_scrape:
                prepare_three_days_and_store(second_file_to_scrape)
            else:
                print('No file/other matches the requirements ')
        else:
            print('Not a valid day . Try again...')


# This method calculates and stores the 3 days in a tuple. It then invokes scrape_all_tables to 
# format the html data into a list of tuples and uses this list, along with the table name and schema,
# to create and populate a new table in the database.  
def prepare_three_days_and_store(file_name_to_scrape):
    file_date = get_date_of_file(file_name_to_scrape)
    today = dt.strptime(file_date, '%Y-%m-%d')
    yesterday = today - td(days=1)
    yesterday2 = yesterday - td(days=1)
    three_days = (today, yesterday, yesterday2)
    # Storing the data of local html file in database
    htmlBinaries = get_html_local_binary(gv.HTML_DIRECTORY + file_name_to_scrape)
    corona_data = scrape_all_tables(htmlBinaries, three_days)
    write_to_DB(schema.corona_table_name, schema.corona_table_keys, corona_data)


# finds name of the second file to scrape
def find_other_file_name_to_scrape(file_name_to_scrape):
    file_date_str = get_date_of_file(file_name_to_scrape)
    file_date = dt.strptime(file_date_str, '%Y-%m-%d')
    possibility1 = str(file_date - td(days=3))
    possibility2 = str(file_date + td(days=3))

    filename_str1 = "local_page" + possibility1[0:10] + ".html"  # remove timestamp and concatenate
    filename_str2 = "local_page" + possibility2[0:10] + ".html"

    if filename_str1 in gv.HTML_FILES_LIST:
        return filename_str1
    elif filename_str2 in gv.HTML_FILES_LIST:
        return filename_str2


# returns date of html file in str (2021-03-21)
def get_date_of_file(file_name):
    startIndex = file_name.rfind("e") + 1
    endIndex = file_name.rfind(".")
    file_day = file_name[startIndex: endIndex]
    return file_day


# This method will be used every time we scrape locally. It returns html bytes.
def get_html_local_binary(filename):
    html_file = FileIO(filename)
    html_file.read_html_binary()
    html_binary = html_file.get_data_file_result()
    return html_binary


# This method will use ScrapeClass to scrape 3-days worth
# of data from the provided html bytes.
def scrape_all_tables(html_bytes, three_days):
    scrape_obj = ScrapeClass(html_bytes)
    scrape_obj.scrape_tables(three_days)
    final_corona_data = scrape_obj.get_lst_tuples()
    return final_corona_data


# write_to_DB uses an object of the My_DB_SQL class to establish a connection with a new database,
# store the clean data into a table and close the connection once everything is committed.
def write_to_DB(table, dbSchema, list_clean_tuples):
    dbs_obj = dbm()
    dbs_obj.connection_db(schema.data_base_name)
    dbs_obj.populate_table(table, dbSchema, list_clean_tuples)
    dbs_obj.close_connection()


# This method verifies if the html file of a specific day exists in the current list of saved files
# and if so returns it.
def get_file_to_scrape(day):
    for file in gv.HTML_FILES_LIST:
        startIndex = file.rfind("-") + 1
        endIndex = file.rfind(".")
        # removes the month and year portions of the date
        file_day = file[startIndex: endIndex]
        if file_day == day:
            return file
    return None


# use_json gets a list of data from the json file, that is formatted 
# in accordance with its table in the database. Invoked by clean_save_json,
# this method is run first as part of the main program. 
def use_json():
    json_obj = FileIO(gv.JSON_DIRECTORY)
    json_obj.readJsonFile()
    json_obj.format_json_to_tuples()
    countries_tuples = json_obj.get_data_file_result()
    return countries_tuples
# ---------------------------------------------------------------end of scraping and saving methods
