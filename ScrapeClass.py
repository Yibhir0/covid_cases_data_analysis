# Yassine Ibhir & David Pizzolongo
from datetime import datetime as dt, timedelta as td
from bs4 import BeautifulSoup as bs
import Global_variables as gv
import data_base_schema as schema
from FileIO import FileIO
from Database_management import My_DB_SQL as dbm


class ScrapeClass:

    def __init__(self, binary_html):
        self.__binary_html = binary_html
        self.__bs_obj = bs(self.__binary_html, features='html.parser')
        self.__lst_unclean_stats = None
        self.__lst_clean_stats = None
        self.__combined_tables_clean_stats = []
        self.__lst_clean_tuples = []

    def scrape_tables(self, table_days):

        table_list = self.__bs_obj.find_all('table')

        for tableIndex in range(0, len(table_list)):
            self.__lst_unclean_stats = []
            day_table = table_list[tableIndex].find('tbody')
            day_rows = day_table.find_all('tr')

            # removes all rows with classes (the total_row_world row_continent)
            for trow in day_rows:
                if not trow.has_attr('class'):
                    self.__lst_unclean_stats.append(trow)
            self.__arrange_Stats(table_days[tableIndex])
            self.__combined_tables_clean_stats = self.__combined_tables_clean_stats + self.__lst_clean_stats

    def __arrange_Stats(self, day):
        self.__lst_clean_stats = []
        for row in self.__lst_unclean_stats:

            row_td_fields = [day]

            all_td_row = row.find_all('td')

            for td_field in all_td_row:
                td_text = td_field.text
                if len(td_text) == 0 or td_text == ' ' or td_text == "N/A":
                    td_text = None
                else:
                    td_text = td_text.replace(',', '')
                    td_text = td_text.replace('+', '')
                    # cast to the appropriate type
                    temp_text = None  # backup value in case an exception is thrown
                    try:
                        if td_text.find('.') > -1:
                            temp_text = td_text
                            td_text = float(td_text)
                        else:
                            temp_text = td_text
                            td_text = int(td_text)
                    except ValueError:
                        td_text = temp_text

                row_td_fields.append(td_text)

            self.__lst_clean_stats.append(row_td_fields)

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


# main method to scrape and save the html data of 3 days into database
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


# This method make up the 3 days and store the data accordingly
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


# This method will use  ScrapeClass to scrape 3-days worth
# of data from the provided html bytes.
def scrape_all_tables(html_bytes, three_days):
    scrape_obj = ScrapeClass(html_bytes)
    scrape_obj.scrape_tables(three_days)
    final_corona_data = scrape_obj.get_lst_tuples()
    return final_corona_data


# write_to_Db will use My_DB_SQL class to create and store data
def write_to_DB(table, dbSchema, list_clean_tuples):
    dbs_obj = dbm()
    dbs_obj.connection_db(schema.data_base_name)
    dbs_obj.populate_table(table, dbSchema, list_clean_tuples)
    dbs_obj.close_connection()


# checks if html file of a specific day exist and returns it
def get_file_to_scrape(day):
    for file in gv.HTML_FILES_LIST:
        startIndex = file.rfind("-") + 1
        endIndex = file.rfind(".")
        file_day = file[startIndex: endIndex]
        if file_day == day:
            return file
    return None


# use_json will get a list of data of the json file. This methods runs first.
def use_json():
    json_obj = FileIO(gv.JSON_DIRECTORY)
    json_obj.readJsonFile()
    json_obj.format_json_to_tuples()
    countries_tuples = json_obj.get_data_file_result()
    return countries_tuples
# ---------------------------------------------------------------end of scraping and saving methods
