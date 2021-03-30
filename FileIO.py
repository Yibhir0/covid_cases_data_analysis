# Yassine Ibhir & David Pizzolongo
import json


class FileIO:

    # initializes all variables of the FileIO object to None, except for the filename
    def __init__(self, filename):
        self.__filename = filename
        self.__file_obj = None
        self.__data_file_result = None

    # This method reads from the provided json file and computes a list of countries and borders.
    def readJsonFile(self):

        try:
            self.__file_obj = open(self.__filename)
            self.__data_file_result = json.load(self.__file_obj)
        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()

    # format_json_to_tuples applies a format to the json dictionary data (countries, combined with borders and their distance)
    # and generates a list of tuples for the country_borders table.
    def format_json_to_tuples(self):
        countries_border = self.__data_file_result
        self.__data_file_result = []  # list of tuples
        for countries in countries_border:
            for country, borders in countries.items():
                for border, distance in borders.items():
                    tuples_borders = (country, border, distance)
                    self.__data_file_result.append(tuples_borders)

    # returns data_file_result which could be htmlBytes or countries_borders (list of tuples)
    def get_data_file_result(self):
        return self.__data_file_result

    # writes html bytes to a local file and prints a message if it is successful
    def save_to_local_file(self, html_bytes):
        try:
            self.__file_obj = open(self.__filename, 'wb')
            self.__file_obj.write(bytes(html_bytes))
            print(self.__filename, ' is saved into local_html..')

        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()

    # reads and stores local html file data in data_file_result
    def read_html_binary(self):
        try:
            self.__file_obj = open(self.__filename, 'rb')
            self.__data_file_result = self.__file_obj.read()
        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()
