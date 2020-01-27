import sys

def part1():
        with open('day-1.txt') as f:
                total = 0
                for line in f:
                        x = int(line)
                        total += x // 3 - 2
                print(total)

def part2():
        with open('day-1.txt') as f:
                total = 0
                for line in f:
                        x = int(line)
                        while x > 0:
                                total += max(x // 3 - 2,0)
                                x = x // 3 - 2
                print(total)

part = part1
try:
        if sys.argv[1] == '1':
                part = part1
        elif sys.argv[1] == '2':
                part = part2
except:
        pass

if __name__ == '__main__':
        part()