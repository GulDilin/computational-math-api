# f - function (x:float, y:float)
def solve(f, x: list, y_0):
    n = len(x)
    y = [0 for _ in range(n)]
    y[0] = y_0
    print(f'first y = {y}')
    for i in range(0, n - 1):
        h = x[i + 1] - x[i]
        k_0 = h * f(x[i], y[i])
        k_1 = h * f(x[i] + h / 2, y[i] + k_0 / 2)
        k_2 = h * f(x[i] + h / 2, y[i] + k_1 / 2)
        k_3 = h * f(x[i] + h, y[i] + k_2)
        y[i+1] = y[i] + 1 / 6 * (k_0 + 2 * k_1 + 2 * k_2 + k_3)
    return y
