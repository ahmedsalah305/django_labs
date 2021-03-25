from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User, Group
from django.forms.fields import EmailField
from rest_framework import serializers

# Create your models here.


class UserCreationFormEdit(UserCreationForm):
    username = UsernameField
    first_name = UsernameField
    last_name = UsernameField
    email = EmailField
    password = forms.PasswordInput

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    overView = models.TextField(max_length=255)
    year = models.DateField()
    image = models.ImageField(upload_to="movie/image/%Y/%m/%d")
    video = models.FileField(upload_to="movie/video/%Y/%m/%d")

    def __str__(self):
        return str(self.title)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'overView', 'year', 'image', 'video', ]


