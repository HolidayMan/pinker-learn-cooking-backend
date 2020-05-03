from django.contrib import admin
from .models import *


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'image']


@admin.register(Measure)
class AdminMeasure(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Dish)
class AdminDish(admin.ModelAdmin):
    list_display = ['name', 'image', 'category']


@admin.register(DishIngredient)
class AdminDishIngredient(admin.ModelAdmin):
    list_display = ['dish', 'ingredient', 'measure', 'amount']
