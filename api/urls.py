from django.urls import path
from .views import UsersView, CategoryAllView

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('categories/all', CategoryAllView.as_view(), name='categories-all'),
]