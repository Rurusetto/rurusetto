import markdown
from django import template

register = template.Library()


def convert_markdown(value):
    return markdown.markdown(value)


register.filter('convert_markdown', convert_markdown)
