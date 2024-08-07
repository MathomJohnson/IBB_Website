"""
URL configuration for IBB_Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
import home.views as HomeViews
import appointments.views as AppointmentViews
import forum.views as ForumViews
from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar/', AppointmentViews.calendar),
    path('calendar/add-event/', AppointmentViews.add_event),
    path('calendar/get-events/', AppointmentViews.get_events),
    path('calendar/delete-event/', AppointmentViews.delete_event),
    path('calendar/meet/', AppointmentViews.setup_google_meet),
    path('calendar/google-login', AppointmentViews.google_login),
    path('calendar/oauth2callback', AppointmentViews.oauth2callback),
    path('forum/', ForumViews.main_forum),
    path('forum/submit-question/', ForumViews.submit_question),
    path('forum/new-comment/', ForumViews.new_comment),
    path('forum/get-comments/', ForumViews.get_comments),
    path('register/', v.register),
    path('', HomeViews.homepage),
    path('', include('django.contrib.auth.urls')),
    
]
