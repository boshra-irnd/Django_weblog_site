from datetime import time
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    STATUS = (
        ("draft",'Draft'),
        ("published",'Published')
    )
    author = ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS,default='draft')

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ('publish',)
