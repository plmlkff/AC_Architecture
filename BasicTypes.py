from enum import Enum
from dataclasses import dataclass
import json
from typing import cast


class OpCode(Enum):
    NOPE = 63
    ADD = 20  # +
    SUB = 22  # -

    LD = 24  # Load from memory
    WR = 26  # Write to memory
    PUSH = 28  # Put value on the stack
    POP = 31  # Take value from the stack

    CALL = 36  # Call function
    RET = 41  # Return from function
    CMP = 46  # Compare AC with given value
    JMP = 48  # Jump to address
    JE = 50  # Jump if equals
    JNE = 53  # Jump if not equals
    JG = 56  # Jump if greater
    JL = 59  # Jump if lower

    HLT = 62

    def __str__(self):
        return self.name


class AddressingType(Enum):
    ABSOLUTE_STRAIGHT = 0
    STRAIGHT_RELATIVE = 1
    INDIRECT_STRAIGHT = 2
    STACK_RELATIVE = 3
    DIRECT_LOAD = 4
    NO_ADDRESS = 5

    def __str__(self):
        return self.name


@dataclass
class Command:
    name: str
    op_code: OpCode
    addressing_type: AddressingType
    is_start: bool
    address: int

    def __init__(self, name, opcode):
        self.name = name
        self.op_code = opcode
        self.addressing_type = AddressingType.NO_ADDRESS
        self.is_start = False
        self.address = 0


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Command):
            return obj.__dict__
        elif isinstance(obj, OpCode):
            return obj.__str__()
        elif isinstance(obj, AddressingType):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


def dictToCommand(dict):
    if isinstance(dict, int): return dict
    command = Command(dict['name'], OpCode[dict['op_code']])
    command.addressing_type = AddressingType[dict['addressing_type']]
    command.address = int(dict['address'])
    command.is_start = bool(dict['is_start'])
    return command


class MicroInstruction(Enum):
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
    LOAD_AR = 13
    CR_ADDR_TO_BUS = 14  # Выставляет адрес команды из CR на правый вход АЛУ

    # Чтение данных из памяти по AR
    WR_MEM = 15
    RD_MEM = 16

    # Управляющие сигналы АЛУ
    INV_L = 17  # Invert left
    INV_R = 18  # Invert right
    INC = 19  # Increment output
    AND = 20  # Binary AND (default do sum)
    SUM = 21  # Binary AND (default do sum)

    # Сигналы проверки флагов
    SET_NZ = 22  # Set sign and zero flags

    # Сигналы управляющих микрокоманд
    CHCK_ADDR_TYPE = 23  # Проверка типа адресации
    JUMP = 24  # Переход по адресу внутри памяти микрокоманд
    JUMP_TO_CR_OPCODE = 25  # Перейти на опкод инструкции
    JUMP_IF = 26  # Перейти если
    CHECK_Z = 27 # Проверить Z
    CHECK_N = 28 # Проверить N
    CHECK_nZ = 29 # Проверить не Z
    CHECK_nN = 30 # Проверить не N
    HLT = 31 # Завершение работы машины


class MicroCommand:
    is_control: bool
    signals: list[MicroInstruction]
    expression: bool
    value: int

    def __init__(self, is_control, signals, value=0, expression=False):
        self.is_control = is_control
        self.signals = signals
        self.value = value
        self.expression = expression


commands = {
    'nope': OpCode.NOPE,
    'add': OpCode.ADD,
    'sub': OpCode.SUB,
    'ld': OpCode.LD,
    'wr': OpCode.WR,
    'push': OpCode.PUSH,
    'pop': OpCode.POP,
    'call': OpCode.CALL,
    'ret': OpCode.RET,
    'cmp': OpCode.CMP,
    'jmp': OpCode.JMP,
    'je': OpCode.JE,
    'jne': OpCode.JNE,
    'jg': OpCode.JG,
    'jl': OpCode.JL,
    'hlt': OpCode.HLT
}
