from django.db import models
import numpy as np
from django.contrib.auth.models import User

def get_default_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()

class Restaurant(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=1000)
    latitud = models.CharField(max_length=250)
    longitud = models.CharField(max_length=250)
    image = models.ImageField(upload_to='nomy/images/', default='nomy/images/default.jpeg')
    emb = models.BinaryField(default=get_default_array())
    direccion = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0

class searchahistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query} - {self.timestamp}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.restaurant.nombre}'
