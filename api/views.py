from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import CategorySerializer, CategoryFullSerializer, DishSerializer, DishFullSerializer
from .models import Category, Dish


class CategoryAllView(APIView):
    """view for /category/all and /category/all/full"""
    full = False

    def get(self, request):
        objects = Category.objects.all()
        if self.full:
            serializer = CategoryFullSerializer(objects, many=True)
        else:
            serializer = CategorySerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExactCategoryView(APIView):
    """view for /category/<int:id> and /category/<int:id>/full"""
    full = False
    dishes = False

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "info": f"Category with id {category_id} does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        if self.full:
            serializer = CategoryFullSerializer(category)
        elif self.dishes:
            serializer = DishFullSerializer(category.dishes, many=True)
        else:
            serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DishView(APIView):
    full = False

    def get(self, request):
        dishes = Dish.objects.all()
        if self.full:
            serializer = DishFullSerializer(dishes, many=True)
        else:
            serializer = DishSerializer(dishes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
