#IPP 2020, VUT FIT
#file: instruction_list.py
#author: Daniel Patek (xpatek08)

from interpret_library.instruction import Instruction

class InstructionList() :
    def __init__(self):
        super().__init__()
        self.list = {}
        self.instructionCounter = 0
        self.current = 1
    
    def insertInstruction(self, instruction: Instruction) :
        self.instructionCounter += 1
        self.list[self.instructionCounter] = instruction
        
    def getNextInstruction(self) -> Instruction :
        if (self.current <= self.instructionCounter) :
            self.current += 1
            return self.list[self.current - 1]
        else:
            return None

