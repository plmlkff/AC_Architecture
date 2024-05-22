from __future__ import annotations

import json
import logging
import re
import sys
from io import TextIOWrapper
from random import randint
from impl.BasicTypes import AddressingType, Command, MicroCommand, MicroInstruction, OpCode, dictToCommand


class ALU:
    N: int = 0
    Z: int = 0
    right_bus: int | Command = 0
    left_bus: int | Command = 0
    out_bus: int | Command = 0

    def invert_left(self):
        if isinstance(self.left_bus, Command): self.left_bus = self.left_bus.op_code.value
        self.left_bus = ~self.left_bus

    def invert_right(self):
        if isinstance(self.right_bus, Command): self.right_bus = self.right_bus.op_code.value
        self.right_bus = ~self.right_bus

    def sum(self):
        if self.left_bus == 0 or self.right_bus == 0:
            self.out_bus = self.left_bus if self.left_bus != 0 else self.right_bus
        else:
            if isinstance(self.left_bus, Command): self.left_bus = self.left_bus.op_code.value
            if isinstance(self.right_bus, Command): self.right_bus = self.right_bus.op_code.value
            self.out_bus = self.right_bus + self.left_bus
        self.left_bus = 0
        self.right_bus = 0

    def and_(self):
        if isinstance(self.left_bus, Command): self.left_bus = self.left_bus.op_code.value
        if isinstance(self.right_bus, Command): self.right_bus = self.right_bus.op_code.value
        self.out_bus = self.right_bus & self.left_bus
        self.left_bus = 0
        self.right_bus = 0

    def inc(self):
        if isinstance(self.out_bus, Command): self.out_bus = self.out_bus.op_code.value
        self.out_bus = self.out_bus + 1

    def set_NZ(self):
        if isinstance(self.out_bus, Command): self.out_bus = self.out_bus.op_code.value
        self.N = self.out_bus < 0
        self.Z = self.out_bus == 0


class AddressDecoder:
    MEMORY_ACCESS_TIME: int = 10
    CACHE_LINES_COUNT: int = 0
    INPUT_MAPPED: int = 1023
    OUTPUT_MAPPED: int = 1022
    MEM_SIZE = 1024
    input_buffer: list[int | str] = []
    output_buffer: list[str] = []
    mem: list[int | Command] = []
    cache: {int: Command | int}

    def __init__(self, mem, input_buffer):
        self.mem = mem
        self.cache = {}
        self.input_buffer = input_buffer
        self.output_buffer = []

    def get(self, address: int, tick_log_callback):
        if address < 0:
            address = self.MEM_SIZE + address
        if address == self.INPUT_MAPPED:
            if len(self.input_buffer) == 0:
                raise Exception("Buffer is empty!")
            for i in range(self.MEMORY_ACCESS_TIME):
                tick_log_callback("MEMORY ACCESS TICK")
            stream_val = self.input_buffer.pop(0)
            return stream_val if isinstance(stream_val, int) else ord(stream_val)
        if address in self.cache:
            tick_log_callback("CACHE ACCESS TICK")
            return self.cache[address]
        else:
            if len(self.cache) == self.CACHE_LINES_COUNT and self.CACHE_LINES_COUNT != 0:
                tick_log_callback("CACHE DELETE TICK")
                del self.cache[list(self.cache.keys())[randint(0, self.CACHE_LINES_COUNT - 1)]]
            if self.CACHE_LINES_COUNT != 0:
                self.cache[address] = self.mem[address]
            for i in range(self.MEMORY_ACCESS_TIME):
                tick_log_callback("MEMORY ACCESS TICK")
            return self.mem[address]

    def set(self, address: int, value: int | Command, tick_log_callback):
        if address < 0:
            address = self.MEM_SIZE + address
        if address == self.OUTPUT_MAPPED:
            for i in range(self.MEMORY_ACCESS_TIME):
                tick_log_callback("MEMORY ACCESS TICK")
            self.output_buffer.append(chr(value))
        if address in self.cache:
            tick_log_callback("CACHE WRITE TICK")
            self.cache[address] = value
        for i in range(self.MEMORY_ACCESS_TIME):
            tick_log_callback("MEMORY ACCESS TICK")
        self.mem[address] = value


