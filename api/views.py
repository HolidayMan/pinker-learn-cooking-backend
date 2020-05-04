from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CategorySerializer
from .models import Category


class UsersView(APIView):
    """Пользователи"""

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryAllView(APIView):
    """view for /category/all"""

    def get(self, request):
        objects = Category.objects.all()
        serializer = CategorySerializer(objects, many=True)
        return Response(serializer.data, status=200)

