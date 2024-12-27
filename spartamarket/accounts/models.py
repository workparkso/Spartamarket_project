from django.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser



def user_profile_image_path(instance, filename): 
    return f"profile_image/{instance.username}/{filename}"
class User(AbstractUser):
    profile_image = models.ImageField(upload_to = user_profile_image_path, blank=True, null=True)



# 팔로우 수 n대n
    follows = models.ManyToManyField("self",symmetrical=False, related_name = "followers", blank=True)

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.follows.count()  #

    def __str__(self):
        return self.username #