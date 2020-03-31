#IPP 2020, VUT FIT
#file: instruction_list.py
#author: Daniel Patek (xpatek08)

import interpret_library.instruction as instruction
from interpret_library.error import *

class InstructionList() :
    def __init__(self):
        super().__init__()
        self.list = {}
        self.instructionCounter = 0
        self.current = 1
        self.callstack = []
        self.labels = {}
    
    def insertInstruction(self, instruction: instruction.Instruction) :
        self.instructionCounter += 1
        self.list[self.instructionCounter] = instruction

        if instruction.type == 'LABEL' :
            name = instruction.arg1['data']
            if name not in self.labels :
                self.labels[name] = self.instructionCounter
            else :
                printErrAndExit('Pokus o redefinici navesti.', 52)
        
    def getNextInstruction(self) -> instruction.Instruction :
        if (self.current <= self.instructionCounter) :
            self.current += 1
            return self.list[self.current - 1]
        else:
            return None

    def storePosition(self) :
        self.callstack.append(self.current)

    def restorePosition(self) :
        if len(self.callstack) :
            self.current = self.callstack.pop()
        else :
            printErrAndExit('Zadna hodnota v zasobniku volani.', 56)

    def jump(self, argument: dict) :
        name = argument['data']
        if name in self.labels :
            self.current = self.labels[name]
        else :
            printErrAndExit('Pokus o skok na neexistujici navesti.', 52)

    def checkLabel(self, argument: dict) :
        name = argument['data']
        if name not in self.labels :
            printErrAndExit('Pokus o skok na neexistujici navesti.', 52)

    def fixString(self, string: str) -> str :
        index: int = string.find('\\')
        while(index != -1) :
            string = string.replace(string[index:index+4], chr(int(string[index+1:index+4])))
            index = string.find('\\', index + 1)
        return string
        
    def checkStrings(self) :
        for ins in self.list:
            instruction = self.list[ins]
            if hasattr(instruction, 'arg1') :
                if instruction.arg1['type'] == 'string' :
                    instruction.arg1['data'] = self.fixString(instruction.arg1['data'])
            if hasattr(instruction, 'arg2') :
                if instruction.arg2['type'] == 'string' :
                    instruction.arg2['data'] = self.fixString(instruction.arg2['data'])
            if hasattr(instruction, 'arg3') :
                if instruction.arg3['type'] == 'string' :
                    instruction.arg3['data'] = self.fixString(instruction.arg3['data'])



