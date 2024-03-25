from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category',blank=True)


    class Meta:
         ordering=('name',)
         verbose_name='category'
         verbose_name_plural='categories'


    def get_url(self):
        return reverse('finalapp5:products_by_category',args=[self.slug])


    def __str__(self):
         return '{}'.format(self.name)
class Movie(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    year=models.IntegerField()
    trailer_link = models.URLField(blank=True)
    actors = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='movie',blank=True)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    trailer_link = models.URLField(blank=True)
    actors = models.CharField(max_length=200, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_url(self):
        return reverse('finalapp5:prodCatdetail', kwargs={'c_slug': self.category.slug, 'movie_slug': self.slug})



    class Meta:
        ordering=('name',)
        verbose_name='movie'
        verbose_name_plural='movies'
    def __str__(self):
        return '{}'.format(self.name)
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s review for {self.movie.name}'
