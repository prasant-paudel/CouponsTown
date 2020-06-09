from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    is_best_seller = models.BooleanField()

    def __str__(self):
        return self.name
    