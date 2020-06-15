from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    # fields for the movie table
    name = models.CharField(max_length=300)
    director = models.CharField(max_length=300)
    cast = models.CharField(max_length=800)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    average_rating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    name = models.CharField(max_length=300)
    studio = models.CharField(max_length=300)
    platform = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    average_rating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    def __str__(self):
        return self.name
