from django.db import models
from django.contrib.auth.models import User

"""
1. Change your models (in models.py).
2. Run python manage.py makemigrations, to create migrations for those changes
3. Run python manage.py migrate, to apply those changes to the database.
"""

# Create your models here.
class ClothingItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cloth_type = models.CharField(max_length=50)
    cloth_color = models.CharField(max_length=50)
    image = models.ImageField()

    def __str__(self):
        return f"{self.cloth_color}, {self.cloth_type}"