from django import forms
from django.contrib.auth import get_user_model

from web.models import Product

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
    class Meta:
        model: Product
        fields = ('name', 'weight', 'fats_count', 'protein_count', 'carbohydrates_count', 'calories_count', 'image')

