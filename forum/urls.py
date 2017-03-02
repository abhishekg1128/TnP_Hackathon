from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'forum'

urlpatterns = [
    # url(r'^$', views.index, name='forum-index'),
    url(r'^(?P<forum_id>[0-9]+)/$', views.forum, name='forum-detail'),
    url(r'^topic/(\d+)/$', views.topic, name='topic-detail'),
    url(r'^reply/(\d+)/$', views.post_reply, name='reply'),
    url(r'newtopic/(\d+)/$', views.new_topic, name='new-topic'),
]
