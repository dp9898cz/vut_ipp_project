#IPP 2020, VUT FIT
#file: error.py
#author: Daniel Patek (xpatek08)

import sys

def printStderr(error_string: str) :
    sys.stderr.write(error_string)

def printErr(s_string: str) :
    sys.stderr.write(s_string + '\n')

def printErrAndExit(s_string: str, exit_code: int) :
    sys.stderr.write(s_string + '\n')
    exit(exit_code)