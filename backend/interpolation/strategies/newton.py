from domain.approx import InterpolationResult, InterpolationData
from math import factorial


def process(data: InterpolationData) -> InterpolationResult:
    x = data.x
    y = data.y

    n = len(x)
    finite_differences = calc_diff(x, y)
    s = f'{y[0]}'

    for k in range(1, n):
        s += " + "

        h = x[k] - x[k - 1]
        fn_d = (finite_differences[0][k] / (pow(h, k) * factorial(k)))

        tmp = ""
        for i in range(k):
            if i > 0:
                tmp += "*"
            tmp += f'(x - ({round(x[i], 5)}))'
        s += f'({fn_d} * {tmp})'

    return InterpolationResult(s)


def calc_diff(x, y):
    n = len(x)
    diff = [[0] * n for _ in range(n)]
    print()
    for i in range(n):
        diff[i][0] = y[i]
    k = 1
    while k <= n:
        for i in range(n - k):
            diff[i][k] = (diff[i + 1][k - 1] - diff[i][k - 1]) / (x[i + k] - x[i])
        k += 1
    return diff
