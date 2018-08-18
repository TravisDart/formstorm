from django.db import models

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)


class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    sub_title = models.CharField(max_length=100)
