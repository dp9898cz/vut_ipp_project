from interpret_library.args_checker import ArgsChecker
from interpret_library.error import *
from interpret_library.instruction_list import InstructionList
from interpret_library.XMLparser import XMLparser
from interpret_library.frame import Frame

def Main() :
    #check arguments
    argsChecker = ArgsChecker()
    argsChecker.check()

    #create instance of Frame helper
    frame = Frame()

    #create empty instruction list
    instructionList = InstructionList()

    #create stack
    dataStack = []

    #parse the XML file
    parser = XMLparser(argsChecker.getXMLPath())
    parser.parse()

    #import instructions to the instruction list
    parser.importInstructions(instructionList)

    #check strings and replace \ sign
    instructionList.checkStrings()

    #start interpreting
    lineCounter = 0
    
    while True :
        instruction = instructionList.getNextInstruction()
        if (instruction == None) :
            break

        #switch - every instruction 

        if instruction.type == 'WRITE' or instruction.type == 'DPRINT':
            aType, aData = instruction.getArgTypeAndData(instruction.arg1, frame)
            if aData == None:
                printErrAndExit('Pokud o pristup k neinicializovane promenne.', 56)
            else :
                if (aType == 'nil' and aData == 'nil') :
                    aData = ''

                #aData = instructionList.fixString(aData)
                #print('adata_: ', aData)

                if instruction.type == 'WRITE' :
                    print(aData, end='')
                else:
                    printStderr(aData)

        elif instruction.type == 'BREAK' :
            printStderr('Tady bude vypis.')     #TODO

        elif instruction.type == 'CREATEFRAME' :
            frame.createFrame()
        
        elif instruction.type == 'PUSHFRAME' :
            frame.pushFrame()

        elif instruction.type == 'POPFRAME' :
            frame.popFrame()
        
        elif instruction.type == 'DEFVAR' :
            frame.defVar(instruction.arg1)

        elif instruction.type == 'PUSHS' :
            typee, data = instruction.getArgTypeAndData(instruction.arg1, frame)
            dataStack.append((typee, data))
        
        elif instruction.type == 'POPS' :
            try:
                typee, data = dataStack.pop()
            except IndexError :
                printErrAndExit('Instrukce POPS: prazdny datastack.', 56)
            frame.setVar(instruction.arg1, typee, data)

        elif instruction.type == 'MOVE' :
            typee, data = instruction.getArgTypeAndData(instruction.arg2, frame)
            frame.setVar(instruction.arg1, typee, data)

        elif instruction.type == 'CALL' :
            instructionList.storePosition()
            instructionList.jump(instruction.arg1)

        elif instruction.type == 'RETURN' :
            instructionList.restorePosition()

        elif instruction.type in ['ADD', 'SUB', 'MUL', 'IDIV'] :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)
            if type1 == type2 == 'int' :
                if instruction.type == 'ADD':
                    frame.setVar(instruction.arg1, 'int', str(int(data1)+int(data2)))
                elif instruction.type == 'SUB':
                    frame.setVar(instruction.arg1, 'int', str(int(data1) - int(data2)))
                elif instruction.type == 'MUL':
                    frame.setVar(instruction.arg1, 'int', str(int(data1) * int(data2)))
                else:
                    if int(data2) == 0:
                        printErrAndExit('CHYBA: Deleni nulou.', 57)
                    else:
                        frame.setVar(instruction.arg1, 'int', str(int(data1) // int(data2)))
            else :
                printErrAndExit('Spatne typy operandu v matematicke instrukci.', 53)

        elif instruction.type in ['LT', 'GT', 'EQ'] :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            if type1 == type2 :
                if instruction.type == 'EQ' :
                    frame.setVar(instruction.arg1, 'bool', 'true' if data1 == data2 else 'false')
                elif (instruction.type in ['GT', 'LT'] and (type1 == 'nil' and type2 == 'nil')) :
                    printErrAndExit('Nelze porovnat typy ' + type1 + ' a ' + type2 + ' v instrukci LT nebo GT.', 53)
                elif instruction.type == 'LT' :
                    if type1 == 'string' :
                        frame.setVar(instruction.arg1, 'bool', 'true' if data1 < data2 else 'false')
                    elif type1 == 'nil' :
                        frame.setVar(instruction.arg1, 'bool', 'false')
                    elif type1 == 'bool':
                        frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'false' and data2 == 'true' else 'false')
                    else :
                        frame.setVar(instruction.arg1, 'bool', 'true' if int(data1) < int(data2) else 'false')
                else :
                    if type1 == 'string' :
                        frame.setVar(instruction.arg1, 'bool', 'true' if data1 > data2 else 'false')
                    elif type1 == 'nil' :
                        frame.setVar(instruction.arg1, 'bool', 'false')
                    elif type1 == 'bool':
                        frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'true' and data2 == 'false' else 'false')
                    else :
                        frame.setVar(instruction.arg1, 'bool', 'true' if int(data1) > int(data2) else 'false')

            elif instruction.type == 'EQ' and (type1 == 'nil' or type2 == 'nil') :
                frame.setVar(instruction.arg1, 'bool', 'false')
            else :
                printErrAndExit('Nelze porovnat typy ' + type1 + ' a ' + type2 + '.', 53)

        elif instruction.type in ['AND', 'OR'] :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            if type1 == type2 == 'bool' :
                if instruction.type == 'AND' :
                    frame.setVar(instruction.arg1, 'bool', 'true' if data1 == data2 == 'true' else 'false')
                else :
                    frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'true' or data2 == 'true' else 'false')
            else :
                printErrAndExit('Nelze provadet and nebo or s typy ' + type1 + ' a ' + type2 + '.', 53)

        elif instruction.type == 'NOT' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            if type1 == 'bool':
                frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'false' else 'false')
            else :
                printErrAndExit('Nelze provadet not s typem' + type1 + '.', 53)

        elif instruction.type == 'INT2CHAR' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            if type1 == 'int' :
                try:
                    char = chr(int(data1))
                except ValueError:
                    printErrAndExit('Nebylo mozne prevest hodnotu' + data1 + 'do podoby char.', 58)
                frame.setVar(instruction.arg1, 'string', char)
            else :
                printErrAndExit('Nelze provadet int2char s typem' + type1 + '.', 53)

        elif instruction.type == 'STRI2INT' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            if type1 == 'string' and type2 == 'int' :
                i = int(data2)
                if i >= 0 and i <= len(data1) - 1 :
                    ordd = ord(data1[i])
                    frame.setVar(instruction.arg1, 'int', ordd)
                else :
                    printErrAndExit('Indexace mimo retezec u instrukce STR2INT.', 58)
            else :
                printErrAndExit('Nelze provadet stri2int s typem' + type1 + ' a ' + type2 + '.', 53)

        elif instruction.type == 'READ' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)

            if len(argsChecker.getInputPath()) :
                try :
                    with open(argsChecker.getInputPath()) as file :
                        uis = file.read().splitlines()
                        #print(uis)
                except FileNotFoundError :
                    printErrAndExit('Nebylo mozne otevrit a precist input ze souboru.', 11)
                
                try:
                    userInput = uis[lineCounter]
                except IndexError:
                    printErr('Chybejici udaj do promenne.')
                    frame.setVar(instruction.arg1, 'nil', '')
                    continue
                finally :
                    lineCounter += 1
            else :
                try :
                    userInput = input()
                except Exception :
                    printErrAndExit('Nebylo mozne vzit input ze stdin.', 11)
            
            if data1 == 'int' :
                try:
                    number = str(int(userInput))
                except :
                    printErr('Byl zadan chybny udaj do promenne typu int.')
                    frame.setVar(instruction.arg1, 'nil', '')
                else :
                    frame.setVar(instruction.arg1, 'int', number)
            elif data1 == 'bool' :
                if userInput.lower() == 'true' :
                    frame.setVar(instruction.arg1, 'bool', 'true')
                elif userInput.lower() == 'false' :
                    frame.setVar(instruction.arg1, 'bool', 'false')
                else :
                    printErr('Byl zadan chybny udaj do promenne typu bool.')
                    frame.setVar(instruction.arg1, 'bool', 'false')
            else :
                frame.setVar(instruction.arg1, 'string', userInput)
        
        elif instruction.type == 'CONCAT' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            if type1 == type2 == 'string' :
                data1 = '' if data1 is None else data1
                data2 = '' if data2 is None else data2
                frame.setVar(instruction.arg1, 'string', data1 + data2)
            else :
                printErrAndExit('Neni mozne provest konkatenaci retezcu.', 53) 
                
        elif instruction.type == 'STRLEN' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)

            if type1 == 'string' :
                frame.setVar(instruction.arg1, 'int', len(data1))
            else :
                printErrAndExit('Nebylo mozne zjistit delku retezce (spatny operand)', 53)

        elif instruction.type == 'GETCHAR' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            if type1 == 'string' and type2 == 'int' :
                number = int(data2)
                if number >= 0 and number < len(data1) :
                    frame.setVar(instruction.arg1, 'string', data1[number])
                else :
                    printErrAndExit('Indexace mimo retezec u instrukce GETCHAR.', 58)
            else :
                printErrAndExit('Nebylo mozne provest operaci getchar (spatne operandy)', 53)

        elif instruction.type == 'SETCHAR' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)
            dataV: str
            typeV, dataV = instruction.getArgTypeAndData(instruction.arg1, frame)

            if type1 == 'int' and type2 == 'string' and typeV == 'string':
                number = int(data1)
                if number < 0 or number >= len(dataV) or dataV == '' :
                    printErrAndExit('Indexace mimo retezec u instrukce SETCHAR.', 58)
                if data2 == '' :
                    printErrAndExit('Prazdny retezec - chyba u instrukce SETCHAR.', 58)
                else :
                    data_list = list(dataV)
                    data_list[number] = data2[0]
                    dataV = "".join(data_list)
                    frame.setVar(instruction.arg1, 'string', dataV)
            else :
                printErrAndExit('Nebylo mozne provest operaci setchar (spatne operandy)', 53)

        elif instruction.type == 'TYPE' :
            type1 = instruction.getType(instruction.arg2, frame)
            if type1 is None :
                type1 = ''
            frame.setVar(instruction.arg1, 'string', type1)
        
        elif instruction.type == 'LABEL' :
            continue
        
        elif instruction.type in ['JUMPIFEQ', 'JUMPIFNEQ'] :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg2, frame)
            type2, data2 = instruction.getArgTypeAndData(instruction.arg3, frame)

            instructionList.checkLabel(instruction.arg1)

            if (type1 == type2 or type1 == 'nil' or type2 == 'nil') :
                if instruction.type == 'JUMPIFEQ' and data1 == data2 :
                    instructionList.jump(instruction.arg1)
                elif instruction.type == 'JUMPIFNEQ' and data1 != data2 :
                    instructionList.jump(instruction.arg1)
                else :
                    pass
            else :
                printErrAndExit('Argumenty instrukce JUMPIFEQ nejsou stejneho typu.', 53)
        
        elif instruction.type == 'JUMP' :
            instructionList.jump(instruction.arg1)
        
        elif instruction.type == 'EXIT' :
            type1, data1 = instruction.getArgTypeAndData(instruction.arg1, frame)

            if type1 != 'int' :
                printErrAndExit('Chybny typ argumentu v instrukci exit.', 53)
            else :
                number = int(data1)
                if number < 0 or number > 49 :
                    printErrAndExit('Chybny ciselna hodnota v argumentu instrukce exit.', 57)
                else :
                    printErrAndExit('', number)
            



        


        
        








if __name__ == '__main__':
    Main()