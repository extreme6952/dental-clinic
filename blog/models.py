import numbers
from unicodedata import category
from django.db import models

from django.utils import timezone

from django.urls import reverse

from django.contrib.auth.models import User

from taggit.managers import TaggableManager



class PublishedManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Category(models.Model):

    name = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250)
    
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['name']

        indexes = [
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:category_detail",args=[self.slug])
    
    


class Post(models.Model):

    class Status(models.TextChoices):

        DRAFT = 'DF','Draft'

        PUBLISHED = 'PB','Published'


    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    
    body = models.TextField()

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category')
    
    publish = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    
    objects = models.Manager()

    published = PublishedManager()

    class Meta:

        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):

        return f"Title the post {self.title}"
    

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
    

class Gallery(models.Model):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='images')
    
    imageq = models.ImageField(upload_to='post_media')
    


class Comment(models.Model):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    
    name = models.CharField(max_length=250)

    email = models.EmailField()

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:

        ordering = ['created']

        indexes = [
            models.Index(fields=['created'])
        ]

    
    def __str__(self):

        return f"Comment {self.name} by {self.post}"
    


class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile_users')

    phone_number = models.IntegerField(null=True)

    date_of_birthy = models.DateTimeField(null=True)

    image = models.ImageField(upload_to='user/%M/%y/%d')

    def __str__(self):
        return self.user.last_name
    
    def __str__(self):
        return f"profile {self.user.username}" 
    
    

