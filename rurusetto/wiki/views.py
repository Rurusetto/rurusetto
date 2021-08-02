from django.shortcuts import render
from .models import Changelog

# Create your views here.


def home(request):
    return render(request, 'wiki/home.html')


def changelog(request):
    context = {
        'changelog_list': Changelog.objects.all().order_by('-time')
    }
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    return render(request, 'wiki/listing.html')