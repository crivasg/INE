''' data.py'''

import time
import datetime
import io
import pathlib
import os
import re
import sys
import zipfile

import sqlite3
from sqlite3 import Error

def _is_int(element) -> bool:
    try:
        int(element)
        return True
    except ValueError:
        return False

def _is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def _get_column_width(data):

    column_width = []
    for line in list(zip(*data)):
        column_width.append(max([ len(str(i)) for i in line ]))

    #print(column_width)
    return column_width

def _print_data(headers, data, column_width):

    #print(*column_width)
    sepa_str = ''
    for w in column_width:
        sepa='-'*w
        sepa_str+=f'+-{sepa:^{w}}-'
    sepa_str+='+'
    
    output_str=''
    if headers:
        output_str+=f'{sepa_str}\n'
        for item,w in zip(headers,column_width):
            output_str+=f'| {item:^{w}} '
        output_str+='|\n'

    output_str+=f'{sepa_str}\n'
    for line in data:
        for item,w in zip(line,column_width):

            is_integer = _is_int(item)
            if is_integer:
                item = int(item)
                output_str+=f'| {item:>{w}} '
            else:
                output_str+=f'| {item:<{w}} '
        output_str+='|\n'
    output_str+=f'{sepa_str}'

    print(output_str)
    
    


def _get_database_filename():
    '''returns the defined name of the database'''

    database_file = pathlib.Path(os.getenv('APPDATA'), 'ine','ine.sqlite3').resolve()
    #print(str(database_file),str(database_file.parent),sep='\n')
    if not database_file.parent.exists():
        database_file.parent.mkdir(exist_ok=True)

    return database_file

def _create_connection(database_filename = ':memory:'):
    """
    creates a database connection to a SQLite database
"""
    conn = None
    try:
        conn = sqlite3.connect(database_filename)
        #print('version',sqlite3.version, sep=' = ')
        #print('sqlite_version',sqlite3.sqlite_version, sep=' = ')
        
    except Error as e:
        print('error',e, file=sys.stderr)

    return conn

def _create_table_in_database(conn, table_name, column_data):

    stmt_str = [ f'CREATE TABLE IF NOT EXISTS {table_name} (']
    for column_name, column_type in column_data:
        stmt_str.append(f'\t{column_name} {column_type},')

    stmt_str='\n'.join(stmt_str)[:-1]+f'\n)'
    #print(stmt_str)

    conn.execute(stmt_str)
    conn.commit()

    conn.execute(f'DELETE FROM {table_name}')
    conn.commit()

def _insert_rows_to_database(conn, table_name, data):

    cursor = conn.cursor()
    cur = cursor.execute(f'SELECT * FROM {table_name}')
    columns_name = []
    
    for description in cur.description:
        columns_name.append(description[0])

    num_columns = len(columns_name)
    values_str = [ '?' ]*num_columns
    
    columns_name = ','.join(columns_name)
    values_str = ','.join(values_str)

    #print('-->', num_columns)
    #print('-->', len(data))

    conn.executemany(f'INSERT INTO {table_name}({columns_name}) VALUES ({values_str})',data)
    conn.commit()

    

