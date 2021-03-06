def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def take_step(data, n):
    new_data = [row.copy() for row in data]
    DIRECTIONS = (
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1, -1), ( 1,  0), ( 1,  1),
    )
    for r in range(n):
        for c in range(n):
            if data[r][c] == '.':
                trees = 0
                for dr, dc in DIRECTIONS:
                    a, b = r + dr, c + dc
                    if 0 <= a < n and 0 <= b < n:
                        if data[a][b] == '|':
                            trees += 1
                if trees >= 3:
                    new_data[r][c] = '|'
            elif data[r][c] == '|':
                lumbers = 0
                for dr, dc in DIRECTIONS:
                    a, b = r + dr, c + dc
                    if 0 <= a < n and 0 <= b < n:
                        if data[a][b] == '#':
                            lumbers += 1
                if lumbers >= 3:
                    new_data[r][c] = '#'
            elif data[r][c] == '#':
                trees = lumbers = 0
                for dr, dc in DIRECTIONS:
                    a, b = r + dr, c + dc
                    if 0 <= a < n and 0 <= b < n:
                        if data[a][b] == '|':
                            trees += 1
                        elif data[a][b] == '#':
                            lumbers += 1
                if trees == 0 or lumbers == 0:
                    new_data[r][c] = '.'
            else:
                assert False, data[r][c]
    return new_data


def resource_value(data):
    woodlands = lumberyards = 0
    for row in data:
        for acre in row:
            if acre == '|':
                woodlands += 1
            elif acre == '#':
                lumberyards += 1
    return woodlands * lumberyards


def tree_sim(data):
    n = len(data)
    for _ in range(10):
        data = take_step(data, n)
    return resource_value(data)


def fast_forward(data):
    n = len(data)
    seens = {}
    minute = 0
    while True:
        hashable = ''.join(''.join(row) for row in data)
        if hashable in seens:
            first = seens[hashable]
            second = minute
            break
        else:
            seens[hashable] = minute
            minute += 1
            data = take_step(data, n)
    gap = second - first
    remainder = (10 ** 9 - first) % gap
    for _ in range(remainder):
        data = take_step(data, n)
    return resource_value(data)


def main():
    year, day = 2018, 18
    data = get_data(year, day)
    print(tree_sim(data))
    print(fast_forward(data))


if __name__ == "__main__":
    main()
