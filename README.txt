Using an OOP approach, this project consists of html request, scraping, file io, database and data analysis classes. It also contains files that hold global variables 
(url, directory listing of local_html and the location of the json file) and the database schemas for both tables. These files are saved in their
respective folders (local_html and countries_json). 

By running the DriverClass, the main method will ask the user for input to scrape, explore a country, make a request for the current day or exit. Based on this 
response, it will call the appropriate method (scrape_save_main_program(), explore_saved_data_main_program(), make_request_main_program()). 

The scrape_save_main_program method invokes a method to scrape both files (the first file provided by the user and the second file which is 3 days apart), and a method to 
and uses the write_to_DB method to create a connection and populate the tables of the database.
explore_saved_data_main_program() calls the three methods to plot each graph, while the make_request_main_program function instanciates an object of WebRequest, 
retrieves the html bytes and saves these bytes to a local file. 

Once the user enters 'E', the program terminates.