class ACCopm:
    alu: ALU
    address_decoder: AddressDecoder
    mem_bus: int | Command = 0
    DR_bus_selector: bool = False
    AC: int = 0
    BR: int | Command = 0
    DR: int | Command = 0
    CR: int | Command = Command("nope", OpCode.NOPE)
    SP: int | Command = -3
    IP: int | Command = 0
    AR: int = 0

    def __init__(self, alu: ALU, address_decoder: AddressDecoder):
        self.alu = alu
        self.address_decoder = address_decoder

    def latch_AC(self):
        if isinstance(self.alu.out_bus, Command): self.alu.out_bus = self.alu.out_bus.op_code.value
        self.AC = self.alu.out_bus

    def latch_BR(self):
        self.BR = self.alu.out_bus

    def latch_DR(self):
        if self.DR_bus_selector:
            self.DR = self.mem_bus
        else:
            self.DR = self.alu.out_bus
        self.DR_bus_selector = False  # Переключаем шину снова на основную шину из АЛУ

    def latch_CR(self):
        self.CR = self.alu.out_bus

    def latch_SP(self):
        self.SP = self.alu.out_bus

    def latch_IP(self):
        self.IP = self.alu.out_bus

    def latch_AR(self):
        if isinstance(self.alu.out_bus, Command): self.alu.out_bus = self.alu.out_bus.op_code.value
        self.AR = self.alu.out_bus
        if self.AR > 1023: raise Exception("AR out of bounds")

    def rd_mem(self, tick_call_back):
        self.mem_bus = self.address_decoder.get(self.AR, tick_call_back)
        self.DR_bus_selector = True

    def wr_mem(self, tick_call_back):
        self.address_decoder.set(self.AR, self.DR, tick_call_back)

    def load_AC(self):
        self.alu.left_bus = self.AC

    def load_BR(self):
        self.alu.left_bus = self.BR

    def load_DR(self):
        self.alu.right_bus = self.DR

    def load_CR(self):
        self.alu.right_bus = self.CR

    def load_SP(self):
        self.alu.right_bus = self.SP

    def load_IP(self):
        self.alu.right_bus = self.IP

    def CR_addr_to_bus(self):
        self.alu.right_bus = self.CR.address