def _process_entities_data(zip_filename,filename):
    ''' opens the zip file and extracts the contents of the file 'filename' without extracting the
file to the harddrive. extracts the separator character, then extracts the headers and finally the
entity data.
creates the sqlite statement string for the entity table
'''

    #print('*'*10,os.getenv('VIRTUAL_ENV'))
    
    if not zipfile.is_zipfile(zip_filename):
        print(f'ERROR: File is not a zip file', file=sys.stderr)
        return -1

    data = []
    with zipfile.ZipFile(zip_filename, mode='r') as archive:
        with archive.open(filename, mode="r") as fin:
            for line in io.TextIOWrapper(fin,encoding='latin-1'):
                data.append(line.strip())

    # get the separator character
    sepa_char = ','
    sepa_data = [ line.strip().split('=') for line in data if line.lower().startswith('sep=') ]
    for sepa_item in sepa_data:
        if len(sepa_item) > 2:
            sepa_char = sepa_item[1].strip()
    
    # get headers
    headers = [ line.strip().split(sepa_char) for line in data if re.match('^[A-Za-z]',line) and
                     not line.lower().startswith('sep=') ][0]
    #print('->',headers)

    # get the entities data. starts with an integer, the entity id (state id)
    entity_data = [ line.strip().split(sepa_char) for line in data if re.match('^[0-9]',line) ]
    output_data = []
    for item in entity_data:
        id_entity, entity_name, federal_entity_id, federal_entity_name, section, unit, seat = item
        id_entity = int(id_entity)
        federal_entity_id = int(federal_entity_id)
        section = int(section)
        unit = int(unit)
        ##print(id_entity, entity_name, federal_entity_id, federal_entity_name, section, unit, seat, sep=';')
        output_data.append((id_entity, entity_name.title(), federal_entity_id,
                            federal_entity_name.title(), section, unit, seat))

    #print('-->',len(output_data))
    #for line_data in output_data[12299:12349]:
    #   print(line_data)

    row0 = entity_data[0]
    # create the create table and insert the data.
    #table_columns = []
    #stmt_str = [ 'CREATE TABLE IF NOT EXISTS entities (\n' ]
    entity_headers = []
    for table_item,item in zip(headers,row0):
        tmp = table_item.lower().replace(' ','_')
        column_type = 'STRING'
        if item.isnumeric():
            column_type = 'INTEGER'
        entity_headers.append([tmp,column_type])

    #stmt_str = ''.join(stmt_str).strip()[:-1]+'\n)'
    #stmt_str.append(')')
    #stmt_str = ''.join(stmt_str)
    #stmt_str = stmt_str.replace(', )',')')

    #print(stmt_str)
    #print(entity_headers)
    return [ entity_headers, output_data]
    
    

def _process_votes_data(zip_filename,filename):
    '''
'''
    if not zipfile.is_zipfile(zip_filename):
        print(f'ERROR: File is not a zip file', file=sys.stderr)
        return -1

    data = []
    with zipfile.ZipFile(zip_filename, mode='r') as archive:
        with archive.open(filename, mode="r") as fin:
            for line in io.TextIOWrapper(fin,encoding='latin-1'):
                data.append(line.strip())


    # get the index of the division between the 1st and 2nd section. split the data into 2 lists
    indeces = [ i for i, line in enumerate(data) if len(line.strip())==0 ]
    index = indeces[0]
    data1 = data[0:index]
    data2 = data[index+1:]

    # get the separator character
    sepa_char = ','
    sepa_data = [ line.strip().split('=') for line in data1 if line.lower().startswith('sep=') ]
    for sepa_item in sepa_data:
        if len(sepa_item) > 2:
            sepa_char = sepa_item[1].strip()

    #print(f'\n\n{sepa_char = }')
    #print(f'\n\n{indeces = } -> {index}')

    title_str = data1[1].strip()
    datatime_str = data1[2].strip()
    datatime_format = '%d/%m/%Y %H:%M (%Z)'
    headers1_lst = data1[3].strip().split(sepa_char)

    '''fix the data since the INE uses a formula to show the percentaje as a string
    example, ="100.0000" '''
    data1_str = data1[4].strip()
    data1_str = data1_str.replace('=','')
    data1_str = data1_str.replace('"','')
    data1_str = data1_str.split(sepa_char)

    #print(f'{title_str = }')
    #print(f'{datatime_str = }')
    #print(f'{datetime_object = }')
    #print(f'{headers1_lst = }')
    #print(f'{data1_str = }')

    '''get the summary columns and type and store them in the variable "summary_columns". Also,
store the summary values and store them in the list "summary_data"'''
    summary_columns = []
    summary_data = []
    summary_temp = []
    
    summary_columns.append(['title','STRING'])
    summary_columns.append(['date_time','STRING'])

    summary_temp.append(title_str)
    summary_temp.append(datatime_str)
    
    for table_item,item in zip(headers1_lst,data1_str):
        tmp = table_item.lower().replace(' ','_')
        column_type = 'INTEGER'
        if '.' in item:
            column_type = 'REAL'
        summary_columns.append([tmp,column_type])
        summary_temp.append(item)

    summary_data.append(tuple(summary_temp))
    
    # print out
    #print('-'*120,'-'*120,sep='\n')
    #for item in summary_columns:
    #    print('->',item)
    #for item in summary_data:
    #   print('>>',item)
    #print('-'*120,'-'*120,sep='\n')

    '''process the vote headers
    get the votes headers and thier SQL types (STRING, INTEGER). Then process the vote data
    for each section/entity/state.
'''
    tmp_headers = [ i.lower().replace(' ','_') for i in data2[0].split(sepa_char) ]
    vote_headers = []
    search_str = '^(id_|total_|lista_|nulos|que_|secc|ext_)'
    integer_indeces = []
    
    for column in tmp_headers:
        column_type = 'STRING'
        tmp = column.replace('á','a').replace('é','e').replace('í','i')
        tmp = tmp.replace('ó','o').replace('ú','u').replace('ü','u')
        result = re.search(search_str, tmp)
        is_integer = 0
        if result:
            column_type = 'INTEGER'
            is_integer = 1
        vote_headers.append([tmp,column_type])
        integer_indeces.append(is_integer)
    
    #print('-'*120,'-'*120,sep='\n')
    #for item in vote_headers:
    #    print('->',item)
    #print('-'*120,'-'*120,sep='\n')

    '''process the vote date'''
    vote_data = data2[1:]
    output_data = []
    for vote_item in vote_data:
        tmp = vote_item.replace('\'','')
        output_data.append(tuple(tmp.split(sepa_char)))

    #for item in output_data[0:5]:
    #   print(item)

    #print(integer_indeces)

    return [ summary_columns, summary_data, vote_headers, output_data ]
    

