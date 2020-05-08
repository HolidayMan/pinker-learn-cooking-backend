from django.urls import path, re_path
from .views import CategoryAllView, ExactCategoryView, DishView

urlpatterns = [
    re_path('categories/(?P<category_id>[0-9]+)/?$', ExactCategoryView.as_view(), name="exact-category"),
    re_path('categories/(?P<category_id>[0-9]+)/full/?$', ExactCategoryView.as_view(full=True), name="exact-category-full"),
    re_path('categories/(?P<category_id>[0-9]+)/dishes/?$', ExactCategoryView.as_view(dishes=True), name="exact-category-dishes"),
    re_path(r'categories/all/?$', CategoryAllView.as_view(), name='categories-all'),
    re_path(r'categories/all/full/?$', CategoryAllView.as_view(full=True), name='categories-all-full'),
    re_path(r'dishes/all/?$', DishView.as_view(), name='dishes-all'),
    re_path(r'dishes/all/full?$', DishView.as_view(full=True), name='dishes-all-full'),
]
