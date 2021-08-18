from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.templatetags.static import static
from .models import Changelog, Ruleset
from .forms import RulesetForm
from .function import make_listing_view, make_wiki_view, source_link_type
from unidecode import unidecode
from django.template.defaultfilters import slugify


def home(request):
    hero_image = 'img/home-cover-night.png'
    hero_image_light = 'img/home-cover-light.jpeg'
    latest_add_rulesets = []
    for i in range(3):
        try:
            latest_add_rulesets.append(Ruleset.objects.all().order_by('-created_at')[i])
        except:
            continue

    context = {
        'title': 'home',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'A page that contain all osu! ruleset',
        'opengraph_url': resolve_url('home'),
        'opengraph_image': static(hero_image),
        'latest_add_rulesets': make_listing_view(latest_add_rulesets)
    }
    return render(request, 'wiki/home.html', context)


def changelog(request):
    hero_image = 'img/684477.png'

    context = {
        'changelog_list': Changelog.objects.all().order_by('-time'),
        'title': 'changelog',
        'hero_image': hero_image,
        'opengraph_description': 'All update history of website are here.',
        'opengraph_url': resolve_url('changelog'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    hero_image = "img/765703.png"
    hero_image_light = 'img/765112.png'

    context = {
        'rulesets': make_listing_view(Ruleset.objects.all()),
        'title': 'listing',
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_description': 'List of available rulesets.',
        'opengraph_url': resolve_url('listing'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/listing.html', context)


@login_required
def create_ruleset(request):
    hero_image = "img/743487.jpeg"
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
        'title': 'add a new ruleset',
        'hero_image': hero_image,
        'opengraph_description': "Let's add a new ruleset! Is it yours? Don't worry! You can add it although you don't make that ruleset.",
        'opengraph_url': resolve_url('create_ruleset'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/create_ruleset.html', context)


def wiki_page(request, slug):
    ruleset = get_object_or_404(Ruleset, slug=slug)
    context = {
        'content': ruleset,
        'source_type': source_link_type(ruleset.source),
        'user_detail': make_wiki_view(ruleset),
        'title': ruleset.name,
        'opengraph_description': ruleset.description,
        'opengraph_url': resolve_url('wiki', slug=ruleset.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
    return render(request, 'wiki/wiki_page.html', context)


@login_required
def edit_ruleset_wiki(request, slug):
    hero_image = "img/737403.png"
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
        'title': f'edit {ruleset.name}',
        'hero_image': hero_image,
        'opengraph_description': f'You are currently edit content on ruleset name "{Ruleset.objects.get(slug=slug).name}".',
        'opengraph_url': resolve_url('edit_wiki', slug=slug),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/edit_ruleset_wiki.html', context)