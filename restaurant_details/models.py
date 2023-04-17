from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True    

class Restaurant(TimeStampModel):
    title = models.CharField(max_length=255)
    cost_for_two = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    owner = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    timings = models.CharField(max_length=255)
    VEG = 'V'
    VEGAN = 'VG'
    NON_VEG = 'NV'
    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (VEGAN, 'Vegan'),
        (NON_VEG, 'Non-Vegetarian'),
    ]
    food_type = MultiSelectField(choices=FOOD_TYPE_CHOICES, max_length=10)
    cuisines = models.ManyToManyField('Cuisine')
    menu = models.ManyToManyField('Dish')
        
    def __str__(self):
        return self.title

class Dish(TimeStampModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    VEG_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NVEG', 'Non-Vegetarian'),
        ('VEGAN', 'Vegan')
    ]
    veg_type = models.CharField(max_length=5, choices=VEG_CHOICES)
    def __str__(self):
        return f"{self.name} - {self.price}"


class Cuisine(TimeStampModel):
    name = models.CharField(max_length=255)


class ReviewAndRating(TimeStampModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.CharField(max_length=255)


class BookmarkAndVisited(TimeStampModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visited = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)



