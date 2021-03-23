from bs4 import BeautifulSoup as bs
from FileIO import FileIO
from WebRequestClass import WebRequestClass


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


# testing

# data_days = ['2021-03-19', '2021-03-18', '2021-03-18']
#
# filename = "local_html/local_page2021-03-19.html"
# html_file = FileIO(filename)
# html_file.read_html_binary()
# html_binary = html_file.get_data_file_result()
# scr = ScrapeClass(html_binary)
# scr.scrape_tables(data_days)
# data_of_3_days = scr.get_lst_tuples()
# print(data_of_3_days)

# The code below has to be in the driverClass
# file_name = "local_html/local_page2021-03-19.html"

# make request
# def url_request():
#     url = "https://www.worldometers.info/coronavirus/"
#     req = WebRequestClass(url)  # request to the web which will happen twice
#     html_bytes = req.get_html_binary()  # get_html bytes
#     return html_bytes
#
#
# def save_to_local(html_bits, filename):
#     html_file = FileIO(filename)
#     html_file.save_to_local_file(html_bits)

# this method will be used everytime we run the program
# def scrape_from_local_file(filename):
#     html_file = FileIO(filename)
#     html_file.read_html_binary()
#     html_binary = html_file.get_data_file_result()
#     return html_binary


#
#
# def scrape_all_tables(html_bytes,data_days):
#     scrape_obj = ScrapeClass(html_bytes)
#     table_list = scrape_obj.scrape_tables()
#     final_corona_data = scrape_obj.get_lst_tuples()
#     return final_corona_data


#
#
# # testing
# file_name = "local_html/local_page2021-03-21.html"
# # make a request
# html_file_content = url_request()
# # save to local file
# save_to_local(html_file_content, file_name)
# # # scrape from local file

# html_file_content = scrape_from_local_file(file_name)
#
# corona_data = scrape_all_tables(html_file_content, '2021-03-21', '2021-03-22', '2021-03-23')
# print(len(corona_data))
