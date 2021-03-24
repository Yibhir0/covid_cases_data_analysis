# Yassine Ibhir & David Pizzolongo
from bs4 import BeautifulSoup as bs

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

