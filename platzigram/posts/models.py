from users.models import Profile
from django.contrib.auth.models import User
from django.db import models
from django.db.models import base
from django.template.defaultfilters import slugify
# Create your models here.

# TODO: forma de registrar un usuario personalzado en django diferencia que no tengo temas de password

# class User(models.Model):

#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)

#     is_admin = models.BooleanField(default=False)

#     bio = models.TextField(blank=True)

#     birthdate = models.DateField(blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
# return f'{self.first_name} {self.last_name} : {self.email}'


class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        'users.Profile', related_name='post_user_profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='posts/')
    slug = models.SlugField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} @{}'.format(self.title, self.user.username)

    def get_slug(self):
        return slugify(self.title)