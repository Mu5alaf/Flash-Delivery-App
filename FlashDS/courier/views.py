# Using Python Libraries in Django
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from FlashDS.models import *
from django.contrib import messages
from FlashDS.courier import forms

# Create your views here.


@login_required(login_url="/sign-in/?next=/courier/")
def home(request):
    return redirect(reverse('courier:available_task'))
# -------------------------------------------------------------


@login_required(login_url="/sign-in/?next=/courier/")
def available_task_page(request):
    context = {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    }
    return render(request, 'courier/available_task.html', context)
# -------------------------------------------------------------


@login_required(login_url="/sign-in/?next=/courier/")
def tasks_details_page(request, id):
    task = Request.objects.filter(
        pk=id, status=Request.PROCESSING_STATUS).last()
    if not task:
        return redirect(reverse('courier:available_task'))
    if request.method == "POST":
        task.courier = request.user.courier
        task.status = task.PICKING_STATUS
        task.save()
        return redirect(reverse('courier:available_task'))
    context = {
        "task": task,
    }
    return render(request, 'courier/tasks_details.html', context)
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def current_task_page(request):
    # Retrieve the latest task for the current courier with a certain status
    task = Request.objects.filter(
        courier=request.user.courier,
        status__in=[Request.PICKING_STATUS, Request.DELIVERING_STATUS]
    ).last()
    # Create a context dictionary containing the task and Google Maps API key
    context = {
        "task": task,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    }

    # Render the 'courier/current_task.html' template with the provided context
    return render(request, 'courier/current_task.html', context)
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def current_task_picture_page (request,id):
    task = Request.objects.filter(
        id=id,
        courier = request.user.courier,
        status__in={
            Request.PICKING_STATUS,
            Request.DELIVERING_STATUS
        }
    ).last()

    if not task :
        return redirect(reverse("courier:current_task"))
    context={
        "task":task,
    }
    return render(request,'courier/current_task_picture.html',context)
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def task_done_page (request):
    return render(request,'courier/task_done.html')
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def task_archive_page (request):
    task = Request.objects.filter(
        courier = request.user.courier,
        status=Request.COMPLETED_STATUS
    )
    return render(request,'courier/task_archive.html',{
        "task":task,
    })
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def Profile_page (request):
    task = Request.objects.filter(
        courier=request.user.courier,
        status=Request.COMPLETED_STATUS
    )
    total_service = round(sum(Request.price for Request in task ) * 0.5, 2)
    total_tasks = len(task)
    total_dist = sum(Request.distance for Request in task)
    context = {
        "total_service":total_service,
        "total_tasks":total_tasks,
        "total_dist":total_dist,
    }
    return render(request,'courier/profile.html',context)
# -------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/courier/")
def payout_page (request):
    payout_form = forms.PayoutForm(instance=request.user.courier)
    if request.method == "POST":
        payout_form = forms.PayoutForm(request.POST,instance=request.user.courier)
        if payout_form.is_valid():
            payout_form.save()
            messages.success(request,"Payout Mail has been added sucssefuly ")
            return redirect(reverse('courier:Profile_page'))
    context={
        "payout_form":payout_form,
        }
    return render(request,'courier/payout.html',context)

