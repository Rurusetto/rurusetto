from typing import Union
from django import template
from . import constants

register = template.Library()


def get_genre_name(genre_id: Union[str, int]):
    """Get genre name from osu! genre id."""
    genre_id = int(genre_id)
    return constants.genres.get(genre_id, "Unknown")

register.filter('get_genre_name', get_genre_name)