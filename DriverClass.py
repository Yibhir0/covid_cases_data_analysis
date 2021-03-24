# Yassine Ibhir & David Pizzolongo

from datetime import date

import data_base_schema as schema

from Database_management import My_DB_SQL
from WebRequestClass import WebRequestClass
from FileIO import FileIO
from ScrapeClass import ScrapeClass

# make request
def url_request():
    url = "https://www.worldometers.info/coronavirus/"
    req = WebRequestClass(url)  # request to the web which will happen twice
    html_bytes = req.get_html_binary()  # get_html bytes
    return html_bytes

# save_to_local saves a local file containing the html bytes
def save_to_local(html_bits, filename):
    html_file = FileIO(filename)
    html_file.save_to_local_file(html_bits)

# this method will be used every time we scrape locally 
def scrape_from_local_file(filename):
    html_file = FileIO(filename)
    html_file.read_html_binary()
    html_binary = html_file.get_data_file_result()
    return html_binary

#This method will scrape 3-days worth of data from the provided html bytes
def scrape_all_tables(html_bytes, data_days):
    scrape_obj = ScrapeClass(html_bytes)
    scrape_obj.scrape_tables(data_days)
    final_corona_data = scrape_obj.get_lst_tuples()
    return final_corona_data

def save_web_file():
    today = str(date.today())
    fileName = 'local_html/local_page' + today + '.html'
    page_bytes = url_request()
    save_to_local(page_bytes, fileName)

def use_json():
    json_obj = FileIO('countries_json/country_neighbour_dist_file.json')
    json_obj.format_json_to_tuples(json_obj.readJsonFile())
    countries_tuples = json_obj.get_data_file_result()
    return countries_tuples

def write_to_DB(table, schema, list_clean_tuples):
    dbs_obj = My_DB_SQL()
    dbs_obj.connection_db(None)
    dbs_obj.populate_table(table, schema, list_clean_tuples)
 
if __name__ == "__main__":

    DATA_DAYS = ('2021-03-19', '2021-03-20', '2021-03-21')
    filename = "local_html/local_page2021-03-21.html"
    DATA_DAYS1 = ('2021-03-22', '2021-03-23', '2021-03-24')
    filename1 = "local_html/local_page2021-03-24.html"

    html_bytes = scrape_from_local_file(filename)
    clean_data_corona = scrape_all_tables(html_bytes, DATA_DAYS)

    html_bytes1 = scrape_from_local_file(filename1)
    clean_data_corona1 = scrape_all_tables(html_bytes, DATA_DAYS1)
    
    clean_data_country = use_json()
    
    schemaCorona = schema.corona_table
    write_to_DB('corona_table', schemaCorona, clean_data_corona)
    write_to_DB('corona_table', schemaCorona, clean_data_corona1)
    
    schemaCountry = schema.country_borders_table
    write_to_DB('country_borders_table', schemaCountry, clean_data_country)
    # save_web_file()