from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    name = models.CharField(max_length=100)


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if len(self.title) + len(self.subtitle) > 150:
            raise ValidationError(
                "Title and subtitle can't have a combined length greater than "
                "150 characters."
            )

    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(
        max_length=100, blank=True, null=False, default=""
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_fiction = models.BooleanField(default=False)
    pages = models.IntegerField()
    genre = models.ManyToManyField(Genre)
