from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import RulesetSerializer
from .models import Changelog, Ruleset, Subpage
from .forms import RulesetForm, SubpageForm
from .function import make_listing_view, make_wiki_view, source_link_type, get_user_by_id
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
    hero_image = 'img/changelog-cover-night2.png'
    hero_image_light = 'img/changelog-cover-light3.png'

    context = {
        'changelog_list': Changelog.objects.all().order_by('-time'),
        'title': 'changelog',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'All update history of website are here.',
        'opengraph_url': resolve_url('changelog'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    hero_image = "img/listing-cover-night.png"
    hero_image_light = 'img/listing-cover-light.png'

    context = {
        'rulesets': make_listing_view(Ruleset.objects.all()),
        'title': 'listing',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'List of available rulesets.',
        'opengraph_url': resolve_url('listing'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/listing.html', context)


@login_required
def create_ruleset(request):
    hero_image = 'img/create-rulesets-cover-night.png'
    hero_image_light = 'img/create-rulesets-cover-light.png'
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
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': "Let's add a new ruleset! Is it yours? Don't worry! You can add it although you don't make that ruleset.",
        'opengraph_url': resolve_url('create_ruleset'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/create_ruleset.html', context)


def wiki_page(request, slug):
    ruleset = get_object_or_404(Ruleset, slug=slug)
    hero_image = ruleset.cover_image.url
    hero_image_light = ruleset.cover_image.url
    context = {
        'content': ruleset,
        'subpage': Subpage.objects.filter(ruleset_id=ruleset.id),
        'source_type': source_link_type(ruleset.source),
        'user_detail': make_wiki_view(ruleset),
        'title': ruleset.name,
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_description': ruleset.description,
        'opengraph_url': resolve_url('wiki', slug=ruleset.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
    return render(request, 'wiki/wiki_page.html', context)


@login_required
def edit_ruleset_wiki(request, slug):
    hero_image = 'img/edit-wiki-cover-night.jpeg'
    hero_image_light = 'img/edit-wiki-cover-light.png'
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
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': f'You are currently edit content on ruleset name "{Ruleset.objects.get(slug=slug).name}".',
        'opengraph_url': resolve_url('edit_wiki', slug=slug),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/edit_ruleset_wiki.html', context)


@login_required
def add_subpage(request, slug):
    target_ruleset = Ruleset.objects.get(slug=slug)
    hero_image = 'img/add-subpage-cover-night.jpeg'
    hero_image_light = 'img/add-subpage-cover-light.png'
    if request.method == 'POST':
        form = SubpageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.ruleset_id = target_ruleset.id
            form.instance.creator = request.user.id
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('title')))
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'Subpage "{title}" for {target_ruleset.name} has been created! ')
            return redirect('wiki', slug=slug)
    else:
        form = SubpageForm()
    context = {
        'form': form,
        'title': f'add a new subpage for {target_ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': f'You are currently add a subpage for ruleset name "{target_ruleset.name}".',
        'opengraph_url': resolve_url('add_subpage', slug=slug),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/add_subpage.html', context)


def install(request):
    hero_image = 'img/install-cover-night.png'
    hero_image_light = 'img/install-cover-light.jpeg'
    context = {
        'title': 'install and update rulesets',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'How to install and update rulesets by using Rūrusetto.',
        'opengraph_url': resolve_url('install'),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/install.html', context)


def subpage(request, rulesets_slug, subpage_slug):
    subpage = get_object_or_404(Subpage, slug=subpage_slug)
    ruleset = get_object_or_404(Ruleset, slug=rulesets_slug)
    hero_image = ruleset.cover_image.url
    hero_image_light = ruleset.cover_image.url
    context = {
        'content': subpage,
        'ruleset': ruleset,
        'user_detail': get_user_by_id(int(subpage.last_edited_by)),
        'title': f"{ruleset.name} > {subpage.title}",
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_description': ruleset.description,
        'opengraph_url': resolve_url('subpage', rulesets_slug=ruleset.slug, subpage_slug=subpage.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
    return render(request, 'wiki/subpage.html', context)


@login_required
def edit_subpage(request, rulesets_slug, subpage_slug):
    hero_image = 'img/edit-subpage-cover-night.png'
    hero_image_light = 'img/edit-subpage-cover-light.png'
    ruleset = Ruleset.objects.get(slug=rulesets_slug)
    subpage = Subpage.objects.get(slug=subpage_slug)
    if request.method == 'POST':
        form = SubpageForm(request.POST, request.FILES, instance=subpage)
        if form.is_valid():
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('title')))
            form.save()
            changed_slug = form.instance.slug
            messages.success(request, f'Edit subpage successfully!')
            return redirect('wiki', slug=changed_slug)
    else:
        form = SubpageForm(instance=subpage)
    context = {
        'form': form,
        'ruleset_name': Ruleset.objects.get(slug=rulesets_slug).name,
        'subpage_name': Subpage.objects.get(slug=subpage_slug).title,
        'title': f'edit {ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': f'You are currently edit subpage "{Subpage.objects.get(slug=subpage_slug).title}" on ruleset name "{Ruleset.objects.get(slug=rulesets_slug).name}".',
        'opengraph_url': resolve_url('edit_subpage', rulesets_slug=ruleset.slug, subpage_slug=subpage.slug),
        'opengraph_image': static(hero_image)
    }
    return render(request, 'wiki/edit_subpage.html', context)


# Views for API


@csrf_exempt
def ruleset_list(request):
    if request.method == 'GET':
        rulesets = Ruleset.objects.all()
        serializer = RulesetSerializer(rulesets, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def ruleset_detail(request, slug):
    # try to fetch ruleset from database
    try:
        ruleset = Ruleset.objects.get(slug=slug)
    except Ruleset.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RulesetSerializer(ruleset)
        return JsonResponse(serializer.data)