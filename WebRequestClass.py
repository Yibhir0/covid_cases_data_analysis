# Yassine Ibhir & David Pizzolongo
from datetime import date
from urllib.request import Request, urlopen
import Global_variables as gv

# request the page and stores the binary_html
from FileIO import FileIO


class WebRequestClass:

    def __init__(self, url):
        self.__url = url
        self.__html_binary = None

    def get_html_binary(self):
        try:
            req = Request(self.__url, headers={'user-agent': 'Mozilla/5.0'})
            html_code = urlopen(req)
            self.__html_binary = html_code.read()
        except Exception as err:
            print('Can not get the request{}'.format(err))
        return self.__html_binary


# nested methods makes a request  and stores the html files locally.
def make_request_main_program():
    # make a request
    def url_request():
        req = WebRequestClass(gv.URL)  # request to the web which will happen twice
        html_bytes = req.get_html_binary()  # get_html bytes
        return html_bytes

    # save_to_local saves a local file containing the html bytes
    def save_to_local(html_bits):
        filename = gv.HTML_DIRECTORY + "local_page" + str(date.today()) + ".html"
        html_file = FileIO(filename)
        html_file.save_to_local_file(html_bits)

    html_code = url_request()
    save_to_local(html_code)
