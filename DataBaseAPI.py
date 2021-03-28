# Yassine Ibhir & David Pizzolongo

import Database_management 
import pandas as pd

class DataBaseAPI:
    def __init__(self, db_conn):    
        self.__db_conn = db_conn
        self.__list_query_tuples = [] 
        
    def fetch_query(self, query):

     
        
        