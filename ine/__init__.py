'''__init__.py'''

import os
import uuid

__prog_name__ = 'ine'
__author__  = 'Cesar A. Rivas'

__version__ = '0.0.0'
try:
    with open(pathlib.Path(__file__).parent / "VERSION", encoding="utf-8") as f:
        __version__ = f.read().strip()
except IOError:
    print('File not find')
finally:
    pass


__desc__ = 'process the INE results from a zip file'
__url__ = 'https://computosrm2022.ine.mx/assets/JSON/REVOCACION_MANDATO/NACIONAL/Revocacion_Mandato_NACIONAL.json'
__epilog__ = 'that\'s it, folks...'
__uuid__ = str(uuid.uuid4())
__width__ = 82

# creates the %APPDATA%\submit and %TEMP%\submit folder if not exist
__appdata_folder__ = os.path.join(os.sep,os.getenv('APPDATA'),__prog_name__.lower())
if not os.path.isdir(__appdata_folder__):
    os.makedirs(__appdata_folder__, exist_ok=True)
    
__tmp_folder__ = os.path.join(os.sep,os.getenv('TEMP'),__prog_name__.lower())
if not os.path.isdir(__tmp_folder__):
    os.makedirs(__tmp_folder__, exist_ok=True)
