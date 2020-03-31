#IPP 2020, VUT FIT
#file: args_checker.py
#author: Daniel Patek (xpatek08)

from interpret_library.error import printErr, printErrAndExit
import sys

class ArgsChecker:
    def __init__(self):
        super().__init__()
        self.sourceXML = ''
        self.sourceInput = ''

    def check(self):
        #check number of args
        if len(sys.argv) > 3 or len(sys.argv) < 2 :
            printErrAndExit('Zadan spatny pocet argumentu.', 10)

        for argument in sys.argv[1:]:
            if argument == '--help' or argument == '-h':
                print("Program načte XML reprezentaci programu a tento program s využitím vstupu dle parametrů příkazové řádky")
                print("interpretuje a generuje výstup. Vstupní XML reprezentace je např. generována skriptem parse.php ")
                print("(ale ne nutně) ze zdrojového kódu v IPPcode20.")
                exit(0)

            elif argument.startswith('--source='):
                #vstupní soubor s XML reprezentací zdrojového kódu
                self.sourceXML = argument[9:]

            elif argument.startswith('--input='):
                #soubor se vstupy pro samotnou interpretaci zadaného zdrojového kódu
                self.sourceInput = argument[8:]

            else :
                printErrAndExit('Byl zadan chybny argument: ' + argument, 10)
    
    def getXMLPath(self):
        if self.sourceXML == '' :
            return 'sys.stdin'
        return self.sourceXML

    def getInputPath(self):
        return self.sourceInput