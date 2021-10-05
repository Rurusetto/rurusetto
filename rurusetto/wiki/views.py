from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import RulesetSerializer
from .models import Changelog, Ruleset, Subpage, RecommendBeatmap, Action
from users.models import Profile
from django.contrib.auth.models import User
from .forms import RulesetForm, SubpageForm, RecommendBeatmapForm
from .function import make_listing_view, make_wiki_view, source_link_type, get_user_by_id, make_recommend_beatmap_view, \
    make_beatmap_aapproval_view, make_status_view
from unidecode import unidecode
from django.template.defaultfilters import slugify
from rurusetto.settings import OSU_API_V1_KEY
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
import os
import threading
from .action import update_all_beatmap_action


def home(request):
    """
    View for homepage.

    :param request: WSGI request from user
    :return: Render the wiki page and pass the value from context to the template (home.html)
    """
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
        'latest_add_rulesets': make_listing_view(latest_add_rulesets)
        # Use make_listing_view function to get the User object from database and pass to template
    }
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
        'title': 'changelog',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'All update history of website are here.',
        'opengraph_url': resolve_url('changelog'),
    }
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
        'rulesets': make_listing_view(Ruleset.objects.all()),
        'title': 'listing',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'List of available rulesets.',
        'opengraph_url': resolve_url('listing'),
    }
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
            messages.success(request, f'Ruleset name {name} has added to the list!')
            return redirect('listing')
    else:
        form = RulesetForm()
    context = {
        'form': form,
        'title': 'add a new ruleset',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': "Let's add a new ruleset! Is it yours? Don't worry! You can add it even if you didn't make the ruleset.",
        'opengraph_url': resolve_url('create_ruleset'),
    }
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
    can_support = False
    try:
        ruleset_owner_profile = Profile.objects.get(user=User.objects.get(id=int(ruleset.owner)))
        if ruleset_owner_profile.support_message != '':
            can_support = True
    except User.DoesNotExist:
        can_support = False
    hero_image = ruleset.cover_image.url
    hero_image_light = ruleset.cover_image.url
    if (ruleset.source != "") and (ruleset.github_download_filename != "") and (
            source_link_type(ruleset.source) == "github"):
        # Currently support for GitHub so let's generate link by this method
        can_download = True
        if ruleset.source[-1] != "/":
            download_link = f"{ruleset.source}/releases/latest/download/{ruleset.github_download_filename}"
        else:
            download_link = f"{ruleset.source}releases/latest/download/{ruleset.github_download_filename}"
    else:
        can_download = False
        download_link = "/#"
    context = {
        'content': ruleset,
        'subpage': Subpage.objects.filter(ruleset_id=ruleset.id),
        'source_type': source_link_type(ruleset.source),
        'user_detail': make_wiki_view(ruleset),
        'can_support': can_support,
        'can_download': can_download,
        'download_link': download_link,
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
    if request.method == 'POST':
        form = RulesetForm(request.POST, request.FILES, instance=ruleset)
        if form.is_valid():
            if source_link_type(form.instance.source) == "github":
                # Check that the download link when render is valid
                if form.instance.source[-1] != "/":
                    download_url = f"{form.instance.source}/releases/latest/download/{form.instance.github_download_filename}"
                else:
                    download_url = f"{form.instance.source}releases/latest/download/{form.instance.github_download_filename}"
                html_status = requests.head(download_url)
                if (html_status.status_code != 200) and (html_status.status_code != 302):
                    error_message = f"The response of {download_url} is not success ({html_status.status_code}). Please check your filename or ruleset source link!"
                    messages.error(request, error_message)
                    return redirect('edit_wiki', slug=ruleset.slug)
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
        'ruleset': ruleset,
        'name': Ruleset.objects.get(slug=slug).name,
        'source_type': source_link_type(ruleset.source),
        'title': f'edit {ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': f'You are currently editing content on ruleset named "{Ruleset.objects.get(slug=slug).name}".',
        'opengraph_url': resolve_url('edit_wiki', slug=slug),
    }
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
    }
    return render(request, 'wiki/add_subpage.html', context)


