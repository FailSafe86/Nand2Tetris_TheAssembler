__author__ = 'tkorrison'
# Chapter 6 from Nand2Tetris Course

# The assembler development is the first in a series of five software construction projects that build our hierarchy
# of translators (assembler, virtual machine, and compiler). The proposed project comprises an API  describing several
# modules, each containing several routes.

# The Assembler

# The Parser Module

import sys
import re


def main():
    if len(sys.argv) != 3:
        print ("Usage: Assembler.py infile outfile")
        return

    while Parser(sys.argv[1], sys.argv[2]).advance():

        if Code.dest(Parser.dest()):
            print()
            f = open(sys.argv[2], 'w')
            string = '111' + Parser.dest() + Parser.comp() + Parser.jump()
            f.write(string)


class Parser:
    def __init__(self, sourcename, destname):
        self.sourcename = sourcename
        self.destname = destname
        self.destfile = open(destname, 'w')

    # Opens the input file/stream and gets ready to parse
    def initializer(self):
        sourcefile = open(self.sourcename, 'r')
        line = sourcefile.readline()
        return line

    @staticmethod
    def hasmorecommands():
        if Parser.initializer > 0:
            return True
        else:
            return False

    @staticmethod
    def advance():
        if Parser.hasmorecommands:
            return True

    @staticmethod
    def commandtype():
        string = str(Parser.initializer)
        if re.findall(r'@', string):
            return "A_COMMAND"
        elif re.findall(r'=|;', string):
            return "C_COMMAND"
        else:
            return "L_COMMAND"

    @staticmethod
    def dest():

        if Parser.commandtype() == 'C_COMMAND':
            string = Parser.initializer
            s = str(string)
            regex = compile(r'(\w+)\b=(\w+)\b;(\w+)$')
            match = regex(s)
            if match.group(1):
                return match.group(1)

    @staticmethod
    def jump():
        if Parser.commandtype() == 'C_COMMAND':
            string = Parser.initializer
            s = str(string)
            regex = compile(r'(\w+)\b=(\w+)\b;(\w+)$')
            match = regex(s)
            if match.group(2):
                return match.group(2)

    @staticmethod
    def comp():
        if Parser.commandtype() == 'C_COMMAND':
            string = Parser.initializer
            s = str(string)
            regex = compile(r'(\w+)\b=(\w+)\b;(\w+)$')
            match = regex(s)
            if match.group(3):
                return match.group(3)


# The Code Module
class Code:
    def __init__(self, mnemonic):
        self.mnemonic = mnemonic

    @staticmethod
    def dest(mnemonic):
        if re.findall(r'AMD', mnemonic):
            return "111"
        elif re.findall(r'MD', mnemonic):
            return "011"
        elif re.findall(r'AM', mnemonic):
            return "101"
        elif re.findall(r'AD', mnemonic):
            return "110"
        elif re.findall(r'M', mnemonic):
            return "001"
        elif re.findall(r'D', mnemonic):
            return "010"
        elif re.findall(r'A', mnemonic):
            return "100"
        elif re.findall(r'""', mnemonic):
            return "000"
        else:
            return "Not a valid dest value"

    @staticmethod
    def jump(mnemonic):
        if re.findall(r'JMP', mnemonic):
            return "111"
        elif re.findall(r'JGE', mnemonic):
            return "011"
        elif re.findall(r'JNE', mnemonic):
            return "101"
        elif re.findall(r'JLE', mnemonic):
            return "110"
        elif re.findall(r'JGT', mnemonic):
            return "001"
        elif re.findall(r'JEQ', mnemonic):
            return "010"
        elif re.findall(r'JLT', mnemonic):
            return "100"
        elif re.findall(r'""', mnemonic):
            return "000"
        else:
            return "Not a valid dest value"

    @staticmethod
    def comp(mnemonic):
        if re.findall(r'0', mnemonic):
            return "101010"
        else:
            return "Not a valid dest value"

# SymbolTable Module
# class SymbolTable(self, ):
main()
