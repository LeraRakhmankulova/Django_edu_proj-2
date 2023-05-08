from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

from web.forms import RegistrationForm, AuthForm, ProductCreateForm, MealsCreateForm, MealFilterForm, ImportForm
from web.models import Product, Meal
from web.services import filter_meals, export_meals_csv, import_meals_from_csv, get_stat

User = get_user_model()


@cache_page(60)
@login_required
def main_view(request):
    meals = Meal.objects.filter(user=request.user)
    page = request.GET.get("page", 10)

    filter_form = MealFilterForm(request.GET)
    filter_form.is_valid()
    meals = filter_meals(meals, filter_form.cleaned_data)

    meals = meals.prefetch_related("products").select_related("user").annotate(
        product_count=Count("products")
    )
    total_count = meals.count()
    paginator = Paginator(meals, per_page=100)

    if request.GET.get("export") == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={"Content-Disposition": "attachment; filename=meals.csv"}
        )
        export_meals_csv(meals, response)

    return render(request, "web/main.html", {
        'meals': paginator.get_page(page),
        'total_count': total_count
    })


@login_required
def stat_view(request):
    return render(request, "web/stat.html", {"results": get_stat()})


@login_required
def import_view(request):
    if request.method == 'POST':
        form = ImportForm(files=request.FILES)
        if form.is_valid():
            import_meals_from_csv(form.cleaned_data['file'], request.user.id)
            return redirect("main")
    return render(request, "web/import.html", {
        "form": ImportForm()
    })


@login_required
def analytics_view(request):
    overall_stat = Meal.objects.aggregate(
        count=Count("id"),
        max_date=Max("date"),
        min_date=Min("date")
    )

    days_stat = (
        Meal.objects.exclude(date__isnull=True)
        .annotate(date=TruncDate("date"))
        .values("date")
        .annotate(
            count=Count("id")
        )
        .order_by('-date')
    )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
        'days_stat': days_stat
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.filter(user=request.user)
    form = form_cls()
    if request.method == 'POST':
        form = form_cls(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect(url_name)
    return render(request, f"web/{template_name}.html", {"items": items, "form": form})


@login_required
def product_edit_view(request, id=None):
    products = Product.objects.filter(user=request.user)
    product = None
    if id is None:
        product = Product.objects.get(id=id)
    form = ProductCreateForm(instance=product)
    if request.method == 'POST':
        product = get_object_or_404(Product, user=request.user, id=id)
        form = ProductCreateForm(data=request.POST, initial={"user": request.user}, files=request.FILES,
                                 instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_add")
    return render(request, "web/product_form.html", {"products": products, "form": form})


@login_required
def product_delete_view(requset, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('main')


@login_required
def meals_edit_view(request, id=None):
    meal = get_object_or_404(Meal, user=request.user, id=id)
    return _list_editor_view(request, Meal, MealsCreateForm, "main", "meal_form")


@login_required
def meal_delete_view(requset, id):
    meal = Meal.objects.get(id=id)
    meal.delete()
    return redirect('main')
