def mean(values: list[float]) -> float:
    """Return the arithmetic mean of ``values``. Raises on empty input."""
    if not values:
        raise ValueError("values must be non-empty")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Return the median of ``values``. Raises on empty input."""
    if not values:
        raise ValueError("values must be non-empty")
    ordered = sorted(values)
    n = len(ordered)
    if n % 2 == 1:
        return ordered[n // 2]
    return (ordered[n // 2 - 1] + ordered[n // 2]) / 2


def variance(values: list[float]) -> float:
    """Return the population variance of ``values``. Raises on empty input."""
    if not values:
        raise ValueError("values must be non-empty")
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)
