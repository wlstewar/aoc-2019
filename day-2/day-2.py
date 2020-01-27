import sys
from operator import add, mul
from copy import deepcopy as cpy

def get_instrs(fn):
        instrs = []
        with open(fn) as f:
                for line in f:
                        instrs += [int(instr) for instr in line.split(',')]
                return instrs

def get_modes(instr):
        modes = []
        while(instr):
                modes.append(instr % 10)
                instr //= 10
        return modes

def run_prog(instrs, ins=None):
        pc = 0
        while True:
                instr = instrs[pc] % 100
                modes = get_modes(instrs[pc] // 100)
                next_instr = pc
                if instr == 1 or instr == 2:
                        op = add if instr == 1 else mul
                        try:
                                op1 = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        except:
                                op1 = instrs[instrs[pc+1]]
                        try:
                                op2 = instrs[pc+2] if modes[1] else instrs[instrs[pc+2]]
                        except:
                                op2 = instrs[instrs[pc+2]]
                        dst = instrs[pc+3]
                        instrs[dst] = op(op1,op2)
                        next_instr += 4
                elif instr == 99:
                        break
                pc = next_instr
        return instrs

def part1():
        instrs = get_instrs('day-2.txt')
        instrs = run_prog(instrs)
        print(instrs[0])

def part2():
        instrs = get_instrs('day-2.txt')
        goal = 19690720
        for noun in range(100):
                for verb in range(100):
                        arg = cpy(instrs)
                        arg[1] = noun
                        arg[2] = verb
                        ret = run_prog(arg )
                        if ret[0] == goal:
                                print(noun * 100 + verb)
                                return

if __name__ == '__main__':
        try:
                if sys.argv[1] == '1':
                        part1()
                elif sys.argv[1] == '2':
                        part2()
        except:
                part2()