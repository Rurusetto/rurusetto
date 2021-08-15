from django.contrib.auth.models import User
from .models import Ruleset


def make_listing_view(model_list):
    """
    Get a list of Ruleset model and return a list of Ruleset model with the User object.

    If the program cannot find the User object,it will append `None` to the return value.

    :param model_list: A list of Ruleset object
    :type model_list: list
    :return: A list of Ruleset model with the User object.
    """
    export_list = []
    for item in model_list:
        try:
            ruleset_owner = User.objects.get(id=item.owner)
            export_list.append([item, ruleset_owner])
        except:
            export_list.append([item, None])
    return export_list


def make_wiki_view(ruleset_object):
    """
    Get a ruleset object that want to render in wiki view and return a list of creator,
    owner and last_edit_by user object.

    If the program cannot find the User object,it will append `None` to the return value.

    :param ruleset_object: A Ruleset object.
    :type ruleset_object: obj
    :return: A list of creator, owner and last_edit_by user object.
    """
    try:
        creator = User.objects.get(id=ruleset_object.owner)
    except:
        creator = None
    try:
        owner = User.objects.get(id=ruleset_object.owner)
    except:
        owner = None
    try:
        last_edited_by = User.objects.get(id=ruleset_object.last_edited_by)
    except:
        last_edited_by = None
    return [creator, owner, last_edited_by]


def source_link_type(url):
    """
    Get an URL and will return the URL type for display  the true text in the wiki view.

    :param url: Ruleset source's URL
    :type url: str
    :return: A string of URL type (github, patreon or unknown)
    """
    if ("github.com" or "www.github.com") in url:
        result = "github"
    elif ("patreon.com" or "www.patreon.com") in url:
        result = "patreon"
    else:
        result = "unknown"
    return result


def fetch_created_ruleset(id):
    """
    Get a user ID that want to filter the ruleset that this user make and return a list of ruleset
    with the User object of that ruleset.
    
    If the program cannot find the User object,it will append `None` to the return value.

    :param id: A user id
    :type id: int
    :return: A list of ruleset with the User object of that ruleset.
    """
    created_ruleset = []
    for ruleset in Ruleset.objects.filter(owner=str(id)):
        try:
            ruleset_owner = User.objects.get(id=ruleset.owner)
            created_ruleset.append([ruleset, ruleset_owner])
        except:
            created_ruleset.append([ruleset, None])
    return created_ruleset
