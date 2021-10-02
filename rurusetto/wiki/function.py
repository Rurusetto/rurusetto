from django.contrib.auth.models import User
from .models import Ruleset, RecommendBeatmap


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
        except User.DoesNotExist:
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
    except User.DoesNotExist:
        creator = None
    try:
        owner = User.objects.get(id=ruleset_object.owner)
    except User.DoesNotExist:
        owner = None
    try:
        last_edited_by = User.objects.get(id=ruleset_object.last_edited_by)
    except User.DoesNotExist:
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


def fetch_created_ruleset(creator_id):
    """
    Get a user ID that want to filter the ruleset that this user make and return a list of ruleset
    with the User object of that ruleset.
    
    If the program cannot find the User object,it will append `None` to the return value.

    :param creator_id: A user ID
    :type creator_id: int
    :return: A list of ruleset with the User object of that ruleset.
    """
    created_ruleset = []
    for ruleset in Ruleset.objects.filter(owner=str(creator_id)):
        try:
            ruleset_owner = User.objects.get(id=ruleset.owner)
            created_ruleset.append([ruleset, ruleset_owner])
        except User.DoesNotExist:
            created_ruleset.append([ruleset, None])
    return created_ruleset


def get_user_by_id(user_id):
    """
    Get a user ID and return the User object of that given user ID. If user ID is not found, return None.

    :param user_id: A user ID
    :type user_id: int
    :return: User object. If not found return None.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def make_recommend_beatmap_view(ruleset_id):
    """
    Get ruleset ID that want to generate a recommend beatmaps view and return a list of

    1. A list of recommend beatmaps that is recommend by ruleset creator
    2. A list of recommend beatmaps that is recommend by other player

    In both list 1 and list 2 inside will be include user objects and RecommendBeatmap object

    If the program cannot find the User object,it will append `None` to the return value.

    :param ruleset_id: A ruleset ID that want to generate a recommend beatmaps view.
    :type ruleset_id: int
    :return: Two list from description
    """
    ruleset = Ruleset.objects.get(id=ruleset_id)
    # Create a list of recommend beatmaps that is recommend by ruleset creator
    try:
        owner = User.objects.get(id=ruleset.owner)
    except User.DoesNotExist:
        owner = None
    recommend_by_owner = []
    if len(RecommendBeatmap.objects.filter(user_id=ruleset.owner)) != 0:
        for beatmap in RecommendBeatmap.objects.filter(user_id=ruleset.owner, ruleset_id=ruleset.id):
            recommend_by_owner.append([beatmap, owner])
    # Create a list of recommend beatmaps that is recommend by other player
    recommend_by_other = []
    if len(RecommendBeatmap.objects.exclude(user_id=ruleset.owner).filter(ruleset_id=ruleset.id)) != 0:
        for beatmap in RecommendBeatmap.objects.exclude(user_id=ruleset.owner).filter(ruleset_id=ruleset.id, owner_approved=True, owner_seen=True):
            try:
                user_detail = User.objects.get(id=beatmap.user_id)
                recommend_by_other.append([beatmap, user_detail])
            except User.DoesNotExist:
                recommend_by_other.append([beatmap, None])
    return recommend_by_owner, recommend_by_other


def make_beatmap_aapproval_view(ruleset_id):
    """
    Get ruleset ID that want to generate a recommend beatmap approval view and return a list of
    recommend beatmap that is not approved.

    In the sublist include RecommendBeatmap object and User object who recommend this beatmap.

    If the program cannot find the User object,it will append `None` to the return value.

    :param ruleset_id: A ruleset ID that want to generate a recommend beatmap approval view.
    :type ruleset_id: int
    :return: A list from description
    """
    ruleset = Ruleset.objects.get(id=ruleset_id)
    beatmap_list = []
    beatmap_not_approved = RecommendBeatmap.objects.filter(ruleset_id=ruleset.id, owner_seen=False).exclude(user_id=ruleset.owner)
    if len(beatmap_not_approved) != 0:
        for beatmap in beatmap_not_approved:
            try:
                user_detail = User.objects.get(id=beatmap.user_id)
                beatmap_list.append([beatmap, user_detail])
            except User.DoesNotExist:
                beatmap_list.append([beatmap, None])
    return beatmap_list


def make_status_view():
    """
    Get all Ruleset object and generate the list of ruleset that show in status page

    Return the list for each source type of the ruleset.

    - GitHub with github_download_filename : [ruleset, 'github_with_direct', [download_link, latest_release]]
    - GitHub without github_download_filename : [ruleset, 'github', latest_release]
    - Patreon : [ruleset, 'patreon', ruleset.source]

    :return: The list of data needed to render in status page template.
    """
    show_ruleset = []
    for ruleset in Ruleset.objects.all():
        if source_link_type(ruleset.source) == 'patreon':
            # Patreon source is just need to go to Patreon owner page.
            show_ruleset.append([ruleset, 'patreon', ruleset.source])
        elif (source_link_type(ruleset.source) == 'github') and (ruleset.github_download_filename != ""):
            # When GitHub filename is not blank, we can render the direct download link.
            if ruleset.source[-1] != "/":
                download_link = f"{ruleset.source}/releases/latest/download/{ruleset.github_download_filename}"
                latest_release = f"{ruleset.source}/releases"
            else:
                download_link = f"{ruleset.source}releases/latest/download/{ruleset.github_download_filename}"
                latest_release = f"{ruleset.source}releases"
            show_ruleset.append([ruleset, 'github_with_direct', [download_link, latest_release]])
        elif (source_link_type(ruleset.source) == 'github') and (ruleset.github_download_filename == ""):
            # No filename, so we can render only the link to release page.
            if ruleset.source[-1] != "/":
                latest_release = f"{ruleset.source}/releases"
            else:
                latest_release = f"{ruleset.source}releases"
            show_ruleset.append([ruleset, 'github', latest_release])
        else:
            continue
    return show_ruleset
