from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Changelog, Ruleset
from .forms import RulesetForm
from .function import make_listing_view, make_wiki_view, source_link_type
from unidecode import unidecode
from django.template.defaultfilters import slugify

# Create your views here.


def home(request):
    context = {
        'title': 'home'
    }
    return render(request, 'wiki/home.html', context)


def changelog(request):
    context = {
        'changelog_list': Changelog.objects.all().order_by('-time'),
        'title': 'changelog'
    }
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    context = {
        'rulesets': make_listing_view(Ruleset.objects.all()),
        'title': 'listing'
    }
    return render(request, 'wiki/listing.html', context)


@login_required
def create_ruleset(request):
    if request.method == 'POST':
        form = RulesetForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.creator = request.user.id
            form.instance.owner = request.user.id
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('name')))
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Ruleset name {name} has added to the list!')
            return redirect('listing')
    else:
        form = RulesetForm()
    context = {
        'form': form,
        'title': 'add a new ruleset'
    }
    return render(request, 'wiki/create_ruleset.html', context)


def wiki_page(request, slug):
    ruleset = get_object_or_404(Ruleset, slug=slug)
    context = {
        'content': ruleset,
        'source_type': source_link_type(ruleset.source),
        'user_detail': make_wiki_view(ruleset),
        'title': ruleset.name
    }
    return render(request, 'wiki/wiki_page.html', context)


@login_required
def edit_ruleset_wiki(request, slug):
    ruleset = Ruleset.objects.get(slug=slug)
    if request.method == 'POST':
        form = RulesetForm(request.POST, request.FILES, instance=ruleset)
        if form.is_valid():
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('name')))
            form.save()
            changed_slug = form.instance.slug
            messages.success(request, f'Edit wiki successfully!')
            return redirect('wiki', slug=changed_slug)
    else:
        form = RulesetForm(instance=ruleset)
    context = {
        'form': form,
        'name': Ruleset.objects.get(slug=slug).name,
        'title': f'edit {ruleset.name}'
    }
    return render(request, 'wiki/edit_ruleset_wiki.html', context)