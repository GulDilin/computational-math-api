from functools import reduce


def l(f, x, new_x, ind):
    return reduce(lambda k, y: k * y,
                  [(new_x - x[i]) / (x[ind] - x[i]) for i in range(len(x)) if i != ind]) * f[ind]


def interpolate(f, x, new_x):
    return sum([l(f, x, new_x, i) for i in range(len(x))])
