#IPP 2020, VUT FIT
#file: error.py
#author: Daniel Patek (xpatek08)

import sys

def printErr(s_string) :
    sys.stderr.write(s_string + '\n')

def printErrAndExit(s_string, exit_code) :
    sys.stderr.write(s_string + '\n')
    exit(exit_code)