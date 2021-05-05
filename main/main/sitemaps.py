from django.contrib.sitemaps import Sitemap
from .models import Good


class GoodSitemap(Sitemap):
    """
    Class for generating sitemap for Good model
    """
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Good.objects.filter(is_publish=True)

