import csv

from foodcalculate.redis import get_redis_client
from web.models import Meal, Product


def filter_meals(meals_qs, filters: dict):
    if filters['search']:
        meals_qs = meals_qs.filter(title_icontains=filters['search'])

    if filters['start_date']:
        meals_qs = meals_qs.filter(date__gre=filters['start_date'])

    if filters['end_date']:
        meals_qs = meals_qs.filter(date__lte=filters['end_date'])
    return meals_qs


def export_meals_csv(meals_qs, response):
    writer = csv.writer(response)
    writer.writerow(("name", "date", "products"))

    for meal in meals_qs:
        writer.writerow((
            meal.name, meal.date,
            " ".join([t.title for t in meal.products.all()]),
        ))

    return response


def import_meals_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    meals = []
    meal_products = []
    for row in reader:
        meals.append(Meal(
            name=row['name'],
            date=row['date'],
            user_id=user_id
        ))
        meal_products.append(row['products'].split(" ") if row['products'] else [])

    saved_meals = Meal.objects.bulk_create(meals)

    products_map = dict(Product.objects.all().values_list("name", "id"))
    meal_products = []
    for meal, meal_products_item in zip(saved_meals, meal_products):
        for product in meal_products_item:
            product_id = products_map[product]
            meal_products.append(
                Meal.products.through(meal_id=meal.id, mealproducts_id=product_id)
            )
    Meal.products.through.objects.bulk_create(meal_products)


def get_stat():
    redis = get_redis_client()
    keys = redis.keys("stat_*")
    return [
        (key.decode().replace("stat_", ""), redis.get(key).decode())
        for key in keys
    ]
