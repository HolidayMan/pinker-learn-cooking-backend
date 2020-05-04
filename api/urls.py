from django.urls import path, re_path
from .views import UsersView, CategoryAllView

urlpatterns = [
    path('users/', UsersView.as_view()),
    re_path(r'categories/all/?$', CategoryAllView.as_view(), name='categories-all'),
    re_path(r'categories/all/full/?$', CategoryAllView.as_view(full=True), name='categories-all-full'),
]