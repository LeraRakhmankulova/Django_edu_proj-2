import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import Product, User, Meal


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        products = Product.objects.filter(user=user)

        for index in range(30):
            for slot_index in range(randint(5, 10)):
                products.append(Product(
                    name=f'generated {index}',
                    weight=random.randint(100, 500),
                    fats_count=random.randint(0, 100),
                    protein_count=random.randint(0, 100),
                    carbohydrates_count=random.randint(0, 100),
                    calories_count=random.randint(100, 500),
                    user=user
                ))

            saved_products = Product.objects.bulk_create(products)
            meals = []
            for product in saved_products:
                count_of_products = randint(0, len(products))
            for product_index in range(count_of_products):
                meals.append(
                    Meal.products.through(product_id=product.id, meal_id=meals[product_index].id)
                )
        Meal.products.through.objects.bulk_create(product)
