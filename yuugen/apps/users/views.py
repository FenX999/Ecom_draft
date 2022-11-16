from django.template.response import TemplateResponse
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)

from yuugen.apps.core.profile import get_or_create_store_proxy_user

from .models import (
    User,
)

from .forms import(
    UserCreationForm,
)



def login_view(request):
    template = 'users/navigation/login.html'
    app = request.get_full_path().split('/')[1]
    url = app+':home'
    context = {'path': app}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect(url)
        else:
            messages.error(request, "Email or password does not exist")
    return TemplateResponse(request, template, context)

def logout_view(request):
    app = request.get_full_path().split('/')[1]
    url = app+':home'
    logout(request)
    return redirect(url)

def register_view(request):
    template = 'users/navigation/register.html'
    app = request.get_full_path().split('/')[1]
    creator = request.user.email
    url = app+':home'
    print(f"current url is: {app}")
    if app == 'shop'and  request.user.is_anonymous:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            print(f'errors shows as:\n{form.errors}')
            if form.is_valid():
                print(f' form valid as:\n{form.cleaned_data}')
                user = form.save(commit=False)
                user.url_creation = app
                print(f'url creation = {user.url_creation}')
                user.save()
                login(request, user)
                return redirect(url)
        else: 
            form = UserCreationForm()

    elif app != 'shop':
        if request.user.is_manager:
            if request.method == 'POST':
                form = UserCreationForm(request.POST)
                form.fields['created_by'].queryset = User.objects.filter(Q(is_manager=True) & Q(groups__name=app) | Q(is_superuser=True) )
                print(f'errors shows as:\n{form.errors}')
                if form.is_valid():
                    
                    print(f' form valid as:\n{form.cleaned_data}')
                    user = form.save(commit=False)
                    user.url_creation = app
                    print(f'url creation = {user.url_creation}')
                    user.save()
                    return redirect(url)
            else: 
                form = UserCreationForm()
        else:
            return HttpResponseForbidden
    context = {
        'form':form,
        'path': app,
        'creator' : creator,
    }
    return TemplateResponse(request, template, context)