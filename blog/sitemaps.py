from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.5

    def items(self):
        return Post.published.all()

    def Lastmod(self, obj):
        return obj.created
