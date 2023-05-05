from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    weight = models.PositiveIntegerField(verbose_name="Вес")
    fats_count = models.PositiveIntegerField(verbose_name="Количество жиров")
    protein_count = models.PositiveIntegerField(verbose_name="Количество белков")
    carbohydrates_count = models.PositiveIntegerField(verbose_name="Количество углеводов")
    calories_count = models.PositiveIntegerField(verbose_name="Количество калорий")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Картинка")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.name


class Meal(models.Model):
    time = models.TimeField(verbose_name="Время")
    name = models.CharField(max_length=256, verbose_name="Название")
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')


class CaloriesLog(models.Model):
    date = models.DateTimeField(verbose_name="Дата")
    meals = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="Прием пищи")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
