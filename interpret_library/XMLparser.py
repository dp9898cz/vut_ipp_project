#IPP 2020, VUT FIT
#file: XMLparser.py
#author: Daniel Patek (xpatek08)
from interpret_library.error import printErr, printErrAndExit

import xml.etree.ElementTree as elmTree
import sys

class XMLparser():
    def __init__(self, XMLpath):
        super().__init__()
        self.XMLpath = XMLpath
    def parse(self):
        self.checkTreeIntegrity()

    def checkTreeIntegrity(self):
        printErr('Kontrola integrity XML.')
        try:
            if self.XMLpath == 'sys.stdin' :
                printErr('Cteni XML ze stdin.')
                myTree = elmTree.parse(sys.stdin)
            else :
                myTree = elmTree.parse(self.XMLpath)
        except FileNotFoundError:
            printErrAndExit('Vyskytla se chyba pri otevirani souboru ' + self.XMLpath, 11)
        except Exception:
            printErrAndExit('XML format neni v poradku.', 31)

        try:
            root = myTree.getroot()
        except:
            printErrAndExit('Nebylo mozne ziskat koren XML souboru.', 31)

