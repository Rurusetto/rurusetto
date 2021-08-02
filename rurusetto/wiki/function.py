from django.contrib.auth.models import User


def make_listing_view(model_list):
    export_list = []
    for item in model_list:
        ruleset_owner = User.objects.get(id=item.owner)
        export_list.append([item, ruleset_owner])
    return export_list


def make_wiki_view(ruleset_object):
    creator = User.objects.get(id=ruleset_object.owner)
    owner = User.objects.get(id=ruleset_object.owner)
    last_edited_by = User.objects.get(id=ruleset_object.last_edited_by)
    return [creator, owner, last_edited_by]