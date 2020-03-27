from interpret_library.args_checker import ArgsChecker
from interpret_library.error import *
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

    #import instructions to the instruction list
    parser.importInstructions(instructionList)

    #start interpreting
    while True :
        instruction = instructionList.getNextInstruction()
        if (instruction == None) :
            break

        #switch - every instruction 

        if instruction.type == 'WRITE' or instruction.type == 'DPRINT':
            aType, aData = instruction.getArgTypeAndData(instruction.arg1)
            if aData == None:
                printErrAndExit('Pokud o pristup k neinicializovane promenne.', 56)
            else :
                if (aType == 'nil' and aData == 'nil') :
                    aData = ''
                index: int = aData.find('\\')
                while(index != -1) :
                    aData = aData.replace(aData[index:index+4], chr(int(aData[index+1:index+4])))
                    index = aData.find('\\', index + 1)
                if instruction.type == 'WRITE' :
                    print(aData, end='')
                else:
                    printStderr(aData)








if __name__ == '__main__':
    Main()