from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *


def home(request):
    all_sensitive_news = RecentNews.objects.filter(post_date=date.today())
    all_recent_news = RecentNews.objects.order_by('-post_date')

    context = {
        'all_sensitive_news': all_sensitive_news,
        'all_recent_news': all_recent_news,
    }
    # return HttpResponse("You are in home page.")
    return render(request, 'home/home.html', context)


def for_students(request):
    return render(request, 'home/for_students.html')


def for_companies(request):
    return render(request, 'home/for_companies.html')
