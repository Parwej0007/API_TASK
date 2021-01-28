from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, verbose_name='title')
    released_year = models.IntegerField(verbose_name='released year')
    rating = models.CharField(max_length=255, verbose_name='rating')
    movie_id = models.CharField(max_length=255, null=False, verbose_name='movie id')
    genres= models.TextField(null=True)

    def __str__(self):
        return self.title