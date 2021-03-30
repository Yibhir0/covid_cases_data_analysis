import os

# Global variables: directory where new and old local html files are saved, listing of this directory,
# relative path of the json file and the URL that will be used to make the request.  
HTML_DIRECTORY = 'local_html/'
HTML_FILES_LIST = os.listdir(HTML_DIRECTORY)
JSON_DIRECTORY = 'countries_json/country_neighbour_dist_file.json'
URL = "https://www.worldometers.info/coronavirus/"
