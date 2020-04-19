from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_fiction = models.BooleanField(default=False)
    pages = models.IntegerField(default=False)
    genre = models.ManyToManyField(Genre)
