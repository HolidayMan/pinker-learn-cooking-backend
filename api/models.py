import os

from django.db import models
from pinker_backend.settings import MEDIA_ROOT


class Category(models.Model):
    image = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"<Category {self.name}>"
