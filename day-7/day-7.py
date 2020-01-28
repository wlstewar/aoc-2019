import sys
from operator import add, mul, lt, eq
from copy import deepcopy as cpy
from itertools import permutations

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
                        instrs += [int(instr) for instr in line.rstrip().split(',') if instr != '']
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
        instrs = get_instrs('day-7.txt')
        res = 0
        for p in permutations(range(5)):
                ins = [0]
                for i in range(5):
                        _,outs = run_prog(cpy(instrs), iter([p[i]]+ins))
                        ins = outs
                res = max(res,ins[0])
        return res

if __name__ == '__main__':
        print(part1())