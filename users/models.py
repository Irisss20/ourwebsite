from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'



class InMessages(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=30)
    text = models.TextField()

