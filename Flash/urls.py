"""
URL configuration for Flash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from FlashDS import views
from django.conf import settings
from django.conf.urls.static import static
from FlashDS.client import views as client_views
from django.views.generic import TemplateView
from FlashDS.courier import views as courier_views, apis as courier_apis
# -------------------------------------------------------------------------
client_urlpatterns = [
    path('',client_views.home, name='home'),
    path('profile/',client_views.client_profile, name='profile'),
    path('payment/',client_views.client_Payment, name='payment'),
    path('job_request/',client_views.job_request, name='job_request'),
    path('task/current',client_views.current_task, name='current_task'),
    path('task/done',client_views.done_task, name='done_task'),
    path('task/<task_id>/',client_views.task_info, name='task_status'),
]
# -------------------------------------------------------------------------

courier_urlpatterns = [
    path('',courier_views.home, name='home'),
    path('task/available/',courier_views.available_task_page, name='available_task'), 
    path('task/available/<id>/',courier_views.tasks_details_page, name='tasks_details'), 
    path('task/current/',courier_views.current_task_page, name='current_task'), 
    path('task/current/<id>/task_picture/',courier_views.current_task_picture_page, name='current_task_picture'), 
    path('task/done/',courier_views.task_done_page, name='task_done'), 
    path('task/archive/',courier_views.task_archive_page, name='task_archive'), 
    path('Profile/',courier_views.Profile_page, name='Profile_page'), 
    path('payout/',courier_views.payout_page, name='payout_page'), 

    path('api/task/current/<str:id>/update/',courier_apis.current_task_update_api, name='current_task_update_api'), 
    path('api/task/available/',courier_apis.available_task_api, name='available_task_api'), 
    path('api/fcm_token/upgrade/',courier_apis.fcm_token_upgrade_api, name='fcm_token_upgrade_api'), 
]
# -------------------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('accounts/', include('allauth.urls')),

    path('sign-in/', auth_views.LoginView.as_view(template_name="sign_in.html")),
    path('sign-out/', auth_views.LogoutView.as_view(next_page="/")),
    path('sign-up/',views.sign_up),
    
    path('client/', include((client_urlpatterns,"client"))),
    path('courier/', include((courier_urlpatterns, "courier"))),
    path('firebase-messaging-sw.js',(TemplateView.as_view(template_name='firebase-messaging-sw.js',content_type='application/javascript',))),
]
#--------------------------------------------------------------------------
#durning developing mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
#------------------------------------------------------------------------