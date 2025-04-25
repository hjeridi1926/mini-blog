from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userDetail(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,)
    hobby = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=False,blank=False,max_length=20)
    text = models.TextField(null=False,blank=False,max_length=2000)
    def __str__(self):
        return self.title
    def last_comment(self):
        try:
            return self.comment_set.all().order_by('-id')[0]
        except IndexError:
            pass
    
class Comment(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False,blank=False,max_length=1000)

