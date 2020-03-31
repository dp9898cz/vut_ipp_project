#IPP 2020, VUT FIT
#file: frame.py
#author: Daniel Patek (xpatek08)

from interpret_library.error import *
import interpret_library.instruction as i

class Frame :
    def __init__(self):
        super().__init__()
        self.globalFrame = {}
        self.tmpFrame = {}
        self.tmpFrameDefined = False
        self.frameStack = []

    def getFrame(self, frame: str) -> dict:
        if frame == 'GF':
            return self.globalFrame
        elif frame == 'LF':
            return (self.frameStack[-1] if len(self.frameStack) > 0 else None)
        elif frame == 'TF':
            return (self.tmpFrame if self.tmpFrameDefined else None)
        else:
            return None

    def createFrame(self) :
        self.tmpFrame = {}
        self.tmpFrameDefined = True

    def pushFrame(self) :
        if self.tmpFrameDefined :
            self.frameStack.append(self.tmpFrame)
            self.tmpFrameDefined = False
        else :
            printErrAndExit('Pokus o pushframe s nedefinovanym ramcem.', 55)

    def popFrame(self) :
        if len(self.frameStack) :
            self.tmpFrame = self.frameStack.pop()
            self.tmpFrameDefined = True
        else :
            printErrAndExit('Pokus o popframe s prazdnym zasobnikem ramcu.', 55)

    def setVar(self, argument, typee, data) :
        frame, name = i.Instruction.splitVar(argument)
        frameObj = self.getFrame(frame)
        if frameObj is None :
            printErrAndExit('Pokus o cteni promenne z nedefinovaneho ramce.', 55)
        if name not in frameObj :
            printErrAndExit('Pokus o zapis do neexistujici promenne.', 54)
        frameObj[name]['type'] = typee
        frameObj[name]['data'] = data
        #print('type: ' + typee)
        #print('data:   _' + data)

    def defVar(self, argument) :
        frame, name = i.Instruction.splitVar(argument)
        frameObj = self.getFrame(frame)
        if frameObj is None :
            printErrAndExit('Pokus o vytvoreni promenne na nedefinovanem ramci.', 55)
        else :
            if name in frameObj :
                printErrAndExit('Pokus o vytvoreni jiz existujici promenne.', 52)
            else :
                frameObj[name] = {'data': None, 'type': None}




