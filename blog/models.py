from datetime import time
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


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
    objects = models.Manager()
    published = PublishedManager()
    
    def get_absolute_url(self):
        return reverse("blog:post_detail",args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ('publish',)

