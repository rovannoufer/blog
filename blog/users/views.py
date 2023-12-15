from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profiles = Profile.objects.get(id=pk)
    topSkills = profiles.skill_set.exclude(description__exact="")
    otherSkills = profiles.skill_set.filter(description="")

    context = {'profile': profiles,'topSkills': topSkills,
               "otherSkills": otherSkills}
    return render(request, 'users/user-profile.html',context)



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
                # auth.login(request, user)
                return redirect('login')
            except:
                error_message = 'Error on creating account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = 'Password don\'t match'
            return render(request, 'users/signup.html', {'error_message': error_message})
    return render(request, 'users/sign_up.html')