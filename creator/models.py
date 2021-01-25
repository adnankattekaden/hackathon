from django.db import models
from django.contrib.auth.models import User,auth
from builtins import property

# Create your models here.

class CreatorDeatails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about_me = models.CharField(max_length=255)
    role = models.CharField(default='Podcaster',max_length=255)


class Contents(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    episode_name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    date_of_published = models.DateField(auto_now_add=True)
    podcast = models.FileField(upload_to='podcasts/')
    thumbnail = models.FileField(upload_to='thumbnail/')



    @property
    def ImageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url


    @property
    def PodcastURL(self):
        try:
            url = self.podcast.url
        except:
            url = ''
        return url