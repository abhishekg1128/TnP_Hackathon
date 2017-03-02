from django.db import models
from django.utils import timezone
from datetime import date


# class SensitiveNews(models.Model):
#     news = models.CharField(max_length=250)
#     link = models.CharField(max_length=250, default="#")
#
#     def __str__(self):
#         return self.news
#     @classmethod
#     def create(cls, news,link):
#         sens = cls(news=news, link=link)
#         sens.news = news
#         sens.link = link
#         return sens


class RecentNews(models.Model):
    news = models.CharField(max_length=250)
    link = models.CharField(max_length=250, default="#")
    post_date = models.DateField()

    def __str__(self):
        return self.news
