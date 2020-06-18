from django.db import models


class Course(models.Model):    
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200)
    affiliate_url = models.CharField(max_length=256,blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    best_seller = models.BooleanField()
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, blank=True)
    duration = models.DurationField(blank=True, default=0, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=5, blank=True)

    category_coices = (
        ('DEVELOPMENT', 'development'),
        ('IT & SOFTWARE', 'it&software'),
        ('OFFICE & PRODUCTIVITY', 'office&productivity'),
        ('DESIGN & PHOTOGRAPHY', 'design&photography'),
        ('MARKETING & BUSINESS', 'marketing&business'),
        ('OTHERS', 'others'),
    )
    category = models.CharField(choices=category_coices, default='others', max_length=21)

    def __str__(self):
        return self.name
    
    # class Meta:
    #     ordering = ['upload_date']

class Subscriber(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

