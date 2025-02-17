#IPP 2020, VUT FIT
#file: instruction.py
#author: Daniel Patek (xpatek08)

from interpret_library.frame import Frame
from interpret_library.error import *

class Instruction():

    def __init__(self, type, arg1=None, arg2=None, arg3=None):
        super().__init__()
        self.type = type
        self.argsCount = 0
        if arg1 is not None :
            self.arg1 = {'type': arg1.attrib['type'], 'data': (arg1.text if arg1.text is not None else '')}
            self.argsCount += 1
        if arg2 is not None :
            self.arg2 = {'type': arg2.attrib['type'], 'data': (arg2.text if arg2.text is not None else '')}
            self.argsCount += 1
        if arg3 is not None :
            self.arg3 = {'type': arg3.attrib['type'], 'data': (arg3.text if arg3.text is not None else '')}
            self.argsCount += 1

    @staticmethod
    def splitVar(variable) -> (str, str) :
        return variable['data'].split('@', 1)


    def getArgTypeAndData(self, argument: dict, frameClassObj: Frame) -> (str, str):
        if argument['type'] in ['int', 'bool', 'string', 'type', 'label', 'nil'] :
            return(argument['type'], argument['data'])
        else :
            #zpracovavame promennou -> podivat se na stav ramcu
            frame, data = self.splitVar(argument)
            frameObj = frameClassObj.getFrame(frame)
            if frameObj is None :
                printErrAndExit('Pokus o cteni promenne z nedefinovaneho ramce.', 55)
            if data not in frameObj :
                printErrAndExit('Pokus o cteni nedefinovane promenne v existujicim ramci.', 54)
            else :
                if (frameObj[data]['type'] is None or frameObj[data]['data'] is None) :
                    printErrAndExit('Pokus o cteni nedefinovane promenne. (nebyla definovana)', 56)
                    
                return(frameObj[data]['type'], frameObj[data]['data'])

    def getType(self, argument: dict, frameObj: Frame) -> str:
        if argument['type'] in ['int', 'bool', 'string', 'type', 'label', 'nil'] :
            return argument['type']
        else :
            frame, data = self.splitVar(argument)
            frameObj = frameObj.getFrame(frame)
            if frameObj is None :
                printErrAndExit('Pokus o cteni promenne z nedefinovaneho ramce.', 55)
            if data not in frameObj :
                printErrAndExit('Pokus o cteni nedefinovane promenne v existujicim ramci.', 54)
            else :
                if frameObj[data]['type'] is None :
                    return None
                return frameObj[data]['type']

