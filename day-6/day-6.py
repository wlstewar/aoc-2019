def get_system(fn):
        system = {}
        system['COM'] = None
        with open(fn) as f:
                for l in f:
                        l = l.rstrip()
                        i = l.index(')')
                        system[l[i+1:]] = l[0:i]
        return system

def get_path(system, key):
        path = []
        while key:
                path.append(key)
                key = system[key]
        return path

def part1(system):
        total = 0
        for key in system:
                k = key
                while k:
                        total += 1
                        k = system[k]
                total -= 1
        return total

def part2(system):
        you_path = get_path(system, 'YOU')
        san_path = get_path(system, 'SAN')
        x = 0
        node = None # unnecessary but we need to save the node from the loop
        for node in you_path:
                if node in san_path:
                        break
                x += 1
        # subtract 2, 1 because we don't need to move from our current orbiting pos
        # and 1 because we double count the intersecting node
        return x + san_path.index(node) - 2

if __name__ == '__main__':
        system = get_system('day-6.txt')
        print(part1(system))
        print(part2(system))