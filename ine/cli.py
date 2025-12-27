''' cli.py'''

import argparse
import pathlib

def read_user_cli_args():
    '''Handle the CLI arguments and options'''

    parser = argparse.ArgumentParser(prog='ine',
                                     description='process the INE results from a zip file')

    '''controls the output to the screen.'''    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", 
                       required=False,
                       action="store_true",
                       default=False,
                       help='Increase output verbosity')
    group.add_argument("-q", "--quiet", 
                       required=False,
                       action="store_true"
                      default=True,help='Make the program quiet')

    return parser.parse_args()

