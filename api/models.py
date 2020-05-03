import os

from django.db import models


class Category(models.Model):
    image = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Dish(models.Model):
    image = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"


class DishIngredient(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Dish Ingredient"
        verbose_name_plural = "Dish Ingredients"


class Ingredient(models.Model):
    name = models.CharField(max_length=256, unique=True)
    dish = models.ManyToManyField('Dish', through="DishIngredient", related_name='ingredients')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
