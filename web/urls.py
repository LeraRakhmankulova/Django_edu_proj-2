from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, product_edit_view, meals_edit_view, \
    product_delete_view, meal_delete_view, analytics_view, import_view, stat_view

urlpatterns = [
    path("", main_view, name="main"),
    path("import/", import_view, name="import"),
    path("analytics/", analytics_view, name="analytics"),
    path("stat/", stat_view, name="stat"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("product/add/", product_edit_view, name="product_add"),
    path("product/<int:id>", product_edit_view, name="product_edit"),
    path("meal/<int:id>/delete/", product_delete_view, name="product_delete"),
    path("meal/add", meals_edit_view, name="meal_add"),
    path("meal/<int:id>", meals_edit_view, name="meal_edit"),
    path("meal/<int:id>/delete/", meal_delete_view, name="meal_delete"),
]
