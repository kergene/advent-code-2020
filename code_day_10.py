from math import prod

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(i) for i in data]
    data.append(0)
    data.sort()
    data.append(data[-1] + 3)
    return data

def find_gaps(data):
    ones = sum(data[i+1] - data[i] == 1 for i in range(len(data) - 1))
    threes = sum(data[i+1] - data[i] == 3 for i in range(len(data) - 1))
    return ones * threes

def count_ways(data):
    mults = []
    last_three_idx = -1
    for i in range(len(data) - 1):
        if data[i+1] - data[i] == 3:
            mults.append(three_term_fib(i - last_three_idx))
            last_three_idx = i
    return prod(mults)

def three_term_fib(n): # have n numbers, can go up by 1,2,3 numbers at time
    if n == 1: return 1
    if n == 2: return 1
    a = 0
    b = 1
    c = 1
    for i in range(n-2):
        c, b, a = a+b+c, c, b
    return c

def main():
    day = 10
    data = get_data(day)
    print(find_gaps(data))
    print(count_ways(data))   

if __name__ == "__main__":
    main()
