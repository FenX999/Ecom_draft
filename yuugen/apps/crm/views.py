from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.



def crm_home(request):
    return TemplateResponse(request, 'crm/navigation/crm-home.html')