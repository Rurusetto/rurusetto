from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Changelog, Ruleset
from .forms import RulesetCreateForm
from .function import make_listing_view

# Create your views here.


def home(request):
    return render(request, 'wiki/home.html')


def changelog(request):
    context = {
        'changelog_list': Changelog.objects.all().order_by('-time')
    }
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    context = {
        'rulesets': make_listing_view(Ruleset.objects.all()),
    }
    return render(request, 'wiki/listing.html', context)


@login_required
def create_ruleset(request):
    if request.method == 'POST':
        form = RulesetCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.creator = request.user.id
            form.instance.owner = request.user.id
            form.instance.last_edited_by = request.user.id
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Ruleset name {name} has added to the list!')
            return redirect('listing')
    else:
        form = RulesetCreateForm()
    return render(request, 'wiki/create_ruleset.html', {'form': form})


def wiki_page(request, slug):
    ruleset = get_object_or_404(Ruleset, slug=slug)
    context = {
        'content': ruleset,
        'user_detail': make_wiki_view(ruleset)
    }
    return render(request, 'wiki/wiki_page.html', context)