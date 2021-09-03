from django import template

register = template.Library()


def convert_star_rating(value):
    try:
        return round(float(value), 2)
    except ValueError:
        return None


register.filter('convert_star_rating', convert_star_rating)
