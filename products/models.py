from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name      = models.CharField(max_length=200)
    slug      = models.SlugField(unique=True, blank=True)
    parent    = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    image     = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    BADGE_CHOICES = [('', 'None'), ('new', 'New'), ('sale', 'Sale'), ('hot', 'Hot')]

    name        = models.CharField(max_length=300)
    slug        = models.SlugField(unique=True, blank=True)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    stock       = models.PositiveIntegerField(default=0)
    badge       = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True, default='')
    is_active   = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def discount_percent(self):
        if self.sale_price and self.price > 0:
            return int((1 - self.sale_price / self.price) * 100)
        return 0

    @property
    def main_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def avg_rating(self):
        result = self.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
        return round(result, 1) if result else 0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image      = models.ImageField(upload_to='products/')
    alt_text   = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order      = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} — image {self.order}"


class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    rating     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title      = models.CharField(max_length=200, blank=True)
    body       = models.TextField()
    is_approved= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.product.name} ({self.rating}★)"


class Coupon(models.Model):
    code             = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses         = models.PositiveIntegerField(default=100)
    used_count       = models.PositiveIntegerField(default=0)
    is_active        = models.BooleanField(default=True)
    valid_from       = models.DateTimeField()
    valid_to         = models.DateTimeField()

    def __str__(self):
        return f"{self.code} — {self.discount_percent}% off"

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to and self.used_count < self.max_uses
