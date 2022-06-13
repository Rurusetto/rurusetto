from typing import Union
from django import template
from . import constants

register = template.Library()


def get_language_name(language_id: Union[str, int]):
    """Get language from osu! language id."""
    language_id = int(language_id)
    return constants.languages.get(language_id, "Unknown")

register.filter('get_language_name', get_language_name)