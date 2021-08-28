from django import template

register = template.Library()


def convert_star_rating(value):
    return round(float(value), 2)


register.filter('convert_star_rating', convert_star_rating)
