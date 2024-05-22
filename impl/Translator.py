from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from enum import Enum

from impl.BasicTypes import AddressingType, Command, CommandEncoder, commands

"""
Грамматика автомата
S    -> (^[a-zA-Z]+$)MNC | E
MNC  -> ( ^(\[|\+|-|#){0,1}\d+(\]){0,1}$ )ADDR | (^[a-zA-Z]+$)MNC
ADDR -> (^[a-zA-Z]+$)MNC | E
E    -> to stderr
"""

mrk_pattern = re.compile(r"^[a-zA-Z_]+:")
mnc_pattern = re.compile(r"^[a-zA-Z]+$")
addr_pattern = re.compile(r"^[\[+\-#]?[+\-]?\d+]?$")
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
    if word[0] == "[":
        if word[1] == "+" or word[1] == "-":
            return AddressingType.STACK_RELATIVE
        return AddressingType.INDIRECT_STRAIGHT
    if word[0] == "#":
        return AddressingType.DIRECT_LOAD
    if word[0] == "+" or word[0] == "-":
        return AddressingType.STRAIGHT_RELATIVE
    return AddressingType.ABSOLUTE_STRAIGHT


# Переводим лексемы в команды и помещаем в стек памяти
def lexemes_to_commands(lexemes: list[Lexeme]):  # noqa: C901
    global start_address
    memory_stack: list[int | Command] = [0] * 1024
    is_address_changed = False
    is_word_value = False
    address = 0
    for lexeme in lexemes:
        if is_word_value:
            memory_stack[address] = int(re.findall(r"[+-]?\d+", lexeme.word)[0])
            address += 1
            is_word_value = False
            continue
        if is_address_changed:
            address = int(re.findall(r"[+-]?\d+", lexeme.word)[0])
            is_address_changed = False
            continue
        if lexeme.word == "org":
            is_address_changed = True
        if lexeme.word == "word":
            is_word_value = True
        elif lexeme.type == MachineState.MNC and lexeme.word in commands:
            memory_stack[address] = Command(lexeme.word, commands[lexeme.word])
            memory_stack[address].addressing_type = AddressingType.NO_ADDRESS
            if address == start_address:
                memory_stack[address].is_start = True
            address += 1
        elif lexeme.type == MachineState.ADDR:
            memory_stack[address - 1].address = int(re.findall(r"[+-]?\d+", lexeme.word)[0])
            memory_stack[address - 1].addressing_type = parse_addressing_type(lexeme.word)
    return memory_stack


def replace_marks_and_chars(lines: list[str]):
    global start_address
    address = 0
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    lines = "\n".join(lines)
    lines = lines.replace(":\n", ":")
    for line in lines.split("\n"):
        if len(re.findall(r"\'.\'", line)) == 1:  # Замена литералов
            val = re.findall(r"\'.\'", line)[0]
            lines = lines.replace(val, str(ord(val[1: len(val) - 1])), 1)
        if len(re.findall(r"\s?org\s", line)) == 1:  # Поиск и подстановка переходов по памяти
            address = int(re.findall(r"\d+", line)[0])
            continue
        if len(mrk_pattern.findall(line)) == 0:  # Проверка наличия метки в строчке
            address += 1
            continue
        mark = mrk_pattern.findall(line)[0]
        if mark == "START:":  # Запоминаем адрес стартовой метки
            start_address = address
        lines = re.sub(rf"\b{mark}", "", lines)
        lines = re.sub(rf"(?<=[+\-\[#\b ]){mark[0:len(mark) - 1]}\b", str(address), lines)
        address += 1
    return lines


def get_expected_lexeme_name(state: MachineState):
    if state == MachineState.S:
        return "mark or address"
    if state == MachineState.MNC:
        return "address or mnemonic or mark"
    return "mark or mnemonic"


def state_s(word: str):
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def state_mnc(word: str):
    if len(addr_pattern.findall(word)) != 0:
        return Lexeme(word, MachineState.ADDR)
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def state_addr(word: str):
    if len(mnc_pattern.findall(word)) != 0:
        return Lexeme(word.lower(), MachineState.MNC)
    return Lexeme(word, MachineState.E)


def scan_lexemes(lines: str):
    current_state: MachineState = MachineState.S
    words = lines.split()
    transition_matrix = [state_s, state_mnc, state_addr]
    lexemes = []
    for word in words:
        lexeme = transition_matrix[current_state.value](word)
        lexemes.append(lexeme)
        if lexeme.type == MachineState.E:
            print(f"Received wrong line: {lexeme.word}")
            print(f"Expected: {get_expected_lexeme_name(current_state)}")
            print("Shutdown...")
            exit(1)
        current_state = lexeme.type
    return lexemes


def remove_comments(lines: list[str]):
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ; ")[0]
    return lines


def read_file(input_name: str):
    f = open(input_name)
    data = f.readlines()
    f.close()
    return data


def main(if_name, of_name):
    lines = read_file(if_name)
    lines = remove_comments(lines)
    lines = replace_marks_and_chars(lines)
    lexemes = scan_lexemes("".join(lines))
    stack = lexemes_to_commands(lexemes)
    json.dump(stack, open(of_name, "w"), cls=CommandEncoder)
    head, tail = os.path.split(of_name)
    print(tail)


if __name__ == "__main__":
    _, input_file_name, output_file_name = sys.argv
    main(input_file_name, output_file_name)
