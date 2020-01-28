import sys
from operator import add, mul, lt, eq
from copy import deepcopy as cpy
from itertools import permutations
import threading
from threading import Condition
import time


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

def run_prog(instrs, ins=None, outs=[], cvi=None, cvo=None,dbg=None):
        pc = 0
        #outs = []
        first = 1
        while True:
                if dbg:
                        print(dbg,'is running an instr',instrs[pc])
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
                        value = None
                        if cvi:
                                cvi.acquire()
                                while not(len(ins)):
                                        cvi.wait()
                                if dbg:
                                        print('ins:',ins)
                                value = ins.pop(0)
                                cvi.release()
                        else:
                                value = ins.pop(0)
                        if dbg and first == 1:
                                print('phase value:',value,ins)
                                first += 1
                        elif dbg:
                                print('input value:',value)
                                first += 2
                        instrs[dst] = value
                        next_instr += 2
                elif instr == 4:
                        value = instrs[pc+1] if modes[0] else instrs[instrs[pc+1]]
                        if cvo:
                                if dbg:
                                        while 1:
                                                if cvo.acquire(timeout=2):
                                                        break
                                                print('fucc')
                                else:
                                        cvo.acquire()
                                outs.append(value)
                                cvo.notify()
                                cvo.release()
                        else:
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
        #print(outs)
        if dbg:
                print(dbg,'is done')
        return (instrs, outs)

def part1():
        instrs = get_instrs('day-7.txt')
        res = 0
        for p in permutations(range(5)):
                ins = [0]
                for i in range(5):
                        outs = []
                        _,outs = run_prog(cpy(instrs), [p[i]]+ins, outs)
                        ins = outs
                res = max(res,ins[0])
        return res

def part2():
        instrs = get_instrs('day-7.txt')
        res = 0
        for p in permutations(range(5,10)):
                q1,q2,q3,q4,q5 = [p[0],0],[p[1]],[p[2]],[p[3]],[p[4]]
                cv1,cv2,cv3,cv4,cv5 = Condition(),Condition(),Condition(),Condition(),Condition()
                a = threading.Thread(group=None, target=run_prog, args=(instrs[:], q1, q2, cv1, cv2))
                b = threading.Thread(group=None, target=run_prog, args=(instrs[:], q2, q3, cv2, cv3))
                c = threading.Thread(group=None, target=run_prog, args=(instrs[:], q3, q4, cv3, cv4))
                d = threading.Thread(group=None, target=run_prog, args=(instrs[:], q4, q5, cv4, cv5))
                e = threading.Thread(group=None, target=run_prog, args=(instrs[:], q5, q1, cv5, cv1))
                a.start()
                b.start()
                c.start()
                d.start()
                e.start()
                e.join()
                #print('done')
                res = max(res, q1[0])
                #print(q1)
        return res
if __name__ == '__main__':
        print(part1())
        print(part2())