from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=256)
    weight = models.PositiveIntegerField()
    fats_count = models.PositiveIntegerField()
    protein_count = models.PositiveIntegerField()
    carbohydrates_count = models.PositiveIntegerField()
    calories_count = models.PositiveIntegerField()


class Meal(models.Model):
    time = models.TimeField()
    name = models.CharField(max_length=256)
    products = models.ManyToManyField(Product)


class CaloriesLog(models.Model):
    date = models.DateTimeField()
    meals = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



