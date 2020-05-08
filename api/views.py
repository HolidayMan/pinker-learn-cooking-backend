from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CategorySerializer, CategoryFullSerializer
from .models import Category


class CategoryAllView(APIView):
    """view for /category/all and /category/all/full"""
    full = False

    def get(self, request):
        objects = Category.objects.all()
        if self.full:
            serializer = CategoryFullSerializer(objects, many=True)
        else:
            serializer = CategorySerializer(objects, many=True)
        return Response(serializer.data, status=200)


class ExactCategoryView(APIView):
    """view for  /category/<int:id>"""

    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=200)