def read_and_store_data(zip_filename):
    ''' read and store the INE data into a SQLite database
'''

    entities = {}
    data = []
    print('-'*120)

    entities_file = None
    votes_file = None

    if not zipfile.is_zipfile(zip_filename):
        print(f'ERROR: File is not a zip file', file=sys.stderr)
        return -1

    # get the files from the zip file. two files are needed, the one with the entities
    # and the one with the vote counte.
    filenames = []
    with zipfile.ZipFile(zip_filename, mode='r') as archive:
        for info in archive.infolist():
            # skip the folders
            if info.filename.endswith('/') or info.filename.lower().endswith('.txt'):
                continue
            if not info.filename.lower().endswith('.csv'):
                continue

            if '_UNIDADES_' in info.filename:
                entities_file = info.filename
            if '_COMPUTOS_' in info.filename:
                votes_file = info.filename

            print(f"Filename: {info.filename}")
            print(f"Modified: {datetime.datetime(*info.date_time)}")
            print(f"Normal size: {info.file_size} bytes")
            print(f"Compressed size: {info.compress_size} bytes")
            print(f"Compress Ratio: {100.0*info.compress_size/info.file_size:.2f}%")
            print('-'*120)

    '''Check is the files are inside the zip file. The files needed are:
entities files --> CATALOGO_UNIDADES_TERRITORIALES_RM2022
votes files --> 20220411_1845_COMPUTOS_RM2022'''
    if not entities_file:
        print('The entities files doesn\'t exist',file=sys.stderr)
        return -1
    if not votes_file:
        print('The votes files doesn\'t exist',file=sys.stderr)
        return -2
            

    entity_headers, entity_data = _process_entities_data(zip_filename=zip_filename,
                                                         filename=entities_file)

    #print(entity_headers)
    #for entity_item in entity_data[1000:1002]:
    #   print(entity_item)
    
    summary_columns, summary_data, vote_headers, output_data = _process_votes_data(zip_filename=zip_filename,
                                                                                   filename=votes_file)

    #print(summary_columns)
    #for item in summary_data:
    #   print('->','|'.join(item))

    #print(vote_headers)
    #for item in output_data[1000:1006]:
    #   print('->','|'.join(item))


    '''create the database and drop all the data if exist any
Add the entity, summary and vote data to the database'''
    database_filename = 'C:/Temp/read_and_store_data.db'
    conn = _create_connection(database_filename)
    if conn:

        # add the entity data to the database
        _create_table_in_database(conn, 'entity', entity_headers)
        _insert_rows_to_database(conn, 'entity', entity_data)

        # add the summary data to the database
        _create_table_in_database(conn, 'summary', summary_columns)
        _insert_rows_to_database(conn, 'summary', summary_data)

        #add the vote data to the database
        _create_table_in_database(conn, 'vote', vote_headers)
        _insert_rows_to_database(conn, 'vote', output_data)
        
        conn.close()


