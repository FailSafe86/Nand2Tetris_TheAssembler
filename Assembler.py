__author__ = 'tkorrison'
# Chapter 6 from Nand2Tetris Course

# The assembler development is the first in a series of five software construction projects that build our hierarchy
# of translators (assembler, virtual machine, and compiler). The proposed project comprises an API  describing several
# modules, each containing several routes.

# The Assembler

# The Parser Module

import re
import sys


class Parser(object):
    def __init__(self, lines):
        self.lines = lines
        self.command = ''

    def has_more_commands(self):
        return len(self.lines) > 0

    def advance(self):
        self.command = self.lines.pop(0)

    def command_type(self):
        if self.command[:2] == '//':
            return 'comment'
        if '//' in self.command:
            self.command = self.command.split('//')[0].strip()
        self.command = self.command.strip()
        if self.command == '':
            return 'empty line'
        if self.command[0] == '@':
            if self.command[1:].isdigit():
                return 'A_COMMAND'
        elif self.command[0] == '(' and self.command[-1] == ')':
            return 'L_COMMAND'  # Loop
        else:
            return 'C_COMMAND'  # dest=comp;jump

    # SymbolTable Module
    def symbol(self):
        # call if commandType is A or L
        if self.command_type() == 'A_COMMAND':
            return self.command[1:]  # Xxx from @Xxx
        elif self.command_type() == 'L_COMMAND':
            return self.command[1:-1]  # Xxx from (Xxx)

    def dest(self):
        if self.command_type() == 'C_COMMAND':
            if ';' in self.command and '=' in self.command:
                return self.command.replace(';', ',').replace('=', ',').split(',')[0]
            elif '=' in self.command:
                return self.command.split('=')[0]
            else:
                return ''

    def jump(self):
        if self.command_type() == 'C_COMMAND':
            if ';' in self.command and '=' in self.command:
                return self.command.replace(';', ',').replace('=', ',').split(',')[2]
            elif '=' in self.command:
                return ''
            else:
                return self.command.split(';')[1]

    def comp(self):
        if self.command_type() == 'C_COMMAND':
            if ';' in self.command and '=' in self.command:
                return self.command.replace(';', ',').replace('=', ',').split(',')[1]
            elif '=' in self.command:
                return self.command.split('=')[1]
            else:
                return self.command.split(';')[0]

# The Code Module
class Code(object):
    def __init__(self, mnemonic):
        self.mnemonic = mnemonic

    def dest(self):
        translate = {'': '000',
                     'M': '001',
                     'D': '010',
                     'MD': '011',
                     'A': '100',
                     'AM': '101',
                     'AD': '110',
                     'AMD': '111'}
        return translate[self.mnemonic]

    def comp(self):
        translate = {  # a=0
                       '0': '0101010',
                       '1': '0111111',
                       '-1': '0111010',
                       'D': '0001100',
                       'A': '0110000',
                       '!D': '0001101',
                       '!A': '0110001',
                       '-D': '0001111',
                       '-A': '0110011',
                       'D+1': '0011111',
                       'A+1': '0110111',
                       'D-1': '0001110',
                       'A-1': '0110010',
                       'D+A': '0000010',
                       'D-A': '0010011',
                       'A-D': '0000111',
                       'D&A': '0000000',
                       'D|A': '0010101',
                       # a=1
                       'M': '1110000',
                       '!M': '1110001',
                       '-M': '1110011',
                       'M+1': '1110111',
                       'M-1': '1110010',
                       'D+M': '1000010',
                       'D-M': '1010011',
                       'M-D': '1000111',
                       'D&M': '1000000',
                       'D|M': '1010101'}
        return translate[self.mnemonic]

    def jump(self):
        translate = {
            '': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'}
        return translate[self.mnemonic]


def main():
    filename = sys.argv[1]
    asm_file = open(filename)
    lines = asm_file.readlines()
    parser = Parser(lines)
    f = open(filename.split('.')[0] + '.hack', 'w')

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'A_COMMAND' or parser.command_type() == 'L_COMMAND':
            f.write('{0:0>16}'.format(str(bin(int(parser.symbol()))[2:])) + '\n')
        elif parser.command_type() == 'C_COMMAND':
            f.write('111' + Code(parser.comp()).comp() + Code(parser.dest()).dest() + Code(parser.jump()).jump())

    f.close()
if __name__ == "__main__":
    main()
