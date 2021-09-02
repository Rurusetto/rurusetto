from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth import logout
from .forms import UserUpdateForm, ProfileUpdateForm, UpdateProfileEveryLoginConfigForm, UserDeleteAccountForm, UserConfigForm, UserSubpageConfigForm
from .models import Profile, Tag
from allauth.socialaccount.models import SocialAccount
from wiki.function import fetch_created_ruleset


@login_required
def settings(request):
    """
    View for setting form and related user setting like website configuration that is from Account and Config model.
    User must be logged in before access this page.

    This view has many condition due to the UpdateProfileEveryLogin setting that need more condition requirement on save.

    :param request: WSGI request from user.
    :return: Render the settings page with the many account related form and pass the value from context to the template (settings.html)
    """
    hero_image = "img/settings-cover-night.jpeg"
    hero_image_light = 'img/settings-cover-light.png'
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(request.POST, instance=request.user.config)
        website_config_form = UserConfigForm(request.POST, instance=request.user.config)
        subpage_config_form = UserSubpageConfigForm(request.POST, instance=request.user.config)
        if SocialAccount.objects.filter(user=request.user).exists():
            # User that send request are login by social account, must check on profile sync field
            if profile_sync_form['update_profile_every_login'].value() == request.user.config.update_profile_every_login:
                # If value from the form and the value in database is the same, user doesn't change this config
                if not profile_sync_form['update_profile_every_login'].value():
                    # Tha value in form and database is all False -> User want to change value in other form
                    user_form.save()
                    profile_form.save()
                    website_config_form.save()
                    subpage_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
                else:
                    # Nothing changed here except website config that must be save
                    website_config_form.save()
                    subpage_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
            else:
                if not profile_sync_form['update_profile_every_login'].value() and request.user.config.update_profile_every_login:
                    # User want to change sync config from True to False, save only sync config value
                    profile_sync_form.save()
                    website_config_form.save()
                    subpage_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
                else:
                    # User want to change sync config from False to True, must check on the valid of other form too.
                    user_form.save()
                    profile_form.save()
                    profile_sync_form.save()
                    website_config_form.save()
                    subpage_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
        else:
            # User that send request are login by normal Django login, cannot use profile sync system.
            # So we don't have to save profile_sync_form value
            user_form.save()
            profile_form.save()
            website_config_form.save()
            subpage_config_form.save()
            messages.success(request, f'Your settings has been updated!')
            return redirect('settings')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(instance=request.user.config)
        website_config_form = UserConfigForm(instance=request.user.config)
        subpage_config_form = UserSubpageConfigForm(instance=request.user.config)

    if SocialAccount.objects.filter(user=request.user).exists():
        osu_confirm_username = SocialAccount.objects.get(user=request.user).extra_data['username']
    else:
        osu_confirm_username = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_sync_form': profile_sync_form,
        'website_config_form': website_config_form,
        'website_subpage_config_form': subpage_config_form,
        'title': 'settings',
        'social_account': SocialAccount.objects.filter(user=request.user).exists(),
        'can_edit_profile': (not SocialAccount.objects.filter(user=request.user).exists()) or (SocialAccount.objects.filter(user=request.user).exists() and (not request.user.config.update_profile_every_login)),
        'osu_confirm_username': osu_confirm_username,
        'hero_image': static(hero_image),
        'hero_image_light': static(hero_image_light),
        'opengraph_description': 'All profile and website settings are here!',
        'opengraph_url': resolve_url('settings'),
        'opengraph_image': static(hero_image)
    }

    return render(request, 'users/settings.html', context)


def profile_detail(request, pk):
    """
    View for user detail page or user profile page. Can access publicly but if user open your own profile page it
    will have 'Edit profile' button that navigate to setting page.

    :param request: WSGI request from user
    :param pk: User ID
    :type pk: int
    :return: Render the profile detail page and pass the value from context to the template (profile.html)
    """
    profile_object = get_object_or_404(Profile, pk=pk)
    tag_list = profile_object.tag.split(',')
    tag_object_list = []
    for tag_id in tag_list:
        tag_id = int(tag_id)
        try:
            tag_object_list.append(Tag.objects.get(id=tag_id))
        except Tag.DoesNotExist:
            pass

    context = {
        'profile_object': profile_object,
        'tag_list': tag_object_list,
        'created_ruleset': fetch_created_ruleset(profile_object.id),
        'title': f"{profile_object.user.username}'s profile",
        'hero_image': profile_object.cover.url,
        'hero_image_light': profile_object.cover.url,
        'opengraph_description': f"{profile_object.user.username}'s profile page",
        'opengraph_url': resolve_url('profile', pk=profile_object.user.id),
        'opengraph_image': profile_object.cover.url
    }
    return render(request, 'users/profile.html', context)


@login_required
def delete_account(request):
    """
    View for delete account page. User must be logged in before access this page.
    This view has function for verification when the condition is met it will logout the user before delete the User, Profile and Config objects.

    :param request: WSGI request from user
    :return: Render the delete account page with delete account form and pass the value from context to the template (delete_account.html)
    """
    if request.method == 'POST':
        account_delete_form = UserDeleteAccountForm(request.POST)
        if request.user.username == account_delete_form['confirm_username'].value() and request.user.check_password(account_delete_form['confirm_password'].value()):
            user = request.user
            # Logout before we delete. This will make request.user
            # unavailable (or actually, it points to AnonymousUser).
            logout(request)
            # Delete user (and any associated ForeignKeys, according to
            # on_delete parameters).
            user.delete()
            messages.success(request, 'Account successfully deleted.')
            return redirect('home')
        else:
            messages.error(request, f'Delete Account failed. Please check your username and password.')
            return redirect('settings')
    else:
        account_delete_form = UserDeleteAccountForm()

    context = {
        'form': account_delete_form
    }
    return render(request, 'users/delete_account.html', context)
