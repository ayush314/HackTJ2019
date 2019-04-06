from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Team, HackerProfile, InfoSection, HackerForm, UserForm, LoginForm, TeamCreationForm, \
    TeamJoiningForm, HardwareItem, BreakfastForm, LunchForm, DinnerForm


def index(request):
    sections = InfoSection.objects.all()

    return render(request, 'core/index.html', {'sections': sections})


def register(request):
    successful = False
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        hacker_form = HackerForm(request.POST, prefix='hacker')

        if user_form.is_valid() and hacker_form.is_valid():
            user = user_form.save()
            hacker_profile = hacker_form.save(commit=False)
            hacker_profile.user = user
            hacker_profile.save()
            hacker_form.save_m2m()

            successful = True
        else:
            return render(request, 'core/register.html', {'user_form': user_form, 'hacker_form': hacker_form, 'successful': successful})

    else:
        user_form = UserForm(prefix='user')
        hacker_form = HackerForm(prefix='hacker')

    return render(request, 'core/register.html',
                  {'user_form': user_form, 'hacker_form': hacker_form, 'successful': successful})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, prefix='login')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if 'login-next' in request.POST:
                    return redirect(form.cleaned_data['next'])
                return redirect('/')

        else:
            return render(request, 'core/login.html', {'form': form})

    else:
        form = LoginForm(prefix='login')

    return render(request, 'core/login.html', {'form': form})


@login_required
def manage_profile(request):
    context = {}
    if request.method == 'POST':
        if 'submit-new-team' in request.POST:
            new_team_form = TeamCreationForm(request.POST, prefix='new_team')
            if new_team_form.is_valid():
                new_team = new_team_form.save()
                new_team.hackerprofile_set.add(request.user.hackerprofile)0
            else:
                return render(request, 'core/manage.html', {'new_team_form': new_team_form})
        if 'submit-join-team' in request.POST:
            join_team_form = TeamJoiningForm(request.POST, prefix='join_team')
            if join_team_form.is_valid():
                Team.objects.get(code=join_team_form.cleaned_data['code']).hackerprofile_set.add(
                    request.user.hackerprofile)
            else:
                return render(request, 'core/manage.html', {'join_team_form': join_team_form})

        if 'submit-leave-team' in request.POST:
            team = request.user.hackerprofile.team
            request.user.hackerprofile.team = None
            request.user.hackerprofile.save()
            if HackerProfile.objects.filter(team__code=team.code).count() == 0:
                team.delete()

        if 'submit-breakfast' in request.POST:
            breakfast_form = BreakfastForm(request.POST, prefix='breakfast')
            if breakfast_form.is_valid():
                request.user.hackerprofile.breakfast = breakfast_form.cleaned_data['choice']
                request.user.hackerprofile.save()

        if 'submit-lunch' in request.POST:
            lunch_form = LunchForm(request.POST, prefix='lunch')
            if lunch_form.is_valid():
                request.user.hackerprofile.lunch = lunch_form.cleaned_data['choice']
                request.user.hackerprofile.save()

        if 'submit-dinner' in request.POST:
            dinner_form = DinnerForm(request.POST, prefix='dinner')
            if dinner_form.is_valid():
                request.user.hackerprofile.dinner = dinner_form.cleaned_data['choice']
                request.user.hackerprofile.save()

    if request.user.hackerprofile.breakfast is None:
        breakfast_form = BreakfastForm(prefix='breakfast')
        context['breakfast_form'] = breakfast_form

    if request.user.hackerprofile.lunch is None:
        lunch_form = LunchForm(prefix='lunch')
        context['lunch_form'] = lunch_form

    if request.user.hackerprofile.dinner is None:
        dinner_form = DinnerForm(prefix='dinner')
        context['dinner_form'] = dinner_form

    if request.user.hackerprofile.team is None:
        new_team_form = TeamCreationForm(prefix='new_team')
        join_team_form = TeamJoiningForm(prefix='join_team')
        context['new_team_form'] = new_team_form
        context['join_team_form'] = join_team_form
    else:
        context['team_members'] = User.objects.filter(hackerprofile__team__name=request.user.hackerprofile.team.name)

    context['your_hardware'] = HardwareItem.objects.filter(hacker=request.user.hackerprofile)
    context['available_hardware'] = HardwareItem.objects.filter(hacker__isnull=True)

    return render(request, 'core/manage.html', context)


def paramount(request):
    return render(request, 'core/paramount.html', {})
