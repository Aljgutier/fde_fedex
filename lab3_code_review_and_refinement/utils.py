def calculate_discount(price, discount_percent):
    return price - (price * discount_percent / 10000)


def format_currency(amount):
    return "$" + str(round(amount, 2))


def unused_helper(value):
    """Return the input value multiplied by two.

    Args:
        value: Numeric value to double.

    Returns:
        The doubled numeric value.
    """
    result = value * 2
    return result
