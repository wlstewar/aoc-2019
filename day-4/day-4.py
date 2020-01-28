lo, hi = 123257, 647015

'''

abusing the fact that we always have a six digit number:

hundred thousands => i // 100000 % 10
ten thousands     => i // 10000 % 10
thousands         => i // 1000 % 10
hundreds          => i // 100 % 10
tens              => i // 10 % 10
ones              => i % 10

'''


def part1():
        count = 0
        for v in range(lo, hi+1):
                double, inc = False, True
                digits = [v // (10**i) % 10 for i in reversed(range(6))]
                for i in range(1,6):
                        if digits[i-1] > digits[i]:
                                inc = False
                                break
                        if digits[i-1] == digits[i]:
                                double = True
                if double and inc:
                        count += 1
        return count

def part2():
        count = 0
        for v in range(lo, hi+1):
                double, inc = False, True
                digits = [v // (10**i) % 10 for i in reversed(range(6))]
                stk = [digits[0]]
                for i in range(1,6):
                        if digits[i-1] > digits[i]:
                                inc = False
                                break
                        if digits[i] == stk[0]:
                                stk.append(digits[i])
                        else:
                                if len(stk) == 2:
                                        double = True
                                stk = [digits[i]]
                if len(stk) == 2:
                        double = True
                if double and inc:
                        count += 1
        return count
if __name__ == '__main__':
        print(part1())
        print(part2())