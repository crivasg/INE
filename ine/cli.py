''' cli.py'''

import argparse
import pathlib

def read_user_cli_args():
    '''Handle the CLI arguments and options'''

    parser = argparse.ArgumentParser(prog='ine',
                                     description='process the INE results from a zip file')

    '''controls the output to the screen.'''
    parser.add_argument('-v','--verbose',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Increase output verbosity')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", 
                       action="store_true")
    group.add_argument("-q", "--quiet", 
                       action="store_true")

    return parser.parse_args()
