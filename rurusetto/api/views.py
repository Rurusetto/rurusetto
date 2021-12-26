from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from wiki.models import Ruleset
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
