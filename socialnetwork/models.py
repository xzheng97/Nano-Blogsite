from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_author = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    post_input_text = models.CharField(max_length=200)
    post_time = models.DateTimeField()
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
    comment_author = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    comment_input_text = models.CharField(max_length=200)
    comment_time = models.DateTimeField()
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'

class Profile(models.Model):
    bio_input_text = models.CharField(max_length=200, default = "hello, welcome to my profile!")
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    profile_picture = models.FileField(blank=True, default = None)
    content_type = models.CharField(max_length=50, default = "")
    following = models.ManyToManyField("self", default = None)
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'