class ControlUnit:
    INSTR_FETCH = 0
    OPERAND_FETCH_INDEX = 18
    POST_EXECUTION_INDEX = 69

    mIP: int = 0  # Micro memory IP
    comp: ACCopm
    microcode_mem: list[MicroCommand]
    ticks_counter: int = 0
    f: TextIOWrapper

    def __init__(self, comp: ACCopm, f):
        self.comp = comp
        self.microcode_mem = [
            # Instruction fetch
            MicroCommand(False, [MicroInstruction.LOAD_IP, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 0: IP -> AR
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 1: MEM(AR) -> DR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_CR]),  # 2: DR -> CR
            # Address fetch
            MicroCommand(True, [MicroInstruction.CHCK_ADDR_TYPE]),  # 3: ADDR_TYPE handler addr -> mIP
            # Absolute straight
            MicroCommand(False, [MicroInstruction.CR_ADDR_TO_BUS, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 4: CR(address) -> AR
            MicroCommand(True, [MicroInstruction.JUMP], self.OPERAND_FETCH_INDEX),  # 5: To operand fetch
            # Straight relative
            MicroCommand(False, [MicroInstruction.CR_ADDR_TO_BUS, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_BR]),  # 6: CR(address) -> BR
            MicroCommand(False, [MicroInstruction.LOAD_IP, MicroInstruction.LOAD_BR,
                                 MicroInstruction.SUM, MicroInstruction.LATCH_AR]),  # 7: BR + IP -> AR
            MicroCommand(True, [MicroInstruction.JUMP], self.OPERAND_FETCH_INDEX),  # 8: To operand fetch
            # Indirect straight
            MicroCommand(False, [MicroInstruction.CR_ADDR_TO_BUS, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 9: CR(address) -> AR
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 10: MEM(AR) -> DR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 11: DR -> AR
            MicroCommand(True, [MicroInstruction.JUMP], self.OPERAND_FETCH_INDEX),  # 12: To operand fetch
            #  Stack relative
            MicroCommand(False, [MicroInstruction.CR_ADDR_TO_BUS, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_BR]),  # 13: CR(address) -> BR
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.LOAD_BR,
                                 MicroInstruction.SUM, MicroInstruction.LATCH_AR]),  # 14: BR + SP -> AR
            MicroCommand(True, [MicroInstruction.JUMP], self.OPERAND_FETCH_INDEX),  # 15: To operand fetch
            # Direct load
            MicroCommand(False, [MicroInstruction.CR_ADDR_TO_BUS, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_DR]),  # 16: CR(address) -> DR
            MicroCommand(True, [MicroInstruction.JUMP_TO_CR_OPCODE]),  # 17: Jump to command execution
            # Operand fetch
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 18: MEM(AR) -> DR
            MicroCommand(True, [MicroInstruction.JUMP_TO_CR_OPCODE]),  # 19: Jump to command execution
            # add
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.LOAD_AC,
                                 MicroInstruction.SUM, MicroInstruction.SET_NZ,
                                 MicroInstruction.LATCH_AC]),  # 20: DR + AC -> AC & SET N,V
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 21: Post-exec -> mIP
            # sub
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.LOAD_AC,
                                 MicroInstruction.INV_R, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.SET_NZ,
                                 MicroInstruction.LATCH_AC]),  # 22: ~DR + AC + 1 -> AC & SET N,V
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 23: Post-exec -> mIP
            # ld
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AC]),  # 24: DR -> AC
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 25: Post-exec -> mIP
            # wr
            MicroCommand(False, [MicroInstruction.LOAD_AC, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_DR, MicroInstruction.WR_MEM]),  # 26: AC -> DR -> MEM(AR)
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 27: Post-exec -> mIP
            # push
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.INV_L,
                                 MicroInstruction.SUM, MicroInstruction.LATCH_SP,
                                 MicroInstruction.LATCH_AR]),  # 28: SP + ~0 -> SP, AR
            MicroCommand(False, [MicroInstruction.LOAD_AC, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_DR, MicroInstruction.WR_MEM]),  # 29: AC -> DR -> MEM(AR)
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 30: Post-exec -> mIP
            # pop
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 31: SP -> AR
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 32: MEM(AR) -> DR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AC]),  # 33: DR -> AC
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.LATCH_SP]),  # 34: SP + 1 -> SP
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 35: Post-exec -> mIP
            # swap
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 36: SP -> AR
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 37: MEM(AR) -> DR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_BR]),  # 38: DR -> BR
            MicroCommand(False, [MicroInstruction.LOAD_AC, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_DR, MicroInstruction.WR_MEM]),  # 39: AC -> DR -> MEM(AR)
            MicroCommand(False, [MicroInstruction.LOAD_BR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AC]),  # 40: BR -> AC
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 41: Post-exec -> mIP
            # call (use with direct load by default)
            MicroCommand(False, [MicroInstruction.LOAD_IP, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.LATCH_BR]),  # 42: IP + 1 -> BR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 43: DR -> IP
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.INV_L,
                                 MicroInstruction.SUM, MicroInstruction.LATCH_SP,
                                 MicroInstruction.LATCH_AR]),  # 44: SP + ~0 -> SP, AR
            MicroCommand(False, [MicroInstruction.LOAD_BR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_DR, MicroInstruction.WR_MEM]),  # 45: BR -> DR -> MEM(AR)
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 46: 0 -> mIP
            # ret
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_AR]),  # 47: SP -> AR
            MicroCommand(False, [MicroInstruction.RD_MEM, MicroInstruction.LATCH_DR]),  # 48: MEM(AR) -> DR
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 49: DR -> IP
            MicroCommand(False, [MicroInstruction.LOAD_SP, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.LATCH_SP]),  # 50: SP + 1 -> SP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 51: 0 -> mIP
            # cmp
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.LOAD_AC,
                                 MicroInstruction.INV_R, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.SET_NZ]),  # 52: AC + ~DR + 1 -> SET N,V
            MicroCommand(True, [MicroInstruction.JUMP], self.POST_EXECUTION_INDEX),  # 53: Post-exec -> mIP
            # jmp use with direct load of address by default
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 54: DR -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 55: 0 -> mIP
            # je use with direct load of address by default
            MicroCommand(True, [MicroInstruction.JUMP_IF, MicroInstruction.CHECK_nZ],
                         self.POST_EXECUTION_INDEX),  # 56: if not Zero -> Post-exec
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 57: DR -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 58: 0 -> mIP
            # jne use with direct load of address by default
            MicroCommand(True, [MicroInstruction.JUMP_IF, MicroInstruction.CHECK_Z],
                         self.POST_EXECUTION_INDEX),  # 59: if Zero -> Post-exec
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 60: DR -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 61: 0 -> mIP
            # jg use with direct load of address by default
            MicroCommand(True, [MicroInstruction.JUMP_IF, MicroInstruction.CHECK_N,
                                MicroInstruction.CHECK_Z], self.POST_EXECUTION_INDEX),
            # 62: if Sign or Zero -> Post-exec
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 63: DR -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 64: 0 -> mIP
            # jl use with direct load of address by default
            MicroCommand(True, [MicroInstruction.JUMP_IF, MicroInstruction.CHECK_nN,
                                MicroInstruction.CHECK_Z], self.POST_EXECUTION_INDEX),
            # 65: if not Sign or Zero -> Post-exec
            MicroCommand(False, [MicroInstruction.LOAD_DR, MicroInstruction.SUM,
                                 MicroInstruction.LATCH_IP]),  # 66: DR -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH),  # 67: 0 -> mIP
            # hlt
            MicroCommand(True, [MicroInstruction.HLT]),  # 68: stop impl
            # Post-execution
            MicroCommand(False, [MicroInstruction.LOAD_IP, MicroInstruction.SUM,
                                 MicroInstruction.INC, MicroInstruction.LATCH_IP]),  # 69: IP + 1 -> IP
            MicroCommand(True, [MicroInstruction.JUMP], self.INSTR_FETCH)  # 70: 0 -> mIP
        ]
        self.f = f

    def start(self):
        while self.process_mc():
            continue

    # Функция выполняет очередную команду, возращает True, если не было Hlt и False, если был (надо ли продолжать)
    def process_mc(self):
        self.tick_log()
        mc = self.microcode_mem[self.mIP]
        if mc.is_control:
            if MicroInstruction.CHCK_ADDR_TYPE in mc.signals:
                if isinstance(self.comp.CR, int):  # Если в CR попало числовое значение - пропускаем
                    self.mIP = self.POST_EXECUTION_INDEX
                    return True
                addr_type = self.comp.CR.addressing_type
                if addr_type == AddressingType.ABSOLUTE_STRAIGHT:
                    self.mIP += 1
                    return True
                if addr_type == AddressingType.STRAIGHT_RELATIVE:
                    self.mIP = 6
                    return True
                if addr_type == AddressingType.INDIRECT_STRAIGHT:
                    self.mIP = 9
                    return True
                if addr_type == AddressingType.STACK_RELATIVE:
                    self.mIP = 13
                    return True
                if addr_type == AddressingType.DIRECT_LOAD:
                    self.mIP = 16
                    return True
                if addr_type == AddressingType.NO_ADDRESS:
                    self.mIP = 18
            if MicroInstruction.JUMP in mc.signals:
                self.mIP = mc.value
                return True
            if MicroInstruction.JUMP_TO_CR_OPCODE in mc.signals:
                self.mIP = self.comp.CR.op_code.value
                return True
            if MicroInstruction.JUMP_IF in mc.signals:
                check_res = False
                if MicroInstruction.CHECK_nZ in mc.signals and self.comp.alu.Z == 0:
                    check_res = True
                if MicroInstruction.CHECK_Z in mc.signals and self.comp.alu.Z == 1:
                    check_res = True
                if MicroInstruction.CHECK_nN in mc.signals and self.comp.alu.N == 0:
                    check_res = True
                if MicroInstruction.CHECK_N in mc.signals and self.comp.alu.N == 1:
                    check_res = True
                self.mIP = mc.value if check_res else self.mIP + 1
                return True
            if MicroInstruction.HLT in mc.signals:
                return False
        else:
            if MicroInstruction.LOAD_AC in mc.signals:
                self.comp.load_AC()
            if MicroInstruction.LOAD_BR in mc.signals:
                self.comp.load_BR()
            if MicroInstruction.LOAD_DR in mc.signals:
                self.comp.load_DR()
            if MicroInstruction.LOAD_SP in mc.signals:
                self.comp.load_SP()
            if MicroInstruction.LOAD_CR in mc.signals:
                self.comp.load_CR()
            if MicroInstruction.LOAD_IP in mc.signals:
                self.comp.load_IP()
            if MicroInstruction.CR_ADDR_TO_BUS in mc.signals:
                self.comp.CR_addr_to_bus()
            if MicroInstruction.RD_MEM in mc.signals:
                self.comp.rd_mem(self.tick_log)

            if MicroInstruction.INV_L in mc.signals:
                self.comp.alu.invert_left()
            if MicroInstruction.INV_R in mc.signals:
                self.comp.alu.invert_right()
            if MicroInstruction.AND in mc.signals:
                self.comp.alu.and_()
            if MicroInstruction.SUM in mc.signals:
                self.comp.alu.sum()
            if MicroInstruction.INC in mc.signals:
                self.comp.alu.inc()
            if MicroInstruction.SET_NZ in mc.signals:
                self.comp.alu.set_NZ()
            if MicroInstruction.LATCH_AC in mc.signals:
                self.comp.latch_AC()
            if MicroInstruction.LATCH_BR in mc.signals:
                self.comp.latch_BR()
            if MicroInstruction.LATCH_DR in mc.signals:
                self.comp.latch_DR()
            if MicroInstruction.LATCH_SP in mc.signals:
                self.comp.latch_SP()
            if MicroInstruction.LATCH_CR in mc.signals:
                self.comp.latch_CR()
            if MicroInstruction.LATCH_IP in mc.signals:
                self.comp.latch_IP()
            if MicroInstruction.LATCH_AR in mc.signals:
                try:
                    self.comp.latch_AR()
                except Exception as e:
                    print(e)
                    return False
            if MicroInstruction.WR_MEM in mc.signals:
                self.comp.wr_mem(self.tick_log)
        self.mIP += 1
        return True

    def tick_log(self, info: str = ""):
        log = (f"Tick #{self.ticks_counter}: {info} mIP: {self.mIP}; AC: {self.comp.AC}; BR: {self.comp.BR}; "
               f"DR: {self.comp.DR}; SP: {self.comp.SP}; CR: {self.comp.CR}; IP: {self.comp.IP}; "
               f"AR: {self.comp.AR}; N: {self.comp.alu.N}; Z: {self.comp.alu.Z}")
        logging.debug(log)
        self.f.write(log + "\n")
        self.ticks_counter += 1


def check_start(mem: list[Command | int]):
    for i in range(len(mem)):
        if isinstance(mem[i], Command) and mem[i].is_start:
            return i
    return 0


def main(code, input_stream, output):
    logging.getLogger().setLevel(logging.DEBUG)
    mem = json.load(open(code), object_hook=dictToCommand)
    input_str = open(input_stream).read()  # Считываем файл в строку
    input_len = re.findall(r"^\d+(?=[^\d])", input_str)[0]  # Парсим регуляркой длину входного потока
    input_str = input_str.replace(input_len, "", 1)  # Убираем длину вхожного потока из входной строки
    input: list[int | str] = [int(input_len)] + list(input_str)  # Помещаем во входной буффер его длину + содержание
    alu = ALU()
    address_decoder = AddressDecoder(mem, input)
    comp = ACCopm(alu, address_decoder)
    comp.IP = check_start(mem)
    with open(output, "w") as f:
        cu = ControlUnit(comp, f)
        cu.start()
    print("".join(address_decoder.output_buffer))
    print(f"Ticks count: {cu.ticks_counter - 1}")


if __name__ == "__main__":
    _, code, input_stream, output = sys.argv
    main(code, input_stream, output)
