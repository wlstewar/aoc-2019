def part1(fn):
        with open(fn) as f:
                line = f.readline().rstrip()
                chunk = 25 * 6
                idx = 0
                fewest = (25 * 6 + 1, idx)
                l = line[idx:idx+chunk]
                while len(l):
                        fewest = min(fewest, (l.count('0'), idx), key=lambda x:x[0])
                        idx += chunk
                        l = line[idx:idx+chunk]
                l = line[fewest[1]:fewest[1]+chunk]
                return l.count('2') * l.count('1')

def part2(fn,x,y):
        line = ''
        with open(fn) as f:
                line = f.readline().rstrip()
        img = [2 for _ in range(x * y)]
        idx = 0
        for chunk in range(len(line) // (x * y)):
                for i in range(idx,(x*y)+idx):
                        if img[i - idx] == 2:
                                img[i - idx] = int(line[i])
                if img.count(2) == 0:
                        break
                idx += x * y
        for i in range(y):
                for j in range(x):
                        pixel = img[(x * i) + j]
                        if img[x * i + j] == 2:
                                print('_',end='')
                        elif pixel == 1:
                                print('@',end='')
                        else:
                                print(' ',end='')
                print('')

if __name__ == '__main__':
        print(part1('day-8.txt'))
        part2('day-8.txt',25,6)