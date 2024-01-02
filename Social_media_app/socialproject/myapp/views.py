from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from posts.models import Post

# Create your views here.

def user_login(req):

    if req.method=="POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(req,username=data['username'],password=data['password'])
            if user is not None:
                login(req,user)
                return HttpResponse('user succesfully logged in')
            else:
                return HttpResponse('user does not exist')

    else:
        form = LoginForm

    res = render(req,'users/login.html', {'form':form})
    return res

@login_required
def index(req):
    current_user = req.user
    posts = Post.objects.filter(user=current_user)
    profile = Profile.objects.filter(user=current_user).first()
    res = render(req, 'users/index.html', {'posts':posts, 'profile':profile})
    return res

def user_registration(req):

    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.save()
            return render(req,'users/registration_done.html')
    else:
        form = RegistrationForm()
    return render(req,'users/registration.html', {'form':form})

@login_required
def edit(req):

    if req.method=='POST':
        user_form = UserEditForm(instance=req.user, data=req.POST)
        profile_form = ProfileEditForm(instance=req.user.profile, data=req.POST, files=req.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            res = render(req, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})
        return res
    else:
        user_form = UserEditForm(instance=req.user)
        # profile_form = ProfileEditForm(instance=req.user.profile)

    return render(req, 'users/edit.html', {'user_form': user_form})
