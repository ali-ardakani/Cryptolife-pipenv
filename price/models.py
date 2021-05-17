from django.db import models
from django.urls import reverse

class Cryptocurrency(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('price_detail', kwargs={'slug': self.slug})
