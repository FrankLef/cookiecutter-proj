import math


def log1ps(x: float, base: float = math.e) -> list[float] | float:
    """Return 'math.log1p' of `x` to the given `base`, keeping the sign of `x`.

    Args:
        x (float): Value to process.
        base (float, optional): Base of the logarithm. Defaults to `math.e`.

    Returns:
        list[float] | float: Number converted with `log1ps`.
    """
    def fun(x):
        y = abs(x)
        y = math.log1p(y) / math.log(base)
        return math.copysign(y, x)
    if hasattr(x, "__iter__"):
        out = [fun(item) for item in x]
    else:
        out = fun(x)
    return out


def expm1s(x: float, base: float = math.e) -> list[float] | float:
    """Return 'math.expm1' of `x` at the given `base`, keeping the sign of `x`.

    Args:
        x (float): Value to process, it is the power of the given `base`.
        base (float, optional): Base of the power. Defaults to `math.e`.

    Returns:
        list[float] | float: Number converted with `expm1s`.
    """
    def fun(x):
        y = abs(x)
        y = math.pow(base, y) - 1
        return math.copysign(y, x)
    if hasattr(x, "__iter__"):
        out = [fun(item) for item in x]
    else:
        out = fun(x)
    return out


def log1ps10(x: float) -> list[float] | float:
    """Same as `log1ps(x, base=10)`.

    Args:
        x (float): Value to process.

    Returns:
        list[float] | float: Number converted with `log1ps`.
    """
    return log1ps(x, base=10)


def expm1s10(x: float) -> list[float] | float:
    """Same as `expm1s(x, base=10)`

    Args:
        x (float): Value to process.

    Returns:
        list[float] | float: Number converted with `expm1s`.
    """
    return expm1s(x, base=10)
