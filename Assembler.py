__author__ = 'tkorrison'
# Chapter 6 from Nand2Tetris Course

# The assembler development is the first in a series of five software construction projects that build our hierarchy
# of translators (assembler, virtual machine, and compiler). The proposed project comprises an API  describing several
# modules, each containing several routes.

# The Assembler


import sys

# The Parser Module
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


# The SymbolTable Module
class SymbolTable(object):
    def __init__(self):
        self._symbols = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
                         'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
                         'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
                         'SCREEN': 0x4000, 'KBD': 0x6000}

    def add_entry(self, symbol, address):
        self._symbols[symbol] = address

    def contains(self, symbol):
        return symbol in self._symbols

    def get_address(self, symbol):
        return self._symbols[symbol]



# First parse
def pass0(filename):
    asm_file = open(filename)
    lines = asm_file.readlines()
    parser = Parser(lines)
    cur_address = 0
    while parser.has_more_commands():
        parser.advance()
        cmd = parser.command_type()
        if cmd == 'A_COMMAND' or cmd == 'C_COMMAND':
            cur_address += 1
        elif cmd == 'L_COMMAND':
            SymbolTable().add_entry(symbol=parser.symbol(), address=cur_address)


# Second parse
def pass1(infile, outfile):
    asm_file = open(infile)
    lines = asm_file.readlines()
    parser = Parser(lines)
    f = open(outfile.split('.')[0] + '.hack', 'w')
    while parser.has_more_commands():
        parser.advance()
        cmd = parser.command_type()
        if cmd == 'A_COMMAND':
            f.write('{0:0>16}'.format(str(bin(int(_get_address(parser.symbol())))[2:])) + '\n')
        elif cmd == 'C_COMMAND':
            f.write('111' + Code(parser.comp()).comp() + Code(parser.dest()).dest() + Code(parser.jump()).jump() + '\n')
        elif cmd == 'L_COMMAND':
            pass
    f.close()


def _get_address(symbol):
    symbol_address = 16
    if symbol.isdigit():
        return symbol
    else:
        if not SymbolTable.contains(symbol):
            SymbolTable.add_entry(symbol, symbol_address)
            symbol_address += 1
        return SymbolTable.get_address(symbol)


# Drive the assembly process
def assemble(filein):
    pass0(filein)
    pass1(filein, _outfile(filein))


def _outfile(infile):
    if infile.endswith('.asm'):
        return infile.replace('.asm', '.hack')
    else:
        return infile + '.hack'


# Main Assembler Program
def main():
    if len(sys.argv) != 2:
        print "Usage: Assembler file.asm"
    else:
        infile = sys.argv[1]
        assemble(infile)

if __name__ == "__main__":
    main()
