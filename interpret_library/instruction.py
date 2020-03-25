#IPP 2020, VUT FIT
#file: instruction.py
#author: Daniel Patek (xpatek08)

class Instruction():
    def __init__(self, type, arg1=None, arg2=None, arg3=None):
        super().__init__()
        self.type = type
        self.argsCount = 0
        if arg1 is not None :
            self.arg1 = arg1
            self.argsCount += 1
        if arg2 is not None :
            self.arg2 = arg2
            self.argsCount += 1
        if arg3 is not None :
            self.arg3 = arg3
            self.argsCount += 1

