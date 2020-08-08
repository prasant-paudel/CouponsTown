from django.contrib.sitemaps import Sitemap
from .models import Course

class CourseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.64

    def items(self):
        return Course.objects.order_by('upload_date')

    def lastmod(self, obj):
        return obj.upload_date
