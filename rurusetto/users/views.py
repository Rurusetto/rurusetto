from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UpdateProfileEveryLoginConfigForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can log in now!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title': 'register'
    }
    return render(request, 'users/register.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(request.POST, instance=request.user.config)
        if request.user.profile.social_account:
            # User that send request are login by social account, must check on profile sync field
            if profile_sync_form['update_profile_every_login'].value() == request.user.config.update_profile_every_login:
                # If value from the form and the value in database is the same, user doesn't change this config
                if not profile_sync_form['update_profile_every_login'].value():
                    # Tha value in form and database is all False -> User want to change value in other form
                    user_form.save()
                    profile_form.save()
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
                    messages.success(request, f'Your settings has been updated!')
                    return redirect('settings')
        else:
            # User that send request are login by normal Django login, cannot use profile sync system.
            # So we don't have to save profile_sync_form value
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your settings has been updated!')
            return redirect('settings')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile_sync_form = UpdateProfileEveryLoginConfigForm(instance=request.user.config)

    if (not request.user.profile.social_account) or (
            request.user.profile.social_account and (not request.user.config.update_profile_every_login)):
        can_edit_profile = True
    else:
        can_edit_profile = False

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_sync_form': profile_sync_form,
        'title': 'settings',
        'can_edit_profile': can_edit_profile,
    }

    return render(request, 'users/settings.html', context)


def profile_detail(request, pk):
    profile_object = get_object_or_404(Profile, pk=pk)

    if "http://" in profile_object.website:
        website_show = profile_object.website.replace("http://", "")
    else:
        website_show = profile_object.website.replace("https://", "")

    context = {
        'profile_object': profile_object,
        'title': f"{profile_object.user.username}'s profile",
        'website_show': website_show
    }
    return render(request, 'users/profile.html', context)
