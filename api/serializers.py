from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from web.models import User, Product, Meal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProductSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        self.validated_data['user_id'] = self.context['request'].user.id
        return super().save(**kwargs)

    class Meta:
        model = Product
        fields = ('id', 'name')


class MealSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)

    def save(self, **kwargs):
        products = self.validated_data.pop("product_ids")
        self.validated_data['user_id'] = self.context['request'].user.id
        instance = super().save(**kwargs)
        instance.products.set(products)
        return instance

    class Meta:
        model = Meal
        fields = ('id', 'name', 'date', 'products', 'user', 'product_ids')
