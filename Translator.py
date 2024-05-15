from dataclasses import dataclass
from enum import Enum
import re
from BasicTypes import AddressingType, OpCode, commands, CommandEncoder, Command
import json

'''
Грамматика автомата
S    -> (^[a-zA-Z]+$)MNC | E
MNC  -> ( ^(\[|\+|-|#){0,1}\d+(\]){0,1}$ )ADDR | (^[a-zA-Z]+$)MNC
ADDR -> (^[a-zA-Z]+$)MNC | E
E    -> to stderr
'''

mrk_pattern = re.compile(r'^\.?[a-zA-Z_-]+:')
mnc_pattern = re.compile(r'^[a-zA-Z]+$')
addr_pattern = re.compile(r'^[\[\+\-#]?[\+\-]?\d+\]?$')
start_address = 0


class MachineState(Enum):
    S = 0
    MNC = 1
    ADDR = 2
    E = 3


@dataclass
class Lexeme:
    word: str
    type: MachineState


def parse_addressing_type(word: str):
    if word[0] == '[':
        if word[1] == '+' or word[1] == '-':
            return AddressingType.STACK_RELATIVE
        return AddressingType.INDIRECT_STRAIGHT
    elif word[0] == '#':
        return AddressingType.DIRECT_LOAD
    else:
        if word[0] == '+' or word[0] == '-':
            return AddressingType.STRAIGHT_RELATIVE
        return AddressingType.ABSOLUTE_STRAIGHT


# Переводим лексемы в команды и помещаем в стек памяти
def lexemes_to_commands(lexemes: list[Lexeme]):
    memory_stack: list[int | Command] = [0] * 1024
    is_address_changed = False
    is_word_value = False
    address = 0
    for lexeme in lexemes:
        if is_word_value:
            memory_stack[address] = int(re.findall(r'[+-]?\d+', lexeme.word)[0])
            address += 1
            is_word_value = False
            continue
        if is_address_changed:
            address = int(re.findall(r'[+-]?\d+', lexeme.word)[0])
            is_address_changed = False
            continue
        if lexeme.word == 'org':
            is_address_changed = True
        if lexeme.word == 'word':
            is_word_value = True
        elif lexeme.type == MachineState.MNC and lexeme.word in commands:
            memory_stack[address] = Command(lexeme.word, commands[lexeme.word])
            memory_stack[address].addressing_type = AddressingType.NO_ADDRESS
            if address == start_address:
                memory_stack[address].is_start = True
            address += 1
        elif lexeme.type == MachineState.ADDR:
            memory_stack[address - 1].address = int(re.findall(r'[+-]?\d+', lexeme.word)[0])
            memory_stack[address - 1].addressing_type = parse_addressing_type(lexeme.word)
    return memory_stack


def replace_marks(lines: list[str]):
    global start_address
    address = 0
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    lines = '\n'.join(lines)
    lines = lines.replace(':\n', ':')
    for line in lines.split('\n'):
        if len(re.findall(r'\s?org\s', line)) == 1:
            address = int(re.findall(r'\d+', line)[0])
            continue
        if len(mrk_pattern.findall(line)) == 0:
            address += 1
            continue
        mark = mrk_pattern.findall(line)[0]
        if mark == "START:":
            start_address = address
        lines = lines.replace(mark, '').replace(mark[0:len(mark) - 1], str(address))
        address += 1
    return lines


def get_expected_lexeme_name(state: MachineState):
    if state == MachineState.S:
        return 'mark or address'
    if state == MachineState.MNC:
        return 'address or mnemonic or mark'
    if state == MachineState.ADDR:
        return 'mark or mnemonic'


def state_S(word: str):
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def state_MNC(word: str):
    if len(addr_pattern.findall(word)) != 0:
        return Lexeme(word, MachineState.ADDR)
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def state_ADDR(word: str):
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def scan_lexemes(lines: str):
    current_state = MachineState.S
    words = lines.split()
    transition_matrix = [state_S, state_MNC, state_ADDR]
    lexemes = []
    for word in words:
        lexeme = transition_matrix[current_state.value](word)
        lexemes.append(lexeme)
        if lexeme.type == MachineState.E:
            print(f'Received wrong line: {lexeme.word}')
            print(f'Expected: {get_expected_lexeme_name(current_state)}')
            print(f'Shutdown...')
            exit(1)
        current_state = lexeme.type
    return lexemes


def read_file(input_name: str):
    f = open(input_name, "r")
    data = f.readlines()
    f.close()
    return data


if __name__ == '__main__':
    lines = read_file('input.txt')
    lines = replace_marks(lines)
    lexemes = scan_lexemes(''.join(lines))
    stack = lexemes_to_commands(lexemes)
    for instruction in stack:
        if instruction == 0: continue
        print(instruction)
    json.dump(stack, open("output.txt", 'w'), cls=CommandEncoder)
