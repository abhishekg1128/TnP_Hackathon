from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^for-students$', views.for_students, name='for_students'),
    url(r'^for-companies$', views.for_companies, name='for_companies'),
]
