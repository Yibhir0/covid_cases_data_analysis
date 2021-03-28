# Yassine Ibhir & David Pizzolongo
import datetime
from datetime import date

from Data_explore_analyse import explore_saved_data_main_program

from WebRequestClass import make_request_main_program

from ScrapeClass import clean_save_json, scrape_save_main_program


def main():
    # stores json data in database first
    clean_save_json()
    while True:
        choice = input("Enter your choice:\n"
                       "(S)  Scrape and save existing files in database?\n"
                       "(X): Explore and save data \n"
                       "(R): Make a request and save to local file \n"
                       "(E): Exit ? ")
        if choice.lower() == 's':
            scrape_save_main_program()
        elif choice.lower() == 'x':
            explore_saved_data_main_program()
        elif choice.lower() == 'r':
            make_request_main_program()
        elif choice.lower() == 'e':
            print('GoodBye')
            break
        else:
            print('Enter a valid choice.Try again...')


if __name__ == "__main__":
    main()
