from counter import runge_kutt


def solve(f, x: list, y_0):
    n = len(x)
    y = [0 for _ in range(n)]
    y[0:4] = runge_kutt.solve(f, x[0:4], y_0)
    for i in range(3, n - 1):
        h = x[i + 1] - x[i]
        y[i + 1] = y[i - 3] + 4 / 3 * h * (2 * f(x[i], y[i]) - f(x[i - 1], y[i - 1]) + 2 * f(x[i - 2], y[i - 2]))
        y[i + 1] = y[i - 1] + 1 / 3 * h * (f(x[i + 1], y[i + 1]) + 4 * f(x[i], y[i]) + f(x[i - 1], y[i - 1]))
    return y
