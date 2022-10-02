from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name='followers')

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 
    lovers = models.ManyToManyField(User, related_name='lovers')
    
    class Meta:
        ordering = ['-created']
    def  __str__(self):
        return f'{self.owner} writes a post at {self.created}'