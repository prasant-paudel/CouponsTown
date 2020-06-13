from django.db import models


class Course(models.Model):    
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/', blank=True)
    best_seller = models.BooleanField()
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, blank=True)
    duration = models.DurationField(blank=True, default=0, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name
    
    # class Meta:
    #     ordering = ['upload_date']


def get_heading_from_url(url):    
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.content)
    return parsed_html.findAll('h1')[0].get_text()

    