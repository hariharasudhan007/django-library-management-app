from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=255,unique=True)
    author = models.CharField(max_length=255,unique=True)
    ISBN = models.CharField(max_length=13,unique=True)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def clean(self):
        # Custom validation logic for title length
        if len(self.ISBN) != 13:
            raise ValidationError({'title': 'Title must be exactly 12 characters long.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Book, self).save(*args, **kwargs)
