from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth import logout
from .forms import UserUpdateForm, ProfileUpdateForm, UpdateProfileEveryLoginConfigForm, UserDeleteAccountForm, UserConfigForm
from .models import Profile
from allauth.socialaccount.models import SocialAccount


@login_required
def settings(request):
    hero_image = "img/737403.png"
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(request.POST, instance=request.user.config)
        website_config_form = UserConfigForm(request.POST, instance=request.user.config)
        if SocialAccount.objects.filter(user=request.user).exists():
            # User that send request are login by social account, must check on profile sync field
            if profile_sync_form['update_profile_every_login'].value() == request.user.config.update_profile_every_login:
                # If value from the form and the value in database is the same, user doesn't change this config
                if not profile_sync_form['update_profile_every_login'].value():
                    # Tha value in form and database is all False -> User want to change value in other form
                    user_form.save()
                    profile_form.save()
                    website_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
                else:
                    # Nothing changed here
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
            else:
                if not profile_sync_form['update_profile_every_login'].value() and request.user.config.update_profile_every_login:
                    # User want to change sync config from True to False, save only sync config value
                    profile_sync_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
                else:
                    # User want to change sync config from False to True, must check on the valid of other form too.
                    user_form.save()
                    profile_form.save()
                    profile_sync_form.save()
                    website_config_form.save()
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
        else:
            # User that send request are login by normal Django login, cannot use profile sync system.
            # So we don't have to save profile_sync_form value
            user_form.save()
            profile_form.save()
            website_config_form.save()
            messages.success(request, f'Your settings has been updated!')
            return redirect('settings')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(instance=request.user.config)
        website_config_form = UserConfigForm(instance=request.user.config)

    if (not SocialAccount.objects.filter(user=request.user).exists()) or (
            SocialAccount.objects.filter(user=request.user).exists() and (not request.user.config.update_profile_every_login)):
        can_edit_profile = True
    else:
        can_edit_profile = False

    if SocialAccount.objects.filter(user=request.user).exists():
        osu_confirm_username = SocialAccount.objects.get(user=request.user).extra_data['username']
    else:
        osu_confirm_username = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_sync_form': profile_sync_form,
        'website_config_form': website_config_form,
        'title': 'settings',
        'social_account': SocialAccount.objects.filter(user=request.user).exists(),
        'can_edit_profile': can_edit_profile,
        'osu_confirm_username': osu_confirm_username,
        'hero_image': hero_image,
        'opengraph_description': 'All profile and website settings are here!',
        'opengraph_url': resolve_url('settings'),
        'opengraph_image': static(hero_image)
    }

    return render(request, 'users/settings.html', context)


def profile_detail(request, pk):
    profile_object = get_object_or_404(Profile, pk=pk)

    context = {
        'profile_object': profile_object,
        'title': f"{profile_object.user.username}'s profile",
        'hero_image': profile_object.cover.url,
        'opengraph_description': f"{profile_object.user.username}'s profile page",
        'opengraph_url': resolve_url('profile', pk=profile_object.user.id),
        'opengraph_image': profile_object.cover.url
    }
    return render(request, 'users/profile.html', context)


@login_required
def delete_account(request):
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