from django.shortcuts import render
from .serializers import RulesetSerializer
from django.views.decorators.csrf import csrf_exempt
from wiki.models import Ruleset
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def ruleset_list(request):
    """
    View for return the ruleset in JSON format.

    :param request: WSGI request from user
    :return: All ruleset in website with its metadata in JSON format.
    """
    if request.method == 'GET':
        rulesets = Ruleset.objects.all()
        serializer = RulesetSerializer(rulesets, many=True)
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
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RulesetSerializer(ruleset)
        return JsonResponse(serializer.data)