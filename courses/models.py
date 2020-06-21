from django.db import models


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200)
    affiliate_url = models.CharField(max_length=256,blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    best_seller = models.BooleanField(null=True)
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, blank=True)
    duration = models.CharField(blank=True, max_length=10)
    upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=5, blank=True)

    category_coices = (
        ('NOT SET', 'not_set'),
        ('DEVELOPMENT', 'development'),
        ('IT & SOFTWARE', 'it&software'),
        ('OFFICE & PRODUCTIVITY', 'office&productivity'),
        ('DESIGN & PHOTOGRAPHY', 'design&photography'),
        ('MARKETING & BUSINESS', 'marketing&business'),
        ('OTHERS', 'others'),
    )
    category = models.CharField(choices=category_coices, default='not_set', max_length=21)

    def __str__(self):
        return self.name + ' | ' + self.platform
    
    class Meta:
        ordering = ['platform']


class Subscriber(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class RealDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    # title = models.CharField(max_length=200)
    offer = models.CharField(max_length=200)
    coupon = models.CharField(max_length=200, blank=True)
    platform = models.CharField(max_length=30, blank=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        if self.valid:
            validity = 'Valid'
        else:
            validity = 'Invalid'
        return self.coupon + ' | ' + validity

