'''__main__.py'''

import datetime
import pathlib
import os
import re
import sys
import zipfile

from urllib.parse import urljoin, urlsplit, urlunsplit, urlparse

import ine

from ine.cli import read_user_cli_args
from ine.data import read_and_store_data, print_summary_data, print_state_summary
from ine.web_requests import download_file, request_json_url

def _parse_and_download_ine_data():
    '''parse the json url from INE and get path of the file to download.
returns the local name (pathlib.Path) of the downloaded file.'''
    
    temp_folder = os.getenv('TEMP')
    url = ine.__url__
    
    data_url = request_json_url(url=url)
    
    if not data_url:
        print('Bad Web Request...', file=sys.stderr)
        return
    if not 'archivoCorte' in data_url:
        print('Missing \'archivoCorte\' key in dictionary', file=sys.stderr)
        return
    
    path = data_url['archivoCorte']
    split_url = urlparse(url)
    new_url = urlunsplit((split_url.scheme, split_url.netloc, path, None,None))
    local_file = os.path.join(os.path.sep, temp_folder, path)

    if os.path.exists(local_file):
        os.remove(local_file)

    print('-'*120)
    print(path)
    print(url)
    print(new_url)
    print(local_file)
    print('-'*120)

    local_file = download_file(url = new_url,
                               local_filename = local_file)

    return pathlib.Path(local_file).resolve()

def main():
    '''runs INE'''
    local_filename = _parse_and_download_ine_data()
    
    print(f'{local_filename}', local_filename.is_file())

    if not local_filename.is_file():
        print(f'ERROR: local_filename not found', file=sys.stderr)
        print(f'1', file=sys.stderr)
        sys.exit(-1)

if __name__ == '__main__':
    main()
