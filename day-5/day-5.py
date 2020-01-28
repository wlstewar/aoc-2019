import sys
from operator import add, mul, lt, eq
from copy import deepcopy as cpy

class Mode_List(list):
        def __getitem__(self,key):
                try:
                        return super().__getitem__(key)
                except Exception as error:
                        return 0

def get_instrs(fn):
        instrs = []
        with open(fn) as f:
                for line in f:
                        instrs += [int(instr) for instr in line.split(',')]
                return instrs

def get_modes(instr):
        modes = Mode_List([])
        while(instr):
                modes.append(instr % 10)
                instr //= 10
        return modes

def decode(instr):
        if instr == 1:
                return add
        elif instr == 2:
                return mul
        elif instr == 7:
                return lt
        elif instr == 8:
                return eq

def run_prog(instrs, ins=None):
        pc = 0
        outs = []
        while True:
                instr = instrs[pc] % 100
                modes = get_modes(instrs[pc] // 100)
                next_instr = pc
                if instr in [1, 2, 7, 8]:
                        op = decode(instr)
                        op1 = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        op2 = instrs[pc+2] if modes[1] else instrs[instrs[pc+2]]
                        dst = instrs[pc+3]
                        instrs[dst] = op(op1,op2)
                        next_instr += 4
                elif instr == 3:
                        '''
                        TODO: revisit this later, instruction 3 should be able to work in position mode, right?
                        dst = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        '''
                        dst = instrs[pc+1]
                        value = next(ins)
                        instrs[dst] = value
                        next_instr += 2
                elif instr == 4:
                        value = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        outs.append(value)
                        next_instr += 2
                elif instr in [5, 6]:
                        j = instr & 1
                        cond = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        jmp_addr = instrs[pc+2] if modes[1] else instrs[instrs[pc+2]]
                        if cond:
                                next_instr = jmp_addr if j else pc + 3
                        else:
                                next_instr = pc + 3 if j else jmp_addr
                elif instr == 99:
                        break
                else:
                        print('ILLEGAL INSTRUCTION:',instrs[pc])
                        break
                pc = next_instr
        return (instrs, outs)

def part1():
        instrs = get_instrs('day-5.txt')
        instrs_1, outs_1 = run_prog(cpy(instrs), ins=iter([1]))
        instrs_2, outs_2 = run_prog(instrs, ins=iter([5]))
        print('output values (part 1):')
        for o in outs_1:
                print("\t",o,sep='')
        print('\npart 1 pos 0:',instrs_1[0],end='\n\n')
        print('output values (part 2):')
        for o in outs_2:
                print("\t",o,sep='')
        print('\npart 2 pos 0:',instrs_2[0])

if __name__ == '__main__':
        part1()