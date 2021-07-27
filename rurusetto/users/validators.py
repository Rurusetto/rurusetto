from django.core.exceptions import ValidationError
from django.conf import settings


def validate_file_size(value):
    filesize = value.size

    if filesize > settings.MAX_PROFILE_PICTURE_SIZE:
        raise ValidationError(f"The maximum file size that can be uploaded is {int(settings.MAX_PROFILE_PICTURE_SIZE/1024/1024)}MB")
    else:
        return value
