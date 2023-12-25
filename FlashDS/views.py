# Using Python Libraries in Django
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import login
from . import forms
from FlashDS.models import Client

# Create your views here.
##
def home(request):
    client = Client.objects.all()
    return render(request, 'home.html',{
        "client":client
    })
# -------------------------------------------
#function for the sign up form#
def sign_up(request):
    sign_up_form = forms.Sign_up_Form()
    #if theres a post request from user
    if request.method == "POST":
        sign_up_form = forms.Sign_up_Form(request.POST)
        #if data is valid
        if sign_up_form.is_valid():
            email = sign_up_form.cleaned_data.get('email').lower()
            user = sign_up_form.save(commit=False)
            user.username = email
            user.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')
    return render(request, 'sign_up.html', {
        "sign_up_form": sign_up_form
    })
# -------------------------------------------
