from urllib.request import Request, urlopen


# request the page and stores the binary_html

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
            print('Can not get the request'.format(err))
        return self.__html_binary
