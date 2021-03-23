# Yassine Ibhir & David Pizzolongo
import json


class FileIO:

    # initialize all variables of the FileIO object
    def __init__(self, filename):
        self.__filename = filename
        self.__file_obj = None
        self.__data_file_result = None

    # method reads from json file and returns a list of countries and borders
    def readJsonFile(self):
        countries_border = []
        try:
            self.__file_obj = open(self.__filename)
            countries_border = json.load(self.__file_obj)
        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()
        return countries_border

    # format json file data (countries and borders) to list of tuples
    def format_json_to_tuples(self, countries_border):
        self.__data_file_result = []  # list of tuples
        for countries in countries_border:
            for country, borders in countries.items():
                for border, distance in borders.items():
                    tuples_borders = (country, border, distance)
                    self.self.__data_file_result.append(tuples_borders)

    # returns data_file_result which could be htmlBytes or countries_borders (list of tuple)
    def get_data_file_result(self):
        return self.__data_file_result

    # writes html bytes to a local file
    def save_to_local_file(self, html_bytes):
        try:
            self.__file_obj = open(self.__filename, 'wb')
            self.__file_obj.write(bytes(html_bytes))

        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()

    # reads and stores local html file data
    def read_html_binary(self):
        try:
            self.__file_obj = open(self.__filename, 'rb')
            self.__data_file_result = self.__file_obj.read()
        except IOError:
            print('file process problem...')
        finally:
            self.__file_obj.close()
