import sys

def get_lines(fn):
        with open(fn) as f:
                wire1 = {'H':[], 'V':[]}
                wire2 = {'H':[], 'V':[]}
                i = False
                for line in f:
                        cur = None
                        if i:
                                cur = wire2
                        else:
                                cur = wire1
                        x = 0
                        y = 0
                        length = 0
                        for seg in line.split(','):
                                sign = -1 if seg[0] in ['L','D'] else 1
                                if seg[0] in ['R','L']:
                                        l = int(seg[1:])
                                        length += l
                                        cur['H'].append(((x, y), (x + sign * l, y), length))
                                        x += sign * l
                                else:
                                        l = int(seg[1:])
                                        length += l
                                        cur['V'].append(((x, y), (x, y + sign * l), length))
                                        y += sign * l
                        i = True
                return (wire1, wire2)

def get_shortest_point(horiz, vert):
        for (x1,x2,l_x) in horiz:
                x_hi = max(x1[0], x2[0])
                x_lo = min(x1[0], x2[0])
                for (y1,y2,l_y) in vert:
                        for x_cross in range(x_lo,x_hi+1):
                                if y1[0] == x_cross:
                                        y_hi = max(y1[1],y2[1])
                                        y_lo = min(y1[1],y2[1])
                                        for y_cross in range(y_lo, y_hi + 1):
                                                if x1[1] == y_cross:
                                                        # found an intersection, calc manhattan dist and total wire len
                                                        if x_cross != 0 or y_cross != 0:
                                                                yield (abs(x_cross) + abs(y_cross), l_x - abs(x_cross - x2[0]) + l_y - abs(y_cross - y2[1]))

def get_shortest_points(wire1, wire2):
        return [dist for dist in get_shortest_point(wire1['H'], wire2['V'])] + \
               [dist for dist in get_shortest_point(wire2['H'], wire1['V'])]

def day_3():
        wire1, wire2 = get_lines('day-3.txt')
        res = get_shortest_points(wire1, wire2)
        print(min(res, key=lambda x: x[0]))
        print(min(res, key=lambda x: x[1]))
if __name__ == '__main__':
        day_3()