def print_summary_data():

    database_filename = 'C:/Temp/read_and_store_data.db'
    summary_data = []

    if not os.path.exists(database_filename):
        basename = os.path.basename(database_filename)
        print(f'ERROR: database file \'{basename}\' doesn\'t exist', file=sys.stderr)
        return;
        
    conn = _create_connection(database_filename)
    if conn:
        # do some SQLite queries and print output
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM summary')
        r = cur.fetchone()
        #headers = r.keys()

        # get the width of the columns
        #w1 = max([ len(i) for i in r.keys() ])
        #w2 = max([ len(str(i)) for i in tuple(r) ])
        #print(f'{w1 = }\n{w2 = }')
        #

        #separator = '+-'+'-'*w1+'-+-'+'-'*w2+'-+'
        #print('')
        #print(separator)
        for key in r.keys():
            key1 = key.title().replace('_',' ')
            value = r[key]
            if 'porcentaje' in key:
                value = str(value) + '%'
            elif 'acta' in key or 'lista' in key or 'total' in key:
                value = f'{value:,}'
            #print(f'| {key1:{w1}} | {value:>{w2}} |')
            summary_data.append([key1,value])
        #print(separator)
        #print('')

        ##_print_data([ str(i) for i in r.keys() ],[ str(i) for i in tuple(r) ],[w1,w2]

        conn.close()

    column_width= _get_column_width(summary_data)
    _print_data(headers=None,
                data= summary_data,
                column_width=column_width)
        

def print_state_summary():

    stmt_str = 'SELECT id_entidad, entidad, SUM(que_se_le_revoque_el_mandato_por_perdida_de_la_confianza) AS en_contra, SUM(que_siga_en_la_presidencia_de_la_republica) AS a_favor, SUM(nulos) as votos_nulos FROM vote GROUP BY id_entidad ORDER BY a_favor DESC'
    width_list = []
    headers = []
    summary_data = []

    database_filename = 'C:/Temp/read_and_store_data.db'
    if not os.path.exists(database_filename):
        basename = os.path.basename(database_filename)
        print(f'ERROR: database file \'{basename}\' doesn\'t exist', file=sys.stderr)
        return;
    
    conn = _create_connection(database_filename)
    if conn:
        # do some SQLite queries and print output
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(stmt_str)
        r = cur.fetchall()

        headers = []
        for description in cur.description:
            tmp = description[0].replace('_',' ')
            headers.append(tmp.title())

        summary_data = [ ]
        for member in r:
            tmp = [ str(i).title() for i in tuple(member) ]
            summary_data.append(tmp)
        conn.close()
        

    tmp = []
    tmp.extend(summary_data)
    tmp.append(headers)
    width_list= _get_column_width(tmp)
    #print(width_list)
    

    _print_data(headers=headers,
                data= summary_data,
                column_width=width_list)

    
'''
References:
 - https://docs.python.org/3/library/sqlite3.html
 - https://www.sqlitetutorial.net/sqlite-python/delete/
 - https://www.adamsmith.haus/python/answers/how-to-create-dictionary-keys-from-variables-in-python
'''
