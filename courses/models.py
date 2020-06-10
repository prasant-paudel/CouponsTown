from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    best_seller = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, null=True)
    duration = models.DurationField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # class Meta:
    #     ordering = ['upload_date']
    