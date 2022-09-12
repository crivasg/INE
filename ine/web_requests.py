'''web_requests.py'''

import json
import requests
from tqdm import tqdm

def request_json_url(url):
    '''returns the string of a URL'''

    data = {}
    r = requests.get(url, allow_redirects=True)
    status_code = r.status_code
    #print('status_code',r.status_code, sep=' = ')
    # check that the status code is not bad., if bad, returns empty dict
    if r.status_code != requests.codes.ok:
        return data
    status_code = r.status_code
    headers = r.headers
    content_type = r.headers.get('content-type')
    if content_type.lower() == 'application/json':
        data = r.json()

    #print('status_code',r.status_code, sep=' = ')
    #print(json.dumps(dict(headers),sort_keys=False, indent=4))
    #print('\n\nurl', url, sep=' = ')
    #print('content_type',content_type, sep=' = ')
    #print('horaCorte',data['horaCorte'], sep=' = ')
    #print('fechaCorte',data['fechaCorte'], sep=' = ')
    #print('archivoCorte',data['archivoCorte'], sep=' = ')
    #print('\n')
    #print('data', type(data), sep=' = ')

    return data
    

def download_file(url, local_filename=None):
    ''' downloads a file to the local drive from an url with a progress bar thanks to 'tqdm'
Referenes:
 - https://stackoverflow.com/a/16696317
 - Progress Bar while download file over http with Requests: https://stackoverflow.com/a/37573701
'''

    chunk_size=8192

    if not local_filename:
        local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as resp:
        headers = resp.headers
        total_size_in_bytes= int(resp.headers.get('content-length', 0))
        #print(f'{total_size_in_bytes=}')
        resp.raise_for_status()

        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(local_filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
    return local_filename
