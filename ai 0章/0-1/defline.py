def plus(x, y) -> int:
    return x + y


def eq_plus(plus, x, y) -> int:
    return plus(x, y)


print(eq_plus(plus, 3, 4))
