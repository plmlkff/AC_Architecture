from enum import Enum
from dataclasses import dataclass
import json


class OpCode(Enum):
    ADD = 0  # +
    SUB = 1  # -

    LD = 2  # Load from memory
    WR = 3  # Write to memory
    PUSH = 4  # Put value on the stack
    POP = 5  # Take value from the stack

    CALL = 6  # Call function
    RET = 7  # Return from function
    CMP = 8  # Compare AC with given value
    JMP = 9  # Jump to address
    JZ = 10  # Jump if zero
    JE = 11  # Jump if equals
    JNE = 12  # Jump if not equals
    JG = 13  # Jump if greater
    JL = 14  # Jump if lower

    HLT = 15

    def __str__(self):
        return self.name


class AddressingType(Enum):
    ABSOLUTE_STRAIGHT = 0
    ABSOLUTE_RELATIVE = 1
    INDIRECT_STRAIGHT = 2
    INDIRECT_RELATIVE = 3
    DIRECT_LOAD = 4

    def __str__(self):
        return self.name



@dataclass
class Command:
    name: str
    op_code: OpCode
    addressing_type: AddressingType = None
    is_start: bool = False
    address: int = None

    def __init__(self, name, opcode):
        self.name = name
        self.op_code = opcode


def deserialize(filename: str):
    with open(filename, "r") as file:
        json_obj = json.load(file)
    stack = []
    for value in json_obj:
        if isinstance(value, int):
            stack.append(value)
        elif isinstance(value, dict):
            command = Command(value["name"], OpCode[value["op_code"]])
            stack.append(command)
    return stack


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Command):
            return obj.__dict__
        elif isinstance(obj, OpCode):
            return obj.__str__()
        elif isinstance(obj, AddressingType):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


class MicroInstructions(Enum):
    # Сигналы, защелкивающие значения в регистрах с шины
    LATCH_AC = 0
    LATCH_BR = 1
    LATCH_DR = 2
    LATCH_SP = 3
    LATCH_CR = 4
    LATCH_IP = 5
    LATCH_AR = 6

    # Сигналы мультиплексора, направляющие значение регистра в АЛУ
    # Левый вход АЛУ
    LOAD_AC = 7
    LOAD_BR = 8
    # Правый вход АЛУ
    LOAD_DR = 9
    LOAD_SP = 10
    LOAD_CR = 11
    LOAD_IP = 12
    LOAD_ZR = 13

    # Чтение данных из памяти по AR
    WR_MEM = 14
    RD_MEM = 15

    # Управляющие сигналы АЛУ
    INV_L = 16  # Invert left
    INV_R = 17  # Invert right
    INC = 18  # Increment output
    AND = 19  # Binary AND (default do sum)

    # Сигналы проверки флагов
    SET_NZ = 20  # Set sign and zero flags
    SET_V = 21  # Set overflow
    SET_C = 22  # Set carry flag


@dataclass
class MicroCommand:
    signals: list[MicroInstructions]


commands = {
    'add': OpCode.ADD,
    'ld': OpCode.LD,
    'hlt': OpCode.HLT
}


