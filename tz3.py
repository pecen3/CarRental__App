def openfile(filename):
    bin =[]
    data = []
    with open(filename) as f:
        for line in f:
            bin.append([numb for numb in line.split()])
        for mas in bin:
            for ch in mas:
                if ch.isdigit():
                    data.append(float(ch))
    return data


def max(filename):
    data = openfile(filename)
    max = data[0]
    for num in data:
        if max < num:
            max = num
    return max


def min(filename):
    data = openfile(filename)
    min = data[0]
    for num in data:
        if min > num:
            min = num
    return min


def sum(filename):
    data = openfile(filename)
    ans = 0
    for num in data:
        ans += num
    return ans


def mult(filename):
    data = openfile(filename)
    ans = 1
    for num in data:
        ans *= num
    return ans


