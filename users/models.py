from django.db import models
from django.contrib.auth.models import User

from base.models import Vacancy


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def _str_(self):
        return f'{self.user.username} Profile'
    
class InMessages(models.Model):
    vacs = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=30)
    text = models.TextField()
