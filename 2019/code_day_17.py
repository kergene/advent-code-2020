from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


class IntCode:
    def __init__(self, lines):
        # the droid paramter is specific to this
        self.lines = lines.copy()
        self.index = 0
        self.relative_base = 0
        self.input = []
        self.input_index = 0

    @property
    def len(self):
        return len(self.lines)

    def extend(self, diff):
        self.lines += [0] * (diff + 1)

    def get_val(self, index, parameter):
        if index < 0:
            assert False, 'Index < 0'
        if index >= self.len:
            self.extend(index - self.len)
        if parameter == '2':
            # relative mode
            read_index = self.relative_base + self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            return self.lines[read_index]
        elif parameter == '1':
            # immediate mode
            return self.lines[index]
        elif parameter == '0':
            # position mode
            read_index = self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            return self.lines[read_index]
        else:
            assert False, parameter

    def set_val(self, index, parameter, value):
        if index < 0:
            assert False, 'Index < 0'
        if index >= self.len:
            self.extend(index - self.len)
        if parameter == '2':
            # relative mode
            read_index = self.relative_base + self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            self.lines[read_index] = value
        elif parameter == '1':
            # immediate mode
            self.lines[index] = value
        elif parameter == '0':
            # position mode
            read_index = self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            self.lines[read_index] = value
        else:
            assert False, parameter

    def run_intcode(self, *p_in):
        self.input += list(p_in)
        while True:
            opcode = str(self.lines[self.index])
            instruction = int(opcode[-2:])
            params = opcode[:-2]
            if instruction == 99:
                break
            elif instruction == 1:
                param_length = 3
                params = params.zfill(param_length)
                self.set_val(self.index + 3,
                             params[-3],
                             self.get_val(self.index + 1, params[-1]) + self.get_val(self.index + 2, params[-2]))
                self.index += param_length + 1
            elif instruction == 2:
                param_length = 3
                params = params.zfill(param_length)
                self.set_val(self.index + 3,
                             params[-3],
                             self.get_val(self.index + 1, params[-1]) * self.get_val(self.index + 2, params[-2]))
                self.index += param_length + 1
            elif instruction == 3:
                param_length = 1
                params = params.zfill(param_length)
                self.set_val(self.index + 1, params[-1], self.input[self.input_index])
                self.input_index += 1
                self.index += param_length + 1
            elif instruction == 4:
                param_length = 1
                params = params.zfill(param_length)
                output = self.get_val(self.index + 1, params[-1])
                self.index += param_length + 1
                return 0, output
            elif instruction == 5:
                param_length = 2
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]):
                    self.index = self.get_val(self.index + 2, params[-2])
                else:
                    self.index += param_length + 1
            elif instruction == 6:
                param_length = 2
                params = params.zfill(param_length)
                if not self.get_val(self.index + 1, params[-1]):
                    self.index = self.get_val(self.index + 2, params[-2])
                else:
                    self.index += param_length + 1
            elif instruction == 7:
                param_length = 3
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]) < self.get_val(self.index + 2, params[-2]):
                    self.set_val(self.index + 3, params[-3], 1)
                else:
                    self.set_val(self.index + 3, params[-3], 0)
                self.index += param_length + 1
            elif instruction == 8:
                param_length = 3
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]) == self.get_val(self.index + 2, params[-2]):
                    self.set_val(self.index + 3, params[-3], 1)
                else:
                    self.set_val(self.index + 3, params[-3], 0)
                self.index += param_length + 1
            elif instruction == 9:
                param_length = 1
                params = params.zfill(param_length)
                self.relative_base += self.get_val(self.index + 1, params[-1])
                self.index += param_length + 1
            else:
                assert False, instruction
        return 1, 0


class ScaffoldRobot:
    def __init__(self, data):
        self.machine = IntCode(data)
        self.view = []

    def run_droid(self):
        while True:
            exit_code, out = self.machine.run_intcode()
            if exit_code:
                break
            else:
                self.view.append(out)

    def __str__(self):
        view = [chr(i) for i in self.view]
        return ''.join(view[:-1])
    
    def define_grid(self):
        view = self.__str__()
        self.grid = view.splitlines()
    
    def find_intersections(self):
        self.define_grid()
        DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))
        n_rows = len(self.grid)
        n_cols = len(self.grid[0])
        tot = 0
        for r in range(n_rows):
            for c in range(n_cols):
                if self.grid[r][c] == '#':
                    for dr, dc in DIRECTIONS:
                        intersection = False
                        a, b = r + dr, c + dc
                        if 0 <= a < n_rows and 0 <= b < n_cols:
                            if self.grid[a][b] == '#':
                                intersection = True
                        if not intersection:
                            break
                    if intersection:
                        tot += r * c
        return tot
    
    def use_robot(self, input_strings):
        target = []
        for input_string in input_strings:
            for char in input_string:
                target.append(ord(char))
            target.append(10)
        while True:
            exit_code, out = self.machine.run_intcode(*target)
            if exit_code:
                break
            else:
                self.view.append(out)
                self.answer = out
        return self.answer


def alignment_params(data):
    scaffolds = ScaffoldRobot(data)
    scaffolds.run_droid()
    print(scaffolds)
    return scaffolds.find_intersections()


def collect_dust(data):
    scaffolds = ScaffoldRobot(data)
    scaffolds.machine.set_val(0,'1',2)
    input_strings = ['A,A,B,C,B,C,B,C,A,C',
                     'R,6,L,8,R,8',
                     'R,4,R,6,R,6,R,4,R,4',
                     'L,8,R,6,L,10,L,10',
                     'n']
    return scaffolds.use_robot(input_strings)


def main():
    year, day = 2019, 17
    data = get_data(year, day)
    print(alignment_params(data))
    print(collect_dust(data))


if __name__ == "__main__":
    main()
