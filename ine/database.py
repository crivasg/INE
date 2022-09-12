'''database.py'''

import sqlite3
from sqlite3 import Error

def _get_database_filename():

    database_file = pathlib.Path(os.getenv('APPDATA'), 'ine','ine.sqlite3').resolve()
    #print(str(database_file),str(database_file.parent),sep='\n')
    if not database_file.parent.exists():
        database_file.parent.mkdir(exist_ok=True)

    return database_file 



'''

Reference:

    https://www.sqlitetutorial.net/sqlite-python/
'''
