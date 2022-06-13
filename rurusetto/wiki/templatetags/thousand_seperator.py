from django import template

register = template.Library()


def thousand_seperator(value):
    """
    Get an integer value and return string value with thousand seperator.
    Args:
        value (float): The integer value that you want to add thousand seperator.
    Returns:
        str: The string that is the number with thousand seperator.
    """
    try:
        return str(f'{int(value):,}')
    except ValueError:
        return str(value)


register.filter('thousand_seperator', thousand_seperator)