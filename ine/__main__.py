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

def main():
    pass

if __name__ == '__main__':
    main()
