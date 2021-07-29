from django.shortcuts import render
from .models import Changelog

# Create your views here.


def home(request):
    return render(request, 'wiki/home.html')


def changelog(request):
    context = {
        'changelog_list': Changelog.objects.all()
    }
    return render(request, 'wiki/changelog.html', context)