from django.db import models
from django.contrib.auth.models import User


BALL_COVER = ((0, "Soft"), (1, "Hard"))


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=254)
    driver_loft = models.BooleanField(default=False, null=True, blank=True)
    wedge_loft = models.BooleanField(default=False, null=True, blank=True)
    ball_softness = models.IntegerField(choices=BALL_COVER, default=0,
                                        null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments", null=True, blank=True
    )
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    def get_absolute_url(self):
        """ Returns comment with primary key"""
        return reverse('product_detail', kwargs={'pk': self.pk})
