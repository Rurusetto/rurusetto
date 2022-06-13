from django import template
import math

register = template.Library()


def round_up(value):
    """
    Rounds up a value to the nearest integer.
    Arguments:
        value (float): The value to round up.
    Returns:
        int: The rounded up value.
    """
    try:
        return int(math.ceil(float(value)))
    except ValueError:
        return value


register.filter('round_up', round_up)