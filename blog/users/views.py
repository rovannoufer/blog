from django.shortcuts import render,redirect
from .models import Profile, Skill
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SkillForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def profiles(request):

    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__iexact = search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = search_query) | Q(short_intro__icontains = search_query) | Q(skill__in = skills) )
    

    page = request.GET.get('page')
    results = 3
    
    paginator = Paginator(profiles, results)
    
    try:
       profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)   

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        rightindex = paginator.num_pages + 1

    custom_range = range(left_index,right_index)
    
    context = {'profiles': profiles, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profiles = Profile.objects.get(id=pk)
    topSkills = profiles.skill_set.exclude(description__exact="")
    otherSkills = profiles.skill_set.filter(description="")

    context = {'profile': profiles,'topSkills': topSkills,
               "otherSkills": otherSkills}
    return render(request, 'users/user-profile.html',context)

@login_required(login_url='login')
def user_account(request):
    profiles = request.user.profile
    topSkills = profiles.skill_set.all()
    projects = profiles.project_set.all()
    context = {'profile':profiles, 'skills': topSkills, 'projects': projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect('user_account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)


def login(request):

    if request.user.is_authenticated:
        return redirect('blogs')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
          messages.error(request, "Username doesn't exist")

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('blogs')

        else:
           messages.error(request, "Username OR password is incorrect")

    return render(request, 'users/login.html')





def logout(request):
    auth.logout(request)
    messages.error(request, "User was successfully logged out")
    return redirect('login')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('edit_account')
            except:
                error_message = 'Error on creating account'
                return render(request, 'users/sign_up.html', {'error_message': error_message})
        else:
            error_message = 'Password don\'t match'
            return render(request, 'users/sign_up.html', {'error_message': error_message})
    return render(request, 'users/sign_up.html')


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('user_account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)




@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('user_account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('user_account')

    context = {'blogs': skill}
    return render(request, 'core/delete_blog.html', context)