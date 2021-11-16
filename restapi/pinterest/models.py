from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class CommonInfo(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='pinterest-posters')

    watch_count = models.IntegerField()
    likes = models.IntegerField()

    def __str__(self):

        return self.name

    class Meta:
        abstract = True



class Movie(CommonInfo):
    pass


class Series(CommonInfo):
    season = models.CharField(max_length=50)
    eposide = models.CharField(max_length=50)
