from django.contrib import admin

from web.models import Meal, Product


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "user", 'date')
    search_fields = ("id", "name")
    list_filter = "date"
    ordering = '-date'


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'weight', 'fats_count', 'protein_count', 'carbohydrates_count', 'calories_count', 'user')
    search_fields = ("id", "name")
    list_filter = "user"


admin.site.register(Meal, MealAdmin)
admin.site.register(Product, ProductAdmin)
