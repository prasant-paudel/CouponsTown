from django.db import models
from multiselectfield import MultiSelectField
from django.shortcuts import reverse

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    name_base64 = models.CharField(max_length=100, blank=True)
    name_encoded = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200)
    affiliate_url = models.CharField(max_length=256,blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    contents = models.BinaryField(blank=True)
    description = models.BinaryField(blank=True)
    best_seller = models.BooleanField(null=True)
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, blank=True)
    duration = models.CharField(blank=True, max_length=10)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(default='Coupons Town', max_length=100)
    rating = models.FloatField(max_length=5, blank=True, null=True)
    category_coices = (
        ('not_set', 'NOT SET'),
        ( 'development', 'DEVELOPMENT'),
        ('it&software', 'IT & SOFTWARE'),
        ('office&productivity', 'OFFICE & PRODUCTIVITY'),
        ('design&photography', 'DESIGN & PHOTOGRAPHY'),
        ('marketing&business', 'MARKETING & BUSINESS'),
        ('others', 'OTHERS'),
    )
    category = models.CharField(choices=category_coices, default='not_set', max_length=21)
    
    def __str__(self):
        if self.expired:
            return str(self.id) + ' --Expired-- ' + self.name + ' | ' + self.platform
        if self.name:
            return str(self.id) + ' ' + self.name + ' | ' + self.platform
        return str(self.id) + ' | ' + self.platform
    
    class Meta:
        ordering = ['expired' ,'name']
        
    def get_absolute_url(self):
        return reverse('info_page') + '?course=' + self.name_encoded


class Subscriber(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class RealDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    # title = models.CharField(max_length=200)
    offer = models.CharField(max_length=200, unique=True)
    coupon = models.CharField(max_length=200, blank=True, unique=True)
    platform = models.CharField(max_length=30, blank=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        if self.valid:
            validity = 'Valid'
        else:
            validity = 'Invalid'
        return self.coupon + ' | ' + validity



