from interpret_library.args_checker import ArgsChecker
from interpret_library.error import printErr, printErrAndExit
from interpret_library.instruction_list import InstructionList
from interpret_library.XMLparser import XMLparser

def Main() :
    #check arguments
    argsChecker = ArgsChecker()
    argsChecker.check()

    #create empty instruction list
    instructionList = InstructionList()

    #parse the XML file
    parser = XMLparser(argsChecker.getXMLPath())
    parser.parse()






if __name__ == '__main__':
    Main()