import numpy as np


def log1ps(x: float, base: float = np.e) -> list[float] | float:
    """Return 'np.log1p' of `x` to the given `base`, keeping the sign of `x`.

    Args:
        x (float): Value to process.
        base (float, optional): Base of the logarithm. Defaults to `np.e`.

    Returns:
        list[float] | float: Number converted with `log1ps`.
    """
    y = np.abs(x)
    out = np.sign(x) * np.log1p(y) / np.log(base)
    return out


def expm1s(x: float, base: float = np.e) -> list[float] | float:
    """Return 'np.power(x, base) - 1, keeping the sign of `x`.

    Args:
        x (float): Value to process, it is the power of the given `base`.
        base (float, optional): Base of the power. Defaults to `np.e`.

    Returns:
        list[float] | float: Number converted with `expm1s`.
    """
    y = np.abs(x)
    out = np.sign(x) * (np.power(base, y) - 1)
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