def install(request):
    """
    View for install page. This page is static so nothing much here.
    
    :param request: WSGI request from user.
    :return: Render the install page and pass the value from context to the template (install.html)
    """
    hero_image = 'img/install-cover-night.png'
    hero_image_light = 'img/install-cover-light.jpeg'
    context = {
        'title': 'install and update rulesets',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'How to install and update rulesets by using Rūrusetto.',
        'opengraph_url': resolve_url('install'),
    }
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
    }
    return render(request, 'wiki/edit_subpage.html', context)


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
                    messages.success(request,
                                     f"Added {beatmap_json_data['title']} [{beatmap_json_data['version']}] as a recommended beatmap successfully!")
                else:
                    messages.success(request,
                                     f"Added {beatmap_json_data['title']} [{beatmap_json_data['version']}] to a waiting list! Please wait for the ruleset owner to approve your beatmap!")
            else:
                if request_data.status_code != 200:
                    messages.error(request, f"Adding beatmap failed! (Cannot connect to osu! API)")
                elif not request_data.json():
                    messages.error(request, f"Adding beatmap failed! (Beatmap ID not found in osu! mode.)")
                elif RecommendBeatmap.objects.filter(user_id=str(request.user.id), owner_seen=False,
                                                     beatmap_id=form.instance.beatmap_id).exists():
                    messages.error(request, f"Adding beatmap failed! (You are already recommend this beatmap.)")
                elif RecommendBeatmap.objects.filter(beatmap_id=form.instance.beatmap_id, ruleset_id=ruleset.id,
                                                     owner_approved=True, owner_seen=True).exclude(
                        user_id=str(request.user.id)).exists:
                    messages.error(request,
                                   f"Adding beatmap failed! (This beatmap is already recommended by other user in this ruleset.)")
                else:
                    messages.error(request, f"Adding beatmap failed! (Unknown error.)")
            return redirect('recommend_beatmap', slug=ruleset.slug)
    else:
        form = RecommendBeatmapForm()
    context = {
        'form': form,
        'title': f'add a new recommend beatmap for {ruleset.name}',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': f'You are currently add a new recommend beatmap for {ruleset.name}.',
        'opengraph_url': resolve_url('add_recommend_beatmap', slug=ruleset.slug),
    }
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
        'title': f'recommend beatmaps for {ruleset.name}',
        'ruleset': ruleset,
        'beatmap_owner': beatmap_list_owner,
        'beatmap_other': beatmap_list_other,
        'is_owner': int(ruleset.owner) == request.user.id,
        'no_beatmap': no_beatmap,
        'hero_image': hero_image,
        'hero_image_light': hero_image_light,
        'opengraph_description': f'Recommend beatmaps for playing with {ruleset.name} from ruleset creator and other player.',
        'opengraph_url': resolve_url('recommend_beatmap', slug=ruleset.slug),
        'opengraph_image': ruleset.opengraph_image.url
    }
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
    if request.user.id == int(ruleset.owner):
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
            'title': f'approve a recommend beatmap for {ruleset.name}',
            'opengraph_description': f"Let's see how is the recommendation from other player.",
            'opengraph_url': resolve_url('recommend_beatmap', slug=ruleset.slug),
            'opengraph_image': ruleset.opengraph_image.url
        }
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
    if request.user.id == int(ruleset.owner):
        if beatmap.owner_seen:
            messages.error(request, f"You already qualified this beatmap!")
        else:
            beatmap.owner_approved = True
            beatmap.owner_seen = True
            beatmap.save()
            messages.success(request, f"Approve beatmap successfully!")
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
    if request.user.id == int(ruleset.owner):
        if beatmap.owner_seen:
            messages.error(request, f"You already qualified this beatmap!")
        else:
            # Delete beatmap cover and thumbnail before delete the object out
            os.remove(f"media/{beatmap.beatmap_cover}")
            os.remove(f"media/{beatmap.beatmap_thumbnail}")
            beatmap.delete()
            messages.success(request, f"Deny beatmap successfully!")
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
    hero_image_light = 'img/status-cover-light.jpg'
    context = {
        'all_ruleset': make_status_view(),
        'title': 'status',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'Status of all rulesets are here. (and you can download and update the rulesets instantly with this page!)',
        'opengraph_url': resolve_url('status')
    }
    return render(request, 'wiki/status.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def maintainer_menu(request):
    hero_image = 'img/status-cover-night.jpg'
    hero_image_light = 'img/status-cover-light.jpg'
    action_list = []
    for action in Action.objects.all().order_by('-id'):
        action_list.append([action, get_user_by_id(action.start_user)])
    context = {
        'action_list': action_list,
        'title': 'maintainer menu',
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'Menu for maintainer only!',
        'opengraph_url': resolve_url('maintainer')
    }
    return render(request, 'wiki/maintainer.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_beatmap_action(request):
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
    # TODO : Docstring


def check_action_log(request, log_id):
    action = get_object_or_404(Action, id=log_id)
    if action.status == 1:
        duration = (timezone.now() - action.time_start).seconds
    elif action.status == 2:
        duration = (action.time_finish - action.time_start).seconds
    else:
        duration = "Unknown"

    if duration != "Unknown":
        hours = duration//3600
        duration = duration - (hours*3600)
        minutes = duration//60
        seconds = duration - (minutes*60)
        duration = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    if request.method == "GET":
        return JsonResponse({"running_text": action.running_text, "status": action.status, "duration": duration}, status=200)
    return JsonResponse({}, status=400)


# Views for API


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
