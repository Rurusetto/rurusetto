from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from wiki.models import Ruleset, Subpage
from users.models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse


def make_404_json_response(message):
    return {
        'detail': message
    }


@csrf_exempt
def listing(request):
    """
    View for return information to make listing page

    :param request: WSGI request from user
    :return:
    """
    if request.method == 'GET':
        all_public_ruleset = Ruleset.objects.filter(hidden=False)
        serializer = RulesetListingSerializer(all_public_ruleset, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def ruleset_detail(request, slug):
    """
    View for return the specific ruleset that user pass by using its slug in JSON format.

    :param request: WSGI request from user
    :return: Specific ruleset metadata in JSON format.
    """
    # try to fetch ruleset from database
    try:
        ruleset = Ruleset.objects.get(slug=slug)
    except Ruleset.DoesNotExist:
        return JsonResponse(make_404_json_response('The ruleset is not found'), status=404, content_type="application/json")

    # Return 404 if that ruleset is hidden
    if ruleset.hidden:
        return JsonResponse(make_404_json_response('The ruleset is not found'), status=404, content_type="application/json")

    if request.method == 'GET':
        serializer = RulesetsDetailSerializer(ruleset)
        return JsonResponse(serializer.data)


@csrf_exempt
def all_ruleset_subpage(request, rulesets_slug):
    """
    View for return the list of subpage title in targeted ruleset

    :param request: WSGI request from user
    :return: list of subpage title in targeted ruleset
    """
    try:
        all_public_subpage = Subpage.objects.filter(hidden=False, ruleset_id=str(Ruleset.objects.get(slug=rulesets_slug).id))
    except Ruleset.DoesNotExist:
        return JsonResponse(make_404_json_response('The ruleset is not found'), status=404, content_type="application/json")

    if request.method == 'GET':
        serializer = RulesetsSubpageSerializer(all_public_subpage, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def subpage(request, rulesets_slug, subpage_slug):
    """
    View for return full detail of subpage

    :param request: WSGI request from user
    :return: full detail of requested subpage
    """
    try:
        subpage = Subpage.objects.get(slug=subpage_slug, ruleset_id=str(Ruleset.objects.get(slug=rulesets_slug).id), hidden=False)
    except Ruleset.DoesNotExist:
        return JsonResponse(make_404_json_response('The ruleset is not found'), status=404, content_type="application/json")
    except Subpage.DoesNotExist:
        return JsonResponse(make_404_json_response('The subpage is not found'), status=404,
                            content_type="application/json")

    if request.method == 'GET':
        serializer = SubpageSerializer(subpage)
        return JsonResponse(serializer.data)

@csrf_exempt
def user(request, user_id):
    """
    View for return full detail of subpage

    :param request: WSGI request from user
    :return: full detail of requested subpage
    """
    try:
        profile = Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
        return JsonResponse(make_404_json_response('The user is not found'), status=404, content_type="application/json")
    except User.DoesNotExist:
        return JsonResponse(make_404_json_response('The user is not found'), status=404,
                            content_type="application/json")

    if request.method == 'GET':
        serializer = UserFullSerializer(profile)
        return JsonResponse(serializer.data)
