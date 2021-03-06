def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def find_brackets(string):
    start_idx = string.index('(')
    count = 0
    for i in range(start_idx, len(string)):
        if string[i] == '(':
            count += 1
        elif string[i] == ')':
            count -= 1
            if count == 0:
                end_idx = i
                return start_idx, end_idx


def ltr_eval(string):
    if '(' in string:
        start_idx, end_idx = find_brackets(string)
        return ltr_eval(string[:start_idx]
            + str(ltr_eval(string[start_idx + 1:end_idx]))
            + string[end_idx + 1:])
    else:
        line = string.split(' ', 3)
        if len(line) == 4:
            return ltr_eval(str(eval(''.join(line[:3]))) + ' ' + line[3])
        else:
            return eval(string)


def left_to_right(data):
    return sum(ltr_eval(line) for line in data)


def switched_eval(string):
    if '(' in string:
        start_idx, end_idx = find_brackets(string)
        return switched_eval(string[:start_idx]
            + str(switched_eval(string[start_idx + 1:end_idx]))
            + string[end_idx + 1:])
    else:
        if '*' in string:
            idx = string.index('*')
            return switched_eval(string[:idx-1]) * switched_eval(string[idx+2:])
        else:
            return eval(string)


def switched(data):
    return sum(switched_eval(line) for line in data)


def main():
    year, day = 2020, 18
    data = get_data(year, day)
    print(left_to_right(data))
    print(switched(data))


if __name__ == "__main__":
    main()
