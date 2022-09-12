''' cli.py'''

import argparse
import pathlib

def read_user_cli_args():
    '''Handle the CLI arguments and options'''

    parser = argparse.ArgumentParser(prog='ine',
                                     description='process the INE results from a zip file')
    parser.add_argument('-f','--input-file',
                        metavar='FILE',
                        type=pathlib.Path,
                        default=None,
                        help='read INE results from a file')

    return parser.parse_args()
