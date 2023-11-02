from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title       = models.CharField(max_length=100)
    #cover      = models.ImageField()
    description = models.TextField(null=True) # required
    summary     = models.TextField(blank=True)
    author      = models.CharField(max_length=50)
    
    states = [('Want to Read','Want to Read') , ('Reading','Reading') , ('Read','Read')]
    read_states = models.CharField(max_length=12, choices=states , default='Want to Read')

    def __str__(self):
        return self.title
