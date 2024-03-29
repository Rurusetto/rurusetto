from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.templatetags.static import static
from django.utils import timezone, translation
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext
from .models import Changelog, Ruleset, Subpage, RecommendBeatmap, Action, RulesetStatus
from users.models import Profile
from django.contrib.auth.models import User
from .forms import RulesetForm, SubpageForm, RecommendBeatmapForm, RulesetStatusForm
from .function import *
from unidecode import unidecode
from django.template.defaultfilters import slugify
from rurusetto.settings import OSU_API_V1_KEY, TEST_SERVER, DEBUG
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
import os
import threading
from .action import update_all_beatmap_action, update_ruleset_version_action, update_ruleset_version_once_action
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models.functions import datetime


def home(request):
    """
    View for homepage.

    :param request: WSGI request from user
    :return: Render the wiki page and pass the value from context to the template (home.html)
    """
    hero_image = 'img/home-cover-night.png'
    hero_image_light = 'img/home-cover-light.jpeg'

    context = {
        'title': gettext('home'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('wiki_that_contain'),
        'opengraph_url': resolve_url('home'),
        # Use make_listing_view function to get the User object from database and pass to template
        'rulesets': make_listing_view(Ruleset.objects.filter(hidden=False, archive=False).order_by(Lower('name'))),
        'test_server': TEST_SERVER,
        'is_in_debug': DEBUG
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/home.html', context)


def changelog(request):
    """
    View for changelog page.

    :param request: WSGI request from user
    :return: Render the changelog page and pass the value from context to the template (changelog.html)
    """
    hero_image = 'img/changelog-cover-night2.png'
    hero_image_light = 'img/changelog-cover-light3.png'

    context = {
        'changelog_list': Changelog.objects.all().order_by('-time'),
        'title': gettext('changelog'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('changelog_description'),
        'opengraph_url': resolve_url('changelog'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/changelog.html', context)


def listing(request):
    """
    View for listing page

    :param request: WSGI request from user
    :return: Render the listing page and pass the value from context to the template (changelog.html)
    """
    hero_image = "img/listing-cover-night.png"
    hero_image_light = 'img/listing-cover-light.png'

    context = {
        'hidden_rulesets': make_listing_view(
            Ruleset.objects.filter(hidden=True, owner=str(request.user.id)).order_by(Lower('name'))),
        'rulesets': make_listing_view(Ruleset.objects.filter(hidden=False, archive=False).order_by(Lower('name'))),
        'title': gettext('listing'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('listing_description'),
        'opengraph_url': resolve_url('listing'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/listing.html', context)


@login_required
def create_ruleset(request):
    """
    View for create ruleset form. User must be logged in before access this page.

    This view has a function to pass the automatically assign value to the Ruleset object that user has created.

    :param request: WSGI request from user
    :return: Render the create ruleset and pass the value from context to the template (create_ruleset.html)
    """
    hero_image = 'img/create-rulesets-cover-night.png'
    hero_image_light = 'img/create-rulesets-cover-light.png'
    if request.method == 'POST':
        form = RulesetForm(request.POST, request.FILES)
        if form.is_valid():
            # Save who make the ruleset and auto generate the slug to make the ruleset main wiki page.
            form.instance.creator = request.user.id
            form.instance.owner = request.user.id
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('name')))
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, gettext('Ruleset name %(name)s has added to the list!') % {'name': name})
            return redirect('listing')
    else:
        form = RulesetForm()
    context = {
        'form': form,
        'title': gettext('add_a_new_ruleset'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('add_a_new_ruleset_description'),
        'opengraph_url': resolve_url('create_ruleset'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/create_ruleset.html', context)


def wiki_page(request, slug):
    """
    View for wiki page. This page is the main page of each ruleset.

    :param request: WSGI request from user
    :param slug: Ruleset slug (slug in Ruleset model)
    :type slug: str
    :return: Render the wiki page and pass the value from context to the template (wiki_page.html)
    """
    ruleset = get_object_or_404(Ruleset, slug=slug)
    try:
        ruleset_owner_profile = Profile.objects.get(user=User.objects.get(id=int(ruleset.owner)))
        if ruleset_owner_profile.support_message == '' and ruleset_owner_profile.support_patreon == '' and ruleset_owner_profile.support_kofi == '' and ruleset_owner_profile.support_github_sponsors == '':
            can_support = False
        else:
            can_support = True
    except User.DoesNotExist:
        can_support = False
    hero_image = ruleset.cover_image.url
    hero_image_light = ruleset.cover_image_light.url
    download_link = direct_download_link_generator(ruleset)
    context = {
        'content': ruleset,
        'hidden_subpage': Subpage.objects.filter(ruleset_id=ruleset.id, hidden=True, creator=str(request.user.id)),
        'subpage': Subpage.objects.filter(ruleset_id=ruleset.id, hidden=False),
        'source_type': source_link_type(ruleset.source),
        'user_detail': make_wiki_view(ruleset),
        'can_support': can_support,
        'can_download': ruleset.can_download,
        'download_link': download_link,
        'title': ruleset.name,
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_description': ruleset.description,
        'opengraph_url': resolve_url('wiki', slug=ruleset.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/wiki_page.html', context)


@login_required
def edit_ruleset_wiki(request, slug):
    """
    View for editing the main ruleset page and main configuration form of the ruleset.

    User must be logged in before access this page.

    This view include the migration to the new name like changing the slug to make the ruleset
    successfully transfer to the new name with new URL.

    :param request: WSGI request from user
    :param slug: Ruleset slug (slug in Ruleset model)
    :type slug: str
    :return: Render the edit ruleset page with the form and pass the value from context to the template (edit_ruleset_wiki.html)
    """
    hero_image = 'img/edit-wiki-cover-night.jpeg'
    hero_image_light = 'img/edit-wiki-cover-light.png'
    ruleset = Ruleset.objects.get(slug=slug)
    ruleset_status = RulesetStatus.objects.get(ruleset=ruleset)
    if request.method == 'POST':
        form = RulesetForm(request.POST, request.FILES, instance=ruleset)
        status_form = RulesetStatusForm(request.POST, instance=ruleset_status)
        if form.is_valid() and status_form.is_valid():
            if source_link_type(form.instance.source) == "github" and not ruleset_status.pre_release and not \
            status_form.cleaned_data['pre_release']:
                # Check that the download link when render is valid
                if form.instance.source[-1] != "/":
                    download_url = f"{form.instance.source}/releases/latest/download/{form.instance.github_download_filename}"
                else:
                    download_url = f"{form.instance.source}releases/latest/download/{form.instance.github_download_filename}"
                html_status = requests.head(download_url)
                if (html_status.status_code != 200) and (html_status.status_code != 302) and (
                        html_status.status_code != 301):
                    error_message = f"The response of {download_url} is not success ({html_status.status_code}). Please check your filename or ruleset source link!"
                    messages.error(request, error_message)
                    return redirect('edit_wiki', slug=ruleset.slug)
                else:
                    form.instance.direct_download_link = direct_download_link_generator(form.instance)
                    if not form.instance.can_download:
                        form.instance.can_download = True
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('name')))
            form.save()
            status_form.save()
            changed_slug = form.instance.slug
            messages.success(request, f'Edit wiki successfully!')
            return redirect('wiki', slug=changed_slug)
    else:
        form = RulesetForm(instance=ruleset)
        status_form = RulesetStatusForm(instance=ruleset_status)
    context = {
        'form': form,
        'status_form': status_form,
        'ruleset': ruleset,
        'name': Ruleset.objects.get(slug=slug).name,
        'source_type': source_link_type(ruleset.source),
        'has_edit_permission': ruleset.owner == str(
            request.user.id) or request.user.is_superuser or request.user.is_staff,
        'title': f'edit {ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext("You are currently editing content on ruleset named \"%(ruleset_name)s\".") % {
            'ruleset_name': Ruleset.objects.get(slug=slug).name},
        'opengraph_url': resolve_url('edit_wiki', slug=slug),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/edit_ruleset_wiki.html', context)


@login_required
def add_subpage(request, slug):
    """
    View for adding subpage form. User must be logged in before access this page.

    This view can mainly access from the URL or the ruleset main page.

    This view has a function to bind a Subpage object with a ruleset and create slug for the subpage URL too.

    :param request: WSGI request from user
    :param slug: Ruleset slug (slug in Ruleset model)
    :type slug: str
    :return: Render the add ruleset page with the form and pass the value from context to the template (add_subpage.html)
    """
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
            messages.success(request, gettext('Subpage "%(title)s" for %(name)s has been created!') % {'title': title,
                                                                                                       'name': target_ruleset.name})
            return redirect('wiki', slug=slug)
    else:
        form = SubpageForm()
    context = {
        'form': form,
        'title': f'add a new subpage for {target_ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('You are currently add a subpage for ruleset name "%(name)s".') % {
            'name': target_ruleset.name},
        'opengraph_url': resolve_url('add_subpage', slug=slug),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/add_subpage.html', context)


def install(request):
    """
    View for install page. This page is static so nothing much here.
    
    :param request: WSGI request from user.
    :return: Render the install page and pass the value from context to the template (install.html)
    """
    hero_image = 'img/install-cover-night.png'
    hero_image_light = 'img/install-cover-light.png'
    context = {
        'title': gettext('install_and_update_rulesets'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('install_and_update_rulesets_description'),
        'opengraph_url': resolve_url('install'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/install.html', context)


def subpage(request, rulesets_slug, subpage_slug):
    """
    View for subpage.
    
    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :param subpage_slug: Subpage slug (slug in Subpage model)
    :type subpage_slug: str
    :return: Render the subpage and pass the value from context to the template (subpage.html)
    """
    subpage = get_object_or_404(Subpage, slug=subpage_slug)
    ruleset = get_object_or_404(Ruleset, slug=rulesets_slug)
    hero_image = ruleset.cover_image.url
    hero_image_light = ruleset.cover_image_light.url
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
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/subpage.html', context)


@login_required
def edit_subpage(request, rulesets_slug, subpage_slug):
    """
    View for edit subpage form. User must be logged in before access this page.

    This view include the function to change the slug and redirect to the new slug when user change the subpage title
    with assign some value that must be automatically assign to the Subpage model.

    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :param subpage_slug: Subpage slug (slug in Subpage model)
    :type subpage_slug: str
    :return: Render the edit subpage page with the edit subpage form and pass the value from context to the template (edit_subpage.html)
    """
    hero_image = 'img/edit-subpage-cover-night.png'
    hero_image_light = 'img/edit-subpage-cover-light.jpg'
    ruleset = Ruleset.objects.get(slug=rulesets_slug)
    subpage = Subpage.objects.get(slug=subpage_slug)
    if request.method == 'POST':
        form = SubpageForm(request.POST, request.FILES, instance=subpage)
        if form.is_valid():
            form.instance.last_edited_by = request.user.id
            form.instance.slug = slugify(unidecode(form.cleaned_data.get('title')))
            form.save()
            changed_slug = form.instance.slug
            messages.success(request, gettext('Edit subpage successfully!'))
            return redirect('wiki', slug=changed_slug)
    else:
        form = SubpageForm(instance=subpage)
    context = {
        'form': form,
        'subpage_creator': request.user.id == int(subpage.creator),
        'ruleset_owner': request.user.id == int(ruleset.owner),
        'ruleset_name': ruleset.name,
        'subpage_name': subpage.title,
        'ruleset_slug': rulesets_slug,
        'subpage_slug': subpage_slug,
        'title': f'edit {ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext(
            "You are currently edit subpage \"%(subpage_name)s\" on ruleset name \"%(ruleset_name)s\".") % {
                                     'subpage_name': Subpage.objects.get(slug=subpage_slug).title,
                                     'ruleset_name': Ruleset.objects.get(slug=rulesets_slug).name},
        'opengraph_url': resolve_url('edit_subpage', rulesets_slug=ruleset.slug, subpage_slug=subpage.slug),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/edit_subpage.html', context)


@login_required
def delete_subpage(request, rulesets_slug, subpage_slug):
    """
    View for delete subpage. Mainly this link will be direct from subpage setting menu.

    This link must check on user who request to delete too. If user who request is not subpage creator or owner,
    it will be redirect to subpage with messages.

    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :param subpage_slug: Subpage slug (slug in Subpage model)
    :type subpage_slug: str
    :return: Redirect to rulesets main wiki page or if user who request is not subpage owner, redirect to that subpage
    with wiki.
    """
    ruleset = Ruleset.objects.get(slug=rulesets_slug)
    subpage = Subpage.objects.get(slug=subpage_slug)
    if subpage.creator == str(request.user.id) or ruleset.owner == str(request.user.id):
        subpage.delete()
        messages.success(request, gettext("Delete subpage successfully!"))
    else:
        messages.error(request, gettext("You don't have permission to do this!"))
    return redirect('wiki', slug=rulesets_slug)


@login_required
def add_recommend_beatmap(request, slug):
    """
    View for add a recommend beatmap to the target ruleset that include in the slug. User must be logged in before access this page.

    This view include the function to find the beatmap ID that user put in the form, get the data from osu! API and
    assign the beatmap metadata to the RecommendBeatmap object.

    :param request: WSGI request from user.
    :param slug: Ruleset slug (slug in Ruleset model)
    :type slug: str
    :return: Render the recommend beatmap page with the recommend beatmap form and pass the value from context to the template (add_recommend_beatmap.html)
    """
    hero_image = 'img/add-recommend-beatmap-cover-night.png'
    hero_image_light = 'img/add-recommend-beatmap-cover-light.jpg'
    ruleset = Ruleset.objects.get(slug=slug)
    if request.method == 'POST':
        form = RecommendBeatmapForm(request.POST)
        if form.is_valid():
            # Fetch beatmap detail from osu! API
            parameter = {'b': int(form.instance.beatmap_id), 'm': 0, 'k': OSU_API_V1_KEY}
            request_data = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameter)
            if (request_data.status_code == 200) and (request_data.json() != []) and (
                    not RecommendBeatmap.objects.filter(beatmap_id=form.instance.beatmap_id, ruleset_id=ruleset.id,
                                                        owner_approved=True, owner_seen=True).exists()) and (
                    not RecommendBeatmap.objects.filter(user_id=str(request.user.id), owner_seen=False,
                                                        beatmap_id=form.instance.beatmap_id).exists()):
                beatmap_json_data = request_data.json()[0]
                # Download beatmap cover from osu! server and save it to the media storage and put the address in the
                # RecommendBeatmap model that user want to add.
                cover_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/cover.jpg")
                cover_temp = NamedTemporaryFile(delete=True)
                cover_temp.write(cover_pic.content)
                cover_temp.flush()
                form.instance.beatmap_cover.save(f"{form.instance.beatmap_id}.jpg", File(cover_temp), save=True)
                # Download beatmap thumbnail to beatmap_thumbnail field
                thumbnail_pic = requests.get(
                    f"https://b.ppy.sh/thumb/{beatmap_json_data['beatmapset_id']}l.jpg")
                thumbnail_temp = NamedTemporaryFile(delete=True)
                thumbnail_temp.write(thumbnail_pic.content)
                thumbnail_temp.flush()
                form.instance.beatmap_thumbnail.save(f"{form.instance.beatmap_id}.jpg",
                                                     File(thumbnail_temp), save=True)
                # Download beatmap card to beatmap_card field
                card_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/card.jpg")
                card_temp = NamedTemporaryFile(delete=True)
                card_temp.write(card_pic.content)
                card_temp.flush()
                form.instance.beatmap_card.save(f"{form.instance.beatmap_id}.jpg",
                                                File(card_temp), save=True)
                # Download beatmap list picture to beatmap_list field
                list_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/list.jpg")
                list_temp = NamedTemporaryFile(delete=True)
                list_temp.write(list_pic.content)
                list_temp.flush()
                form.instance.beatmap_list.save(f"{form.instance.beatmap_id}.jpg",
                                                File(list_temp), save=True)
                # Put the beatmap detail from osu! to the RecommendBeatmap object.
                form.instance.beatmapset_id = beatmap_json_data['beatmapset_id']
                form.instance.title = beatmap_json_data['title']
                form.instance.artist = beatmap_json_data['artist']
                form.instance.source = beatmap_json_data['source']
                form.instance.creator = beatmap_json_data['creator']
                form.instance.approved = beatmap_json_data['approved']
                form.instance.difficultyrating = beatmap_json_data['difficultyrating']
                form.instance.bpm = beatmap_json_data['bpm']
                form.instance.version = beatmap_json_data['version']
                form.instance.playcount = beatmap_json_data['playcount']
                form.instance.favourite_count = beatmap_json_data['favourite_count']
                form.instance.total_length = beatmap_json_data['total_length']
                form.instance.creator_id = beatmap_json_data['creator_id']
                form.instance.genre_id = beatmap_json_data['genre_id']
                form.instance.language_id = beatmap_json_data['language_id']
                form.instance.tags = beatmap_json_data['tags']
                form.instance.submit_date = make_aware(datetime.datetime.strptime(beatmap_json_data['submit_date'], '%Y-%m-%d %H:%M:%S'))
                if beatmap_json_data['approved_date'] is not None:
                    form.instance.approved_date = make_aware(datetime.datetime.strptime(beatmap_json_data['approved_date'], '%Y-%m-%d %H:%M:%S'))
                form.instance.last_update = make_aware(datetime.datetime.strptime(beatmap_json_data['last_update'], '%Y-%m-%d %H:%M:%S'))
                # Save the ruleset and user ID to the RecommendBeatmap object.
                form.instance.ruleset_id = ruleset.id
                form.instance.user_id = request.user.id
                # Generate the URL to the osu! web from beatmap ID and beatmapset ID.
                form.instance.url = f"https://osu.ppy.sh/beatmapsets/{beatmap_json_data['beatmapset_id']}#osu/{form.instance.beatmap_id}"
                if request.user.id == int(ruleset.owner):
                    form.instance.owner_approved = True
                    form.instance.owner_seen = True
                form.save()
                if request.user.id == int(ruleset.owner):
                    messages.success(request, gettext("Added %(title)s [%(version)s] as a recommended beatmap successfully!") % {"title": beatmap_json_data['title'], "version": beatmap_json_data['version']})
                else:
                    messages.success(request, gettext("Added %(title)s [%(version)s] to a waiting list! Please wait for the ruleset owner to approve your beatmap!") % {"title": beatmap_json_data['title'], "version": beatmap_json_data['version']})
            else:
                if request_data.status_code != 200:
                    messages.error(request, gettext(f"Adding beatmap failed! (Cannot connect to osu! API)"))
                elif not request_data.json():
                    messages.error(request, gettext(f"Adding beatmap failed! (Beatmap ID not found in osu! mode.)"))
                elif RecommendBeatmap.objects.filter(user_id=str(request.user.id), owner_seen=False,
                                                     beatmap_id=form.instance.beatmap_id).exists():
                    messages.error(request, gettext(f"Adding beatmap failed! (You are already recommend this beatmap.)"))
                elif RecommendBeatmap.objects.filter(beatmap_id=form.instance.beatmap_id, ruleset_id=ruleset.id,
                                                     owner_approved=True, owner_seen=True).exclude(
                    user_id=str(request.user.id)).exists:
                    messages.error(request,
                                   gettext(f"Adding beatmap failed! (This beatmap is already recommended by other user in this ruleset.)"))
                else:
                    messages.error(request, gettext(f"Adding beatmap failed! (Unknown error.)"))
            return redirect('recommend_beatmap', slug=ruleset.slug)
    else:
        form = RecommendBeatmapForm()
    context = {
        'form': form,
        'title': gettext(f'add a new recommend beatmap for %(name)s') % {'name': ruleset.name},
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'ruleset': ruleset,
        'opengraph_url': resolve_url('add_recommend_beatmap', slug=ruleset.slug),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/add_recommend_beatmap.html', context)


def recommend_beatmap(request, slug):
    """
    View for recommend beatmap listing page in the ruleset that include in the slug.

    :param request: WSGI request from user.
    :param slug: Ruleset slug (slug in Ruleset model)
    :type slug: str
    :return: Render the recommend beatmap page and pass the value from context to the template (recommend_beatmap.html)
    """
    ruleset = get_object_or_404(Ruleset, slug=slug)
    hero_image = ruleset.recommend_beatmap_cover.url
    hero_image_light = ruleset.recommend_beatmap_cover.url
    beatmap_list_owner, beatmap_list_other = make_recommend_beatmap_view(ruleset.id)
    if (len(beatmap_list_owner) == 0) and (len(beatmap_list_other) == 0):
        no_beatmap = True
    else:
        no_beatmap = False
    context = {
        'title': gettext('recommend beatmaps for %(name)s') % {'name': ruleset.name},
        'ruleset': ruleset,
        'beatmap_owner': beatmap_list_owner,
        'beatmap_other': beatmap_list_other,
        'is_owner': int(ruleset.owner) == request.user.id,
        'no_beatmap': no_beatmap,
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_url': resolve_url('recommend_beatmap', slug=ruleset.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/recommend_beatmap.html', context)


@login_required
def recommend_beatmap_approval(request, rulesets_slug):
    """
    View for recommend beatmap approval for the ruleset owner.

    If other user that are not ruleset owner try to access this link, a server will reply 302 page.

    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :return: Render the recommend beatmap approval page and pass the value from context to the template (recommend_beatmap_approval.html)
    """
    ruleset = get_object_or_404(Ruleset, slug=rulesets_slug)
    hero_image = ruleset.recommend_beatmap_cover.url
    hero_image_light = ruleset.recommend_beatmap_cover.url
    if request.user.id == int(ruleset.owner) or request.user.is_staff:
        beatmap_list = make_beatmap_aapproval_view(ruleset.id)
        if len(beatmap_list) == 0:
            no_beatmap = True
        else:
            no_beatmap = False
        context = {
            'ruleset': ruleset,
            'beatmap_list': beatmap_list,
            'no_beatmap': no_beatmap,
            'hero_image': hero_image,
            'hero_image_light': hero_image_light,
            'title': gettext('approve a recommend beatmap for %(name)s') % {'name': ruleset.name},
            'opengraph_url': resolve_url('recommend_beatmap', slug=ruleset.slug),
            'opengraph_image': ruleset.opengraph_image.url
        }
        if request.user.is_authenticated:
            translation.activate(request.user.config.language)
        return render(request, 'wiki/recommend_beatmap_approval.html', context)
    else:
        raise PermissionDenied()


@login_required
def approve_recommend_beatmap(request, rulesets_slug, beatmap_id):
    """
    View that are approve the target beatmap.

    If other user that are not ruleset owner try to access this link, a server will reply 302 page.

    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :param beatmap_id: Beatmap ID of that RecommendBeatmap objects
    :type beatmap_id: int
    :return: Redirect to recommend beatmap approval page.
    """
    beatmap = RecommendBeatmap.objects.get(id=beatmap_id)
    ruleset = Ruleset.objects.get(id=beatmap.ruleset_id)
    if request.user.id == int(ruleset.owner) or request.user.is_staff:
        if beatmap.owner_seen:
            messages.error(request, gettext("You already qualified this beatmap!"))
        else:
            beatmap.owner_approved = True
            beatmap.owner_seen = True
            beatmap.save()
            messages.success(request, gettext("Approve beatmap successfully!"))
        return redirect('recommend_beatmap_approval', rulesets_slug)
    else:
        raise PermissionDenied()


@login_required
def deny_recommend_beatmap(request, rulesets_slug, beatmap_id):
    """
    View that are deny the target beatmap and delete it from the database.

    :param request: WSGI request from user.
    :param rulesets_slug: Ruleset slug (slug in Ruleset model)
    :type rulesets_slug: str
    :param beatmap_id: Beatmap ID of that RecommendBeatmap objects
    :type beatmap_id: int
    :return: Redirect to recommend beatmap approval page.
    """
    beatmap = RecommendBeatmap.objects.get(id=beatmap_id)
    ruleset = Ruleset.objects.get(id=beatmap.ruleset_id)
    if request.user.id == int(ruleset.owner) or request.user.is_staff:
        if beatmap.owner_seen:
            messages.error(request, gettext("You already qualified this beatmap!"))
        else:
            # Delete beatmap cover and thumbnail before delete the object out
            os.remove(f"media/{beatmap.beatmap_cover}")
            os.remove(f"media/{beatmap.beatmap_thumbnail}")
            beatmap.delete()
            messages.success(request, gettext("Deny beatmap successfully!"))
        return redirect('recommend_beatmap_approval', rulesets_slug)
    else:
        raise PermissionDenied()


def status(request):
    """
    View for status page.

    :param request: WSGI request from user.
    :return: Render the status page and pass the value from context to the template (status.html)
    """
    hero_image = 'img/status-cover-night.jpg'
    hero_image_light = 'img/status-cover-light.png'
    context = {
        'all_ruleset': make_status_view(),
        'title': gettext('status'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('status_description'),
        'opengraph_url': resolve_url('status')
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/status.html', context)


def install_localization_page(request):
    """
    View for how to install localisation file page. This page is static so nothing much here.

    :param request: WSGI request from user.
    :return: Render the install page and pass the value from context to the template (localisation_how_to.html)
    """
    hero_image = 'img/install-localization-cover-night.jpg'
    hero_image_light = 'img/install-localization-cover-light.png'
    context = {
        'title': gettext('install_and_update_localization'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('install_and_update_localization_description'),
        'opengraph_url': resolve_url('install_localization_page'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/localisation_how_to.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def maintainer_menu(request):
    """
    View for maintainer menu page.

    This page can only access by superuser and maintainer.

    :param request: WSGI request from user.
    :return: Render the maintainer menu page and pass the value from context to the template (maintainer.html)
    """
    hero_image = 'img/maintainer-cover-night.png'
    hero_image_light = 'img/maintainer-cover-light.jpg'
    action_list = []
    for action in Action.objects.all().order_by('-id'):
        action_list.append([action, get_user_by_id(action.start_user)])
    context = {
        'action_list': action_list,
        'title': gettext('maintainer_menu'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('maintainer_menu_description'),
        'opengraph_url': resolve_url('maintainer')
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/maintainer.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_beatmap_action(request):
    """
    View for activate the new runner for running update_all_beatmap_action function.

    This view can only activate by superuser and staff. Mainly activate by Maintainer menu.

    :param request: WSGI request from user.
    :return: Redirect to maintainer menu with message
    """
    action_log = Action()
    action_log.title = "Update all beatmap metadata"
    action_log.action_field = "maintainer"
    action_log.running_text = "Start working thread..."
    action_log.status = 1
    action_log.start_user = request.user.id
    action_log.save()
    thread_worker = threading.Thread(target=update_all_beatmap_action, args=[action_log])
    thread_worker.setDaemon(True)
    thread_worker.start()
    messages.success(request, f"Start worker successfully! (Log ID : {action_log.id})")
    return redirect('maintainer')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_ruleset_status_action(request):
    """
    View for activate the new runner for running update_ruleset_version_action function.

    This view can only activate by superuser and staff. Mainly activate by Maintainer menu.

    :param request: WSGI request from user.
    :return: Redirect to maintainer menu with message
    """
    action = Action()
    action.title = "Update ruleset version"
    action.action_field = "maintainer"
    action.running_text = "Start working thread..."
    action.status = 1
    action.start_user = request.user.id
    action.save()
    thread_worker = threading.Thread(target=update_ruleset_version_action, args=[action])
    thread_worker.setDaemon(True)
    thread_worker.start()
    messages.success(request, f"Start worker successfully! (Log ID : {action.id})")
    return redirect('maintainer')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_ruleset_status_once_action(request):
    """
    View for activate the new runner for running update_ruleset_version_once_action function.

    This view can only activate by superuser and staff. Mainly activate by Maintainer menu.

    :param request: WSGI request from user.
    :return: Redirect to maintainer menu with message
    """
    action = Action()
    action.title = "Update ruleset version once"
    action.action_field = "maintainer"
    action.running_text = "Start working thread..."
    action.status = 1
    action.start_user = request.user.id
    action.save()
    thread_worker = threading.Thread(target=update_ruleset_version_once_action, args=[action])
    thread_worker.setDaemon(True)
    thread_worker.start()
    messages.success(request, f"Start worker successfully! (Log ID : {action.id})")
    return redirect('maintainer')


def check_action_log(request, log_id):
    """
    API that will update the action progress on the action log list.

    :param request: WSGI request from user.
    :param log_id: Action ID that want to request the progress.
    :return: JSON contain running_text, status and duration.
    """
    action = get_object_or_404(Action, id=log_id)
    if action.status == 1 or action.status == 0:
        duration = (timezone.now() - action.time_start).total_seconds()
    elif action.status == 2:
        duration = (action.time_finish - action.time_start).total_seconds()
    else:
        duration = "Unknown"

    if duration != "Unknown":
        hours = duration // 3600
        duration = duration - (hours * 3600)
        minutes = duration // 60
        seconds = duration - (minutes * 60)
        duration = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    if request.method == "GET":
        return JsonResponse({"running_text": action.running_text, "status": action.status, "duration": duration},
                            status=200)
    return JsonResponse({}, status=400)


def archived_rulesets(request):
    """
    View for show the archived rulesets.

    :param request: WSGI request from user.
    :return: Render archived_rulesets.html with context
    """
    hero_image = "img/archived-rulesets-cover-night.jpg"
    hero_image_light = "img/archived-rulesets-cover-light.png"
    context = {
        'rulesets': make_listing_view(Ruleset.objects.filter(archive=True, hidden=False).order_by(Lower('name'))),
        'title': gettext('archived_rulesets'),
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': gettext('archived_rulesets_description'),
        'opengraph_url': resolve_url('listing'),
    }
    if request.user.is_authenticated:
        translation.activate(request.user.config.language)
    return render(request, 'wiki/archived_rulesets.html', context)


# Fallback view for redirect user from old website URL to the new website's path


def redirect_from_old_link(request, slug):
    """
    View for redirect the user that use the old link path (pages/<RulesetsName>) to the new path
    that we currently use (rulesets/<RulesetsName>)

    :param request: WSGI request from user
    :param slug: Ruleset slug (slug in Ruleset model)
    :return: Redirect the user to the cuurent wiki_page's link
    """
    if Ruleset.objects.filter(slug=slug).exists():
        return redirect('wiki', slug=slug)
    else:
        return HttpResponse(status=404)
