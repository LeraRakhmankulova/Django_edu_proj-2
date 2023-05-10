from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers import MealSerializer, ProductSerializer
from web.models import Meal, Product


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


class MealModelViewSet(ModelViewSet):
    serializer_class = MealSerializer

    def get_queryset(self):
        return Meal.objects.all().select_related("user").prefetch_related("products").filter(user=self.request.user)


class ProductsViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().filter(user=self.request.user)
