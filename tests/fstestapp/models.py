from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author)
    is_fiction = models.BooleanField(default=False)
    pages = models.IntegerField(default=False)
    genre = models.ManyToManyField(Genre)

    def __unicode__(self):
        return self.title
