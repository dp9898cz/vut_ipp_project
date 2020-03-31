#IPP 2020, VUT FIT
#file: XMLparser.py
#author: Daniel Patek (xpatek08)

from interpret_library.error import printErr, printErrAndExit
from interpret_library.instruction import Instruction
from interpret_library.instruction_list import InstructionList

import xml.etree.ElementTree as elmTree
import sys

class XMLparser():
    def __init__(self, XMLpath):
        super().__init__()
        self.XMLpath = XMLpath
    
    def parse(self):
        self.checkTreeIntegrity()
        self.checkRoot()
        self.checkInstructions()

    def checkTreeIntegrity(self):
        try:
            if self.XMLpath == 'sys.stdin' :
                myTree = elmTree.parse(sys.stdin)
            else :
                myTree = elmTree.parse(self.XMLpath)
        except FileNotFoundError:
            printErrAndExit('Vyskytla se chyba pri otevirani souboru ' + self.XMLpath, 11)
        except Exception:
            printErrAndExit('XML format neni v poradku.', 31)

        try:
            self.root = myTree.getroot()
        except:
            printErrAndExit('Nebylo mozne ziskat koren XML souboru.', 31)

    def checkRoot(self) :
        if self.root.tag != 'program' :
            printErrAndExit('XML kořen nemá název program.', 31)
        for atribute in self.root.attrib :
            if atribute not in ['language', 'name', 'description'] :
                printErrAndExit('Nepovoleny atribut u korenoveho elementu XML.', 32)
        if 'language' not in self.root.attrib :
            printErrAndExit('Chybi atribut language u korenoveho elementu XML.', 31)
        if self.root.attrib['language'].lower() != 'ippcode20':
            printErrAndExit('Atribut language u korenoveho elementu musi byt ippcode20.', 31)

    def checkInstructions(self) :
        order_tmp = 0
        for instruction in self.root :
            if instruction.tag != 'instruction':
                printErrAndExit('Nespravny nazev elementu instruction.', 32)
            if 'order' not in instruction.attrib :
                printErrAndExit('Chybi atribut order u elmentu instrukce.', 32)
            if 'opcode' not in instruction.attrib :
                printErrAndExit('Chybi atribut opcode u elementu instrukce,', 32)
            try:
                instr_number = int(instruction.attrib['order'])
            except ValueError:
                printErrAndExit('Nebylo mozne precist hodnotu int u parametru order u argumentu instrukce.', 32)
            if instr_number <= order_tmp :
                printErrAndExit('Cisla instrukci musi jit vzestupne a nesmi byt duplicitni.', 32)
            if instr_number <= 0 :
                printErrAndExit('Cisla instrukci musi byt kladne a nenulove.', 32)
            order_tmp = instr_number
            arg_counter = 0
            for argument in instruction :
                arg_counter += 1
                if argument.tag != 'arg'+str(arg_counter) :
                    printErrAndExit('Argumenty u instrukce musi byt serazeny vzestupne a adekvatnim nazvem.', 32)
                if 'type' not in argument.attrib :
                    printErrAndExit('Chybejici atribut type u argumentu instrukce.', 32)
                if argument.attrib['type'] not in ['string', 'int', 'bool', 'label', 'type', 'nil', 'var'] :
                    printErrAndExit('Chybny udaj atributu type u argumentu instrukce.', 32)


    def importInstructions(self, instrList: InstructionList):
        for instruction in self.root:
            if instruction.attrib['opcode'].upper() in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'BREAK', 'RETURN'] :
                self.checkNumOfArg(instruction, 0)
                i = Instruction(instruction.attrib['opcode'].upper()) 
                instrList.insertInstruction(i)
            elif instruction.attrib['opcode'].upper() in ['DPRINT', 'DEFVAR', 'CALL', 'PUSHS', 'POPS', 'LABEL', 'JUMP', 'WRITE', 'EXIT'] :
                self.checkNumOfArg(instruction, 1)
                i = Instruction(instruction.attrib['opcode'].upper(), instruction[0]) 
                instrList.insertInstruction(i)
            elif instruction.attrib['opcode'].upper() in ['MOVE', 'INT2CHAR', 'READ', 'STRLEN', 'TYPE', 'NOT'] :
                self.checkNumOfArg(instruction, 2)
                i = Instruction(instruction.attrib['opcode'].upper(), instruction[0], instruction[1]) 
                instrList.insertInstruction(i)
            elif instruction.attrib['opcode'].upper() in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'JUMPIFEQ', 'JUMPIFNEQ', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR'] :
                self.checkNumOfArg(instruction, 3)
                i = Instruction(instruction.attrib['opcode'].upper(), instruction[0], instruction[1], instruction[2]) 
                instrList.insertInstruction(i)
            else :
                printErrAndExit('Neocekavana chyba programu.', 32)
            
            


    def checkNumOfArg(self, instruction: Instruction, number: int) :
        if (len(list(instruction))) != number :
            printErrAndExit('Instrukce ' + instruction.attrib['opcode'] + 'musi mit pouze ' + number + 'argumentu.', 32)

