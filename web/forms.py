from django import forms
from django.contrib.auth import get_user_model

from web.models import Product, Meal

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["confirmPassword"]:
            self.add_error("password", "Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "confirmPassword")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProductCreateForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model: Product
        fields = (
            'name', 'weight', 'fats_count', 'protein_count', 'carbohydrates_count', 'calories_count', 'image', 'user')


class MealsCreateForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model: Meal
        fields = ('date', 'name', 'user', 'products')
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "date"}, format='%Y-%m-%d')
        }


class MealFilterForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    start_date = forms.DateTimeField(
        label="От",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )
    end_date = forms.DateTimeField(
        label="до",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )


class ImportForm(forms.Form):
    file = forms.FileField()
