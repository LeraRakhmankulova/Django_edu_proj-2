from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect

from web.forms import RegistrationForm, AuthForm, ProductCreateForm, MealsCreateForm
from web.models import Product, Meal

User = get_user_model()


def main_view(request):
    products = Product.objects.all()
    return render(request, "web/main.html", {
        'products': products
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


def product_edit_view(request, id=None):
    product = None
    if id is None:
        product = Product.objects.get(id=id)
    form = ProductCreateForm(instance=product)
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/product_form.html", {"form": form})


def meals_edit_view(request, id=None):
    meal = None
    if id is None:
        meal = Meal.objects.get(id=id)
    form = MealsCreateForm(instance=meal)
    if request.method == 'POST':
        form = MealsCreateForm(data=request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/meal_form.html", {"form": form})
